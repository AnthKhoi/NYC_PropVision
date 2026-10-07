import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import joblib
from scipy import stats

st.set_page_config(
    page_title="Dự Đoán & Trực Quan Hóa Giá Bất Động Sản New York",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.1rem;
        font-weight: 800;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
        text-transform: uppercase;
    }
    .sub-header {
        text-align: center;
        color: #4B5563;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
        font-weight: 500;
    }
    .metric-container {
        background: #F8FAFC;
        border-radius: 8px;
        padding: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .insight-card {
        background-color: #EFF6FF;
        border-left: 4px solid #2563EB;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 1rem;
        color: #1E3A8A;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        padding-top: 8px;
        padding-bottom: 8px;
        font-weight: 600;
        font-size: 0.92rem;
    }
</style>
""", unsafe_allow_html=True)

theme = "plotly_white"

def safe_sample(df, n=1500, random_state=42):
    if df is None or len(df) == 0:
        return df
    if len(df) <= n:
        return df
    return df.sample(n=n, random_state=random_state)

# Tai va chuan hoa du lieu
@st.cache_data
def load_and_prepare_data():
    try:
        df = pd.read_csv('final_dashboard_data.csv', low_memory=False)
    except FileNotFoundError:
        try:
            df = pd.read_csv('du_lieu_dashboard_tieng_viet.csv', low_memory=False)
        except FileNotFoundError:
            df = pd.read_csv('du_lieu_da_xu_ly.csv', low_memory=False)
        
    col_map = {
        'Borough': 'QUAN',
        'SALE PRICE': 'GIA_BAN',
        'GROSS SQUARE FEET': 'DIEN_TICH_SU_DUNG',
        'PRICE_SEGMENT': 'PHAN_KHUC_GIA',
        'Neighborhood': 'KHU_PHO',
        'SALE_YEAR_MONTH': 'THANG_NAM_BAN',
        'PRICE_PER_SQFT': 'GIA_TREN_SQFT',
        'PROPERTY_AGE': 'TUOI_THO_NHA',
        'MEDIAN_HOUSEHOLD_INCOME': 'THU_NHAP_TRUNG_BINH',
        'LOG_SALE_PRICE': 'LOG_GIA_BAN'
    }
    for old_c, new_c in col_map.items():
        if new_c not in df.columns and old_c in df.columns:
            df[new_c] = df[old_c]
            
    if 'GIA_BAN' in df.columns and 'LOG_GIA_BAN' not in df.columns:
        df['LOG_GIA_BAN'] = np.log1p(df['GIA_BAN'])
    if 'GIA_BAN' in df.columns and 'DIEN_TICH_SU_DUNG' in df.columns and 'GIA_TREN_SQFT' not in df.columns:
        df['GIA_TREN_SQFT'] = df['GIA_BAN'] / df['DIEN_TICH_SU_DUNG'].replace(0, np.nan)
    if 'PHAN_KHUC_GIA' not in df.columns and 'GIA_BAN' in df.columns:
        df['PHAN_KHUC_GIA'] = pd.qcut(df['GIA_BAN'], q=3, labels=['Phổ thông', 'Tầm trung', 'Cao cấp'])
        
    coords = {
        'Manhattan': (40.7831, -73.9712),
        'Bronx': (40.8448, -73.8648),
        'Brooklyn': (40.6782, -73.9442),
        'Queens': (40.7282, -73.7949),
        'Staten Island': (40.5795, -74.1502)
    }
    if 'lat' not in df.columns or 'lon' not in df.columns:
        col_q = 'QUAN' if 'QUAN' in df.columns else 'Borough'
        df['lat'] = df[col_q].map(lambda x: coords.get(x, (40.7128, -74.0060))[0])
        df['lon'] = df[col_q].map(lambda x: coords.get(x, (40.7128, -74.0060))[1])
        np.random.seed(42)
        df['lat'] += np.random.normal(0, 0.022, size=len(df))
        df['lon'] += np.random.normal(0, 0.022, size=len(df))
        
    return df

df_data = load_and_prepare_data()

# Bo loc du lieu sidebar
st.sidebar.markdown("## BỘ LỌC DỮ LIỆU")
st.sidebar.caption("Tùy chỉnh thông số theo đặc điểm và vị trí bất động sản.")

ds_quan_all = sorted(df_data['QUAN'].dropna().unique().tolist())
ds_quan = st.sidebar.multiselect(
    "1. Vị trí Quận (Borough):",
    options=ds_quan_all,
    default=ds_quan_all
)

ds_pk_all = df_data['PHAN_KHUC_GIA'].dropna().unique().tolist()
ds_phan_khuc = st.sidebar.multiselect(
    "2. Phân khúc giá:",
    options=ds_pk_all,
    default=ds_pk_all
)

min_dt = int(df_data['DIEN_TICH_SU_DUNG'].min())
max_dt = int(df_data['DIEN_TICH_SU_DUNG'].quantile(0.99))
loc_dien_tich = st.sidebar.slider(
    "3. Diện tích sử dụng (Sqft):",
    min_value=0,
    max_value=15000,
    value=(0, 6000),
    step=200
)

min_age = int(df_data['TUOI_THO_NHA'].min())
max_age = int(df_data['TUOI_THO_NHA'].max())
loc_tuoi_nha = st.sidebar.slider(
    "4. Tuổi thọ công trình (Năm):",
    min_value=min_age,
    max_value=150,
    value=(min_age, 130),
    step=5
)

df_loc = df_data[
    (df_data['QUAN'].isin(ds_quan)) &
    (df_data['PHAN_KHUC_GIA'].isin(ds_phan_khuc)) &
    (df_data['DIEN_TICH_SU_DUNG'] >= loc_dien_tich[0]) &
    (df_data['DIEN_TICH_SU_DUNG'] <= loc_dien_tich[1]) &
    (df_data['TUOI_THO_NHA'] >= loc_tuoi_nha[0]) &
    (df_data['TUOI_THO_NHA'] <= loc_tuoi_nha[1])
].copy()

st.sidebar.markdown("---")
ty_le = (len(df_loc) / len(df_data)) * 100 if len(df_data) > 0 else 0
st.sidebar.info(f"Tập dữ liệu sau lọc: **{len(df_loc):,}** / **{len(df_data):,}** giao dịch ({ty_le:.1f}%)")

if len(df_loc) == 0:
    st.warning("Không có dữ liệu phù hợp với điều kiện lọc. Vui lòng mở rộng khoảng lọc ở thanh bên.")
    st.stop()

# Header va KPI tong quan
st.markdown("<div class='main-header'>DỰ ĐOÁN VÀ TRỰC QUAN HÓA XU HƯỚNG GIÁ BẤT ĐỘNG SẢN TẠI NEW YORK</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Nghiên Cứu Và Phân Tích Đa Chiều Giá Trị Bất Động Sản Theo Đặc Điểm Công Trình Và Vị Trí Địa Lý</div>", unsafe_allow_html=True)

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
tong_doanh_so = df_loc['GIA_BAN'].sum() / 1e9
gia_trung_vi = df_loc['GIA_BAN'].median()
don_gia_sqft = df_loc['GIA_TREN_SQFT'].median()
tuoi_nha_tb = df_loc['TUOI_THO_NHA'].mean()
so_giao_dich = len(df_loc)

kpi1.metric("Tổng Doanh Số Tích Lũy", f"${tong_doanh_so:.2f} Tỷ USD")
kpi2.metric("Số Lượng Giao Dịch", f"{so_giao_dich:,} căn")
kpi3.metric("Mức Giá Trung Vị", f"${gia_trung_vi:,.0f}")
kpi4.metric("Đơn Giá Trung Vị / Sqft", f"${don_gia_sqft:,.0f}")
kpi5.metric("Tuổi Thọ Trung Bình", f"{tuoi_nha_tb:.0f} năm")

st.markdown("---")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "1. XU HƯỚNG THỊ TRƯỜNG & THỊ PHẦN",
    "2. PHÂN BỐ KHÔNG GIAN & VỊ TRÍ",
    "3. CẤU TRÚC ĐÔ THỊ & DRILL-DOWN",
    "4. ĐẶC ĐIỂM CÔNG TRÌNH & QUY MÔ",
    "5. HỌC MÁY ĐỊNH GIÁ BẤT ĐỘNG SẢN",
    "6. DỰ BÁO XU HƯỚNG THỊ TRƯỜNG"
])

# Tab 1: Xu huong thoi gian va thi phan
with tab1:
    st.markdown("<div class='insight-card'><b>Nhận định thị trường:</b> Doanh số giao dịch có tính chu kỳ và mùa vụ rõ nét. Phân khúc bất động sản tại Manhattan và Brooklyn dẫn đầu về quy mô dòng tiền và chiếm thị phần áp đảo toàn thành phố.</div>", unsafe_allow_html=True)
    c1, c2 = st.columns([6, 4])
    
    with c1:
        st.markdown("#### 1. Biểu đồ Miền (Area Chart): Xu Hướng Doanh Số Giao Dịch Theo Tháng")
        df_trend = df_loc.groupby('THANG_NAM_BAN')['GIA_BAN'].sum().reset_index()
        fig_area = px.area(
            df_trend, x='THANG_NAM_BAN', y='GIA_BAN',
            markers=True, color_discrete_sequence=['#2563EB'], template=theme,
            labels={'THANG_NAM_BAN': 'Thời gian (Năm-Tháng)', 'GIA_BAN': 'Tổng doanh số (USD)'}
        )
        fig_area.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=380)
        st.plotly_chart(fig_area, use_container_width=True)
        
    with c2:
        st.markdown("#### 2. Biểu đồ Vành Khuyên (Donut Chart): Thị Phần Doanh Số Theo Quận")
        fig_donut = px.pie(
            df_loc, names='QUAN', values='GIA_BAN', hole=0.55,
            color_discrete_sequence=px.colors.qualitative.Bold, template=theme
        )
        fig_donut.update_traces(textposition='inside', textinfo='percent+label')
        fig_donut.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=380, showlegend=False)
        st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("#### 3. Biểu đồ Đường (Line Chart): Diễn Biến Đơn Giá Trung Vị / Sqft Theo Từng Tháng")
    df_line = df_loc.groupby(['THANG_NAM_BAN', 'QUAN'])['GIA_TREN_SQFT'].median().reset_index()
    fig_line = px.line(
        df_line, x='THANG_NAM_BAN', y='GIA_TREN_SQFT', color='QUAN',
        markers=True, template=theme,
        labels={'THANG_NAM_BAN': 'Thời gian', 'GIA_TREN_SQFT': 'Đơn giá / Sqft (USD)', 'QUAN': 'Quận'}
    )
    fig_line.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=380)
    st.plotly_chart(fig_line, use_container_width=True)

# Tab 2: Phan bo khong gian va vi tri
with tab2:
    st.markdown("<div class='insight-card'><b>Phân tích không gian:</b> Khảo sát phân bố mật độ và tương quan vị trí địa lý giữa 5 quận lớn New York (Manhattan, Brooklyn, Queens, Bronx, Staten Island).</div>", unsafe_allow_html=True)
    m_col1, m_col2 = st.columns([6, 4])
    
    with m_col1:
        st.markdown("#### 4. Bản Đồ Địa Lý Tương Tác (Scatter Map): Phân Bố Vị Trí Giao Dịch")
        df_map = safe_sample(df_loc, n=2000)
        if hasattr(px, "scatter_map"):
            fig_map = px.scatter_map(
                df_map, lat='lat', lon='lon', color='QUAN', size='GIA_BAN',
                center=dict(lat=40.7128, lon=-74.0060), zoom=9.5,
                map_style="carto-positron", hover_name="KHU_PHO",
                hover_data={'GIA_BAN': ':,.0f', 'DIEN_TICH_SU_DUNG': ':.0f', 'QUAN': True, 'lat': False, 'lon': False},
                size_max=18, opacity=0.75, template=theme
            )
        else:
            fig_map = px.scatter_mapbox(
                df_map, lat='lat', lon='lon', color='QUAN', size='GIA_BAN',
                center=dict(lat=40.7128, lon=-74.0060), zoom=9.5,
                mapbox_style="carto-positron", hover_name="KHU_PHO",
                hover_data={'GIA_BAN': ':,.0f', 'DIEN_TICH_SU_DUNG': ':.0f', 'QUAN': True, 'lat': False, 'lon': False},
                size_max=18, opacity=0.75, template=theme
            )
        fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=500)
        st.plotly_chart(fig_map, use_container_width=True)
        
    with m_col2:
        st.markdown("#### 5. Biểu đồ Mật Độ Nhiệt 2 Chiều (Density Heatmap): Tuổi Thọ Nhà vs Đơn Giá")
        p95_sqft_cut = df_loc['GIA_TREN_SQFT'].quantile(0.95)
        df_heat = df_loc[(df_loc['GIA_TREN_SQFT'] <= p95_sqft_cut) & (df_loc['TUOI_THO_NHA'] <= 140)]
        fig_density = px.density_heatmap(
            df_heat, x='TUOI_THO_NHA', y='GIA_TREN_SQFT',
            nbinsx=25, nbinsy=25, color_continuous_scale='Viridis', template=theme,
            labels={'TUOI_THO_NHA': 'Tuổi thọ công trình (Năm)', 'GIA_TREN_SQFT': 'Đơn giá / Sqft (USD)'}
        )
        fig_density.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=500)
        st.plotly_chart(fig_density, use_container_width=True)

# Tab 3: Cau truc do thi va drill-down
with tab3:
    st.markdown("<div class='insight-card'><b>Phân tích phân cấp:</b> Tính năng Drill-Down cho phép người dùng click trực tiếp vào từng ô trên Treemap để đào sâu từ toàn thành phố xuống từng Quận và từng Khu phố trực thuộc.</div>", unsafe_allow_html=True)
    t_col1, t_col2 = st.columns([6, 4])
    
    with t_col1:
        st.markdown("#### 6. Biểu đồ Treemap: Cấu Trúc Đô Thị & Drill-Down Phân Cấp")
        fig_tree = px.treemap(
            df_loc, path=[px.Constant("Toàn TP New York"), 'QUAN', 'KHU_PHO'],
            values='GIA_BAN', color='GIA_BAN', color_continuous_scale='Blues',
            template=theme
        )
        fig_tree.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=480)
        st.plotly_chart(fig_tree, use_container_width=True)
        
    with t_col2:
        st.markdown("#### 7. Biểu đồ Cột Ngang (Horizontal Bar): Top 10 Khu Phố Đắt Đỏ Nhất")
        top_khu = df_loc.groupby('KHU_PHO')['GIA_BAN'].median().reset_index().sort_values('GIA_BAN', ascending=False).head(10)
        fig_bar_h = px.bar(
            top_khu, x='GIA_BAN', y='KHU_PHO', orientation='h',
            color='GIA_BAN', color_continuous_scale='Reds', template=theme,
            labels={'GIA_BAN': 'Giá bán trung vị (USD)', 'KHU_PHO': 'Khu phố'}
        )
        fig_bar_h.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            margin=dict(l=20, r=20, t=20, b=20), height=480, showlegend=False
        )
        st.plotly_chart(fig_bar_h, use_container_width=True)

    st.markdown("---")
    st.markdown("### Khảo Sát Chi Tiết Từng Quận (Drill-Down Inspector)")
    chon_quan_dd = st.selectbox("Chọn quận để phân tích chuyên sâu cấp Khu Phố:", options=ds_quan_all)
    df_quan_selected = df_loc[df_loc['QUAN'] == chon_quan_dd]
    
    if len(df_quan_selected) > 0:
        dd1, dd2 = st.columns([5, 5])
        with dd1:
            top_kp_quan = df_quan_selected.groupby('KHU_PHO')['GIA_BAN'].median().reset_index().sort_values('GIA_BAN', ascending=False).head(8)
            fig_dd_bar = px.bar(
                top_kp_quan, x='KHU_PHO', y='GIA_BAN', text_auto='.2s',
                title=f"Top Khu Phố Thuộc Quận {chon_quan_dd}",
                color='GIA_BAN', color_continuous_scale='Teal', template=theme
            )
            fig_dd_bar.update_layout(xaxis_tickangle=-30, height=340)
            st.plotly_chart(fig_dd_bar, use_container_width=True)
            
        with dd2:
            st.markdown(f"**Thông tin tổng hợp quận {chon_quan_dd}:**")
            st.write(f"- Tổng số giao dịch ghi nhận: **{len(df_quan_selected):,}** căn")
            st.write(f"- Mức giá cao nhất: **${df_quan_selected['GIA_BAN'].max():,.0f}**")
            st.write(f"- Mức giá trung vị: **${df_quan_selected['GIA_BAN'].median():,.0f}**")
            st.write(f"- Đơn giá trung vị / sqft: **${df_quan_selected['GIA_TREN_SQFT'].median():,.0f} / sqft**")
            mode_kp = df_quan_selected['KHU_PHO'].mode()
            if len(mode_kp) > 0:
                st.write(f"- Khu phố có nhiều giao dịch nhất: **{mode_kp.values[0]}**")

# Tab 4: Dac diem cong trinh va quy mo
with tab4:
    st.markdown("<div class='insight-card'><b>Phân tích đặc điểm:</b> Khảo sát phân tán thống kê giá bán, khoảng tứ phân vị (IQR), các giá trị dị biệt (outliers) và nhóm quy mô diện tích công trình.</div>", unsafe_allow_html=True)
    p_col1, p_col2 = st.columns(2)
    
    with p_col1:
        st.markdown("#### 8. Biểu đồ Cột Đứng: Mức Giá Bán Trung Vị Theo Nhóm Diện Tích")
        bins = [0, 1000, 2000, 3000, 5000, np.inf]
        labels = ['Nhỏ (<1000)', 'Vừa (1000-2000)', 'Lớn (2000-3000)', 'Rất Lớn (3000-5000)', 'Biệt Thự/Tòa Nhà (>5000)']
        df_loc_copy = df_loc.copy()
        df_loc_copy['NHOM_DIEN_TICH'] = pd.cut(df_loc_copy['DIEN_TICH_SU_DUNG'], bins=bins, labels=labels)
        df_bin = df_loc_copy.groupby('NHOM_DIEN_TICH', observed=False)['GIA_BAN'].median().reset_index()
        fig_bar_v = px.bar(
            df_bin, x='NHOM_DIEN_TICH', y='GIA_BAN', text_auto='.2s',
            color='NHOM_DIEN_TICH', color_discrete_sequence=px.colors.sequential.Teal,
            template=theme, labels={'NHOM_DIEN_TICH': 'Nhóm Diện Tích (Sqft)', 'GIA_BAN': 'Giá Trung Vị (USD)'}
        )
        fig_bar_v.update_layout(showlegend=False, margin=dict(l=20, r=20, t=20, b=20), height=400)
        st.plotly_chart(fig_bar_v, use_container_width=True)
        
    with p_col2:
        st.markdown("#### 9. Biểu đồ Hộp (Box Plot): Phân Phối Giá Bán Theo Từng Quận")
        df_box_sample = safe_sample(df_loc, n=3000)
        fig_box = px.box(
            df_box_sample, x='QUAN', y='LOG_GIA_BAN', color='QUAN',
            template=theme, points="outliers",
            labels={'QUAN': 'Quận', 'LOG_GIA_BAN': 'Log Giá Bán (USD)'}
        )
        fig_box.update_layout(showlegend=False, margin=dict(l=20, r=20, t=20, b=20), height=400)
        st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("#### 10. Biểu đồ Tần Suất (Histogram): Phân Bố Đơn Giá / Sqft")
    p95_sqft = df_loc['GIA_TREN_SQFT'].quantile(0.95)
    df_hist_sub = df_loc[df_loc['GIA_TREN_SQFT'] <= p95_sqft]
    fig_hist = px.histogram(
        df_hist_sub, x='GIA_TREN_SQFT', nbins=50, marginal='box',
        color_discrete_sequence=['#4F46E5'], template=theme,
        labels={'GIA_TREN_SQFT': 'Đơn giá / Sqft (USD)'}
    )
    fig_hist.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=380)
    st.plotly_chart(fig_hist, use_container_width=True)

# Tab 5: Hoc may dinh gia bat dong san
with tab5:
    st.markdown("<div class='insight-card'><b>Mô hình học máy định giá:</b> Ứng dụng thuật toán Random Forest Regressor để định giá tài sản đa biến dựa trên đặc điểm công trình (Diện tích, Tuổi thọ), điều kiện dân cư (Thu nhập) và vị trí địa lý (Quận).</div>", unsafe_allow_html=True)
    
    rf_data = None
    ai_model = None
    ai_features = None
    try:
        rf_data = joblib.load('nyc_rf_model.pkl')
        ai_model = rf_data['model']
        ai_features = list(rf_data['features'])
    except Exception:
        pass
        
    col_left, col_right = st.columns([1.2, 1], gap="large")
    
    with col_left:
        st.markdown("#### Mức Độ Quan Trọng Của Đặc Trưng (Feature Importances)")
        st.write("Bảng dưới đây giải thích mức độ đóng góp của từng yếu tố vào quyết định định giá của mô hình:")
        
        if ai_model is not None:
            if hasattr(ai_model, 'feature_importances_'):
                importances = ai_model.feature_importances_
            else:
                importances = np.abs(ai_model.coef_)
                
            df_importances = pd.DataFrame({
                'Đặc trưng': ai_features,
                'Mức độ đóng góp (Weight)': importances
            }).sort_values(by='Mức độ đóng góp (Weight)', ascending=False)
            
            df_importances['Đặc trưng'] = df_importances['Đặc trưng'].str.replace('Quan_', 'Vị trí: ')
            st.dataframe(df_importances.style.format({'Mức độ đóng góp (Weight)': '{:.5f}'}), use_container_width=True, height=250)
            
            met = rf_data.get('metrics', {}) if rf_data else {}
            if met:
                m1, m2, m3 = st.columns(3)
                m1.metric("R² Score (Test)", f"{met.get('R2_log', 0):.2f}")
                m2.metric("MAE (Sai số TB)", f"${met.get('MAE_usd', 0):,.0f}")
                m3.metric("Sai lệch trung vị", f"{met.get('MedAPE_%', 0):.1f}%")
                st.caption(f"Mô hình lựa chọn: **{rf_data.get('model_name', 'Random Forest')}** — kiểm thử độc lập trên 20% dữ liệu Test.")
        else:
            st.warning("Đang chờ tải mô hình... Vui lòng chạy `python train_model.py` để tạo `nyc_rf_model.pkl`.")
            
    with col_right:
        st.markdown("#### Mô Phỏng Dự Báo Giá Trị Bất Động Sản")
        st.write("Nhập các thông số đặc điểm và vị trí thực tế bên dưới để mô hình định giá:")
        
        sim_quan = st.selectbox("Chọn Vị trí Quận:", options=ds_quan_all, key="sim_quan_box")
        sim_dt = st.number_input("Diện tích sử dụng (Sqft):", min_value=100, max_value=20000, value=1500, step=100)
        sim_tuoi = st.number_input("Tuổi thọ công trình (Năm):", min_value=0, max_value=200, value=20, step=1)
        
        thu_nhap_goi_y = 60000.0
        if rf_data and 'income_by_borough' in rf_data:
            thu_nhap_goi_y = float(rf_data['income_by_borough'].get(sim_quan, 60000.0))
        sim_thu_nhap = st.number_input("Thu nhập hộ gia đình trung vị (USD/năm):", min_value=10000, max_value=250000, value=int(thu_nhap_goi_y), step=1000)
        sim_nam_du_phong = st.slider("Số năm dự phóng tương lai:", min_value=1, max_value=50, value=20, step=1)
        
        if st.button("Dự Báo Giá Trị Bất Động Sản", type="primary", use_container_width=True):
            if ai_model is not None:
                try:
                    input_df = pd.DataFrame(0.0, index=[0], columns=ai_features)
                    
                    for c_dt in ['DIEN_TICH_SU_DUNG', 'GROSS SQUARE FEET']:
                        if c_dt in input_df.columns:
                            input_df[c_dt] = float(sim_dt)
                    for c_t in ['TUOI_THO_NHA', 'PROPERTY_AGE']:
                        if c_t in input_df.columns:
                            input_df[c_t] = float(sim_tuoi)
                    for c_inc in ['MEDIAN_HOUSEHOLD_INCOME', 'THU_NHAP_TRUNG_BINH']:
                        if c_inc in input_df.columns:
                            input_df[c_inc] = float(sim_thu_nhap)
                    quan_col = f"Quan_{sim_quan}"
                    if quan_col in input_df.columns:
                        input_df[quan_col] = 1.0
                        
                    pred_log = ai_model.predict(input_df)[0]
                    pred_price = np.expm1(pred_log)
                    
                    ty_le_tang = 0.045
                    future_price = pred_price * ((1 + ty_le_tang) ** sim_nam_du_phong)
                    
                    st.success(f"Giá trị dự báo hiện tại: **${pred_price:,.0f} USD**")
                    st.info(f"Đơn giá dự kiến: **${pred_price/sim_dt:,.0f} / Sqft** | Mức Log Giá: **{pred_log:.2f}**")
                    st.warning(f"Dự phóng {sim_nam_du_phong} năm sau: **${future_price:,.0f} USD** (Tăng trưởng kỳ vọng {ty_le_tang*100:.1f}%/năm)")
                except Exception as e:
                    st.error(f"Lỗi khi dự báo: {e}")
            else:
                st.error("Vui lòng huấn luyện mô hình bằng `python train_model.py` trước.")

    st.markdown("---")
    
    c_bot1, c_bot2 = st.columns([1, 1], gap="medium")
    
    with c_bot1:
        st.markdown(f"#### 11. Biểu đồ Xu Hướng Hồi Quy OLS: Diện Tích vs Giá ({sim_quan})")
        df_trend_sub = df_loc[df_loc['QUAN'] == sim_quan].copy()
        if len(df_trend_sub) > 0:
            df_trend_clean = df_trend_sub[df_trend_sub['GIA_BAN'] < df_trend_sub['GIA_BAN'].quantile(0.95)]
        else:
            df_trend_clean = df_trend_sub
            
        if len(df_trend_clean) > 5:
            df_plot_trend = safe_sample(df_trend_clean, n=800)
            fig_reg = px.scatter(
                df_plot_trend, x='DIEN_TICH_SU_DUNG', y='GIA_BAN',
                trendline="ols", opacity=0.6, template=theme,
                color_discrete_sequence=['#2E86AB'],
                labels={'DIEN_TICH_SU_DUNG': 'Diện tích (Sqft)', 'GIA_BAN': 'Giá thực tế (USD)'}
            )
            fig_reg.update_traces(line=dict(color="#D1495B", width=3.5), selector=dict(mode="lines"))
            fig_reg.update_layout(height=380, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_reg, use_container_width=True)
        else:
            st.warning(f"Không đủ dữ liệu để vẽ xu hướng cho {sim_quan}.")

    with c_bot2:
        st.markdown("#### 12. Đối Chiếu: Giá Thực Tế vs AI Dự Báo (Đường Lý Tưởng y=x)")
        try:
            df_eval_sample = safe_sample(df_loc.dropna(subset=['GIA_BAN', 'DIEN_TICH_SU_DUNG', 'TUOI_THO_NHA']), n=800)
            if len(df_eval_sample) > 0 and ai_model is not None:
                X_eval = pd.DataFrame(0.0, index=df_eval_sample.index, columns=ai_features)
                for c_dt in ['DIEN_TICH_SU_DUNG', 'GROSS SQUARE FEET']:
                    if c_dt in X_eval.columns:
                        X_eval[c_dt] = df_eval_sample['DIEN_TICH_SU_DUNG']
                for c_t in ['TUOI_THO_NHA', 'PROPERTY_AGE']:
                    if c_t in X_eval.columns:
                        X_eval[c_t] = df_eval_sample['TUOI_THO_NHA']
                for c_inc in ['MEDIAN_HOUSEHOLD_INCOME', 'THU_NHAP_TRUNG_BINH']:
                    if c_inc in X_eval.columns:
                        if 'THU_NHAP_TRUNG_BINH' in df_eval_sample.columns:
                            X_eval[c_inc] = df_eval_sample['THU_NHAP_TRUNG_BINH'].fillna(df_eval_sample['THU_NHAP_TRUNG_BINH'].median())
                        else:
                            inc_map = rf_data.get('income_by_borough', {}) if rf_data else {}
                            X_eval[c_inc] = df_eval_sample['QUAN'].map(inc_map).fillna(60000)
                            
                for q_name in df_eval_sample['QUAN'].unique():
                    q_c = f"Quan_{q_name}"
                    if q_c in X_eval.columns:
                        X_eval.loc[df_eval_sample['QUAN'] == q_name, q_c] = 1.0
                        
                preds_log = ai_model.predict(X_eval)
                df_eval_sample['GIA_DU_BAO'] = np.expm1(preds_log)
                
                fig_eval = px.scatter(
                    df_eval_sample, x='GIA_BAN', y='GIA_DU_BAO', color='QUAN',
                    opacity=0.65, template=theme, log_x=True, log_y=True,
                    labels={'GIA_BAN': 'Giá Thực Tế (USD)', 'GIA_DU_BAO': 'Giá AI Dự Báo (USD)'}
                )
                min_v = min(df_eval_sample['GIA_BAN'].min(), df_eval_sample['GIA_DU_BAO'].min(), 10000)
                max_v = max(df_eval_sample['GIA_BAN'].max(), df_eval_sample['GIA_DU_BAO'].max(), 50000000)
                fig_eval.add_trace(go.Scatter(
                    x=[min_v, max_v], y=[min_v, max_v], mode='lines',
                    line=dict(color='black', dash='dash', width=2), name='Đường lý tưởng (y=x)'
                ))
                fig_eval.update_layout(height=380, margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(fig_eval, use_container_width=True)
            else:
                st.warning("Đang tải dữ liệu kiểm định mô hình...")
        except Exception as e:
            st.warning("Vui lòng đảm bảo mô hình đã được huấn luyện đầy đủ.")

# Tab 6: Du bao xu huong thi truong
with tab6:
    st.markdown("<div class='insight-card'><b>Hồi quy xu hướng chuỗi thời gian:</b> Mô hình học xu hướng theo tháng từ dữ liệu lịch sử, mở rộng dự phóng ra tương lai kèm <b>khoảng tin cậy 95%</b> và đo kiểm ý nghĩa thống kê (p-value, R²).</div>", unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)
    chi_so = f1.selectbox("Chỉ số dự báo:", ["Giá trung vị (USD)", "Đơn giá trung vị / Sqft (USD)", "Số lượng giao dịch"])
    pham_vi = f2.selectbox("Khu vực thị trường:", ["Toàn New York"] + ds_quan_all)
    so_thang = f3.slider("Số tháng dự báo tương lai:", min_value=1, max_value=12, value=6)

    df_fc = df_loc if pham_vi == "Toàn New York" else df_loc[df_loc['QUAN'] == pham_vi]

    if chi_so.startswith("Giá trung vị"):
        chuoi = df_fc.groupby('THANG_NAM_BAN')['GIA_BAN'].median()
    elif chi_so.startswith("Đơn giá"):
        chuoi = df_fc.groupby('THANG_NAM_BAN')['GIA_TREN_SQFT'].median()
    else:
        chuoi = df_fc.groupby('THANG_NAM_BAN')['GIA_BAN'].count()
    chuoi = chuoi.dropna().sort_index()

    if len(chuoi) < 4:
        st.warning("Cần tối thiểu 4 tháng dữ liệu để chạy mô hình hồi quy. Vui lòng mở rộng bộ lọc ở thanh bên.")
    else:
        st.markdown(f"#### 13. Biểu đồ Dự Báo Xu Hướng: {chi_so} ({pham_vi}) Kèm Khoảng Tin Cậy 95%")
        
        # Tinh toan hoi quy tuyen tinh va khoang tin cay 95%
        t = np.arange(len(chuoi))
        y = chuoi.values.astype(float)
        res = stats.linregress(t, y)
        n = len(t)
        y_fit = res.intercept + res.slope * t
        sigma = np.sqrt(np.sum((y - y_fit) ** 2) / max(1, (n - 2)))
        t_crit = stats.t.ppf(0.975, max(1, n - 2))

        thang_cuoi = pd.Period(chuoi.index[-1], freq="M")
        nhan_tuong_lai = [str(thang_cuoi + i) for i in range(1, so_thang + 1)]
        t_f = np.arange(n, n + so_thang)
        y_f = res.intercept + res.slope * t_f
        se_pred = sigma * np.sqrt(1 + 1 / n + (t_f - t.mean()) ** 2 / max(1e-5, np.sum((t - t.mean()) ** 2)))
        
        if chi_so.startswith("Số lượng"):
            y_f = np.clip(y_f, 0, None)
        low = np.clip(y_f - t_crit * se_pred, 0, None)
        high = y_f + t_crit * se_pred

        tien_to = "" if chi_so.startswith("Số lượng") else "$"
        def fm(v): return f"{tien_to}{v:,.0f}"

        fig_fc = go.Figure()
        fig_fc.add_vrect(x0=chuoi.index[-1], x1=nhan_tuong_lai[-1], fillcolor="rgba(245,158,11,0.07)", line_width=0)
        fig_fc.add_annotation(x=nhan_tuong_lai[0], y=1.0, yref="paper", text="VÙNG DỰ BÁO TƯƠNG LAI", showarrow=False,
                              xanchor="left", yanchor="bottom", font=dict(size=11, color="#B45309"))
        fig_fc.add_trace(go.Scatter(x=nhan_tuong_lai + nhan_tuong_lai[::-1], y=list(high) + list(low[::-1]),
                                    mode="lines", fill="toself", fillcolor="rgba(245,158,11,0.22)", line=dict(width=0),
                                    name="Khoảng tin cậy 95%", hoverinfo="skip"))
        fig_fc.add_trace(go.Scatter(x=list(chuoi.index), y=y_fit, mode="lines", name="Đường xu hướng (Fitted OLS)",
                                    line=dict(color="#9CA3AF", width=2, dash="dot"), hoverinfo="skip"))
        fig_fc.add_trace(go.Scatter(x=list(chuoi.index), y=y, mode="lines+markers", name="Thực tế",
                                    line=dict(color="#2563EB", width=3), marker=dict(size=7)))
        fig_fc.add_trace(go.Scatter(x=[chuoi.index[-1]] + nhan_tuong_lai, y=[y_fit[-1]] + list(y_f),
                                    mode="lines+markers", name="Dự báo xu hướng",
                                    line=dict(color="#F59E0B", width=3, dash="dash"), marker=dict(size=7)))
                                    
        fig_fc.add_annotation(x=chuoi.index[-1], y=y[-1], text=f"Thực tế {chuoi.index[-1]}<br><b>{fm(y[-1])}</b>",
                              showarrow=True, arrowhead=0, ax=-50, ay=-40, font=dict(color="#2563EB", size=11))
        fig_fc.add_annotation(x=nhan_tuong_lai[-1], y=y_f[-1], text=f"Dự báo {nhan_tuong_lai[-1]}<br><b>{fm(y_f[-1])}</b>",
                              showarrow=True, arrowhead=0, ax=0, ay=-45, font=dict(color="#B45309", size=11))
                              
        fig_fc.update_layout(template=theme, height=450, hovermode="x unified",
                             xaxis_title=None, yaxis_title=chi_so, yaxis_tickformat=",.0f",
                             legend=dict(orientation="h", y=1.1, x=0), margin=dict(t=40, l=20, r=20, b=20))
        st.plotly_chart(fig_fc, use_container_width=True)

        doi_phan_tram = (res.slope / y.mean() * 100) if y.mean() != 0 else 0
        lech_xu_huong = ((y[-1] / y_fit[-1] - 1) * 100) if y_fit[-1] != 0 else 0
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Mức biến động mỗi tháng", f"{tien_to}{res.slope:+,.0f}", f"{doi_phan_tram:+.2f}% / tháng")
        k2.metric("R² (Độ phù hợp xu hướng)", f"{res.rvalue ** 2:.2f}", help="Hệ số xác định tương quan tuyến tính")
        k3.metric("p-value", f"{res.pvalue:.3f}", help="p < 0.05 thể hiện xu hướng có ý nghĩa thống kê tin cậy")
        k4.metric(f"Dự báo {nhan_tuong_lai[-1]}", fm(y_f[-1]), f"{(y_f[-1] / y.mean() - 1) * 100:+.1f}% so với TB")

        huong = "tăng" if res.slope > 0 else "giảm"
        co_y_nghia = res.pvalue < 0.05
        dong_lech = ""
        if abs(lech_xu_huong) >= 5:
            dong_lech = (f"\n- **Lưu ý tháng cuối:** Tháng {chuoi.index[-1]} thực tế ({fm(y[-1])}) "
                         f"{'cao hơn' if lech_xu_huong > 0 else 'thấp hơn'} đường xu hướng {abs(lech_xu_huong):.0f}% "
                         f"(biến động ngắn hạn).")
        st.info(
            f"**Kết luận Insight:** {chi_so} tại **{pham_vi}** đang có xu hướng **{huong} {abs(doi_phan_tram):.2f}%/tháng** "
            f"({tien_to}{res.slope:+,.0f}/tháng).\n"
            f"- **Độ tin cậy thống kê:** " + ("Xu hướng **có ý nghĩa thống kê** (p < 0.05)." if co_y_nghia else
                                    "Xu hướng **chưa đủ ý nghĩa thống kê** (p ≥ 0.05), chỉ nên xem là tham khảo.") + "\n"
            f"- **Kỳ vọng {nhan_tuong_lai[-1]}:** {fm(y_f[-1])} (biên độ dao động 95%: {fm(low[-1])} – {fm(high[-1])})."
            + dong_lech
        )

        with st.expander("Xem chi tiết bảng số liệu dự báo theo tháng"):
            bang = pd.DataFrame({
                "Tháng tương lai": nhan_tuong_lai,
                "Giá trị dự báo": y_f.round(0),
                "Cận dưới (95% CI)": low.round(0),
                "Cận trên (95% CI)": high.round(0)
            })
            st.dataframe(bang.style.format({
                "Giá trị dự báo": "{:,.0f}",
                "Cận dưới (95% CI)": "{:,.0f}",
                "Cận trên (95% CI)": "{:,.0f}"
            }), use_container_width=True, hide_index=True)
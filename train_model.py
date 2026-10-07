import sys
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

print("Dang tai va xu ly du lieu...")
try:
    df = pd.read_csv('final_dashboard_data.csv', low_memory=False)
except FileNotFoundError:
    try:
        df = pd.read_csv('du_lieu_dashboard_tieng_viet.csv', low_memory=False)
    except FileNotFoundError:
        df = pd.read_csv('du_lieu_da_xu_ly.csv', low_memory=False)

col_quan = 'QUAN' if 'QUAN' in df.columns else 'Borough'
col_gia = 'GIA_BAN' if 'GIA_BAN' in df.columns else 'SALE PRICE'
col_dien_tich = 'DIEN_TICH_SU_DUNG' if 'DIEN_TICH_SU_DUNG' in df.columns else 'GROSS SQUARE FEET'
col_tuoi = 'TUOI_THO_NHA' if 'TUOI_THO_NHA' in df.columns else 'PROPERTY_AGE'
col_thu_nhap = 'MEDIAN_HOUSEHOLD_INCOME' if 'MEDIAN_HOUSEHOLD_INCOME' in df.columns else 'THU_NHAP_TRUNG_BINH'

# Xu ly gia tri khuyet va ngoai lai
df = df.dropna(subset=[col_gia, col_dien_tich, col_tuoi, col_quan])
df = df[df[col_gia] > 1000].copy()

thu_nhap_quan = df.groupby(col_quan)[col_thu_nhap].median()
df[col_thu_nhap] = df[col_thu_nhap].fillna(df[col_quan].map(thu_nhap_quan))

def loc_ngoai_le(g):
    return g[(g[col_gia] <= g[col_gia].quantile(0.95)) &
             (g[col_dien_tich] <= g[col_dien_tich].quantile(0.99))]

df_clean = pd.concat([loc_ngoai_le(g) for _, g in df.groupby(col_quan)])
print(f"So giao dich hop le sau khi loc: {len(df_clean):,}")

# Chuan bi bien dac trung va muc tieu log(gia)
X = df_clean[[col_dien_tich, col_tuoi, col_thu_nhap]].copy()
X = pd.concat([X, pd.get_dummies(df_clean[col_quan], prefix='Quan')], axis=1)
y = np.log1p(df_clean[col_gia])

# Phan chia tap train/test va danh gia mo hinh
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

def danh_gia(m):
    p = m.predict(X_test)
    gia_that, gia_db = np.expm1(y_test), np.expm1(p)
    return {
        'R2_log': r2_score(y_test, p),
        'MAE_usd': mean_absolute_error(gia_that, gia_db),
        'MedAPE_%': float(np.median(np.abs(gia_that - gia_db) / gia_that) * 100)
    }

ung_vien = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(n_estimators=200, min_samples_leaf=3, random_state=42, n_jobs=-1),
}

ket_qua = {}
for ten, m in ung_vien.items():
    print(f"Huan luyen {ten}...")
    m.fit(X_train, y_train)
    ket_qua[ten] = danh_gia(m)
    r = ket_qua[ten]
    print(f"  R2 = {r['R2_log']:.3f} | MAE = ${r['MAE_usd']:,.0f} | MedAPE = {r['MedAPE_%']:.1f}%")

ten_tot = max(ket_qua, key=lambda k: ket_qua[k]['R2_log'])
print(f"Mo hinh tot nhat: {ten_tot}")

best = ung_vien[ten_tot]
best.fit(X, y)

joblib.dump({
    'model': best,
    'features': X.columns,
    'model_name': ten_tot,
    'metrics': ket_qua[ten_tot],
    'all_metrics': ket_qua,
    'income_by_borough': thu_nhap_quan.to_dict(),
}, 'nyc_rf_model.pkl')
print("Da luu mo hinh tai: nyc_rf_model.pkl")

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Bang mau sac chuyen nghiep sang trong
NAVY = RGBColor(15, 23, 42)          # Slate 900
DARK_BLUE = RGBColor(30, 58, 138)     # Blue 900
ACCENT_BLUE = RGBColor(37, 99, 235)   # Blue 600
LIGHT_BLUE = RGBColor(239, 246, 255)  # Blue 50
TEXT_MAIN = RGBColor(30, 41, 59)      # Slate 800
TEXT_MUTED = RGBColor(100, 116, 139)  # Slate 500
WHITE = RGBColor(255, 255, 255)
BG_LIGHT = RGBColor(248, 250, 252)    # Slate 50
CARD_BG = RGBColor(255, 255, 255)
CARD_BORDER = RGBColor(226, 232, 240)
EMERALD = RGBColor(16, 185, 129)
AMBER = RGBColor(245, 158, 11)
ROSE = RGBColor(225, 29, 72)
CYAN = RGBColor(6, 182, 212)
CODE_BG = RGBColor(241, 245, 249)

def set_slide_background(slide, color):
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = color
    bg_shape.line.fill.background()
    return bg_shape

def create_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)
    else:
        card.line.fill.background()
    return card

def add_header(slide, title_text, category_badge="NYC PROPVISION", subtitle_text=""):
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.35), Inches(2.3), Inches(0.32))
    badge.fill.solid()
    badge.fill.fore_color.rgb = LIGHT_BLUE
    badge.line.color.rgb = ACCENT_BLUE
    badge.line.width = Pt(1)
    tf_b = badge.text_frame
    tf_b.word_wrap = True
    tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_b = tf_b.paragraphs[0]
    p_b.text = category_badge.upper()
    p_b.font.size = Pt(9.5)
    p_b.font.bold = True
    p_b.font.color.rgb = ACCENT_BLUE
    p_b.alignment = PP_ALIGN.CENTER
    
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.75))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = NAVY
    
    if subtitle_text:
        p2 = tf.add_paragraph()
        p2.text = subtitle_text
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MUTED

def add_code_box(slide, left, top, width, height, code_text):
    cbox = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    cbox.fill.solid()
    cbox.fill.fore_color.rgb = CODE_BG
    cbox.line.color.rgb = RGBColor(203, 213, 225)
    cbox.line.width = Pt(1)
    tf = cbox.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = code_text
    p.font.name = "Consolas"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE
    return cbox

# ==================== SLIDE 1: BIA DE TAI ====================
slide1 = prs.slides.add_slide(blank_layout)
set_slide_background(slide1, NAVY)

dec = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.4), Inches(7.5))
dec.fill.solid()
dec.fill.fore_color.rgb = ACCENT_BLUE
dec.line.fill.background()

tb1 = slide1.shapes.add_textbox(Inches(1.2), Inches(1.3), Inches(11.0), Inches(3.2))
tf1 = tb1.text_frame
tf1.word_wrap = True

p_sub = tf1.paragraphs[0]
p_sub.text = "BÁO CÁO ĐỒ ÁN MÔN HỌC • TƯƠNG TÁC DỮ LIỆU VÀ TRỰC QUAN HÓA"
p_sub.font.size = Pt(13)
p_sub.font.bold = True
p_sub.font.color.rgb = CYAN

p_main = tf1.add_paragraph()
p_main.text = "NYC PROPVISION: HỆ THỐNG TRỰC QUAN HÓA\nVÀ DỰ BÁO GIÁ BẤT ĐỘNG SẢN NEW YORK"
p_main.font.size = Pt(28)
p_main.font.bold = True
p_main.font.color.rgb = WHITE
p_main.space_before = Pt(14)

p_desc = tf1.add_paragraph()
p_desc.text = "Quy trình tiền xử lý hơn 84.000 giao dịch • Dashboard tương tác 6 phân hệ • Mô hình Hồi quy tuyến tính định giá"
p_desc.font.size = Pt(13)
p_desc.font.color.rgb = RGBColor(203, 213, 225)
p_desc.space_before = Pt(12)

card_info = create_card(slide1, Inches(1.2), Inches(4.8), Inches(11.0), Inches(1.8), bg_color=RGBColor(30, 41, 59), border_color=RGBColor(51, 65, 85))
tb_info = slide1.shapes.add_textbox(Inches(1.5), Inches(4.95), Inches(10.4), Inches(1.5))
tf_info = tb_info.text_frame
tf_info.word_wrap = True

p_g = tf_info.paragraphs[0]
p_g.text = "NHÓM THỰC HIỆN: NHÓM 10"
p_g.font.size = Pt(11)
p_g.font.bold = True
p_g.font.color.rgb = EMERALD

p_mem1 = tf_info.add_paragraph()
p_mem1.text = "Lê Huỳnh Anh Khôi • Nguyễn Thanh Tâm • Nguyễn Hữu Phát"
p_mem1.font.size = Pt(13)
p_mem1.font.bold = True
p_mem1.font.color.rgb = WHITE
p_mem1.space_before = Pt(6)

p_inst = tf_info.add_paragraph()
p_inst.text = "Khoa Công Nghệ Thông Tin • Bộ Môn Khoa Học Dữ Liệu Và Trực Quan Hóa"
p_inst.font.size = Pt(11)
p_inst.font.color.rgb = RGBColor(148, 163, 184)
p_inst.space_before = Pt(6)

# ==================== SLIDE 2: MUC LUC ====================
slide2 = prs.slides.add_slide(blank_layout)
set_slide_background(slide2, BG_LIGHT)
add_header(slide2, "MỤC LỤC BÁO CÁO", "CẤU TRÚC", "Tổng quan sáu nội dung trọng tâm từ tiền xử lý dữ liệu đến trực quan hóa và mô hình")

agenda_items = [
    ("01", "GIỚI THIỆU CHỦ ĐỀ", "Bối cảnh thị trường và mục tiêu nghiên cứu", DARK_BLUE),
    ("02", "NGUỒN DỮ LIỆU", "Ba tập dữ liệu gốc gồm DOF, Zipcodes và Census", ACCENT_BLUE),
    ("03", "TIỀN XỬ LÝ DỮ LIỆU", "Quy trình làm sạch, khử ngoại lai và kết nối bảng", ROSE),
    ("04", "KẾT QUẢ DỮ LIỆU SẠCH", "Kiểm định phân phối và ma trận tương quan đa biến", EMERALD),
    ("05", "THIẾT KẾ DASHBOARD", "Kiến trúc tương tác Streamlit và bộ lọc đa tầng", CYAN),
    ("06", "HỆ THỐNG BIỂU ĐỒ VÀ MÔ HÌNH", "Mười ba biểu đồ trực quan và mô hình hồi quy định giá", AMBER)
]

for idx, (num, title, desc, color) in enumerate(agenda_items):
    col = idx % 3
    row = idx // 3
    left = Inches(0.8 + col * 3.95)
    top = Inches(1.8 + row * 2.5)
    card = create_card(slide2, left, top, Inches(3.75), Inches(2.2))
    
    nbadge = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(0.7), Inches(0.5))
    nbadge.fill.solid()
    nbadge.fill.fore_color.rgb = color
    nbadge.line.fill.background()
    p_nb = nbadge.text_frame.paragraphs[0]
    p_nb.text = num
    p_nb.font.size = Pt(14)
    p_nb.font.bold = True
    p_nb.font.color.rgb = WHITE
    p_nb.alignment = PP_ALIGN.CENTER
    
    tb = slide2.shapes.add_textbox(left + Inches(0.2), top + Inches(0.55), Inches(3.35), Inches(1.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p_t = tf.paragraphs[0]
    p_t.text = title
    p_t.font.size = Pt(12.5)
    p_t.font.bold = True
    p_t.font.color.rgb = NAVY
    p_d = tf.add_paragraph()
    p_d.text = desc
    p_d.font.size = Pt(10.5)
    p_d.font.color.rgb = TEXT_MUTED
    p_d.space_before = Pt(6)

# ==================== SLIDE 3: GIOI THIEU DE TAI ====================
slide3 = prs.slides.add_slide(blank_layout)
set_slide_background(slide3, BG_LIGHT)
add_header(slide3, "1. GIỚI THIỆU CHỦ ĐỀ VÀ TÍNH CẤP THIẾT", "PHẦN 1", "Động lực nghiên cứu và giải pháp công nghệ tiếp cận")

cards_p1 = [
    ("BỐI CẢNH THỊ TRƯỜNG", [
        "Thị trường địa ốc New York đắt đỏ và phân hóa sâu sắc.",
        "Sự chênh lệch lớn giữa năm quận hành chính.",
        "Nhu cầu minh bạch hóa thông tin định giá tài sản."
    ], "MỤC TIÊU: MINH BẠCH DỮ LIỆU", DARK_BLUE),
    ("THÁCH THỨC DỮ LIỆU", [
        "Dữ liệu mở quy mô lớn hơn 84.000 dòng.",
        "Tỷ lệ nhiễu cao với hơn 29.000 giao dịch 0 USD.",
        "Thiếu công cụ trực quan hóa tương tác đa chiều."
    ], "VẤN ĐỀ: DỮ LIỆU NHIỄU", ROSE),
    ("GIẢI PHÁP ĐỀ TÀI", [
        "Quy trình tiền xử lý dữ liệu chuẩn khoa học.",
        "Dashboard tương tác 6 phân hệ với 13 biểu đồ.",
        "Mô hình Hồi quy tuyến tính định giá tự động."
    ], "GIẢI PHÁP: TRỰC QUAN VÀ AI", EMERALD)
]

for idx, (title, points, pill, col) in enumerate(cards_p1):
    left = Inches(0.8 + idx * 3.95)
    top = Inches(1.7)
    card = create_card(slide3, left, top, Inches(3.75), Inches(5.1))
    
    bar = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(3.75), Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = col
    bar.line.fill.background()
    
    tb = slide3.shapes.add_textbox(left + Inches(0.25), top + Inches(0.25), Inches(3.25), Inches(3.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p_t = tf.paragraphs[0]
    p_t.text = title
    p_t.font.size = Pt(13)
    p_t.font.bold = True
    p_t.font.color.rgb = col
    
    for pt in points:
        p = tf.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(18)
        
    pill_box = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.25), top + Inches(4.3), Inches(3.25), Inches(0.48))
    pill_box.fill.solid()
    pill_box.fill.fore_color.rgb = LIGHT_BLUE
    pill_box.line.color.rgb = col
    pill_box.line.width = Pt(1)
    p_pl = pill_box.text_frame.paragraphs[0]
    p_pl.text = pill
    p_pl.font.size = Pt(9.5)
    p_pl.font.bold = True
    p_pl.font.color.rgb = col
    p_pl.alignment = PP_ALIGN.CENTER
    pill_box.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE

# ==================== SLIDE 4: BA NGUON DU LIEU ====================
slide4 = prs.slides.add_slide(blank_layout)
set_slide_background(slide4, BG_LIGHT)
add_header(slide4, "2. NGUỒN DỮ LIỆU ĐẦU VÀO", "PHẦN 2", "Thu thập và kết hợp ba tập dữ liệu độc lập từ Kaggle và cổng dữ liệu mở New York")

datasets = [
    ("BẢNG 1: NYC ROLLING SALES", "DỮ LIỆU GIAO DỊCH CHÍNH", [
        "Quy mô: 84.548 dòng, 22 thuộc tính.",
        "Thời gian: Giao dịch địa ốc trong 12 tháng.",
        "Trường dữ liệu: Giá bán, diện tích, năm xây dựng, vị trí quận."
    ], DARK_BLUE),
    ("BẢNG 2: NYC ZIP CODES", "TỌA ĐỘ VÀ BẢN ĐỒ ĐỊA LÝ", [
        "Khóa liên kết: Mã bưu chính ZIP Code.",
        "Thuộc tính bổ sung: Vĩ độ và kinh độ địa lý.",
        "Ứng dụng: Xây dựng bản đồ phân bố không gian."
    ], ACCENT_BLUE),
    ("BẢNG 3: US CENSUS", "NHÂN KHẨU VÀ THU NHẬP", [
        "Nguồn: Cục Thống kê Dân số Hoa Kỳ.",
        "Thuộc tính bổ sung: Thu nhập trung vị hộ gia đình.",
        "Ứng dụng: Khảo sát tương quan kinh tế xã hội với giá nhà."
    ], EMERALD)
]

for idx, (title, sub, pts, col) in enumerate(datasets):
    left = Inches(0.8 + idx * 3.95)
    top = Inches(1.7)
    card = create_card(slide4, left, top, Inches(3.75), Inches(5.1))
    
    bar = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(3.75), Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = col
    bar.line.fill.background()
    
    tb = slide4.shapes.add_textbox(left + Inches(0.25), top + Inches(0.3), Inches(3.25), Inches(4.5))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p_t = tf.paragraphs[0]
    p_t.text = title
    p_t.font.size = Pt(12)
    p_t.font.bold = True
    p_t.font.color.rgb = col
    
    p_sub = tf.add_paragraph()
    p_sub.text = sub
    p_sub.font.size = Pt(10)
    p_sub.font.bold = True
    p_sub.font.color.rgb = TEXT_MUTED
    p_sub.space_before = Pt(4)
    
    for pt in pts:
        p = tf.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(22)

# ==================== SLIDE 5: SO DO PIPELINE ====================
slide5 = prs.slides.add_slide(blank_layout)
set_slide_background(slide5, BG_LIGHT)
add_header(slide5, "3. QUY TRÌNH TIỀN XỬ LÝ DỮ LIỆU TỔNG THỂ", "PHẦN 3", "Đường ống năm giai đoạn chuyển hóa dữ liệu thô thành tập dữ liệu phân tích chuẩn hóa")

pipe_img_path = r"images\00_pipeline_architecture.png"
if os.path.exists(pipe_img_path):
    slide5.shapes.add_picture(pipe_img_path, Inches(0.8), Inches(1.7), Inches(5.8), Inches(5.1))
else:
    create_card(slide5, Inches(0.8), Inches(1.7), Inches(5.8), Inches(5.1))

pipe_steps = [
    ("GIAI ĐOẠN 1", "ÉP KIỂU VÀ LÀM SẠCH KÝ TỰ", "Chuyển kiểu chuỗi sang số thực, khử ký tự rác và dấu phân cách.", DARK_BLUE),
    ("GIAI ĐOẠN 2", "KHỬ DỮ LIỆU KHUYẾT THIẾU", "Điền khuyết bằng trung vị theo từng quận cho diện tích và thu nhập.", ACCENT_BLUE),
    ("GIAI ĐOẠN 3", "LỌC DỮ LIỆU NGOẠI LAI", "Khử giao dịch 0 USD và áp dụng lọc phân vị cục bộ 95% giá, 99% diện tích.", ROSE),
    ("GIAI ĐOẠN 4", "LIÊN KẾT ĐA NGUỒN", "Hợp nhất ba bảng dữ liệu theo khóa mã bưu chính ZIP Code.", AMBER),
    ("GIAI ĐOẠN 5", "BIẾN ĐỔI ĐẶC TRƯNG", "Tạo biến đơn giá trên mỗi sqft, tuổi thọ, log giá và mã hóa nhị phân năm quận.", EMERALD)
]

for idx, (gd, name, desc, col) in enumerate(pipe_steps):
    card = create_card(slide5, Inches(6.8), Inches(1.7 + idx * 1.02), Inches(5.7), Inches(0.95))
    tb = slide5.shapes.add_textbox(Inches(6.95), Inches(1.72 + idx * 1.02), Inches(5.4), Inches(0.88))
    tf = tb.text_frame
    tf.word_wrap = True
    p_t = tf.paragraphs[0]
    p_t.text = f"{gd}: {name}"
    p_t.font.size = Pt(10.5)
    p_t.font.bold = True
    p_t.font.color.rgb = col
    p_d = tf.add_paragraph()
    p_d.text = desc
    p_d.font.size = Pt(9.5)
    p_d.font.color.rgb = TEXT_MAIN
    p_d.space_before = Pt(2)

# ==================== SLIDE 6: EP KIEU VA DIEN KHUYET ====================
slide6 = prs.slides.add_slide(blank_layout)
set_slide_background(slide6, BG_LIGHT)
add_header(slide6, "TIỀN XỬ LÝ: ÉP KIỂU VÀ ĐIỀN KHUYẾT DỮ LIỆU", "PHẦN 3", "Chuẩn hóa định dạng số thực và xử lý giá trị khuyết thiếu một cách khách quan")

card_s1 = create_card(slide6, Inches(0.8), Inches(1.7), Inches(5.75), Inches(5.1))
bar1 = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.75), Inches(0.12))
bar1.fill.solid()
bar1.fill.fore_color.rgb = DARK_BLUE
bar1.line.fill.background()

tb_s1 = slide6.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(5.35), Inches(1.4))
tf_s1 = tb_s1.text_frame
tf_s1.word_wrap = True
p_s1_t = tf_s1.paragraphs[0]
p_s1_t.text = "ÉP KIỂU VÀ KHỬ LỖI ĐỊNH DẠNG"
p_s1_t.font.size = Pt(13)
p_s1_t.font.bold = True
p_s1_t.font.color.rgb = DARK_BLUE

p_s1_d = tf_s1.add_paragraph()
p_s1_d.text = "• Vấn đề: Cột giá và diện tích bị lưu dưới dạng chuỗi chứa dấu phân cách.\n• Giải pháp: Ép kiểu số thực bắt buộc qua hàm to_numeric, biến lỗi thành NaN."
p_s1_d.font.size = Pt(11)
p_s1_d.font.color.rgb = TEXT_MAIN
p_s1_d.space_before = Pt(6)

add_code_box(slide6, Inches(1.0), Inches(3.35), Inches(5.35), Inches(1.7),
             "df['SALE PRICE'] = pd.to_numeric(df['SALE PRICE'], errors='coerce')\n"
             "df['GROSS SQUARE FEET'] = pd.to_numeric(df['GROSS SQFT'], errors='coerce')\n"
             "df['SALE DATE'] = pd.to_datetime(df['SALE DATE'])")

tb_s1_res = slide6.shapes.add_textbox(Inches(1.0), Inches(5.2), Inches(5.35), Inches(1.4))
tf_s1_res = tb_s1_res.text_frame
tf_s1_res.word_wrap = True
p_res = tf_s1_res.paragraphs[0]
p_res.text = "Kết quả: Toàn bộ cột định lượng được đưa về dạng số thực chuẩn.\nTrích xuất các trường thời gian năm và tháng phục vụ chuỗi thời gian."
p_res.font.size = Pt(11)
p_res.font.bold = True
p_res.font.color.rgb = EMERALD

card_s2 = create_card(slide6, Inches(6.75), Inches(1.7), Inches(5.75), Inches(5.1))
bar2 = slide6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.75), Inches(1.7), Inches(5.75), Inches(0.12))
bar2.fill.solid()
bar2.fill.fore_color.rgb = ACCENT_BLUE
bar2.line.fill.background()

tb_s2 = slide6.shapes.add_textbox(Inches(6.95), Inches(1.9), Inches(5.35), Inches(1.4))
tf_s2 = tb_s2.text_frame
tf_s2.word_wrap = True
p_s2_t = tf_s2.paragraphs[0]
p_s2_t.text = "XỬ LÝ DỮ LIỆU KHUYẾT THIẾU"
p_s2_t.font.size = Pt(13)
p_s2_t.font.bold = True
p_s2_t.font.color.rgb = ACCENT_BLUE

p_s2_d = tf_s2.add_paragraph()
p_s2_d.text = "• Loại bỏ các bản ghi thiếu biến cốt lõi gồm giá bán, diện tích và quận.\n• Áp dụng phương pháp điền khuyết bằng trung vị theo từng quận hành chính:"
p_s2_d.font.size = Pt(11)
p_s2_d.font.color.rgb = TEXT_MAIN
p_s2_d.space_before = Pt(6)

add_code_box(slide6, Inches(6.95), Inches(3.35), Inches(5.35), Inches(1.7),
             "median_thu_nhap = df.groupby('QUAN')['THU_NHAP'].median()\n"
             "df['THU_NHAP'] = df['THU_NHAP'].fillna(df['QUAN'].map(median_thu_nhap))")

tb_s2_res = slide6.shapes.add_textbox(Inches(6.95), Inches(5.2), Inches(5.35), Inches(1.4))
tf_s2_res = tb_s2_res.text_frame
tf_s2_res.word_wrap = True
p_res2 = tf_s2_res.paragraphs[0]
p_res2.text = "Lý do chọn trung vị: Kháng ngoại lai hiệu quả, không bị méo lệch bởi giá trị cực đoan.\nKết quả: Làm sạch hoàn toàn giá trị khuyết thiếu trên tập dữ liệu."
p_res2.font.size = Pt(11)
p_res2.font.bold = True
p_res2.font.color.rgb = EMERALD

# ==================== SLIDE 7: LOC NGOAI LAI ====================
slide7 = prs.slides.add_slide(blank_layout)
set_slide_background(slide7, BG_LIGHT)
add_header(slide7, "TIỀN XỬ LÝ: CHIẾN LƯỢC LỌC DỮ LIỆU DỊ BIỆT", "PHẦN 3", "Xử lý các giao dịch bất thường nhằm loại bỏ triệt để hiện tượng sai lệch mô hình")

outlier_boxes = [
    ("LOẠI BỎ GIAO DỊCH 0 USD", "CHUYỂN NHƯỢNG NỘI BỘ",
     "29.236 BẢN GHI PHI THƯƠNG MẠI",
     "df = df[df['SALE PRICE'] > 1000]",
     "Bản chất: Giao dịch thừa kế hoặc chuyển nhượng gia đình không theo thị trường.",
     "Kết quả: Loại bỏ mức giá ảo làm sập mức giá trung bình.",
     ROSE),
    ("LỌC DƯỚI 10.000 USD", "MUA BÁN BIỂU TRƯNG",
     "LOẠI BỎ GIAO DỊCH DANH NGHĨA",
     "df = df[df['SALE PRICE'] >= 10000]",
     "Bản chất: Các khoản chuyển giao quyền chọn mua danh nghĩa.",
     "Kết quả: Giữ lại hoàn toàn các giao dịch thương mại thực tế.",
     AMBER),
    ("LỌC PHÂN VỊ THEO QUẬN", "QUANTILE FILTERING",
     "GIÁ DƯỚI 95% VÀ DIỆN TÍCH DƯỚI 99%",
     "g[(g[GIA] <= q0.95) & (g[DT] <= q0.99)]",
     "Bản chất: Khử bỏ các tòa nhà thương mại và biệt thự vài trăm triệu USD.",
     "Kết quả: Bảo toàn phân phối chuẩn cho mô hình hồi quy.",
     EMERALD)
]

for idx, (title, sub, badge_val, code_str, desc, impact, col) in enumerate(outlier_boxes):
    left = Inches(0.8 + idx * 3.95)
    top = Inches(1.7)
    card = create_card(slide7, left, top, Inches(3.75), Inches(5.1))
    
    bar = slide7.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(3.75), Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = col
    bar.line.fill.background()
    
    tb = slide7.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), Inches(3.35), Inches(1.1))
    tf = tb.text_frame
    tf.word_wrap = True
    p_t = tf.paragraphs[0]
    p_t.text = title
    p_t.font.size = Pt(12)
    p_t.font.bold = True
    p_t.font.color.rgb = col
    
    p_s = tf.add_paragraph()
    p_s.text = sub
    p_s.font.size = Pt(9.5)
    p_s.font.bold = True
    p_s.font.color.rgb = TEXT_MUTED
    p_s.space_before = Pt(2)
    
    bg = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.2), top + Inches(1.35), Inches(3.35), Inches(0.42))
    bg.fill.solid()
    bg.fill.fore_color.rgb = LIGHT_BLUE
    bg.line.color.rgb = col
    bg.line.width = Pt(1)
    p_bg = bg.text_frame.paragraphs[0]
    p_bg.text = badge_val
    p_bg.font.size = Pt(10)
    p_bg.font.bold = True
    p_bg.font.color.rgb = col
    p_bg.alignment = PP_ALIGN.CENTER
    bg.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    add_code_box(slide7, left + Inches(0.2), top + Inches(1.9), Inches(3.35), Inches(0.85), code_str)
    
    tb_d = slide7.shapes.add_textbox(left + Inches(0.2), top + Inches(2.85), Inches(3.35), Inches(1.1))
    tf_d = tb_d.text_frame
    tf_d.word_wrap = True
    p_d = tf_d.paragraphs[0]
    p_d.text = desc
    p_d.font.size = Pt(10)
    p_d.font.color.rgb = TEXT_MAIN
    
    box_imp = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.2), top + Inches(4.1), Inches(3.35), Inches(0.75))
    box_imp.fill.solid()
    box_imp.fill.fore_color.rgb = RGBColor(240, 253, 244) if col == EMERALD else (RGBColor(254, 242, 242) if col == ROSE else RGBColor(255, 251, 235))
    box_imp.line.color.rgb = col
    box_imp.line.width = Pt(1)
    p_imp = box_imp.text_frame.paragraphs[0]
    p_imp.text = impact
    p_imp.font.size = Pt(10)
    p_imp.font.bold = True
    p_imp.font.color.rgb = col
    box_imp.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE

# ==================== SLIDE 8: LIEN KET DA NGUON ====================
slide8 = prs.slides.add_slide(blank_layout)
set_slide_background(slide8, BG_LIGHT)
add_header(slide8, "TIỀN XỬ LÝ: LIÊN KẾT ĐA NGUỒN THEO MÔ HÌNH HÌNH SAO", "PHẦN 3", "Hợp nhất ba bảng dữ liệu độc lập thành bảng tổng thể thông qua khóa mã bưu chính ZIP Code")

schemas = [
    ("BẢNG SỐ LIỆU CHÍNH", "NYC PROPERTY SALES", [
        "Khóa liên kết: Mã bưu chính ZIP Code.",
        "Quy mô: 26.862 giao dịch sạch sau chọn lọc.",
        "Thuộc tính: Giá bán, diện tích sàn, năm xây dựng."
    ], DARK_BLUE),
    ("BẢNG TỌA ĐỘ ĐỊA LÝ", "NYC ZIP CODES", [
        "Khóa liên kết: Mã bưu chính ZIP Code.",
        "Thuộc tính: Tọa độ vĩ độ và kinh độ.",
        "Mục đích: Bản đồ nhiệt không gian địa lý."
    ], ACCENT_BLUE),
    ("BẢNG DÂN CƯ KINH TẾ", "US CENSUS DATA", [
        "Khóa liên kết: Mã bưu chính ZIP Code.",
        "Thuộc tính: Thu nhập trung vị hộ gia đình.",
        "Mục đích: Khảo sát tương quan kinh tế khu vực."
    ], EMERALD)
]

for idx, (t_role, t_name, pts, col) in enumerate(schemas):
    left = Inches(0.8 + idx * 3.95)
    top = Inches(1.7)
    card = create_card(slide8, left, top, Inches(3.75), Inches(3.0))
    
    bar = slide8.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(3.75), Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = col
    bar.line.fill.background()
    
    tb = slide8.shapes.add_textbox(left + Inches(0.2), top + Inches(0.25), Inches(3.35), Inches(2.6))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p_r = tf.paragraphs[0]
    p_r.text = t_role
    p_r.font.size = Pt(11)
    p_r.font.bold = True
    p_r.font.color.rgb = col
    
    p_n = tf.add_paragraph()
    p_n.text = t_name
    p_n.font.size = Pt(12)
    p_n.font.bold = True
    p_n.font.color.rgb = NAVY
    p_n.space_before = Pt(2)
    
    for pt in pts:
        p = tf.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(8)

card_bot = create_card(slide8, Inches(0.8), Inches(4.9), Inches(11.7), Inches(1.9), bg_color=LIGHT_BLUE, border_color=ACCENT_BLUE)
tb_bot = slide8.shapes.add_textbox(Inches(1.0), Inches(5.0), Inches(11.3), Inches(0.6))
tf_bot = tb_bot.text_frame
tf_bot.word_wrap = True
p_bt = tf_bot.paragraphs[0]
p_bt.text = "KẾT QUẢ HỢP NHẤT: BẢNG DỮ LIỆU TỔNG THỂ VỚI 35 THUỘC TÍNH PHÂN TÍCH"
p_bt.font.size = Pt(12)
p_bt.font.bold = True
p_bt.font.color.rgb = DARK_BLUE

add_code_box(slide8, Inches(1.0), Inches(5.6), Inches(11.3), Inches(0.95),
             "df_final = df_sales.merge(df_zip[['ZIP CODE', 'lat', 'lon']], on='ZIP CODE', how='left') \\\n"
             "                   .merge(df_demo[['ZIP CODE', 'MEDIAN_INCOME']], on='ZIP CODE', how='left')")

# ==================== SLIDE 9: BIEN DOI DAC TRUNG ====================
slide9 = prs.slides.add_slide(blank_layout)
set_slide_background(slide9, BG_LIGHT)
add_header(slide9, "TIỀN XỬ LÝ: BIẾN ĐỔI ĐẶC TRƯNG VÀ CHUẨN HÓA DỮ LIỆU", "PHẦN 3", "Tạo lập biến số đặc trưng mới và chuẩn hóa phân phối sẵn sàng cho mô hình hồi quy")

fe_cards = [
    ("ĐƠN GIÁ TRÊN SQFT", "CHUẨN HÓA QUY MÔ",
     "GIA_TREN_SQFT = GIA / DIEN_TICH",
     "Loại bỏ khác biệt về diện tích sàn, tạo thước đo công bằng khi so sánh giữa các phân vùng.",
     DARK_BLUE),
    ("TUỔI THỌ CÔNG TRÌNH", "HỆ SỐ KHẤU HAO",
     "TUOI_THO = NAM_BAN - NAM_XAY",
     "Phản ánh mức độ hao mòn công trình theo thời gian, đo lường tác động của tuổi thọ lên giá trị.",
     ACCENT_BLUE),
    ("CHUẨN HÓA LOGARITHM", "KHỬ LỆCH PHẢI",
     "LOG_GIA = np.log1p(GIA_BAN)",
     "Đưa phân phối giá bán bị lệch phải nặng về phân phối chuẩn đối xứng cho mô hình hồi quy tuyến tính.",
     ROSE),
    ("MÃ HÓA NHỊ PHÂN", "ONE-HOT ENCODING",
     "pd.get_dummies(QUAN, drop_first=True)",
     "Mã hóa năm quận hành chính thành các vector nhị phân 0 và 1, tránh giả định thứ tự giả tạo.",
     EMERALD)
]

for idx, (title, sub, formula, desc, col) in enumerate(fe_cards):
    left = Inches(0.8 + idx * 2.95)
    top = Inches(1.7)
    card = create_card(slide9, left, top, Inches(2.8), Inches(5.1))
    
    bar = slide9.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(2.8), Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = col
    bar.line.fill.background()
    
    tb = slide9.shapes.add_textbox(left + Inches(0.15), top + Inches(0.2), Inches(2.5), Inches(1.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p_t = tf.paragraphs[0]
    p_t.text = title
    p_t.font.size = Pt(11)
    p_t.font.bold = True
    p_t.font.color.rgb = col
    p_s = tf.add_paragraph()
    p_s.text = sub
    p_s.font.size = Pt(9)
    p_s.font.bold = True
    p_s.font.color.rgb = TEXT_MUTED
    p_s.space_before = Pt(2)
    
    add_code_box(slide9, left + Inches(0.15), top + Inches(1.3), Inches(2.5), Inches(0.9), formula)
    
    tb_d = slide9.shapes.add_textbox(left + Inches(0.15), top + Inches(2.35), Inches(2.5), Inches(2.5))
    tf_d = tb_d.text_frame
    tf_d.word_wrap = True
    p_d = tf_d.paragraphs[0]
    p_d.text = desc
    p_d.font.size = Pt(10.5)
    p_d.font.color.rgb = TEXT_MAIN
    p_d.space_before = Pt(6)

# ==================== SLIDE 10: KET QUA DU LIEU SACH ====================
slide10 = prs.slides.add_slide(blank_layout)
set_slide_background(slide10, BG_LIGHT)
add_header(slide10, "4. ĐÁNH GIÁ TẬP DỮ LIỆU SAU KHI TIỀN XỬ LÝ", "PHẦN 4", "Bộ dữ liệu hoàn thiện đạt độ tin cậy thống kê cao và sẵn sàng phục vụ trực quan hóa")

metrics4 = [
    ("84.548", "Giao dịch thô ban đầu", DARK_BLUE),
    ("26.862", "Giao dịch sạch hoàn chỉnh", EMERALD),
    ("35 CỘT", "Thuộc tính chuẩn hóa song ngữ", ACCENT_BLUE),
    ("R = 0.61", "Tương quan Diện tích và Giá", ROSE)
]

for idx, (m_v, m_l, m_c) in enumerate(metrics4):
    card = create_card(slide10, Inches(0.8 + idx * 2.95), Inches(1.7), Inches(2.8), Inches(1.3))
    tb = slide10.shapes.add_textbox(Inches(0.9 + idx * 2.95), Inches(1.8), Inches(2.6), Inches(1.1))
    tf = tb.text_frame
    tf.word_wrap = True
    p_v = tf.paragraphs[0]
    p_v.text = m_v
    p_v.font.size = Pt(22)
    p_v.font.bold = True
    p_v.font.color.rgb = m_c
    p_l = tf.add_paragraph()
    p_l.text = m_l
    p_l.font.size = Pt(10)
    p_l.font.color.rgb = TEXT_MUTED
    p_l.space_before = Pt(3)

card_res1 = create_card(slide10, Inches(0.8), Inches(3.2), Inches(5.75), Inches(3.6))
tb_r1 = slide10.shapes.add_textbox(Inches(1.0), Inches(3.35), Inches(5.35), Inches(3.3))
tf_r1 = tb_r1.text_frame
tf_r1.word_wrap = True
p_r1_t = tf_r1.paragraphs[0]
p_r1_t.text = "PHÂN PHỐI DỮ LIỆU MỤC TIÊU"
p_r1_t.font.size = Pt(13)
p_r1_t.font.bold = True
p_r1_t.font.color.rgb = NAVY

r1_pts = [
    "Khử bỏ hoàn toàn 29.236 dòng chuyển nhượng 0 USD.",
    "Trước xử lý: Lệch phải nghiêm trọng với cực đại 2,2 tỷ USD.",
    "Sau biến đổi logarit: Đạt phân phối hình chuông đối xứng chuẩn.",
    "Mô hình hồi quy không còn bị chi phối bởi ngoại lai đột biến."
]
for pt in r1_pts:
    p = tf_r1.add_paragraph()
    p.text = f"• {pt}"
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_MAIN
    p.space_before = Pt(12)

card_res2 = create_card(slide10, Inches(6.75), Inches(3.2), Inches(5.75), Inches(3.6))
tb_r2 = slide10.shapes.add_textbox(Inches(6.95), Inches(3.35), Inches(5.35), Inches(3.3))
tf_r2 = tb_r2.text_frame
tf_r2.word_wrap = True
p_r2_t = tf_r2.paragraphs[0]
p_r2_t.text = "TƯƠNG QUAN VÀ PHÂN HÓA ĐỊA LÝ"
p_r2_t.font.size = Pt(13)
p_r2_t.font.bold = True
p_r2_t.font.color.rgb = NAVY

r2_pts = [
    "Diện tích sàn giải thích mạnh nhất mức biến động giá bán.",
    "Đơn giá trung vị phân hóa sâu sắc giữa năm quận:",
    "   Manhattan: khoảng 1.200 đến 1.500 USD trên mỗi sqft.",
    "   Brooklyn: khoảng 650 USD | Queens: khoảng 500 USD.",
    "   Staten Island: khoảng 350 USD | Bronx: khoảng 280 USD."
]
for pt in r2_pts:
    p = tf_r2.add_paragraph()
    p.text = f"• {pt}"
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_MAIN
    p.space_before = Pt(10)

# ==================== SLIDE 11: KHAM PHA DU LIEU TINH EDA ====================
slide11 = prs.slides.add_slide(blank_layout)
set_slide_background(slide11, BG_LIGHT)
add_header(slide11, "KHÁM PHÁ DỮ LIỆU TĨNH: BỐN GÓC NHÌN THỐNG KÊ", "BƯỚC ĐỆM PHÂN TÍCH", "Khảo sát phân bố dữ liệu bằng Matplotlib và Seaborn trước khi xây dựng Dashboard")

eda_img_path = r"images\00_eda_4_charts.png"
if os.path.exists(eda_img_path):
    slide11.shapes.add_picture(eda_img_path, Inches(0.8), Inches(1.7), Inches(6.8), Inches(5.1))
else:
    create_card(slide11, Inches(0.8), Inches(1.7), Inches(6.8), Inches(5.1))

card_eda = create_card(slide11, Inches(7.8), Inches(1.7), Inches(4.7), Inches(5.1))
tb_eda = slide11.shapes.add_textbox(Inches(8.0), Inches(1.85), Inches(4.3), Inches(4.8))
tf_eda = tb_eda.text_frame
tf_eda.word_wrap = True

p_et = tf_eda.paragraphs[0]
p_et.text = "BỐN PHÁT HIỆN TỪ EDA"
p_et.font.size = Pt(13)
p_et.font.bold = True
p_et.font.color.rgb = NAVY

eda_short = [
    ("Phân phối giá bán:", "Lệch phải nặng, chuẩn hóa hiệu quả sau khi logarit."),
    ("Tương quan diện tích:", "Mối quan hệ đồng biến thực chất giữa quy mô và giá."),
    ("Biến động chu kỳ:", "Số lượng giao dịch sôi động nhất vào mùa hè hàng năm."),
    ("Độ phân tán năm quận:", "Manhattan có phương sai đơn giá lớn nhất thành phố.")
]
for t, d in eda_short:
    p = tf_eda.add_paragraph()
    p.text = f"• {t} {d}"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MAIN
    p.space_before = Pt(14)

# ==================== SLIDE 12: KIEN TRUC DASHBOARD ====================
slide12 = prs.slides.add_slide(blank_layout)
set_slide_background(slide12, BG_LIGHT)
add_header(slide12, "5. THIẾT KẾ VÀ KIẾN TRÚC DASHBOARD TRỰC QUAN HÓA", "PHẦN 5", "Hệ thống tương tác đa chiều xây dựng trên nền tảng Streamlit và thư viện Plotly")

viz_cards = [
    ("KIẾN TRÚC STREAMLIT", [
        "Nền tảng ứng dụng Python phản hồi nhanh.",
        "Cơ chế bộ nhớ đệm tải hơn 26.000 dòng dưới 1.5 giây.",
        "Giao diện chuẩn Wide Layout với năm chỉ số KPI tổng quan."
    ], "TỐC ĐỘ PHẢN HỒI CAO", DARK_BLUE),
    ("TƯƠNG TÁC ĐA CHIỀU", [
        "Bộ lọc Sidebar đa tầng theo quận, giá, diện tích, tuổi thọ.",
        "Khả năng phân cấp từ toàn thành phố xuống từng khu phố.",
        "Tooltip hiển thị tức thì giá bán, diện tích và đơn giá."
    ], "TRẢI NGHIỆM ĐA TẦNG DỮ LIỆU", ACCENT_BLUE),
    ("CẤU TRÚC SÁU PHÂN HỆ", [
        "Phân hệ 1: Xu hướng thị trường và thị phần.",
        "Phân hệ 2: Phân bố không gian và địa lý.",
        "Phân hệ 3: Cấu trúc đô thị và phân cấp khu vực.",
        "Phân hệ 4: Đặc tính công trình và quy mô diện tích.",
        "Phân hệ 5: Mô hình hồi quy định giá bất động sản.",
        "Phân hệ 6: Dự báo xu hướng chuỗi thời gian."
    ], "HỆ THỐNG 13 BIỂU ĐỒ TƯƠNG TÁC", EMERALD)
]

for idx, (title, pts, pill, col) in enumerate(viz_cards):
    left = Inches(0.8 + idx * 3.95)
    top = Inches(1.7)
    card = create_card(slide12, left, top, Inches(3.75), Inches(5.1))
    
    bar = slide12.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(3.75), Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = col
    bar.line.fill.background()
    
    tb = slide12.shapes.add_textbox(left + Inches(0.25), top + Inches(0.25), Inches(3.25), Inches(3.6))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p_t = tf.paragraphs[0]
    p_t.text = title
    p_t.font.size = Pt(13)
    p_t.font.bold = True
    p_t.font.color.rgb = col
    
    for pt in pts:
        p = tf.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(10)
        
    pill_box = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.25), top + Inches(4.3), Inches(3.25), Inches(0.48))
    pill_box.fill.solid()
    pill_box.fill.fore_color.rgb = LIGHT_BLUE
    pill_box.line.color.rgb = col
    pill_box.line.width = Pt(1)
    p_pl = pill_box.text_frame.paragraphs[0]
    p_pl.text = pill
    p_pl.font.size = Pt(9.5)
    p_pl.font.bold = True
    p_pl.font.color.rgb = col
    p_pl.alignment = PP_ALIGN.CENTER
    pill_box.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE

# ==================== SLIDE 13: BIEU DO - PHAN HE 1 & 2 ====================
slide13 = prs.slides.add_slide(blank_layout)
set_slide_background(slide13, BG_LIGHT)
add_header(slide13, "6. HỆ THỐNG BIỂU ĐỒ: PHÂN HỆ 1 VÀ 2 - ĐỊA LÝ VÀ XU HƯỚNG", "PHẦN 6", "Trực quan hóa không gian địa lý và phân tích chuỗi thời gian 12 tháng")

img_map = r"images\01_bando_dialy.png"
img_line = r"images\04_bieudo_duong_dongia.png"

if os.path.exists(img_map):
    slide13.shapes.add_picture(img_map, Inches(0.8), Inches(1.7), Inches(5.8), Inches(3.5))
if os.path.exists(img_line):
    slide13.shapes.add_picture(img_line, Inches(6.8), Inches(1.7), Inches(5.7), Inches(3.5))

card_c1 = create_card(slide13, Inches(0.8), Inches(5.35), Inches(5.8), Inches(1.5))
tb_c1 = slide13.shapes.add_textbox(Inches(0.95), Inches(5.4), Inches(5.5), Inches(1.3))
tf_c1 = tb_c1.text_frame
tf_c1.word_wrap = True
p1_t = tf_c1.paragraphs[0]
p1_t.text = "BIỂU ĐỒ 4: BẢN ĐỒ ĐỊA LÝ KHÔNG GIAN TƯƠNG TÁC"
p1_t.font.size = Pt(11.5)
p1_t.font.bold = True
p1_t.font.color.rgb = DARK_BLUE
p1_d = tf_c1.add_paragraph()
p1_d.text = "• Định vị tọa độ từng điểm giao dịch • Màu sắc biểu thị quận • Kích thước hạt tròn theo giá bán."
p1_d.font.size = Pt(10)
p1_d.font.color.rgb = TEXT_MAIN
p1_d.space_before = Pt(4)

card_c2 = create_card(slide13, Inches(6.8), Inches(5.35), Inches(5.7), Inches(1.5))
tb_c2 = slide13.shapes.add_textbox(Inches(6.95), Inches(5.4), Inches(5.4), Inches(1.3))
tf_c2 = tb_c2.text_frame
tf_c2.word_wrap = True
p2_t = tf_c2.paragraphs[0]
p2_t.text = "BIỂU ĐỒ 1, 2 VÀ 3: XU HƯỚNG THỜI GIAN VÀ THỊ PHẦN QUẬN"
p2_t.font.size = Pt(11.5)
p2_t.font.bold = True
p2_t.font.color.rgb = ACCENT_BLUE
p2_d = tf_c2.add_paragraph()
p2_d.text = "• Biểu đồ Đường: Đơn giá theo tháng • Biểu đồ Vành khuyên: Thị phần quận • Biểu đồ Miền: Quy mô dòng tiền."
p2_d.font.size = Pt(10)
p2_d.font.color.rgb = TEXT_MAIN
p2_d.space_before = Pt(4)

# ==================== SLIDE 14: BIEU DO - PHAN HE 3 & 4 ====================
slide14 = prs.slides.add_slide(blank_layout)
set_slide_background(slide14, BG_LIGHT)
add_header(slide14, "HỆ THỐNG BIỂU ĐỒ: PHÂN HỆ 3 VÀ 4 - CƠ CẤU VÀ PHÂN BỐ", "PHẦN 6", "Phân tích phân cấp đô thị, bảng xếp hạng khu phố và phân phối xác suất")

img_tree = r"images\05_treemap_phancap.png"
img_box = r"images\08_boxplot_quan.png"

if os.path.exists(img_tree):
    slide14.shapes.add_picture(img_tree, Inches(0.8), Inches(1.7), Inches(5.8), Inches(3.5))
if os.path.exists(img_box):
    slide14.shapes.add_picture(img_box, Inches(6.8), Inches(1.7), Inches(5.7), Inches(3.5))

card_c3 = create_card(slide14, Inches(0.8), Inches(5.35), Inches(5.8), Inches(1.5))
tb_c3 = slide14.shapes.add_textbox(Inches(0.95), Inches(5.4), Inches(5.5), Inches(1.3))
tf_c3 = tb_c3.text_frame
tf_c3.word_wrap = True
p3_t = tf_c3.paragraphs[0]
p3_t.text = "BIỂU ĐỒ 6 VÀ 7: PHÂN CẤP TREEMAP VÀ TOP KHU PHỐ"
p3_t.font.size = Pt(11.5)
p3_t.font.bold = True
p3_t.font.color.rgb = DARK_BLUE
p3_d = tf_c3.add_paragraph()
p3_d.text = "• Treemap: Phân cấp từ toàn thành phố xuống quận và khu phố • Biểu đồ Cột ngang: Top 10 khu phố đắt nhất."
p3_d.font.size = Pt(10)
p3_d.font.color.rgb = TEXT_MAIN
p3_d.space_before = Pt(4)

card_c4 = create_card(slide14, Inches(6.8), Inches(5.35), Inches(5.7), Inches(1.5))
tb_c4 = slide14.shapes.add_textbox(Inches(6.95), Inches(5.4), Inches(5.4), Inches(1.3))
tf_c4 = tb_c4.text_frame
tf_c4.word_wrap = True
p4_t = tf_c4.paragraphs[0]
p4_t.text = "BIỂU ĐỒ 8, 9 VÀ 10: QUY MÔ, PHÂN BỐ VÀ MẬT ĐỘ"
p4_t.font.size = Pt(11.5)
p4_t.font.bold = True
p4_t.font.color.rgb = ROSE
p4_d = tf_c4.add_paragraph()
p4_d.text = "• Biểu đồ Hộp: Tứ phân vị năm quận • Biểu đồ Tần suất: Đơn giá sàn • Biểu đồ Cột đứng: Mức giá theo diện tích."
p4_d.font.size = Pt(10)
p4_d.font.color.rgb = TEXT_MAIN
p4_d.space_before = Pt(4)

# ==================== SLIDE 15: BIEU DO - PHAN HE 5 & 6 ====================
slide15 = prs.slides.add_slide(blank_layout)
set_slide_background(slide15, BG_LIGHT)
add_header(slide15, "HỆ THỐNG BIỂU ĐỒ: PHÂN HỆ 5 VÀ 6 - HỒI QUY VÀ DỰ BÁO", "PHẦN 6", "Mô hình hồi quy tuyến tính OLS, kiểm chứng thực nghiệm và dự báo xu hướng chuỗi thời gian")

img_trend = r"images\11_scatter_ols_trendline.png"
img_fc = r"images\13_timeseries_forecast.png"

if os.path.exists(img_trend):
    slide15.shapes.add_picture(img_trend, Inches(0.8), Inches(1.7), Inches(5.8), Inches(3.5))
if os.path.exists(img_fc):
    slide15.shapes.add_picture(img_fc, Inches(6.8), Inches(1.7), Inches(5.7), Inches(3.5))

card_c5 = create_card(slide15, Inches(0.8), Inches(5.35), Inches(5.8), Inches(1.5))
tb_c5 = slide15.shapes.add_textbox(Inches(0.95), Inches(5.4), Inches(5.5), Inches(1.3))
tf_c5 = tb_c5.text_frame
tf_c5.word_wrap = True
p5_t = tf_c5.paragraphs[0]
p5_t.text = "BIỂU ĐỒ 11 VÀ 12: ĐƯỜNG HỒI QUY OLS VÀ ĐỐI CHIẾU THỰC TẾ"
p5_t.font.size = Pt(11.5)
p5_t.font.bold = True
p5_t.font.color.rgb = AMBER
p5_d = tf_c5.add_paragraph()
p5_d.text = "• Hồi quy OLS: Tương quan diện tích và giá • Đối chiếu thực tế và dự báo: Đánh giá độ bám đường chuẩn y = x."
p5_d.font.size = Pt(10)
p5_d.font.color.rgb = TEXT_MAIN
p5_d.space_before = Pt(4)

card_c6 = create_card(slide15, Inches(6.8), Inches(5.35), Inches(5.7), Inches(1.5))
tb_c6 = slide15.shapes.add_textbox(Inches(6.95), Inches(5.4), Inches(5.4), Inches(1.3))
tf_c6 = tb_c6.text_frame
tf_c6.word_wrap = True
p6_t = tf_c6.paragraphs[0]
p6_t.text = "BIỂU ĐỒ 13: DỰ BÁO XU HƯỚNG KÈM KHOẢNG TIN CẬY 95%"
p6_t.font.size = Pt(11.5)
p6_t.font.bold = True
p6_t.font.color.rgb = CYAN
p6_d = tf_c6.add_paragraph()
p6_d.text = "• Hồi quy chuỗi thời gian: Mở rộng dự phóng từ 1 đến 12 tháng • Dải biên độ dao động khoảng tin cậy 95%."
p6_d.font.size = Pt(10)
p6_d.font.color.rgb = TEXT_MAIN
p6_d.space_before = Pt(4)

# ==================== SLIDE 16: MO HINH HOI QUY TUYEN TINH ====================
slide16 = prs.slides.add_slide(blank_layout)
set_slide_background(slide16, BG_LIGHT)
add_header(slide16, "MÔ HÌNH HỒI QUY TUYẾN TÍNH ĐỊNH GIÁ BẤT ĐỘNG SẢN", "MACHINE LEARNING", "Multiple Linear Regression ước lượng giá trị tài sản và lượng hóa hệ số tác động")

# Equation and Metric Banner
eq_card = create_card(slide16, Inches(0.8), Inches(1.6), Inches(11.7), Inches(1.0), bg_color=CODE_BG, border_color=RGBColor(203, 213, 225))
tb_eq = slide16.shapes.add_textbox(Inches(1.0), Inches(1.68), Inches(6.5), Inches(0.85))
tf_eq = tb_eq.text_frame
tf_eq.word_wrap = True
p_eq_lbl = tf_eq.paragraphs[0]
p_eq_lbl.text = "PHƯƠNG TRÌNH HỒI QUY TUYẾN TÍNH ĐA BIẾN"
p_eq_lbl.font.size = Pt(9.5)
p_eq_lbl.font.bold = True
p_eq_lbl.font.color.rgb = DARK_BLUE

p_eq_val = tf_eq.add_paragraph()
p_eq_val.text = "ln(Giá) = 13.43 + 0.000109 × Diện tích - 0.0022 × Tuổi thọ + 0.000004 × Thu nhập + β_Quận"
p_eq_val.font.size = Pt(10.5)
p_eq_val.font.bold = True
p_eq_val.font.color.rgb = ACCENT_BLUE
p_eq_val.space_before = Pt(3)

# 4 Metric badges on the right side of the banner
metrics_ml = [
    ("R² = 0.243", "Độ phù hợp", EMERALD),
    ("MAE = $456K", "Sai số trung bình", DARK_BLUE),
    ("MedAPE = 33%", "Sai số trung vị", AMBER),
    ("Test = 20%", "5.373 quan sát", ROSE)
]
for m_i, (m_val, m_lbl, m_c) in enumerate(metrics_ml):
    m_box = slide16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.7 + m_i * 1.18), Inches(1.72), Inches(1.1), Inches(0.75))
    m_box.fill.solid()
    m_box.fill.fore_color.rgb = WHITE
    m_box.line.color.rgb = m_c
    m_box.line.width = Pt(1)
    tf_mb = m_box.text_frame
    tf_mb.word_wrap = True
    p_mv = tf_mb.paragraphs[0]
    p_mv.text = m_val
    p_mv.font.size = Pt(10.5)
    p_mv.font.bold = True
    p_mv.font.color.rgb = m_c
    p_mv.alignment = PP_ALIGN.CENTER
    p_ml = tf_mb.add_paragraph()
    p_ml.text = m_lbl
    p_ml.font.size = Pt(8)
    p_ml.font.color.rgb = TEXT_MUTED
    p_ml.alignment = PP_ALIGN.CENTER

ml_cards = [
    ("PHƯƠNG PHÁP XÂY DỰNG", [
        "Mô hình: Multiple Linear Regression chuẩn.",
        "Biến mục tiêu: Logarit tự nhiên của giá bán.",
        "Biến giải thích: Diện tích, tuổi thọ, thu nhập và quận.",
        "Phân chia tập mẫu: 80% Train và 20% Test độc lập."
    ], DARK_BLUE),
    ("Ý NGHĨA HỆ SỐ BETA", [
        "Hệ số chặn: 13.4263 giá trị cơ sở toàn thành phố.",
        "Manhattan: +1.7057 có mức giá vượt trội nhất.",
        "Tuổi thọ: -0.0022 hao mòn vật lý giảm giá nhẹ.",
        "Thu nhập: Hệ số dương củng cố giá trị bất động sản."
    ], EMERALD),
    ("ỨNG DỤNG THỰC NGHIỆM", [
        "Công cụ định giá tức thì trên Dashboard tương tác.",
        "Nhập diện tích, quận, năm xây để nhận mức giá USD.",
        "Tự động hoàn nguyên hàm mũ e lũy thừa chính xác.",
        "Tích hợp dự báo tăng trưởng giá trị tài sản theo kỳ vọng."
    ], ROSE)
]

for idx, (title, pts, col) in enumerate(ml_cards):
    left = Inches(0.8 + idx * 3.95)
    top = Inches(2.75)
    card = create_card(slide16, left, top, Inches(3.75), Inches(4.05))
    
    bar = slide16.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(3.75), Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = col
    bar.line.fill.background()
    
    tb = slide16.shapes.add_textbox(left + Inches(0.2), top + Inches(0.25), Inches(3.35), Inches(3.6))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p_t = tf.paragraphs[0]
    p_t.text = title
    p_t.font.size = Pt(12)
    p_t.font.bold = True
    p_t.font.color.rgb = col
    
    for pt in pts:
        p = tf.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_MAIN
        p.space_before = Pt(12)

# ==================== SLIDE 17: KET LUAN VA Q&A ====================
slide17 = prs.slides.add_slide(blank_layout)
set_slide_background(slide17, NAVY)

tb17 = slide17.shapes.add_textbox(Inches(1.5), Inches(2.2), Inches(10.3), Inches(3.2))
tf17 = tb17.text_frame
tf17.word_wrap = True

p_c1 = tf17.paragraphs[0]
p_c1.text = "CẢM ƠN THẦY CÔ VÀ CÁC BẠN ĐÃ LẮNG NGHE!"
p_c1.font.size = Pt(28)
p_c1.font.bold = True
p_c1.font.color.rgb = WHITE
p_c1.alignment = PP_ALIGN.CENTER

p_c2 = tf17.add_paragraph()
p_c2.text = "HỆ THỐNG TRỰC QUAN HÓA BẤT ĐỘNG SẢN NEW YORK • NYC PROPVISION"
p_c2.font.size = Pt(14)
p_c2.font.bold = True
p_c2.font.color.rgb = CYAN
p_c2.alignment = PP_ALIGN.CENTER
p_c2.space_before = Pt(14)

p_c3 = tf17.add_paragraph()
p_c3.text = "PHIÊN VẤN ĐÁP: NHÓM SẴN SÀNG GIẢI ĐÁP MỌI CÂU HỎI TỪ HỘI ĐỒNG"
p_c3.font.size = Pt(13)
p_c3.font.color.rgb = RGBColor(203, 213, 225)
p_c3.alignment = PP_ALIGN.CENTER
p_c3.space_before = Pt(16)

out_path = r"c:\Users\One-Tura\Downloads\TUONGTACDULIEUCUOIKY\SLIDE_THUYET_TRINH_NYC_PROPVISION.pptx"
prs.save(out_path)
print(f"Presentation saved successfully to: {out_path}")

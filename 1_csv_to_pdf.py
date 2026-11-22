import os
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

os.makedirs("output", exist_ok=True)

# 1. Đọc dữ liệu CSV
df = pd.read_csv("data/heart.csv")

# 2. Vẽ biểu đồ minh họa
fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))
counts = df["HeartDisease"].value_counts().sort_index()
axes[0].bar(["Bình thường (0)", "Bệnh tim (1)"], counts.values, color=["#2E86AB", "#D9534F"])
axes[0].set_title("Phân bố nhóm chẩn đoán bệnh tim", fontweight="bold")
axes[0].set_ylabel("Số lượng bệnh nhân")

for label, name, color in [(0, "Bình thường", "#2E86AB"), (1, "Bệnh tim", "#D9534F")]:
    sub = df[df["HeartDisease"] == label]
    axes[1].scatter(sub["Age"], sub["MaxHR"], alpha=0.55, label=name, color=color)
axes[1].set_title("Tương quan Tuổi và Nhịp tim tối đa (MaxHR)", fontweight="bold")
axes[1].set_xlabel("Tuổi (Age)")
axes[1].set_ylabel("Nhịp tim tối đa (MaxHR)")
axes[1].legend()

plt.tight_layout()
chart_path = "output/chart_heart_ca_nhan.png"
plt.savefig(chart_path, dpi=200)
plt.close()

# 3. Xuất báo cáo PDF (Tiêu đề, mô tả, bảng dữ liệu, biểu đồ, kết luận)
pdf = FPDF()
pdf.add_page()
pdf.add_font("ArialVN", "", "C:/Windows/Fonts/arial.ttf")
pdf.add_font("ArialVN", "B", "C:/Windows/Fonts/arialbd.ttf")

pdf.set_font("ArialVN", "B", 15)
pdf.set_text_color(7, 59, 102)
pdf.cell(0, 10, "BÁO CÁO PHÂN TÍCH DỮ LIỆU DỰ ĐOÁN BỆNH TIM MẠCH", ln=True, align="C")

pdf.set_font("ArialVN", "", 11)
pdf.set_text_color(40, 40, 40)
pdf.multi_cell(
    0, 6,
    f"Mô tả dữ liệu: Tập dữ liệu Heart Failure Prediction (Kaggle / UCI) gồm {len(df)} hồ sơ bệnh nhân "
    f"và {df.shape[1]} thuộc tính lâm sàng. Nhóm mắc bệnh tim (HeartDisease = 1) chiếm "
    f"{df['HeartDisease'].mean()*100:.1f}% ({counts[1]}/{len(df)} trường hợp)."
)
pdf.ln(3)

pdf.set_font("ArialVN", "B", 12)
pdf.cell(0, 8, "1. Bảng thống kê mô tả các chỉ số lâm sàng chính", ln=True)
cols = ["Age", "RestingBP", "Cholesterol", "MaxHR", "Oldpeak"]
summary = df[cols].describe().round(2)

headers = ["Chỉ số", "Số mẫu", "Trung bình", "Độ lệch chuẩn", "Thấp nhất", "Cao nhất"]
col_widths = [38, 25, 32, 35, 30, 30]

pdf.set_font("ArialVN", "B", 10)
pdf.set_fill_color(230, 240, 250)
for h, w in zip(headers, col_widths):
    pdf.cell(w, 8, h, border=1, align="C", fill=True)
pdf.ln()

pdf.set_font("ArialVN", "", 10)
for col in cols:
    row_vals = [
        col,
        str(int(summary.loc["count", col])),
        str(summary.loc["mean", col]),
        str(summary.loc["std", col]),
        str(summary.loc["min", col]),
        str(summary.loc["max", col]),
    ]
    for val, w in zip(row_vals, col_widths):
        pdf.cell(w, 7, val, border=1, align="C")
    pdf.ln()
pdf.ln(4)

pdf.set_font("ArialVN", "B", 12)
pdf.cell(0, 8, "2. Biểu đồ minh họa phân bố dữ liệu", ln=True)
pdf.image(chart_path, x=12, w=185)
pdf.ln(3)

pdf.set_font("ArialVN", "B", 12)
pdf.cell(0, 8, "3. Kết luận ngắn", ln=True)
pdf.set_font("ArialVN", "", 11)
pdf.multi_cell(
    0, 6,
    "Bệnh nhân mắc bệnh tim tập trung chủ yếu ở nhóm trên 50 tuổi và có nhịp tim tối đa (MaxHR) thấp hơn rõ rệt "
    "so với nhóm bình thường. Cột Cholesterol và RestingBP có giá trị 0 bất hợp lý, cần làm sạch trước khi huấn luyện AI."
)

pdf.output("output/bao_cao_ca_nhan_csv.pdf")
print("Hoàn tất Bài cá nhân 1 -> output/bao_cao_ca_nhan_csv.pdf")
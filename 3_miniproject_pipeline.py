import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from fpdf import FPDF

def run_pipeline(df_input=None):
    os.makedirs("output", exist_ok=True)
    df = pd.read_csv("data/heart.csv") if df_input is None else df_input.copy()

    # Làm sạch dữ liệu
    df = df.drop_duplicates()
    zero_cols = ["Cholesterol", "RestingBP"]
    zero_counts = (df[zero_cols] == 0).sum().to_dict()
    df[zero_cols] = df[zero_cols].replace(0, np.nan)
    for col in zero_cols:
        df[col] = df[col].fillna(df[col].median())
    df.to_csv("data/heart_cleaned.csv", index=False)

    # Huấn luyện AI (Random Forest)
    X_raw = df.drop(columns=["HeartDisease"])
    y = df["HeartDisease"]
    X = pd.get_dummies(X_raw, drop_first=True)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    clf = RandomForestClassifier(n_estimators=150, max_depth=7, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)[:, 1]

    metrics = {
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred),
        "F1-Score": f1_score(y_test, y_pred),
        "ROC-AUC": roc_auc_score(y_test, y_prob),
    }
    importances = pd.Series(clf.feature_importances_, index=X.columns).sort_values(ascending=True).tail(8)

    # Trực quan hóa
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    num_cols = ["Age", "RestingBP", "Cholesterol", "FastingBS", "MaxHR", "Oldpeak", "HeartDisease"]
    sns.heatmap(df[num_cols].corr(), annot=True, fmt=".2f", cmap="Blues", cbar=False, ax=axes[0], annot_kws={"size": 7.5})
    axes[0].set_title("Ma trận tương quan các biến định lượng", fontweight="bold")

    importances.plot(kind="barh", color="#168C82", ax=axes[1])
    axes[1].set_title("Top 8 đặc trưng quan trọng nhất (Random Forest)", fontweight="bold")
    axes[1].set_xlabel("Trọng số đóng góp")
    plt.tight_layout()
    chart_file = "output/chart_heart_miniproject.png"
    plt.savefig(chart_file, dpi=200)
    plt.close()

    # Xuất báo cáo PDF khoa học 5 phần
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("ArialVN", "", "C:/Windows/Fonts/arial.ttf")
    pdf.add_font("ArialVN", "B", "C:/Windows/Fonts/arialbd.ttf")

    pdf.set_font("ArialVN", "B", 15)
    pdf.set_text_color(7, 59, 102)
    pdf.cell(0, 10, "BÁO CÁO KHOA HỌC: DỰ ĐOÁN NGUY CƠ BỆNH TIM MẠCH BẰNG AI", ln=True, align="C")
    pdf.ln(2)

    sections = [
        ("1. Giới thiệu đề tài",
         "Đề tài xây dựng quy trình tự động hóa phân tích dữ liệu lâm sàng và huấn luyện mô hình học máy Random Forest nhằm hỗ trợ sàng lọc sớm nguy cơ bệnh tim mạch."),
        ("2. Mô tả và Tiền xử lý dữ liệu",
         f"Bộ dữ liệu gồm {len(df)} bệnh nhân với 11 biến đặc trưng. Các giá trị bằng 0 bất hợp lý tại Cholesterol "
         f"({zero_counts['Cholesterol']} ca) và RestingBP ({zero_counts['RestingBP']} ca) đã được chuẩn hóa bằng trung vị; các biến phân loại được mã hóa One-Hot."),
        ("3. Kết quả phân tích và Đánh giá mô hình AI",
         f"Trên tập kiểm thử (20%), mô hình Random Forest đạt: Accuracy = {metrics['Accuracy']*100:.2f}%, "
         f"Precision = {metrics['Precision']*100:.2f}%, Recall = {metrics['Recall']*100:.2f}%, "
         f"F1-Score = {metrics['F1-Score']*100:.2f}% và ROC-AUC = {metrics['ROC-AUC']:.3f}."),
    ]

    for title, body in sections:
        pdf.set_font("ArialVN", "B", 12)
        pdf.set_text_color(11, 111, 164)
        pdf.cell(0, 8, title, ln=True)
        pdf.set_font("ArialVN", "", 10.5)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(0, 6, body)
        pdf.ln(2)

    pdf.set_font("ArialVN", "B", 12)
    pdf.set_text_color(11, 111, 164)
    pdf.cell(0, 8, "4. Biểu đồ minh họa kết quả", ln=True)
    pdf.image(chart_file, x=12, w=185)
    pdf.ln(3)

    pdf.set_font("ArialVN", "B", 12)
    pdf.cell(0, 8, "5. Kết luận và Đề xuất", ln=True)
    pdf.set_font("ArialVN", "", 10.5)
    pdf.set_text_color(30, 30, 30)
    pdf.multi_cell(
        0, 6,
        f"Đặc trưng {importances.index[-1]} và {importances.index[-2]} có ảnh hưởng lớn nhất đến khả năng phân loại bệnh tim. "
        "Đề xuất triển khai dashboard tương tác tại tuyến y tế cơ sở để hỗ trợ sàng lọc nhanh bệnh nhân có nguy cơ cao."
    )

    report_path = "output/bao_cao_khoa_hoc_heart.pdf"
    pdf.output(report_path)
    return report_path, metrics, clf, X.columns.tolist()

if __name__ == "__main__":
    path, m, _, _ = run_pipeline()
    print("Hoàn tất Báo cáo khoa học Mini-project ->", path)
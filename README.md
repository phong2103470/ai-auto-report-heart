# Hệ thống Tự động hóa Phân tích Dữ liệu & Sinh Báo cáo Khoa học (`ai-auto-report-heart`)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-green.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B.svg)](https://streamlit.io/)

## 1. Giới thiệu dự án
Dự án thực hành nội dung **Tự động hóa sáng tạo và quản lý nội dung số** (Trường Đại học Cần Thơ), ứng dụng Python và Học máy (Machine Learning) trên dữ liệu y tế thực tế để tự động hóa toàn bộ quy trình từ tiền xử lý dữ liệu, huấn luyện mô hình dự đoán đến xuất bản báo cáo khoa học PDF, bài thuyết trình PowerPoint (PPTX) và giao diện dashboard tương tác.

* **Tác giả thực hiện:** Đào Trần Quốc Phong
* **Nguồn dữ liệu:** [Heart Failure Prediction Dataset (Kaggle / UCI ML Repository)](https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction) — gồm **918 hồ sơ bệnh nhân** với **12 thuộc tính lâm sàng** (`Age`, `Sex`, `ChestPainType`, `RestingBP`, `Cholesterol`, `FastingBS`, `RestingECG`, `MaxHR`, `ExerciseAngina`, `Oldpeak`, `ST_Slope` và nhãn chẩn đoán `HeartDisease`).

---

## 2. Cấu trúc thư mục dự án

```text
ai-auto-report-heart/
├── data/
│   ├── heart.csv                       # Bộ dữ liệu gốc từ Kaggle / UCI
│   ├── heart_cleaned.csv               # Dữ liệu sau khi làm sạch và chuẩn hóa
│   └── noidung_thuyettrinh.md          # Kịch bản văn bản đầu vào để tạo slide tự động
├── output/
│   ├── bao_cao_ca_nhan_csv.pdf         # Báo cáo PDF xuất từ dữ liệu CSV (Bài cá nhân 1)
│   ├── bai_thuyet_trinh_tu_dong.pptx   # Slide thuyết trình xuất từ Markdown (Bài cá nhân 2)
│   ├── bao_cao_khoa_hoc_heart.pdf      # Báo cáo khoa học tích hợp mô hình AI (Mini-project)
│   ├── chart_heart_ca_nhan.png         # Biểu đồ phân bố và tương quan chỉ số lâm sàng
│   └── chart_heart_miniproject.png     # Biểu đồ ma trận tương quan và mức độ quan trọng đặc trưng
├── 1_csv_to_pdf.py                     # Mô-đun đọc CSV và xuất báo cáo PDF
├── 2_md_to_pptx.py                     # Mô-đun chuyển đổi file Markdown sang slide PPTX
├── 3_miniproject_pipeline.py           # Mô-đun làm sạch dữ liệu, huấn luyện Random Forest và xuất PDF
├── app_streamlit.py                    # Ứng dụng Web Dashboard tương tác bằng Streamlit
├── requirements.txt                    # Danh sách thư viện Python phụ thuộc
├── README.md                           # Tài liệu hướng dẫn sử dụng dự án
└── LICENSE                             # Giấy phép mã nguồn mở MIT
```

---

## 3. Hướng dẫn cài đặt môi trường

1. **Sao chép mã nguồn về máy:**
   ```bash
   git clone [https://github.com/phong2103470/ai-auto-report-heart.git](https://github.com/phong2103470/ai-auto-report-heart.git)
   cd ai-auto-report-heart
   ```

2. **Cài đặt các thư viện cần thiết:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 4. Hướng dẫn chạy chi tiết từng chức năng

### Bước 1: Tạo báo cáo PDF từ dữ liệu CSV (Bài cá nhân 1)
Đọc tệp `data/heart.csv`, tính bảng thống kê mô tả, vẽ biểu đồ phân bố/tương quan và tự động xuất báo cáo PDF tiếng Việt:
```bash
python 1_csv_to_pdf.py
```
* **Kết quả đầu ra:** `output/bao_cao_ca_nhan_csv.pdf` và `output/chart_heart_ca_nhan.png`.

### Bước 2: Tạo slide thuyết trình PowerPoint từ file Markdown (Bài cá nhân 2)
Đọc nội dung từ `data/noidung_thuyettrinh.md`, tự động tách slide tiêu đề, slide nội dung theo từng mục và chèn hình ảnh biểu đồ:
```bash
python 2_md_to_pptx.py
```
* **Kết quả đầu ra:** `output/bai_thuyet_trinh_tu_dong.pptx`.

### Bước 3: Chạy quy trình AI phân tích & xuất báo cáo khoa học (Mini-project)
Thực hiện làm sạch dữ liệu (loại bỏ bản ghi trùng, chuẩn hóa giá trị `0` bất hợp lý tại `Cholesterol` và `RestingBP` bằng trung vị), huấn luyện mô hình phân loại **Random Forest**, đánh giá các chỉ số (`Accuracy`, `Precision`, `Recall`, `F1-Score`, `ROC-AUC`) và xuất báo cáo khoa học 5 phần:
```bash
python 3_miniproject_pipeline.py
```
* **Kết quả đầu ra:** `data/heart_cleaned.csv`, `output/chart_heart_miniproject.png` và `output/bao_cao_khoa_hoc_heart.pdf`.

### Bước 4: Khởi chạy Dashboard tương tác Streamlit
Mở giao diện web cho phép người dùng lọc dữ liệu theo độ tuổi/giới tính, chọn biến lâm sàng xem biểu đồ, nhập chỉ số dự đoán thử nghiệm trên bệnh nhân mới và tải trực tiếp báo cáo PDF:
```bash
streamlit run app_streamlit.py
```
* Truy cập địa chỉ hiển thị trên terminal (mặc định: `http://localhost:8501`).

---

## 5. Giấy phép sử dụng (License)
Dự án này được phân phối theo giấy phép **MIT License** — cho phép tự do sử dụng, sao chép, chỉnh sửa, hợp nhất và phân phối lại cho mục đích học tập và nghiên cứu với điều kiện giữ nguyên thông báo bản quyền. Xem toàn văn tại tệp [LICENSE](LICENSE).

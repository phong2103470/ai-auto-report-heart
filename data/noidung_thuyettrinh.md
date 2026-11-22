# PHÂN TÍCH DỮ LIỆU LÂM SÀNG VÀ DỰ ĐOÁN BỆNH TIM MẠCH
Học viên: Đào Trần Quốc Phong | Đại học Cần Thơ

## 1. Bối cảnh và Mục tiêu nghiên cứu
- Bệnh lý tim mạch là nguyên nhân gây tử vong hàng đầu nhưng có thể phòng ngừa nếu sàng lọc sớm.
- Ứng dụng học máy trên các chỉ số khám lâm sàng giúp hỗ trợ bác sĩ phân tầng nguy cơ nhanh chóng.
- Mục tiêu: Làm sạch dữ liệu, trực quan hóa đặc trưng và tự động hóa quy trình xuất báo cáo khoa học.

## 2. Đặc tả bộ dữ liệu Heart Failure Prediction
- Nguồn dữ liệu: Kaggle / UCI Machine Learning Repository (918 hồ sơ bệnh nhân, 12 thuộc tính).
- Biến đầu vào tiêu biểu: Tuổi, Giới tính, Loại đau ngực (ChestPainType), Huyết áp nghỉ, Cholesterol, Nhịp tim tối đa (MaxHR).
- Tiền xử lý: Loại bỏ bản ghi trùng lặp và chuẩn hóa các giá trị Cholesterol = 0 bằng trung vị (Median).

## 3. Trực quan hóa phân bố chỉ số lâm sàng
- Nhóm dương tính chiếm 55,3% tổng số mẫu khảo sát (508/918 ca).
- Nhịp tim tối đa (MaxHR) giảm dần theo độ tuổi và thấp hơn đáng kể ở nhóm mắc bệnh tim.
[IMAGE: output/chart_heart_ca_nhan.png]

## 4. Kết luận và Hướng phát triển
- Hệ thống Python tự động chuyển đổi dữ liệu CSV thành báo cáo PDF và bài thuyết trình PPTX nhất quán.
- Hướng mở rộng: Triển khai giao diện tương tác Streamlit cho phép bác sĩ nhập chỉ số và dự đoán trực tiếp.
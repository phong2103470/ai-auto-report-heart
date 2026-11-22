import importlib.util
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

spec = importlib.util.spec_from_file_location("pipeline", "3_miniproject_pipeline.py")
pipeline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline)

st.set_page_config(page_title="Heart Disease AI Report Dashboard", layout="wide")
st.title("Hệ thống Phân tích Dữ liệu Tim mạch & Tự động Sinh Báo cáo Khoa học")

df_raw = pd.read_csv("data/heart.csv")
report_path, metrics, model, feature_cols = pipeline.run_pipeline(df_raw)
df_clean = pd.read_csv("data/heart_cleaned.csv")

st.sidebar.header("Bộ lọc & Tùy chọn phân tích")
selected_var = st.sidebar.selectbox("Chọn biến định lượng:", ["MaxHR", "Age", "Cholesterol", "RestingBP", "Oldpeak"])
selected_sex = st.sidebar.multiselect("Giới tính:", options=df_clean["Sex"].unique(), default=list(df_clean["Sex"].unique()))
age_range = st.sidebar.slider("Khoảng tuổi:", int(df_clean["Age"].min()), int(df_clean["Age"].max()), (28, 77))

df_filtered = df_clean[
    (df_clean["Sex"].isin(selected_sex)) &
    (df_clean["Age"] >= age_range[0]) &
    (df_clean["Age"] <= age_range[1])
]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Số hồ sơ đang lọc", len(df_filtered))
c2.metric("Tỷ lệ bệnh tim", f"{df_filtered['HeartDisease'].mean()*100:.1f}%")
c3.metric("Độ chính xác AI (Accuracy)", f"{metrics['Accuracy']*100:.2f}%")
c4.metric("Chỉ số ROC-AUC", f"{metrics['ROC-AUC']:.3f}")

col_left, col_right = st.columns(2)
with col_left:
    st.subheader(f"Phân phối chỉ số {selected_var} theo chẩn đoán")
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    sns.histplot(data=df_filtered, x=selected_var, hue="HeartDisease", kde=True, palette=["#2E86AB", "#D9534F"], ax=ax1)
    st.pyplot(fig1)

with col_right:
    st.subheader("Dự đoán thử nghiệm trên bệnh nhân mới")
    age = st.number_input("Tuổi (Age)", 20, 95, 55)
    sex = st.selectbox("Giới tính (Sex)", ["M", "F"])
    cp = st.selectbox("Loại đau ngực (ChestPainType)", ["ASY", "NAP", "ATA", "TA"])
    max_hr = st.number_input("Nhịp tim tối đa (MaxHR)", 60, 210, 125)
    slope = st.selectbox("Độ dốc đoạn ST (ST_Slope)", ["Flat", "Up", "Down"])

    raw_sample = pd.DataFrame([{
        "Age": age, "Sex": sex, "ChestPainType": cp, "RestingBP": 130,
        "Cholesterol": 220, "FastingBS": 0, "RestingECG": "Normal",
        "MaxHR": max_hr, "ExerciseAngina": "N", "Oldpeak": 1.0, "ST_Slope": slope
    }])
    encoded_sample = pd.get_dummies(raw_sample).reindex(columns=feature_cols, fill_value=0)
    prob = model.predict_proba(encoded_sample)[0][1]
    st.info(f"Xác suất nguy cơ mắc bệnh tim dự đoán: **{prob*100:.1f}%**")

st.divider()
with open(report_path, "rb") as f:
    st.download_button(
        label="Tải xuống Báo cáo Khoa học PDF (Tự động tạo)",
        data=f,
        file_name="Bao_Cao_Khoa_Hoc_Heart_AI.pdf",
        mime="application/pdf"
    )
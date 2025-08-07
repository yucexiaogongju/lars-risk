import streamlit as st
import pandas as pd
import joblib

# 设置网页标题
st.set_page_config(page_title="LARS 风险预测小工具", layout="wide")
st.title("LARS 风险预测小工具")

# 加载模型
model_path = 'lars_risk_model.pkl'  # 如果模型不在当前目录，请写完整路径
model = joblib.load(model_path)

# 左侧输入特征
st.sidebar.header("请输入以下特征：")

age = st.sidebar.number_input("年龄 age", min_value=0.0, max_value=120.0, value=50.0, step=1.0)
BMI = st.sidebar.number_input("BMI", min_value=10.0, max_value=50.0, value=22.0, step=0.1)
tumor_dist = st.sidebar.number_input("肿瘤距离 tumor_dist", value=5.0)
surg_time = st.sidebar.number_input("手术时间 surg_time", value=180.0)
exhaust = st.sidebar.number_input("排气天数 exhaust", value=2.0)
tumor_size = st.sidebar.number_input("肿瘤大小 tumor_size", value=3.0)
TNM = st.sidebar.number_input("TNM 分期", value=2.0)
neoadjuvant = st.sidebar.number_input("是否新辅助治疗 neoadjuvant", min_value=0.0, max_value=1.0, value=0.0)

# 整合输入特征
input_data = pd.DataFrame([{
    'age': age,
    'BMI': BMI,
    'tumor_dist': tumor_dist,
    'surg_time': surg_time,
    'exhaust': exhaust,
    'tumor_size': tumor_size,
    'TNM': TNM,
    'neoadjuvant': neoadjuvant
}])

# 预测
if st.button("点击预测"):
    prediction = model.predict(input_data)[0]

    if prediction == 1:
        st.success("✅ 预测结果：是（存在风险）")
    else:
        st.info("❌ 预测结果：否（无明显风险）")
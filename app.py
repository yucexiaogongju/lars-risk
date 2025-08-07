import streamlit as st
import pandas as pd
import joblib
import sys  # 添加系统库用于版本检查
import warnings  # 添加警告处理

# 设置网页标题
st.set_page_config(page_title="LARS 风险预测小工具", layout="wide")
st.title("LARS 风险预测小工具")

# === 添加的环境检查代码 ===
st.subheader("环境信息")
st.write(f"Python 版本: {sys.version.split()[0]}")  # 显示Python版本

try:
    st.write(f"Streamlit 版本: {st.__version__}")  # 显示Streamlit版本
except:
    st.warning("无法获取Streamlit版本")

# === 模型加载部分（添加了错误处理）===
st.subheader("模型加载状态")
model_path = 'lars_risk_model.pkl'  # 如果模型不在当前目录，请写完整路径

try:
    # 尝试加载模型
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # 忽略警告
        model = joblib.load(model_path)
    st.success("✅ 模型加载成功！")
    model_loaded = True
    
except Exception as e:
    st.error(f"❌ 模型加载失败: {str(e)}")
    st.warning("预测功能将不可用，请检查模型文件是否存在且兼容")
    model_loaded = False

# === 左侧输入特征 ===
st.sidebar.header("请输入以下特征：")

# 创建输入字段
age = st.sidebar.number_input("年龄 age", min_value=0.0, max_value=120.0, value=50.0, step=1.0)
BMI = st.sidebar.number_input("BMI", min_value=10.0, max_value=50.0, value=22.0, step=0.1)
tumor_dist = st.sidebar.number_input("肿瘤距离 tumor_dist", min_value=0.0, max_value=50.0, value=5.0, step=0.1)
surg_time = st.sidebar.number_input("手术时间 surg_time", min_value=0.0, max_value=600.0, value=180.0, step=1.0)
exhaust = st.sidebar.number_input("排气天数 exhaust", min_value=0.0, max_value=30.0, value=2.0, step=0.5)
tumor_size = st.sidebar.number_input("肿瘤大小 tumor_size", min_value=0.1, max_value=20.0, value=3.0, step=0.1)
TNM = st.sidebar.number_input("TNM 分期", min_value=1.0, max_value=4.0, value=2.0, step=1.0)
neoadjuvant = st.sidebar.number_input("是否新辅助治疗 neoadjuvant", min_value=0.0, max_value=1.0, value=0.0, step=1.0)

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

# 显示输入的数据（调试用）
st.subheader("输入的特征数据")
st.dataframe(input_data)

# 预测按钮
if st.button("点击预测"):
    if not model_loaded:
        st.error("模型未正确加载，无法进行预测")
    else:
        try:
            # 尝试进行预测
            prediction = model.predict(input_data)[0]
            
            # 显示预测结果
            if prediction == 1:
                st.success("✅ 预测结果：是（存在风险）")
                st.markdown("**建议措施:**")
                st.markdown("- 请咨询专业医生进行进一步评估")
                st.markdown("- 定期进行复查")
            else:
                st.info("❌ 预测结果：否（无明显风险）")
                st.markdown("**建议:**")
                st.markdown("- 继续保持健康生活习惯")
                st.markdown("- 定期体检")
                
        except Exception as e:
            st.error(f"预测过程中出错: {str(e)}")
            st.warning("请检查输入数据格式是否正确")

# 添加使用说明
st.sidebar.markdown("---")
st.sidebar.subheader("使用说明")
st.sidebar.info("1. 在左侧输入所有特征值\n2. 点击'点击预测'按钮\n3. 查看预测结果和建议")

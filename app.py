import streamlit as st
import pandas as pd
from io import BytesIO

# 你原来的两个格式化函数（完全没有改）
def format_line(spend, gmv, cpp, aov, earning, roi):
    return (f"总消耗${spend:.2f}，GMV${gmv}，CPP${cpp:.2f}，"
            f"AOV${aov:.2f}，Earning${earning:.2f}，ROI {roi:.2f}")

def format_change(spend_change, roi_change):
    def fmt(val):
        return f"{val:+.2f}%"  # 自动正负号 + 两位小数
    return f"消耗环比昨日{fmt(spend_change)}，ROI{fmt(roi_change)}"

# Streamlit 页面设置
st.set_page_config(page_title="博主数据分析工具", layout="centered")
st.title("📊 博主数据分析工具")
st.markdown("请上传符合格式的 Excel 文件（Sheet 名为 Sheet1）")

uploaded_file = st.file_uploader("选择 Excel 文件", type=["xlsx"])

if uploaded_file is not None:
    try:
        # 因为需要读两次，先保存到 bytes 再读
        bytes_data = uploaded_file.read()
        
        # 正常字段（表头第2行）
        df_normal = pd.read_excel(BytesIO(bytes_data), sheet_name="Sheet1", header=1)
        # 涨跌字段（表头第1行）
        df_change = pd.read_excel(BytesIO(bytes_data), sheet_name="Sheet1", header=0)
        
        # 合计行
        total_row = df_normal[df_normal.iloc[:, 0] == "合计"].iloc[0]
        spend = total_row["Spend"]
        gmv = total_row["GMV"]
        cpp = total_row["CPP"]
        aov = total_row["AOV"]
        earning = total_row["Earning"]
        roi = total_row["ROI"]
        
        total_change_row = df_change[df_change.iloc[:, 0] == "合计"].iloc[0]
        spend_change = total_change_row["消耗涨跌"]
        roi_change = total_change_row["ROI涨跌"]
        
        result1 = format_line(spend, gmv, cpp, aov, earning, roi)
        result2 = format_change(spend_change, roi_change)
        
        # 这里原样输出你原来 print 的内容
        st.text(result1)
        st.text(result2)
        
        st.text("分博主分析：")
        st.text("分博主")
        
        for idx, row in df_normal.iterrows():
            blogger = row["博主"]
            if blogger == "合计":
                continue
            spend_val = row["Spend"]
            roi_val = row["ROI"]
            st.text(f"{blogger}：消耗{spend_val:.2f}，ROI {roi_val:.2f}")
    
    except Exception as e:
        st.error(f"处理出错：{e}\n请检查 Excel 格式（Sheet1，需要包含博主、Spend、ROI等列，且存在合计行）")
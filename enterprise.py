import streamlit as st
import pandas as pd
import plotly.express as px

# ======================
# 🎨 페이지 설정
# ======================
st.set_page_config(
    page_title="기업 보고 대시보드",
    page_icon="📈",
    layout="wide"
)

# ======================
# 📂 데이터 업로드
# ======================
st.sidebar.header("📂 데이터 업로드")
uploaded_file = st.sidebar.file_uploader("CSV 또는 Excel 파일을 업로드하세요", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success(f"✅ 데이터 로드 완료: {df.shape[0]}행 × {df.shape[1]}열")
else:
    st.warning("왼쪽 사이드바에서 파일을 업로드하세요.")
    st.stop()

# ======================
# 📌 KPI 카드
# ======================
st.subheader("📌 핵심 지표 (Key Metrics)")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("총 행 수", f"{df.shape[0]:,}")

with col2:
    st.metric("총 열 수", f"{df.shape[1]:,}")

with col3:
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    if len(numeric_cols) > 0:
        st.metric(f"{numeric_cols[0]} 평균", f"{df[numeric_cols[0]].mean():,.2f}")
    else:
        st.metric("수치형 데이터 없음", "-")

with col4:
    if len(numeric_cols) > 1:
        st.metric(f"{numeric_cols[1]} 평균", f"{df[numeric_cols[1]].mean():,.2f}")
    else:
        st.metric("수치형 데이터 없음", "-")

st.divider()

# ======================
# 📊 데이터 미리보기 & 요약
# ======================
tab1, tab2 = st.tabs(["📄 데이터 미리보기", "📊 기술 통계"])

with tab1:
    colA, colB = st.columns(2)
    with colA:
        max_rows = st.number_input("표시할 행 수", min_value=1, max_value=df.shape[0], value=10, step=1)
    with colB:
        max_cols = st.number_input("표시할 열 수", min_value=1, max_value=df.shape[1], value=min(10, df.shape[1]), step=1)

    st.dataframe(df.iloc[:max_rows, :max_cols], use_container_width=True)

with tab2:
    st.dataframe(df.describe(), use_container_width=True)

st.divider()

# ======================
# 📈 시각화 섹션
# ======================
st.subheader("📈 데이터 시각화")

# 컬럼 선택
x_col = st.selectbox("X축 컬럼 선택", df.columns)
y_col = st.selectbox("Y축 컬럼 선택", df.columns)
color_col = st.selectbox("색상 기준 컬럼 선택 (선택 사항)", [None] + list(df.columns))

# 그래프 유형 선택
chart_type = st.radio("그래프 유형", ["Bar", "Line", "Scatter"], horizontal=True)

if chart_type == "Bar":
    fig = px.bar(df, x=x_col, y=y_col, color=color_col if color_col else None, title=f"{x_col} vs {y_col}")
elif chart_type == "Line":
    fig = px.line(df, x=x_col, y=y_col, color=color_col if color_col else None, title=f"{x_col} vs {y_col}")
elif chart_type == "Scatter":
    fig = px.scatter(df, x=x_col, y=y_col, color=color_col if color_col else None, size_max=10, title=f"{x_col} vs {y_col}")

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ======================
# 📤 데이터 다운로드
# ======================
st.subheader("📤 데이터 다운로드")
csv_data = df.to_csv(index=False).encode("utf-8-sig")
st.download_button("CSV 다운로드", csv_data, file_name="processed_data.csv", mime="text/csv")

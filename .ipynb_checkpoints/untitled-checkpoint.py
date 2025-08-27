import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("📊 데이터 빠른 분석기")

file = st.file_uploader("CSV 파일 업로드", type="csv")
if file:
    df = pd.read_csv(file)
    st.subheader("1️⃣ 데이터 미리보기")
    st.write(df.head())

    st.subheader("2️⃣ 기본 정보")
    st.write(df.shape)
    st.write(df.info())

    st.subheader("3️⃣ 결측치 확인")
    st.write(df.isnull().sum())

    st.subheader("4️⃣ 기본 통계")
    st.write(df.describe())

    st.subheader("5️⃣ 간단 시각화")
    num_cols = df.select_dtypes(include='number').columns
    if len(num_cols) >= 2:
        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x=num_cols[0], y=num_cols[1], ax=ax)
        st.pyplot(fig)

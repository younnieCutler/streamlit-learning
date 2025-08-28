# abnb_pandas_lab.py
# ----------------------------------------------
# Airbnb 주가 CSV로 pandas 실습 올인원 스크립트
# 기능:
# 1) CSV 로드 & 점검
# 2) 결측치 처리 / 타입 변환
# 3) 지표 계산: 일간수익률, 누적수익률, 이동평균선(SMA20/50)
# 4) 월간 리샘플링(평균 종가, 총 거래량)
# 5) 간단한 매수/매도 시그널(골든/데드 크로스)
# 6) 시각화(가격+이동평균, 수익률 히스토그램)
# 7) 가공 결과 CSV로 저장

# Airbnbの株価CSVでpandasを実践するオールインワンスクリプト
# 機能:
# 1) CSVの読み込みと点検
# 2) 欠損値の処理 / 型変換
# 3) 指標の計算: 日次収益率、累積収益率、移動平均線(SMA20/50)
# 4) 月間リサンプリング(平均終値、総取引量)
# 5) 簡単な買い/売りシグナル(ゴールデン/デッドクロス)
# 6) 視覚化(価格+移動平均、収益率ヒストグラム)
# 7) 加工結果をCSVで保存

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# ---------------------------
# 1) 데이터 로드 (Data Loading)
# ---------------------------
# @st.cache 데코레이터를 사용하여 데이터 로딩을 캐시합니다.
# 이렇게 하면 앱이 다시 실행될 때마다 데이터를 다시 로드하는 것을 방지하여 성능을 향상시킵니다.
@st.cache
def load_data(path):
    # CSV 파일을 읽어 데이터프레임으로 변환합니다. 'Date' 열은 날짜 형식으로 파싱합니다.
    df = pd.read_csv(path, parse_dates=["Date"])
    # 날짜를 기준으로 데이터프레임을 오름차순으로 정렬하고 인덱스를 재설정합니다.
    df = df.sort_values("Date").reset_index(drop=True)
    return df

# CSV 파일 경로를 지정합니다.
CSV_PATH = 'datasets/ABNB_stock/ABNB_stock.csv' 
# load_data 함수를 호출하여 데이터를 로드합니다.
df = load_data(CSV_PATH)

# ---------------------------
# 2) 사이드바 (Sidebar)
# ---------------------------
# 사이드바에 헤더를 추가합니다.
st.sidebar.header("Filter")

# 날짜 필터 (Date Filter)
# 데이터프레임에서 최소 날짜와 최대 날짜를 가져옵니다.
min_date, max_date = df["Date"].min(), df["Date"].max()
# 사이드바에 날짜 범위 선택 위젯을 추가합니다.
date_range = st.sidebar.date_input(
    "기간 설정", # 위젯의 레이블
    value=[min_date, max_date], # 기본값으로 전체 기간을 설정
    min_value=min_date, # 선택 가능한 최소 날짜
    max_value=max_date # 선택 가능한 최대 날짜
)
# 이동평균선 기간 설정 (Moving Average Period Setting)
# 단기 이동평균선 기간을 설정하는 슬라이더를 추가합니다.
sma_short = st.sidebar.slider("단기 이동평균 (일)", 5, 50, 20)      # 최소 5, 최대 50, 기본값 20
# 장기 이동평균선 기간을 설정하는 슬라이더를 추가합니다.
sma_long = st.sidebar.slider("장기 이동평균 (일)", 50, 200, 100)    # 최소 50, 최대 200, 기본값 100

# ---------------------------
# 3) 데이터 전처리 (Data Preprocessing)
# ---------------------------

# 사용자가 선택한 날짜 범위에 따라 데이터를 필터링합니다.
mask = (df["Date"] >= pd.to_datetime(date_range[0])) & (df["Date"] <= pd.to_datetime(date_range[1]))
df_filtered = df.loc[mask].copy()

# 이동평균선 계산 (Calculate Moving Averages)
# 단기 이동평균선을 계산하여 'SMA_short' 열에 추가합니다.
df_filtered["SMA_short"] = df_filtered["Close"].rolling(window=sma_short).mean()
# 장기 이동평균선을 계산하여 'SMA_long' 열에 추가합니다.
df_filtered["SMA_long"] = df_filtered["Close"].rolling(window=sma_long).mean()

# 수익률 계산 (Calculate Returns)
# 일일 수익률을 계산하여 'Return' 열에 추가합니다.
df_filtered["Return"] = df_filtered["Close"].pct_change()
# 누적 수익률을 계산하여 'CumReturn' 열에 추가합니다. fillna(0)으로 첫 날의 NaN 값을 0으로 처리합니다.
df_filtered["CumReturn"] = (1 + df_filtered["Return"].fillna(0)).cumprod()

# ---------------------------
# 4) 메인 페이지
# ---------------------------
st.title("📊 Airbnb Stock Dashboard")

st.markdown("""
Airbnb (`ABNB`) 株価データを分析するダッシュボード  
サイドバーで **期間**と **移動平均線**を調整してください。
""")

st.divider()


# ---------------------------
# 5) 가격 차트 (이동평균 포함)
# ---------------------------
st.subheader("株価 移動平均線")
fig_price = px.line(df_filtered, x="Date", y="Close", title="ABNB Closing Price")
fig_price.add_scatter(x=df_filtered["Date"], y=df_filtered["SMA_short"], mode="lines", name=f"SMA{sma_short}")
fig_price.add_scatter(x=df_filtered["Date"], y=df_filtered["SMA_long"], mode="lines", name=f"SMA{sma_long}")
st.plotly_chart(fig_price, use_container_width=True)

# ---------------------------
# 6) 누적 수익률
# ---------------------------
st.subheader("累積収益率")
st.line_chart(df_filtered.set_index("Date")["CumReturn"])

# ---------------------------
# 7) 수익률 분포
# ---------------------------
st.subheader("日収分布")
st.bar_chart(df_filtered["Return"].dropna().value_counts(bins=30).sort_index())

# ---------------------------
# 8) 데이터 미리보기
# ---------------------------
with st.expander("データプレビュー"):
    st.dataframe(df_filtered.head(20))
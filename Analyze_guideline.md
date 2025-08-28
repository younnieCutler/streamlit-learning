

---

# 🍏 Apple 주가 데이터 분석 가이드라인 (Streamlit/Jupyter 공용)

## 1. 데이터 개요 확인 (Data Overview)

**목적**: 데이터 구조와 내용을 빠르게 파악

* **데이터 로드**

  ```python
  import pandas as pd
  df = pd.read_csv("AAPL.csv")
  ```

* **기본 확인**

  ```python
  df.head()
  df.info()
  df.describe()
  ```

* **체크 포인트**

  * 컬럼: `Date, Open, High, Low, Close, Adj Close, Volume`
  * `Date` → `datetime` 변환: `pd.to_datetime(df["Date"])`
  * 데이터 기간: `df["Date"].min(), df["Date"].max()`

👉 Streamlit에서는 `st.dataframe(df.head())`로 미리보기 가능

---

## 2. 데이터 전처리 (Data Preprocessing)

**목적**: 결측치 제거 및 분석 친화적 컬럼 생성

* **결측치 확인**

  ```python
  df.isnull().sum()
  ```

* **날짜 파생 컬럼 추가**

  ```python
  df["Year"] = df["Date"].dt.year
  df["Month"] = df["Date"].dt.month
  df["DayOfWeek"] = df["Date"].dt.day_name()
  ```

* **일일 수익률 계산**

  ```python
  df["Daily_Return"] = df["Close"].pct_change()
  ```

---

## 3. 탐색적 데이터 분석 (EDA) 및 시각화

**목적**: 데이터의 패턴, 추세, 관계를 시각화로 직관적으로 파악

* **주가 추세 분석**: 종가(Close), 수정종가(Adj Close) 라인 플롯

* **거래량 분석**: 시간 대비 거래량 바 차트

  ```python
  import plotly.graph_objects as go
  go.Bar(x=df["Date"], y=df["Volume"])
  ```

* **이동평균선 분석**

  ```python
  df["SMA50"] = df["Close"].rolling(50).mean()
  df["SMA200"] = df["Close"].rolling(200).mean()
  ```

* **일일 수익률 분석**

  * 수익률 계산: `pct_change()`
  * 분포:

    ```python
    import seaborn as sns
    sns.histplot(df["Daily_Return"], bins=50)
    ```

* **연도/월별 분석**: 박스플롯으로 계절성 파악

  ```python
  sns.boxplot(x="Month", y="Close", data=df)
  ```

👉 Streamlit에서는 `st.line_chart(df.set_index("Date")[["Close","SMA50","SMA200"]])` 활용 가능

---

## 4. 심화 분석 (Advanced Analysis)

**목적**: 변수 간 연관성 및 예측 모델 적용

* **상관관계 히트맵**

  ```python
  corr = df[["Open","High","Low","Close","Volume"]].corr()
  sns.heatmap(corr, annot=True, cmap="coolwarm")
  ```

* **시계열 분해 (Trend/Seasonality/Residual)**

  ```python
  from statsmodels.tsa.seasonal import seasonal_decompose
  result = seasonal_decompose(df.set_index("Date")["Close"], model="multiplicative", period=252)
  result.plot()
  ```

* **예측 모델링**

  * 전통 시계열: ARIMA, SARIMA
  * 딥러닝: LSTM, GRU (TensorFlow/Keras)

---

## 5. Streamlit 대시보드 설계 팁

* **사이드바 옵션**

  * 기간 선택 (start/end date)
  * 이동평균 기간 (예: 50일, 200일)
  * 시각화 타입 (라인, 캔들스틱, 히스토그램 등)

* **메인 화면 구성**

  * 종가 + 이동평균 그래프
  * 거래량 바 차트
  * 일일 수익률 히스토그램
  * 상관관계 히트맵

---

이제 이 구조대로라면 **Streamlit 뼈대 코드**를 만들어 바로 적용할 수 있어요.
원하시면 제가 Markdown 가이드에 맞춰 **Streamlit 대시보드 기본 코드**까지 붙여드릴 수 있습니다. 그 버전으로 확장할까요?

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import io
from typing import Optional

# path = r'C:\Users\j.kim\py_workspace\python_learning\datasets\tokyo_realstate.csv'
# df = pd.read_csv(path, encoding="cp932")

st.set_page_config(page_title="東京不動産ダッシュボード", layout="wide")

# ファイルパスを直接指定
path = r'C:\Users\j.kim\py_workspace\python_learning\datasets\tokyo_realstate.csv'
df = pd.read_csv(path, encoding="cp932")


@st.cache_data
def load_data(file_bytes: Optional[bytes]) -> pd.DataFrame:
    if file_bytes:
        df = pd.read_csv(io.BytesIO(file_bytes))
    else:
        # 이 부분은 CSV 경로 직접 읽도록 수정해야 함
        df = pd.read_csv(r'C:\Users\j.kim\py_workspace\python_learning\datasets\tokyo_realstate.csv', encoding="cp932")
    return df

# 数値列を安全に変換
for c in ["TRADEPRICE_RAW","AREA_RAW","UNITPRICE_RAW","BUILDING_AGE","YEAR","QUARTER","BUILDINGYEAR"]:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

# 日付列
if "TRADE_DATE" in df.columns:
    df["TRADE_DATE"] = pd.to_datetime(df["TRADE_DATE"], errors="coerce")

# 新築/中古列を整形
if "BUILDING_AGE_GROUP" in df.columns:
    df["NEW_USED"] = df["BUILDING_AGE_GROUP"].replace({"新築":"新築","中古":"中古"}).fillna("不明")

st.title("🏠 東京不動産取引データ (サンプルダッシュボード)")
st.caption(f"行数: {len(df):,}")

# サイドバーにフィルターを配置

with st.sidebar:
    st.header("🔎 フィルター")

    # 年度
    years = sorted(df["YEAR"].dropna().unique())
    year_sel = st.slider("取引年", int(min(years)), int(max(years)), (int(min(years)), int(max(years))))

    # 区（市区）
    muni_opts = sorted(df["MUNICIPALITY"].dropna().unique())
    muni_sel = st.multiselect("市区を選択", muni_opts, default=muni_opts)

    # 物件タイプ（建物用途）
    use_opts = sorted(df["USE"].dropna().unique())
    use_sel = st.multiselect("建物用途", use_opts, default=use_opts)

    # 築年数
    if "BUILDING_AGE" in df:
        age_min, age_max = int(df["BUILDING_AGE"].min()), int(df["BUILDING_AGE"].max())
        age_sel = st.slider("築年数", age_min, age_max, (age_min, age_max))

    # 新築 / 中古
    nu_opts = sorted(df["NEW_USED"].dropna().unique())
    nu_sel = st.multiselect("新築/中古", nu_opts, default=nu_opts)

q = pd.Series([True] * len(df))

q &= df["YEAR"].between(year_sel[0], year_sel[1])
if muni_sel:
    q &= df["MUNICIPALITY"].isin(muni_sel)
if use_sel:
    q &= df["USE"].isin(use_sel)
if "BUILDING_AGE" in df:
    q &= df["BUILDING_AGE"].between(age_sel[0], age_sel[1])
if nu_sel:
    q &= df["NEW_USED"].isin(nu_sel)

df_filtered = df[q].copy()
st.success(f"フィルタ後の件数: {len(df_filtered):,}")

import plotly.express as px

tab1, tab2, tab3, tab4 = st.tabs(["年度別", "市区別", "建物用途", "築年数"])

with tab1:
    g = df_filtered.groupby("YEAR").size().reset_index(name="count")
    fig = px.bar(g, x="YEAR", y="count", title="📅 年度別取引件数")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    g = df_filtered.groupby("MUNICIPALITY").size().reset_index(name="count").sort_values("count", ascending=False)
    fig = px.bar(g, x="MUNICIPALITY", y="count", title="🗺️ 市区別取引件数")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    g = df_filtered.groupby("USE").size().reset_index(name="count")
    fig = px.pie(g, names="USE", values="count", title="🏢 建物用途の割合")
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    fig = px.histogram(df_filtered, x="BUILDING_AGE", nbins=20, color="NEW_USED", title="⏳ 築年数分布")
    st.plotly_chart(fig, use_container_width=True)

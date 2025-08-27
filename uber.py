import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# 1. ウーバーはどんな時間帯によく呼ばれるか。
# 2. よく呼ばれている配達先を調べよう

path = '../python_learning/datasets/Uber/Uber.csv'
df = pd.read_csv(path, skipfooter=1, engine='python')

st.title('ウーバー分析')
st.dataframe(df.head(10))

with st.sidebar:
    st.header('欠損地、ユニーク確認')
    st.write('データ型と欠損値確認')
    st.write(df.info()) # 型、欠損値のまとめ
    st.write("ユニーク個数確認")
    st.write(df.nunique())

# 1) DATETIME 変換
df['start_dt'] = pd.to_datetime(df['START_DATE*'], errors='coerce')

# 2) 時間 parsing
df['hour'] = df['start_dt'].dt.hour

# 3) 曜日 parsing
df['weekday'] = df['start_dt'].dt.weekday

# 可読性のため曜日名をマッピング
weekday_map = {0:'月',1:'火',2:'水',3:'木',4:'金',5:'土',6:'日'}
df['weekday_name'] = df['weekday'].map(weekday_map)

# 集計テーブル
hour_counts = (
    df.groupby('hour')
      .size()
      .reset_index(name='counts')
      .sort_values('hour')
)
weekday_order = ['月','火','水','木','金','土','日']
weekday_counts = (
    df.groupby('weekday_name')
      .size()
      .reindex(weekday_order, fill_value=0)
      .reset_index(name='counts')
      .rename(columns={'index':'weekday_name'})
)

# ヒートマップ用のピボット
heat = (
    df.groupby(['weekday_name','hour'])
      .size()
      .reset_index(name='counts')
      .pivot(index='weekday_name', columns='hour', values='counts')
      .reindex(weekday_order)
      .fillna(0)
)

# ========== 1) ヘッダー ==========
st.title("Uber分析 – 形の違う3種の可視化")

# ========== 2) 時間帯別: エリアチャート ==========
st.subheader(" 時間帯別 呼び出し回数（エリアチャート）")
fig_area = px.area(
    hour_counts,
    x='hour', y='counts',
    title="時間帯別の需要（0–23時）",
)
fig_area.update_traces(mode='lines+markers')
fig_area.update_layout(xaxis=dict(dtick=1))
st.plotly_chart(fig_area, use_container_width=True)

# ========== 3) 曜日別: 円形(Polar)棒グラフ ==========
st.subheader(" 曜日別 呼び出し回数（円形バー）")
# theta(角度)配置: 7曜日を円に均等に配置
theta_labels = weekday_order
theta_degrees = [i * (360/7) for i in range(7)]
r_values = weekday_counts['counts'].tolist()

fig_polar = go.Figure()
fig_polar.add_trace(go.Barpolar(
    theta=theta_degrees,
    r=r_values,
    text=[f"{d}: {c}" for d, c in zip(theta_labels, r_values)],
    hoverinfo="text+r",
    marker_line_width=1
))
fig_polar.update_layout(
    title="曜日別の需要（Polar Bar）",
    polar=dict(
        angularaxis=dict(
            tickmode="array",
            tickvals=theta_degrees,
            ticktext=theta_labels
        )
    ),
    showlegend=False
)
st.plotly_chart(fig_polar, use_container_width=True)

# ========== 4) 曜日×時間帯: ヒートマップ ==========
st.subheader(" 曜日 × 時間帯 ヒートマップ（密度パターン）")
fig, ax = plt.subplots()
sns.heatmap(heat, cmap="YlGnBu", ax=ax)  # 異なる形状を強調するためにseabornを使用
ax.set_xlabel("Hour")
ax.set_ylabel("Weekday")
st.pyplot(fig)

# ========== 5) 要約KPI ==========
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("総呼び出し件数", f"{len(df):,}")
with col2:
    st.metric("ピーク時間帯(件数)", f"{hour_counts.loc[hour_counts['counts'].idxmax(),'hour']}時")
with col3:
    st.metric("ピーク曜日(件数)", weekday_counts.loc[weekday_counts['counts'].idxmax(),'weekday_name'])

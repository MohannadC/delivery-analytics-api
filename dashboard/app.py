import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import requests
import pandas as pd
from os import getenv

st.set_page_config(page_title="Delivery Analytics BI", layout="wide")
st.title("Delivery Analytics Dashboard")

API_URL = getenv("API_URL", "http://localhost:8000")


@st.cache_data(ttl=60)
def fetch_data(endpoint):
    try:
        response = requests.get(f"{API_URL}{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка подключения к API: {e}")
        return None


tab1, tab2 = st.tabs(["Бизнес-метрики", "Технические метрики"])

with tab1:
    st.header("Анализ заказов и выручки")

    cancelled_data = fetch_data("/analytics/cancelled")
    if cancelled_data:
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Всего заказов", value=cancelled_data["total_orders"])
            fig_pie = px.pie(
                names=["Доставлено", "Отменено"],
                values=[
                    cancelled_data["total_orders"] - cancelled_data["cancelled_orders"],
                    cancelled_data["cancelled_orders"],
                ],
                title="Соотношение статусов заказов",
                color_discrete_sequence=["#00C853", "#FF5252"],
            )
            st.plotly_chart(fig_pie, use_container_width=False)
        with col2:
            rate_percent = round(cancelled_data["cancelled_rate"] * 100, 2)
            st.metric(label="Доля отмен", value=f"{rate_percent}%")
            revenue_data = fetch_data("/analytics/revenue")
            if revenue_data:
                df_revenue = pd.DataFrame(revenue_data)
                df_revenue = df_revenue.sort_values(by="total_revenue", ascending=True)
                df_revenue["total_revenue"] /= 1e3

                fig_bar = px.bar(
                    df_revenue,
                    x="total_revenue",
                    y="restaurant",
                    orientation="h",
                    title="Топ ресторанов по выручке",
                    labels={
                        "total_revenue": "Выручка (тыс. руб)",
                        "restaurant": "Ресторан",
                    },
                )
                st.plotly_chart(fig_bar, use_container_width=False)


with tab2:
    st.header("Мониторинг производительности API (за последние 24 часа)")

    # Получаем метрики
    metrics_data = fetch_data("/metrics?time=24")

    if metrics_data and isinstance(metrics_data, dict):
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("RPS (Запросов/сек)", round(metrics_data.get("rps", 0), 6))
        col2.metric("p50 (мс)", round(metrics_data.get("p50", 0), 3))
        col3.metric("p95 (мс)", round(metrics_data.get("p95", 0), 3))
        col4.metric("p99 (мс)", round(metrics_data.get("p99", 0), 3))
        col5.metric(
            "Error Rate (5xx)", f"{round(metrics_data.get('error_rate', 0), 2)}%"
        )

        st.subheader("Распределение времени отклика (Перцентили)")
        percentiles = {
            "p50": metrics_data.get("p50", 0),
            "p95": metrics_data.get("p95", 0),
            "p99": metrics_data.get("p99", 0),
        }

        fig_latency = go.Figure(
            data=[
                go.Bar(
                    x=list(percentiles.keys()),
                    y=list(percentiles.values()),
                    marker_color=["#2196F3", "#FF9800", "#F44336"],
                )
            ]
        )
        fig_latency.update_layout(yaxis_title="Время отклика (мс)")
        st.plotly_chart(fig_latency, use_container_width=True)

    else:
        st.warning("Нет данных о метриках.")

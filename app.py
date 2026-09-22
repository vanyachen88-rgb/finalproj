import streamlit as st
import pandas as pd
import plotly.express as px

from analytics.db import read_sql


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Rental Business Analytics",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("📊 Rental Business Analytics")
st.caption("Data Engineering & Business Intelligence Dashboard")


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    customers = read_sql("""
        SELECT *
        FROM dbo.Customers
    """)

    leads = read_sql("""
        SELECT *
        FROM dbo.Leads
    """)

    rentals = read_sql("""
        SELECT *
        FROM dbo.Rentals
    """)

    payments = read_sql("""
        SELECT *
        FROM dbo.Payments
    """)

    machines = read_sql("""
        SELECT *
        FROM dbo.Machines
    """)

    maintenance = read_sql("""
        SELECT *
        FROM dbo.Maintenance
    """)

    campaigns = read_sql("""
        SELECT *
        FROM dbo.Marketing_Campaigns
    """)

    return (
        customers,
        leads,
        rentals,
        payments,
        machines,
        maintenance,
        campaigns
    )


(
    customers,
    leads,
    rentals,
    payments,
    machines,
    maintenance,
    campaigns
) = load_data()


# ============================================================
# KPI
# ============================================================

customer_count = len(customers)

lead_count = len(leads)

rental_count = len(rentals)

total_revenue = payments.loc[
    payments["payment_status"] == "已付款",
    "amount"
].sum()

avg_monthly_fee = rentals["monthly_fee"].mean()

maintenance_cost = maintenance["cost"].sum()


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Customers",
        f"{customer_count:,}"
    )

with col2:
    st.metric(
        "Leads",
        f"{lead_count:,}"
    )

with col3:
    st.metric(
        "Rentals",
        f"{rental_count:,}"
    )

with col4:
    st.metric(
        "Total Revenue",
        f"${total_revenue:,.0f}"
    )


col5, col6 = st.columns(2)

with col5:
    st.metric(
        "Average Monthly Fee",
        f"${avg_monthly_fee:,.2f}"
    )

with col6:
    st.metric(
        "Maintenance Cost",
        f"${maintenance_cost:,.0f}"
    )


st.divider()


# ============================================================
# CUSTOMER / LEAD / RENTAL
# ============================================================

st.header("Business Overview")

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# Leads by Channel
# ------------------------------------------------------------

with col1:

    lead_channel = (
        leads
        .groupby("channel")
        .size()
        .reset_index(name="lead_count")
        .sort_values("lead_count", ascending=False)
    )

    fig = px.bar(
        lead_channel,
        x="channel",
        y="lead_count",
        title="Leads by Channel",
        text="lead_count"
    )

    fig.update_layout(
        xaxis_title="Channel",
        yaxis_title="Leads"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ------------------------------------------------------------
# Rental Status
# ------------------------------------------------------------

with col2:

    rental_status = (
        rentals
        .groupby("status")
        .size()
        .reset_index(name="rental_count")
    )

    fig = px.pie(
        rental_status,
        names="status",
        values="rental_count",
        title="Rental Status"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# REVENUE
# ============================================================

st.header("Revenue Analysis")

payments["payment_date"] = pd.to_datetime(
    payments["payment_date"]
)

paid_payments = payments[
    payments["payment_status"] == "已付款"
].copy()

revenue_trend = (
    paid_payments
    .groupby(
        paid_payments["payment_date"].dt.to_period("M")
    )["amount"]
    .sum()
    .reset_index()
)

revenue_trend["payment_date"] = (
    revenue_trend["payment_date"]
    .astype(str)
)

fig = px.line(
    revenue_trend,
    x="payment_date",
    y="amount",
    markers=True,
    title="Monthly Revenue Trend"
)

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# MACHINE ANALYSIS
# ============================================================

st.header("Machine Analysis")

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# Machine Status
# ------------------------------------------------------------

with col1:

    machine_status = (
        machines
        .groupby("status")
        .size()
        .reset_index(name="machine_count")
    )

    fig = px.bar(
        machine_status,
        x="status",
        y="machine_count",
        title="Machine Status",
        text="machine_count"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ------------------------------------------------------------
# Maintenance Cost by Type
# ------------------------------------------------------------

with col2:

    maintenance_type = (
        maintenance
        .groupby("maintenance_type")["cost"]
        .sum()
        .reset_index()
        .sort_values("cost", ascending=False)
    )

    fig = px.bar(
        maintenance_type,
        x="maintenance_type",
        y="cost",
        title="Maintenance Cost by Type",
        text="cost"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CAMPAIGN ANALYSIS
# ============================================================

st.header("Marketing Campaign Analysis")

campaign_leads = (
    leads
    .groupby("campaign_id")
    .size()
    .reset_index(name="lead_count")
)

campaign_analysis = campaign_leads.merge(
    campaigns,
    on="campaign_id",
    how="left"
)

campaign_analysis = campaign_analysis.sort_values(
    "lead_count",
    ascending=False
)

st.dataframe(
    campaign_analysis[
        [
            "campaign_id",
            "campaign_name",
            "channel",
            "budget",
            "lead_count"
        ]
    ],
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Rental Business Data Engineering Project | "
    "Python + SQL Server + Google Cloud SQL + Streamlit"
)
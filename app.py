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
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .dashboard-subtitle {
        color: #6b7280;
        font-size: 1rem;
        margin-top: -12px;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 1.35rem;
        font-weight: 600;
        margin-top: 15px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data(ttl=300)
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
# DATA PREPARATION
# ============================================================

date_columns = {
    "customers": ["register_date"],
    "leads": ["lead_date"],
    "rentals": ["start_date", "end_date"],
    "payments": ["payment_date"],
    "machines": ["purchase_date"],
    "maintenance": ["maintenance_date"],
    "campaigns": ["start_date", "end_date"]
}

for df_name, columns in date_columns.items():

    df = locals()[df_name]

    for column in columns:
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("📊 Dashboard")

st.sidebar.markdown("---")

st.sidebar.subheader("Filters")

all_dates = pd.concat(
    [
        customers["register_date"],
        leads["lead_date"],
        rentals["start_date"],
        payments["payment_date"],
        maintenance["maintenance_date"]
    ]
).dropna()

min_date = all_dates.min().date()
max_date = all_dates.max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:

    selected_start = pd.Timestamp(date_range[0])
    selected_end = pd.Timestamp(date_range[1])

else:

    selected_start = pd.Timestamp(min_date)
    selected_end = pd.Timestamp(max_date)


# Channel filter

channels = sorted(
    leads["channel"]
    .dropna()
    .unique()
    .tolist()
)

selected_channels = st.sidebar.multiselect(
    "Marketing Channel",
    options=channels,
    default=channels
)


# Machine model filter

machine_models = sorted(
    machines["model"]
    .dropna()
    .unique()
    .tolist()
)

selected_models = st.sidebar.multiselect(
    "Machine Model",
    options=machine_models,
    default=machine_models
)


# ============================================================
# FILTER DATA
# ============================================================

customers_f = customers[
    customers["register_date"].between(
        selected_start,
        selected_end
    )
].copy()

leads_f = leads[
    leads["lead_date"].between(
        selected_start,
        selected_end
    )
].copy()

if selected_channels:
    leads_f = leads_f[
        leads_f["channel"].isin(selected_channels)
    ]

rentals_f = rentals[
    rentals["start_date"].between(
        selected_start,
        selected_end
    )
].copy()

payments_f = payments[
    payments["payment_date"].between(
        selected_start,
        selected_end
    )
].copy()

machines_f = machines[
    machines["model"].isin(selected_models)
].copy()

maintenance_f = maintenance[
    maintenance["maintenance_date"].between(
        selected_start,
        selected_end
    )
].copy()

maintenance_f = maintenance_f[
    maintenance_f["machine_id"].isin(
        machines_f["machine_id"]
    )
].copy()
# ============================================================
# Project Information
st.sidebar.markdown("---")

st.sidebar.subheader("Project")

st.sidebar.markdown(
    """
    **Tech Stack**

    - Python
    - Pandas
    - SQLAlchemy
    - SQL Server
    - Google Cloud SQL
    - Streamlit
    - Plotly
    - Git / GitHub
    """
)

st.sidebar.caption(
    "Portfolio Data Engineering Project"
)

st.sidebar.link_button(
    "View Source Code",
    "https://github.com/vanyachen88-rgb/finalproj"
)

# ============================================================
# BUSINESS METRICS
# ============================================================

customer_count = len(customers_f)

lead_count = len(leads_f)

rental_count = len(rentals_f)

paid_payments = payments_f[
    payments_f["payment_status"] == "Paid"
].copy()

total_revenue = paid_payments["amount"].sum()

avg_monthly_fee = rentals_f["monthly_fee"].mean()

maintenance_cost = maintenance_f["cost"].sum()


# ============================================================
# LEAD CONVERSION
# ============================================================

# A lead is considered converted when the same customer
# has at least one rental starting on or after the lead date.

lead_rental_match = leads_f[
    ["lead_id", "customer_id", "lead_date"]
].merge(
    rentals_f[
        ["rental_id", "customer_id", "start_date"]
    ],
    on="customer_id",
    how="left"
)

lead_rental_match = lead_rental_match[
    lead_rental_match["start_date"] >=
    lead_rental_match["lead_date"]
]

converted_leads = (
    lead_rental_match["lead_id"]
    .dropna()
    .nunique()
)

conversion_rate = (
    converted_leads / lead_count
    if lead_count > 0
    else 0
)


# ============================================================
# HEADER
# ============================================================

st.title("📊 Rental Business Analytics")

st.markdown(
    """
    <div class="dashboard-subtitle">
    Data Engineering & Business Intelligence Dashboard
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    f"Analysis period: "
    f"{selected_start.strftime('%Y-%m-%d')} "
    f"to "
    f"{selected_end.strftime('%Y-%m-%d')}"
)


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
        f"NT$ {total_revenue:,.0f}"
    )


col5, col6, col7 = st.columns(3)

with col5:
    st.metric(
        "Average Monthly Fee",
        f"NT${avg_monthly_fee:,.0f}"  
        if pd.notna(avg_monthly_fee)
        else "NT$0"
    )

with col6:
    st.metric(
        "Maintenance Cost",
        f"NT${maintenance_cost:,.0f}"
    )

with col7:
    st.metric(
        "Lead Conversion",
        f"{conversion_rate:.1%}"
    )

st.markdown("---")
#各項數據的計算方式說明
with st.expander("KPI Definitions"):

    st.markdown(
        """
        **Total Revenue**  
        Sum of payments with `payment_status = Paid`.

        **Average Monthly Fee**  
        Average monthly rental fee within the selected period.

        **Maintenance Cost**  
        Total machine maintenance cost within the selected period.

        **Lead Conversion Rate**  
        Percentage of leads whose customer subsequently started
        at least one rental on or after the lead date.
        """
    )

# ============================================================
# TABS
# ============================================================

tab_overview, tab_marketing, tab_revenue, tab_machine = st.tabs(
    [
        "📊 Overview",
        "📣 Marketing",
        "💰 Revenue & Rentals",
        "🔧 Machines"
    ]
)


# ============================================================
# TAB 1 — OVERVIEW
# ============================================================

with tab_overview:

    st.subheader("Business Overview")

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # Monthly Revenue
    # --------------------------------------------------------

    with col1:

        revenue_monthly = (
            paid_payments
            .groupby(
                paid_payments["payment_date"].dt.to_period("M")
            )["amount"]
            .sum()
            .reset_index()
        )

        revenue_monthly["month"] = (
            revenue_monthly["payment_date"]
            .astype(str)
        )

        fig = px.line(
            revenue_monthly,
            x="month",
            y="amount",
            markers=True,
            title="Monthly Revenue"
        )

        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Revenue"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # --------------------------------------------------------
    # Leads by Channel
    # --------------------------------------------------------

    with col2:

        lead_channel = (
            leads_f
            .groupby("channel")
            .size()
            .reset_index(name="lead_count")
            .sort_values(
                "lead_count",
                ascending=False
            )
        )

        fig = px.bar(
            lead_channel,
            x="channel",
            y="lead_count",
            text="lead_count",
            title="Leads by Channel"
        )

        fig.update_layout(
            xaxis_title="Channel",
            yaxis_title="Leads"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # Rental Status
    # --------------------------------------------------------

    with col1:

        rental_status = (
            rentals_f
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
            width="stretch"
        )

    # --------------------------------------------------------
    # Customer Acquisition
    # --------------------------------------------------------

    with col2:

        acquisition = (
            customers_f
            .groupby("acquisition_channel")
            .size()
            .reset_index(name="customer_count")
            .sort_values(
                "customer_count",
                ascending=False
            )
        )

        fig = px.bar(
            acquisition,
            x="acquisition_channel",
            y="customer_count",
            text="customer_count",
            title="Customer Acquisition Channel"
        )

        fig.update_layout(
            xaxis_title="Channel",
            yaxis_title="Customers"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )


# ============================================================
# TAB 2 — MARKETING
# ============================================================

with tab_marketing:

    st.subheader("Marketing Performance")

    # --------------------------------------------------------
    # Channel Performance
    # --------------------------------------------------------

    channel_performance = (
        leads_f
        .groupby("channel")
        .agg(
            leads=("lead_id", "count"),
            customers=("customer_id", "nunique")
        )
        .reset_index()
    )

    channel_conversion = []

    for channel in channel_performance["channel"]:

        channel_leads = leads_f[
            leads_f["channel"] == channel
        ]

        channel_match = channel_leads[
            ["lead_id", "customer_id", "lead_date"]
        ].merge(
            rentals_f[
                ["customer_id", "start_date"]
            ],
            on="customer_id",
            how="left"
        )

        channel_match = channel_match[
            channel_match["start_date"]
            >= channel_match["lead_date"]
        ]

        converted = (
            channel_match["lead_id"]
            .dropna()
            .nunique()
        )

        channel_conversion.append(
            {
                "channel": channel,
                "converted_leads": converted
            }
        )

    channel_conversion = pd.DataFrame(
        channel_conversion
    )

    channel_performance = channel_performance.merge(
        channel_conversion,
        on="channel",
        how="left"
    )

    channel_performance["conversion_rate"] = (
        channel_performance["converted_leads"]
        / channel_performance["leads"]
    ).fillna(0)

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            channel_performance,
            x="channel",
            y="leads",
            text="leads",
            title="Leads by Channel"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with col2:

        fig = px.bar(
            channel_performance.sort_values(
                "conversion_rate",
                ascending=False
            ),
            x="channel",
            y="conversion_rate",
            text="conversion_rate",
            title="Lead Conversion Rate by Channel"
        )

        fig.update_traces(
            texttemplate="%{text:.1%}"
        )

        fig.update_layout(
            yaxis_tickformat=".0%"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # --------------------------------------------------------
    # Campaign Performance
    # --------------------------------------------------------

    st.subheader("Campaign Performance")

    campaign_leads = (
        leads_f
        .groupby("campaign_id")
        .agg(
            lead_count=("lead_id", "count"),
            unique_customers=("customer_id", "nunique")
        )
        .reset_index()
    )

    campaign_analysis = campaigns.merge(
        campaign_leads,
        on="campaign_id",
        how="left"
    )

    campaign_analysis["lead_count"] = (
        campaign_analysis["lead_count"]
        .fillna(0)
        .astype(int)
    )

    campaign_analysis["unique_customers"] = (
        campaign_analysis["unique_customers"]
        .fillna(0)
        .astype(int)
    )

    campaign_analysis["cost_per_lead"] = (
        campaign_analysis["budget"]
        / campaign_analysis["lead_count"]
    )

    campaign_analysis["cost_per_lead"] = (
        campaign_analysis["cost_per_lead"]
        .replace(
            [float("inf"), -float("inf")],
            pd.NA
        )
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
                "lead_count",
                "unique_customers",
                "cost_per_lead"
            ]
        ],
        width="stretch",
        hide_index=True
    )


# ============================================================
# TAB 3 — REVENUE & RENTALS
# ============================================================

with tab_revenue:

    st.subheader("Revenue & Rental Analysis")

    # --------------------------------------------------------
    # Revenue Trend
    # --------------------------------------------------------

    revenue_monthly = (
        paid_payments
        .groupby(
            paid_payments["payment_date"].dt.to_period("M")
        )["amount"]
        .sum()
        .reset_index()
    )

    revenue_monthly["month"] = (
        revenue_monthly["payment_date"]
        .astype(str)
    )

    fig = px.line(
        revenue_monthly,
        x="month",
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
        width="stretch"
    )

    # --------------------------------------------------------
    # Rental Trend
    # --------------------------------------------------------

    rental_monthly = (
        rentals_f
        .groupby(
            rentals_f["start_date"].dt.to_period("M")
        )
        .size()
        .reset_index(name="rental_count")
    )

    rental_monthly["month"] = (
        rental_monthly["start_date"]
        .astype(str)
    )

    fig = px.bar(
        rental_monthly,
        x="month",
        y="rental_count",
        text="rental_count",
        title="Monthly Rental Volume"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Rentals"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    # --------------------------------------------------------
    # Revenue by Machine Model
    # --------------------------------------------------------

    rental_revenue = rentals_f[
        [
            "rental_id",
            "machine_id",
            "monthly_fee"
        ]
    ].merge(
        machines_f[
            [
                "machine_id",
                "model"
            ]
        ],
        on="machine_id",
        how="left"
    )

    model_revenue = (
        rental_revenue
        .groupby("model")
        .agg(
            rentals=("rental_id", "count"),
            revenue=("monthly_fee", "sum")
        )
        .reset_index()
        .sort_values(
            "revenue",
            ascending=False
        )
    )

    fig = px.bar(
        model_revenue,
        x="model",
        y="revenue",
        text="revenue",
        title="Revenue by Machine Model"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.dataframe(
        model_revenue,
        width="stretch",
        hide_index=True
    )


# ============================================================
# TAB 4 — MACHINES
# ============================================================

with tab_machine:

    st.subheader("Machine & Maintenance Analysis")

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # Machine Status
    # --------------------------------------------------------

    with col1:

        machine_status = (
            machines_f
            .groupby("status")
            .size()
            .reset_index(name="machine_count")
        )

        fig = px.bar(
            machine_status,
            x="status",
            y="machine_count",
            text="machine_count",
            title="Machine Status"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # --------------------------------------------------------
    # Maintenance Cost by Type
    # --------------------------------------------------------

    with col2:

        maintenance_type = (
            maintenance_f
            .groupby("maintenance_type")
            ["cost"]
            .sum()
            .reset_index()
            .sort_values(
                "cost",
                ascending=False
            )
        )

        fig = px.bar(
            maintenance_type,
            x="maintenance_type",
            y="cost",
            text="cost",
            title="Maintenance Cost by Type"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # --------------------------------------------------------
    # Maintenance Trend
    # --------------------------------------------------------

    maintenance_monthly = (
        maintenance_f
        .groupby(
            maintenance_f["maintenance_date"]
            .dt.to_period("M")
        )["cost"]
        .sum()
        .reset_index()
    )

    maintenance_monthly["month"] = (
        maintenance_monthly["maintenance_date"]
        .astype(str)
    )

    fig = px.line(
        maintenance_monthly,
        x="month",
        y="cost",
        markers=True,
        title="Monthly Maintenance Cost"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Maintenance Cost"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    # --------------------------------------------------------
    # Top Maintenance Cost Machines
    # --------------------------------------------------------

    machine_maintenance = (
        maintenance_f
        .groupby("machine_id")
        .agg(
            maintenance_count=(
                "maintenance_id",
                "count"
            ),
            total_cost=(
                "cost",
                "sum"
            )
        )
        .reset_index()
    )

    machine_maintenance = machine_maintenance.merge(
        machines_f[
            [
                "machine_id",
                "model",
                "status"
            ]
        ],
        on="machine_id",
        how="left"
    )

    machine_maintenance = machine_maintenance.sort_values(
        "total_cost",
        ascending=False
    )

    st.subheader("Highest Maintenance Cost Machines")

    st.dataframe(
        machine_maintenance.head(20),
        width="stretch",
        hide_index=True
    )


# ============================================================
# DATA SOURCE
# ============================================================

st.sidebar.markdown("---")

st.sidebar.caption(
    "Data Source: Google Cloud SQL / SQL Server"
)

st.sidebar.caption(
    f"Loaded: "
    f"{len(customers):,} customers · "
    f"{len(leads):,} leads · "
    f"{len(rentals):,} rentals"
)

if st.sidebar.button("🔄 Refresh Data"):

    st.cache_data.clear()
    st.rerun()
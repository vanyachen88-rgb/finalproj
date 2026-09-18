import pandas as pd

# 共用清理函式

def basic_clean(df):
    df = df.copy()

    # 欄位名稱統一
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    # 移除完全重複資料
    df = df.drop_duplicates()

    # 清理文字欄位前後空白
    text_columns = df.select_dtypes(include="object").columns

    for col in text_columns:
        df[col] = df[col].str.strip()

    return df

# Dim_Date
def transform_dim_date(df):
    df = basic_clean(df)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    return df

# Customers
def transform_customers(df):
    df = basic_clean(df)

    if "join_date" in df.columns:
        df["join_date"] = pd.to_datetime(
            df["join_date"],
            errors="coerce"
        )

    return df

# Marketing_Campaigns
def transform_marketing_campaigns(df):
    df = basic_clean(df)

    if "start_date" in df.columns:
        df["start_date"] = pd.to_datetime(
            df["start_date"],
            errors="coerce"
        )

    if "end_date" in df.columns:
        df["end_date"] = pd.to_datetime(
            df["end_date"],
            errors="coerce"
        )

    return df

# Leads
def transform_leads(df):
    df = basic_clean(df)

    if "lead_date" in df.columns:
        df["lead_date"] = pd.to_datetime(
            df["lead_date"],
            errors="coerce"
        )

    return df

# Machines
def transform_machines(df):
    df = basic_clean(df)

    if "purchase_date" in df.columns:
        df["purchase_date"] = pd.to_datetime(
            df["purchase_date"],
            errors="coerce"
        )

    return df

# Rentals
def transform_rentals(df):
    df = basic_clean(df)

    if "rental_start_date" in df.columns:
        df["rental_start_date"] = pd.to_datetime(
            df["rental_start_date"],
            errors="coerce"
        )

    if "rental_end_date" in df.columns:
        df["rental_end_date"] = pd.to_datetime(
            df["rental_end_date"],
            errors="coerce"
        )

    numeric_columns = [
        "rental_amount",
        "deposit"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    return df

# Payments
def transform_payments(df):
    df = basic_clean(df)

    if "payment_date" in df.columns:
        df["payment_date"] = pd.to_datetime(
            df["payment_date"],
            errors="coerce"
        )

    if "amount" in df.columns:
        df["amount"] = pd.to_numeric(
            df["amount"],
            errors="coerce"
        )

    return df

# Maintenance
def transform_maintenance(df):
    df = basic_clean(df)

    if "maintenance_date" in df.columns:
        df["maintenance_date"] = pd.to_datetime(
            df["maintenance_date"],
            errors="coerce"
        )

    if "maintenance_cost" in df.columns:
        df["maintenance_cost"] = pd.to_numeric(
            df["maintenance_cost"],
            errors="coerce"
        )

    return df
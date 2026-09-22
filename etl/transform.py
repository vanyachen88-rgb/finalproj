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

    if "full_date" in df.columns:
        df["full_date"] = pd.to_datetime(
            df["full_date"],
            errors="coerce"
        )

    return df

# Customers
def transform_customers(df):
    df = basic_clean(df)

    if "register_date" in df.columns:
        df["register_date"] = pd.to_datetime(
            df["register_date"],
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

    if "monthly_fee" in df.columns:
        df["monthly_fee"] = pd.to_numeric(
            df["monthly_fee"],
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

    if "cost" in df.columns:
        df["cost"] = pd.to_numeric(
            df["cost"],
            errors="coerce"
        )

    return df
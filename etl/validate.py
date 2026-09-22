import pandas as pd
# 1. 基本資料品質檢查

def check_basic_quality(df, table_name):
    """
    檢查：
    - 資料筆數
    - 完全重複資料
    - NULL
    """
    print(f"\n{'=' * 60}")
    print(f"資料表：{table_name}")
    print(f"{'=' * 60}")

    # 資料筆數
    print(f"資料筆數：{len(df):,}")

    # 完全重複
    duplicate_count = df.duplicated().sum()

    if duplicate_count == 0:
        print("PASS - 無完全重複資料")
    else:
        print(f"WARNING - 發現 {duplicate_count:,} 筆完全重複資料")

    # NULL
    null_count = df.isnull().sum()
    null_count = null_count[null_count > 0]

    if len(null_count) == 0:
        print("PASS - 無 NULL")
    else:
        print("WARNING - 發現 NULL：")

        for column, count in null_count.items():
            print(f"  {column}: {count:,}")

# 2. PK 唯一性檢查

def check_primary_key(df, table_name, pk_column):

    if pk_column not in df.columns:
        print(
            f"ERROR - {table_name} 找不到 PK 欄位：{pk_column}"
        )
        return

    # NULL PK
    null_count = df[pk_column].isnull().sum()

    if null_count == 0:
        print(
            f"PASS - {table_name}.{pk_column} 無 NULL"
        )
    else:
        print(
            f"ERROR - {table_name}.{pk_column} "
            f"有 {null_count:,} 筆 NULL"
        )

    # 重複 PK
    duplicate_count = df[pk_column].duplicated().sum()

    if duplicate_count == 0:
        print(
            f"PASS - {table_name}.{pk_column} 唯一"
        )
    else:
        print(
            f"ERROR - {table_name}.{pk_column} "
            f"有 {duplicate_count:,} 筆重複"
        )

# 3. FK 檢查

def check_foreign_key(
    child_df,
    child_table,
    child_column,
    parent_df,
    parent_table,
    parent_column
):
    """
    確認 Child Table 的 FK
    是否都能在 Parent Table 找到。
    """

    if child_column not in child_df.columns:
        print(
            f"ERROR - {child_table} 找不到欄位：{child_column}"
        )
        return

    if parent_column not in parent_df.columns:
        print(
            f"ERROR - {parent_table} 找不到欄位：{parent_column}"
        )
        return

    # 排除 NULL
    child_values = child_df[
        child_df[child_column].notna()
    ][child_column]

    invalid = ~child_values.isin(
        parent_df[parent_column]
    )

    invalid_count = invalid.sum()

    if invalid_count == 0:
        print(
            f"PASS - {child_table}.{child_column} "
            f"→ {parent_table}.{parent_column}"
        )
    else:
        print(
            f"ERROR - {child_table}.{child_column} "
            f"有 {invalid_count:,} 筆找不到對應的 "
            f"{parent_table}.{parent_column}"
        )

# 4. 日期邏輯檢查

def check_date_order(
    df,
    table_name,
    start_column,
    end_column
):
    """
    檢查開始日期是否晚於結束日期。
    """

    if start_column not in df.columns:
        return

    if end_column not in df.columns:
        return

    invalid = (
        df[start_column].notna()
        & df[end_column].notna()
        & (df[start_column] > df[end_column])
    )

    invalid_count = invalid.sum()

    if invalid_count == 0:
        print(
            f"PASS - {table_name} 日期邏輯正常"
        )
    else:
        print(
            f"ERROR - {table_name} 有 "
            f"{invalid_count:,} 筆開始日期晚於結束日期"
        )

# 5. 負數檢查

def check_non_negative(
    df,
    table_name,
    column
):
    """
    檢查金額、成本等欄位是否出現負數。
    """

    if column not in df.columns:
        return

    invalid = df[column].notna() & (df[column] < 0)

    invalid_count = invalid.sum()

    if invalid_count == 0:
        print(
            f"PASS - {table_name}.{column} 無負數"
        )
    else:
        print(
            f"ERROR - {table_name}.{column} "
            f"有 {invalid_count:,} 筆負數"
        )

# 6. 數值欄位檢查

def check_numeric_column(
    df,
    table_name,
    column
):
    """
    確認指定欄位是否可以正常作為數值使用。
    """

    if column not in df.columns:
        return

    converted = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    invalid_count = (
        df[column].notna()
        & converted.isna()
    ).sum()

    if invalid_count == 0:
        print(
            f"PASS - {table_name}.{column} 數值格式正常"
        )
    else:
        print(
            f"ERROR - {table_name}.{column} "
            f"有 {invalid_count:,} 筆非數值資料"
        )

# 7. 8 張資料表完整 Validation

def validate_all(data):

    print("\n")
    print("#" * 60)
    print("# DATA VALIDATION")
    print("#" * 60)

    # 基本品質

    for table_name, df in data.items():

        check_basic_quality(
            df,
            table_name
        )

    # PK

    check_primary_key(
        data["Dim_Date"],
        "Dim_Date",
        "date_id"
    )

    check_primary_key(
        data["Customers"],
        "Customers",
        "customer_id"
    )

    check_primary_key(
        data["Marketing_Campaigns"],
        "Marketing_Campaigns",
        "campaign_id"
    )

    check_primary_key(
        data["Leads"],
        "Leads",
        "lead_id"
    )

    check_primary_key(
        data["Machines"],
        "Machines",
        "machine_id"
    )

    check_primary_key(
        data["Rentals"],
        "Rentals",
        "rental_id"
    )

    check_primary_key(
        data["Payments"],
        "Payments",
        "payment_id"
    )

    check_primary_key(
        data["Maintenance"],
        "Maintenance",
        "maintenance_id"
    )

    # FK

    # Leads → Customers
    check_foreign_key(
        data["Leads"],
        "Leads",
        "customer_id",
        data["Customers"],
        "Customers",
        "customer_id"
    )

    # Leads → Marketing_Campaigns
    check_foreign_key(
        data["Leads"],
        "Leads",
        "campaign_id",
        data["Marketing_Campaigns"],
        "Marketing_Campaigns",
        "campaign_id"
    )

    # Rentals → Customers
    check_foreign_key(
        data["Rentals"],
        "Rentals",
        "customer_id",
        data["Customers"],
        "Customers",
        "customer_id"
    )

    # Rentals → Machines
    check_foreign_key(
        data["Rentals"],
        "Rentals",
        "machine_id",
        data["Machines"],
        "Machines",
        "machine_id"
    )


    # Payments → Rentals
    check_foreign_key(
        data["Payments"],
        "Payments",
        "rental_id",
        data["Rentals"],
        "Rentals",
        "rental_id"
    )

    # Maintenance → Machines
    check_foreign_key(
        data["Maintenance"],
        "Maintenance",
        "machine_id",
        data["Machines"],
        "Machines",
        "machine_id"
    )

    # -----------------------------------------------------
    # 日期邏輯
    # -----------------------------------------------------

    check_date_order(
        data["Marketing_Campaigns"],
        "Marketing_Campaigns",
        "start_date",
        "end_date"
    )

    check_date_order(
        data["Rentals"],
        "Rentals",
        "start_date",
        "end_date"
    )

    # -----------------------------------------------------
    # 金額 / 成本
    # -----------------------------------------------------

    check_non_negative(
        data["Rentals"],
        "Rentals",
        "monthly_fee"
    )

    check_non_negative(
        data["Rentals"],
        "Rentals",
        "monthly_fee"
    )

    check_non_negative(
        data["Payments"],
        "Payments",
        "amount"
    )

    check_non_negative(
        data["Maintenance"],
        "Maintenance",
        "cost"
    )

    # -----------------------------------------------------
    # 數值格式
    # -----------------------------------------------------

    check_numeric_column(
        data["Rentals"],
        "Rentals",
        "monthly_fee"
    )

    check_numeric_column(
        data["Rentals"],
        "Rentals",
        "deposit"
    )

    check_numeric_column(
        data["Payments"],
        "Payments",
        "amount"
    )

    check_numeric_column(
        data["Maintenance"],
        "Maintenance",
        "cost"
    )

    print("\n")
    print("#" * 60)
    print("# VALIDATION COMPLETED")
    print("#" * 60)
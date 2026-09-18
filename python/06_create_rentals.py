import pandas as pd
import numpy as np

# 1. 設定
np.random.seed(42)
num_rentals = 3500

# 2. 讀取既有資料
# ========================================

customers = pd.read_csv(
    "C:/Project/finalproj/data/customers.csv"
)

machines = pd.read_csv(
    "C:/Project/finalproj/data/machines.csv"
)

customers["register_date"] = pd.to_datetime(
    customers["register_date"]
)

machines["purchase_date"] = pd.to_datetime(
    machines["purchase_date"]
)


# 3. 建立可租賃設備
# ========================================

available_machines = machines[
    machines["status"] != "Retired"
].copy()

# 4. 建立 Rental ID
# ========================================

rental_id = np.arange(
    1,
    num_rentals + 1
)


# 5. 選擇 Customer
# ========================================

selected_customers = np.random.choice(
    customers["customer_id"],
    size=num_rentals
)

# 6. 選擇 Machine
# ========================================

selected_machines = np.random.choice(
    available_machines["machine_id"],
    size=num_rentals
)


# 7. 取得 Customer 註冊日期
# ========================================

customer_register_dates = (
    customers
    .set_index("customer_id")
    .loc[
        selected_customers,
        "register_date"
    ]
    .reset_index(drop=True)
)

# 8. 取得 Machine 購買日期
# ========================================

machine_purchase_dates = (
    machines
    .set_index("machine_id")
    .loc[
        selected_machines,
        "purchase_date"
    ]
    .reset_index(drop=True)
)


# 9. 建立租賃開始日期
# ========================================

# 租賃開始日必須晚於：Customer 註冊日、Machine 購買日

minimum_start_date = pd.concat(
    [
        customer_register_dates,
        machine_purchase_dates
    ],
    axis=1
).max(axis=1)


# 租賃資料期間
latest_rental_start = pd.Timestamp(
    "2026-10-31"
)

valid_start_days = (
    latest_rental_start - minimum_start_date
).dt.days.clip(lower=0)


random_days = np.array([
    np.random.randint(0, days + 1)
    for days in valid_start_days
])


start_dates = (
    minimum_start_date
    + pd.to_timedelta(
        random_days,
        unit="D"
    )
)


# 10. 租賃期間
# ========================================

rental_months = np.random.choice(
    [1, 2, 3, 6, 12, 18, 24],
    size=num_rentals,
    p=[
        0.18,
        0.15,
        0.18,
        0.22,
        0.15,
        0.08,
        0.04
    ]
)


# 11. End Date
# ========================================

end_dates = []

for start, months in zip(
    start_dates,
    rental_months
):

    end_date = (
        start
        + pd.DateOffset(
            months=int(months)
        )
    )

    end_dates.append(end_date)

end_dates = pd.to_datetime(end_dates)

# 12. Monthly Fee
# ========================================

machine_models = (
    machines
    .set_index("machine_id")
    .loc[
        selected_machines,
        "model"
    ]
    .reset_index(drop=True)
)

monthly_fee_range = {
    "OxygenPro OX-5": (2500, 3800),
    "OxygenPro OX-10": (3500, 5000),
    "CareAir CA-5": (2300, 3500),
    "CareAir CA-10": (3200, 4800),
    "HomeCare HC-5": (2000, 3200)
}

monthly_fee = []

for machine_model in machine_models:

    min_fee, max_fee = monthly_fee_range[
        machine_model
    ]

    fee = np.random.randint(
        min_fee,
        max_fee + 1
    )

    monthly_fee.append(fee)

# 13. Rental Status
# ========================================

today = pd.Timestamp("2026-12-31")

rental_status = []

for end_date in end_dates:

    if end_date > today:

        status = "Active"

    else:

        status = np.random.choice(
            [
                "Completed",
                "Cancelled"
            ],
            p=[
                0.92,
                0.08
            ]
        )

    rental_status.append(status)


# 14. 建立 DataFrame
# ========================================

df_rentals = pd.DataFrame({
    "rental_id": rental_id,
    "customer_id": selected_customers,
    "machine_id": selected_machines,
    "start_date": start_dates,
    "end_date": end_dates,
    "monthly_fee": monthly_fee,
    "status": rental_status
})


# 15. 日期格式
# ========================================

df_rentals["start_date"] = (
    df_rentals["start_date"]
    .dt.strftime("%Y-%m-%d")
)

df_rentals["end_date"] = (
    df_rentals["end_date"]
    .dt.strftime("%Y-%m-%d")
)


# 16. 排序
# ========================================
df_rentals = df_rentals.sort_values(
    "start_date"
).reset_index(drop=True)

# 17. 資料品質檢查
# ========================================

print("========== 前 10 筆 ==========")
print(df_rentals.head(10))

print("\n========== 資料筆數 ==========")
print(len(df_rentals))

print("\n========== PK 檢查 ==========")
print(
    "rental_id 是否有重複：",
    df_rentals["rental_id"].duplicated().any()
)

print("\n========== 缺失值 ==========")
print(df_rentals.isnull().sum())

print("\n========== Rental Status ==========")
print(
    df_rentals["status"].value_counts()
)

print("\n========== Rental Months ==========")
print(
    rental_months
)

print("\n========== Monthly Fee 統計 ==========")
print(
    df_rentals["monthly_fee"].describe()
)

# 18. FK 檢查
# ========================================

print("\n========== Customer FK 檢查 ==========")

invalid_customers = ~df_rentals[
    "customer_id"
].isin(
    customers["customer_id"]
)

print(
    "不存在的 customer_id：",
    invalid_customers.sum()
)


print("\n========== Machine FK 檢查 ==========")

invalid_machines = ~df_rentals[
    "machine_id"
].isin(
    machines["machine_id"]
)

print(
    "不存在的 machine_id：",
    invalid_machines.sum()
)


# ========================================
# 19. 日期邏輯檢查
# ========================================

print("\n========== 日期邏輯檢查 ==========")

start_check = pd.to_datetime(
    df_rentals["start_date"]
)

end_check = pd.to_datetime(
    df_rentals["end_date"]
)

print(
    "end_date < start_date：",
    (end_check < start_check).sum()
)


# ========================================
# 20. 輸出 CSV
# ========================================

df_rentals.to_csv(
    "C:/Project/finalproj/data/rentals.csv",
    index=False,
    encoding="utf-8-sig"
)

print(
    "\n資料已輸出至："
    "../data/rentals.csv"
)
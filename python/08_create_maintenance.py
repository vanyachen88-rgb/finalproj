import pandas as pd
import numpy as np


# 1. 設定
# ========================================

np.random.seed(42)

num_maintenance = 2500

data_end_date = pd.Timestamp("2026-12-31")


# 2. 讀取 Machines
# ========================================

machines = pd.read_csv(
    "C:/Project/finalproj/data/raw/machines.csv"
)

machines["purchase_date"] = pd.to_datetime(
    machines["purchase_date"]
)


# ========================================
# 3. 選擇 Machine
# ========================================

# 使用設備年齡與狀態增加維修機率
machine_weights = []

for _, machine in machines.iterrows():

    age_days = (
        data_end_date
        - machine["purchase_date"]
    ).days

    age_years = max(
        age_days / 365,
        0
    )

    weight = 1 + age_years * 0.35

    if machine["status"] == "Maintenance":
        weight *= 2.5

    elif machine["status"] == "Retired":
        weight *= 1.2

    machine_weights.append(weight)


machine_weights = np.array(
    machine_weights
)

machine_weights = (
    machine_weights
    / machine_weights.sum()
)


selected_machines = np.random.choice(
    machines["machine_id"],
    size=num_maintenance,
    p=machine_weights
)


# ========================================
# 4. 取得 Machine Purchase Date
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


# ========================================
# 5. Maintenance Date
# ========================================

maintenance_dates = []

for purchase_date in machine_purchase_dates:

    days_available = (
        data_end_date
        - purchase_date
    ).days

    if days_available <= 0:

        maintenance_date = purchase_date

    else:

        random_day = np.random.randint(
            0,
            days_available + 1
        )

        maintenance_date = (
            purchase_date
            + pd.Timedelta(
                days=int(random_day)
            )
        )

    maintenance_dates.append(
        maintenance_date
    )


# ========================================
# 6. Maintenance Type
# ========================================

maintenance_types = [
    "定期保養",
    "故障維修",
    "零件更換",
    "清潔消毒",
    "性能檢測"
]

maintenance_type = np.random.choice(
    maintenance_types,
    size=num_maintenance,
    p=[
        0.35,
        0.25,
        0.18,
        0.12,
        0.10
    ]
)


# ========================================
# 7. Maintenance Cost
# ========================================

maintenance_cost_range = {
    "定期保養": (500, 1800),
    "故障維修": (1500, 6000),
    "零件更換": (2000, 8000),
    "清潔消毒": (300, 1200),
    "性能檢測": (400, 1500)
}

maintenance_cost = []

for maintenance in maintenance_type:

    min_cost, max_cost = (
        maintenance_cost_range[
            maintenance
        ]
    )

    cost = np.random.randint(
        min_cost,
        max_cost + 1
    )

    maintenance_cost.append(cost)


# ========================================
# 8. Maintenance ID
# ========================================

maintenance_id = np.arange(
    1,
    num_maintenance + 1
)


# ========================================
# 9. 建立 DataFrame
# ========================================

df_maintenance = pd.DataFrame({
    "maintenance_id": maintenance_id,
    "machine_id": selected_machines,
    "maintenance_date": maintenance_dates,
    "maintenance_type": maintenance_type,
    "cost": maintenance_cost
})


# ========================================
# 10. 日期格式
# ========================================

df_maintenance["maintenance_date"] = (
    df_maintenance["maintenance_date"]
    .dt.strftime("%Y-%m-%d")
)


# ========================================
# 11. 排序
# ========================================

df_maintenance = df_maintenance.sort_values(
    "maintenance_date"
).reset_index(drop=True)


# ========================================
# 12. 資料品質檢查
# ========================================

print("========== 前 10 筆 ==========")
print(df_maintenance.head(10))

print("\n========== 資料筆數 ==========")
print(len(df_maintenance))

print("\n========== PK 檢查 ==========")
print(
    "maintenance_id 是否有重複：",
    df_maintenance[
        "maintenance_id"
    ].duplicated().any()
)

print("\n========== 缺失值 ==========")
print(
    df_maintenance.isnull().sum()
)

print("\n========== Maintenance Type ==========")
print(
    df_maintenance[
        "maintenance_type"
    ].value_counts()
)

print("\n========== Maintenance Cost 統計 ==========")
print(
    df_maintenance["cost"].describe()
)


# ========================================
# 13. FK 檢查
# ========================================

print("\n========== Machine FK 檢查 ==========")

invalid_machines = ~df_maintenance[
    "machine_id"
].isin(
    machines["machine_id"]
)

print(
    "不存在的 machine_id：",
    invalid_machines.sum()
)


# ========================================
# 14. 日期邏輯檢查
# ========================================

print("\n========== Maintenance Date 檢查 ==========")

maintenance_dates_check = pd.to_datetime(
    df_maintenance["maintenance_date"]
)

purchase_dates_check = (
    machines
    .set_index("machine_id")
    .loc[
        df_maintenance["machine_id"],
        "purchase_date"
    ]
    .reset_index(drop=True)
)

print(
    "維修日期早於設備購買日期：",
    (
        maintenance_dates_check.values
        < purchase_dates_check.values
    ).sum()
)

print(
    "是否超過資料截止日：",
    (
        maintenance_dates_check
        > data_end_date
    ).sum()
)


# ========================================
# 15. 輸出 CSV
# ========================================

df_maintenance.to_csv(
    "C:/Project/finalproj/data/raw/maintenance.csv",
    index=False,
    encoding="utf-8-sig"
)

print(
    "\n資料已輸出至："
    "../data/maintenance.csv"
)
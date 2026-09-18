import pandas as pd
import numpy as np


# 1. 設定
np.random.seed(42)
num_machines = 400

start_date = pd.Timestamp("2022-01-01")
end_date = pd.Timestamp("2026-12-31")

# 2. Machine ID
# ========================================

machine_id = np.arange(
    1,
    num_machines + 1
)

# 3. Machine Model
# ========================================

models = [
    "OxygenPro OX-5",
    "OxygenPro OX-10",
    "CareAir CA-5",
    "CareAir CA-10",
    "HomeCare HC-5"
]

model = np.random.choice(
    models,
    size=num_machines,
    p=[
        0.25,
        0.20,
        0.20,
        0.15,
        0.20
    ]
)

# 4. Purchase Date
# ========================================

purchase_date = pd.to_datetime(
    np.random.choice(
        pd.date_range(
            start=start_date,
            end=end_date,
            freq="D"
        ),
        size=num_machines
    )
)


# 5. Purchase Cost
# ========================================

purchase_cost_range = {
    "OxygenPro OX-5": (18000, 28000),
    "OxygenPro OX-10": (28000, 42000),
    "CareAir CA-5": (16000, 26000),
    "CareAir CA-10": (25000, 38000),
    "HomeCare HC-5": (14000, 23000)
}

purchase_cost = []

for machine_model in model:

    min_cost, max_cost = purchase_cost_range[
        machine_model
    ]

    cost = np.random.randint(
        min_cost,
        max_cost + 1
    )

    purchase_cost.append(cost)


# 6. Machine Status
# ========================================

machine_status = []

for purchase in purchase_date:

    # 新購設備較可能為可用狀態
    status = np.random.choice(
        [
            "Available",
            "Rented",
            "Maintenance",
            "Retired"
        ],
        p=[
            0.35,
            0.40,
            0.15,
            0.10
        ]
    )

    # 2023 年以前購買的設備
    # 比較有可能進入維修或報廢
    if purchase.year <= 2023:

        status = np.random.choice(
            [
                "Available",
                "Rented",
                "Maintenance",
                "Retired"
            ],
            p=[
                0.25,
                0.35,
                0.20,
                0.20
            ]
        )

    machine_status.append(status)


# 7. 建立 DataFrame
# ========================================

df_machines = pd.DataFrame({
    "machine_id": machine_id,
    "model": model,
    "purchase_date": purchase_date,
    "purchase_cost": purchase_cost,
    "status": machine_status
})

# 8. 日期格式
# ========================================

df_machines["purchase_date"] = (
    df_machines["purchase_date"]
    .dt.strftime("%Y-%m-%d")
)


# 9. 排序
# ========================================

df_machines = df_machines.sort_values(
    "machine_id"
).reset_index(drop=True)


# 10. 資料品質檢查
# ========================================

print("========== 前 10 筆 ==========")
print(df_machines.head(10))

print("\n========== 資料筆數 ==========")
print(len(df_machines))

print("\n========== PK 檢查 ==========")
print(
    "machine_id 是否有重複：",
    df_machines["machine_id"].duplicated().any()
)

print("\n========== 缺失值 ==========")
print(df_machines.isnull().sum())

print("\n========== Model 分布 ==========")
print(
    df_machines["model"].value_counts()
)

print("\n========== Machine Status ==========")
print(
    df_machines["status"].value_counts()
)

print("\n========== Purchase Cost 統計 ==========")
print(
    df_machines["purchase_cost"].describe()
)

# 11. 輸出 CSV
# ========================================

df_machines.to_csv(
    "C:/Project/finalproj/data/machines.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\n資料已輸出至：../data/machines.csv")
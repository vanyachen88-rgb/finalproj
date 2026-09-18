import pandas as pd
import numpy as np


# ========================================
# 1. 設定隨機種子
# ========================================

np.random.seed(42)


# ========================================
# 2. 基本設定
# ========================================

num_customers = 4000

start_date = "2024-01-01"
end_date = "2026-12-31"


# ========================================
# 3. Customer ID
# ========================================

customer_id = np.arange(1, num_customers + 1)


# ========================================
# 4. Gender
# ========================================

gender = np.random.choice(
    ["M", "F"],
    size=num_customers,
    p=[0.45, 0.55]
)


# ========================================
# 5. Age
# ========================================

# 使用常態分布，讓年齡主要集中在 35～65 歲
age = np.random.normal(
    loc=52,
    scale=13,
    size=num_customers
)

age = np.clip(age, 18, 85).round().astype(int)


# ========================================
# 6. City
# ========================================

cities = [
    "台中市",
    "台北市",
    "新北市",
    "高雄市",
    "桃園市",
    "台南市",
    "彰化縣",
    "新竹市"
]

city = np.random.choice(
    cities,
    size=num_customers,
    p=[
        0.30,  # 台中
        0.15,  # 台北
        0.15,  # 新北
        0.12,  # 高雄
        0.10,  # 桃園
        0.08,  # 台南
        0.06,  # 彰化
        0.04   # 新竹
    ]
)


# ========================================
# 7. Register Date
# ========================================

register_date = pd.to_datetime(
    np.random.choice(
        pd.date_range(
            start=start_date,
            end=end_date,
            freq="D"
        ),
        size=num_customers
    )
)


# ========================================
# 8. Acquisition Channel
# ========================================

channels = [
    "Google Ads",
    "Facebook Ads",
    "LINE",
    "官網",
    "電話",
    "Referral",
    "合作通路"
]

acquisition_channel = np.random.choice(
    channels,
    size=num_customers,
    p=[
        0.22,  # Google Ads
        0.18,  # Facebook Ads
        0.16,  # LINE
        0.15,  # 官網
        0.12,  # 電話
        0.10,  # Referral
        0.07   # 合作通路
    ]
)


# ========================================
# 9. 建立 DataFrame
# ========================================

df_customers = pd.DataFrame({
    "customer_id": customer_id,
    "gender": gender,
    "age": age,
    "city": city,
    "register_date": register_date,
    "acquisition_channel": acquisition_channel
})


# ========================================
# 10. 排序
# ========================================

df_customers = df_customers.sort_values(
    "customer_id"
).reset_index(drop=True)


# ========================================
# 11. 資料品質檢查
# ========================================

print("========== 前 10 筆 ==========")
print(df_customers.head(10))

print("\n========== 資料筆數 ==========")
print(len(df_customers))

print("\n========== PK 檢查 ==========")
print(
    "customer_id 是否有重複：",
    df_customers["customer_id"].duplicated().any()
)

print("\n========== 缺失值檢查 ==========")
print(df_customers.isnull().sum())

print("\n========== 性別分布 ==========")
print(df_customers["gender"].value_counts())

print("\n========== 城市分布 ==========")
print(df_customers["city"].value_counts())

print("\n========== 獲客渠道分布 ==========")
print(df_customers["acquisition_channel"].value_counts())

print("\n========== 年齡統計 ==========")
print(df_customers["age"].describe())


# ========================================
# 12. 輸出 CSV
# ========================================

df_customers.to_csv(
    "C:/Project/finalproj/data/customers.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\n資料已輸出至： ..data/customers.csv")
import pandas as pd
import numpy as np

# 1. 設定隨機種子
# ========================================

np.random.seed(42)

# 2. 基本設定
# ========================================

num_campaigns = 40
start_date = pd.Timestamp("2024-01-01")
end_date = pd.Timestamp("2026-12-31")


# 3. Campaign ID
# ========================================

campaign_id = np.arange(1, num_campaigns + 1)


# 4. Marketing Channel
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

channel = np.random.choice(
    channels,
    size=num_campaigns,
    p=[
        0.25,  # Google Ads
        0.20,  # Facebook Ads
        0.15,  # LINE
        0.15,  # 官網
        0.10,  # 電話
        0.08,  # Referral
        0.07   # 合作通路
    ]
)


# 5. Campaign Name
# ========================================

campaign_themes = [
    "春季推廣",
    "夏季推廣",
    "秋季推廣",
    "冬季推廣",
    "品牌曝光",
    "新客優惠",
    "居家照護",
    "長期租賃"
]

campaign_name = []

for i in range(num_campaigns):

    theme = np.random.choice(campaign_themes)

    campaign_name.append(
        f"{theme}_{i + 1:02d}"
    )


# 6. Start Date
# ========================================

# 最晚讓活動有足夠時間完成
latest_start_date = pd.Timestamp("2026-10-01")

start_dates = pd.to_datetime(
    np.random.choice(
        pd.date_range(
            start=start_date,
            end=latest_start_date,
            freq="D"
        ),
        size=num_campaigns
    )
)

# 7. End Date
# ========================================

# 每個活動持續 14～60 天
campaign_days = np.random.randint(
    14,
    61,
    size=num_campaigns
)

end_dates = (
    start_dates
    + pd.to_timedelta(
        campaign_days,
        unit="D"
    )
)

# 確保不超過資料期間
end_dates = pd.Series(end_dates).clip(
    upper=end_date
)

# 8. Campaign Budget
# ========================================

budget_ranges = {
    "Google Ads": (10000, 30000),
    "Facebook Ads": (10000, 50000),
    "LINE": (40000, 180000),
    "官網": (30000, 120000),
    "電話": (30000, 100000),
    "Referral": (20000, 80000),
    "合作通路": (30000, 150000)
}


budget = []

for ch in channel:

    min_budget, max_budget = budget_ranges[ch]

    amount = np.random.randint(
        min_budget,
        max_budget + 1
    )

    budget.append(amount)


# 9. 建立 DataFrame
# ========================================

df_campaigns = pd.DataFrame({
    "campaign_id": campaign_id,
    "campaign_name": campaign_name,
    "channel": channel,
    "start_date": start_dates,
    "end_date": end_dates,
    "budget": budget
})


# ========================================
# 10. 日期格式
# ========================================

df_campaigns["start_date"] = (
    df_campaigns["start_date"]
    .dt.strftime("%Y-%m-%d")
)

df_campaigns["end_date"] = (
    df_campaigns["end_date"]
    .dt.strftime("%Y-%m-%d")
)


# 11. 排序
# ========================================

df_campaigns = df_campaigns.sort_values(
    "start_date"
).reset_index(drop=True)


# 12. 資料品質檢查
# ========================================

print("========== 前 10 筆 ==========")
print(df_campaigns.head(10))

print("\n========== 資料筆數 ==========")
print(len(df_campaigns))

print("\n========== PK 檢查 ==========")
print(
    "campaign_id 是否有重複：",
    df_campaigns["campaign_id"].duplicated().any())

print("\n========== 缺失值 ==========")
print(df_campaigns.isnull().sum())

print("\n========== Channel 分布 ==========")
print(df_campaigns["channel"].value_counts())

print("\n========== Budget 統計 ==========")
print(df_campaigns["budget"].describe())

print("\n========== 日期檢查 ==========")

start_check = pd.to_datetime(
    df_campaigns["start_date"]
)

end_check = pd.to_datetime(
    df_campaigns["end_date"]
)

print(
    "是否存在 end_date < start_date：",
    (end_check < start_check).any()
)

# 13. 輸出 CSV
# ========================================

df_campaigns.to_csv(
    "C:/Project/finalproj/data/marketing_campaigns.csv",
    index=False,
    encoding="utf-8-sig"
)

print(
    "\n資料已輸出至："
    "../data/marketing_campaigns.csv"
)
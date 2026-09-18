import pandas as pd
import numpy as np


# 1. 設定
np.random.seed(42)
num_leads = 12000

# 2. 讀取既有資料
# ========================================
customers = pd.read_csv(
    "C:/Project/finalproj/data/customers.csv"
)

campaigns = pd.read_csv(
    "C:/Project/finalproj/data/marketing_campaigns.csv"
)

customers["register_date"] = pd.to_datetime(
    customers["register_date"]
)

campaigns["start_date"] = pd.to_datetime(
    campaigns["start_date"]
)

campaigns["end_date"] = pd.to_datetime(
    campaigns["end_date"]
)

# 3. 建立 Campaign 權重
# ========================================

channel_lead_weight = {
    "Google Ads": 0.24,
    "Facebook Ads": 0.20,
    "LINE": 0.16,
    "官網": 0.14,
    "電話": 0.10,
    "Referral": 0.09,
    "合作通路": 0.07
}

campaign_weights = (
    campaigns["channel"]
    .map(channel_lead_weight)
)

campaign_weights = (
    campaign_weights / campaign_weights.sum()
)


# 4. 產生 campaign_id
# ========================================

selected_campaigns = np.random.choice(
    campaigns["campaign_id"],
    size=num_leads,
    p=campaign_weights
)


# 5. 取得 Campaign 資訊
# ========================================

lead_campaigns = campaigns.set_index(
    "campaign_id"
).loc[
    selected_campaigns
].reset_index()

# 6. 產生 Customer
# ========================================

selected_customers = np.random.choice(
    customers["customer_id"],
    size=num_leads
)

# 7. 建立 Lead Date
# ========================================

campaign_start = lead_campaigns[
    "start_date"
].reset_index(drop=True)

campaign_end = lead_campaigns[
    "end_date"
].reset_index(drop=True)

customer_register = customers.set_index(
    "customer_id"
).loc[
    selected_customers,
    "register_date"
].reset_index(drop=True)


# Lead 日期不能早於：
# 1. Campaign 開始日
# 2. Customer 註冊日

valid_start = pd.concat(
    [
        campaign_start,
        customer_register
    ],
    axis=1
).max(axis=1)


# 確保 Lead Date 不超過 Campaign End Date
valid_days = (
    campaign_end - valid_start
).dt.days


# 若註冊日晚於活動結束日，將日期調整到活動結束日前
valid_days = valid_days.clip(
    lower=0
)

random_days = np.array([
    np.random.randint(0, days + 1)
    for days in valid_days
])

lead_date = (
    valid_start
    + pd.to_timedelta(
        random_days,
        unit="D"
    )
)

# 8. Lead Channel
# ========================================

lead_channel = lead_campaigns[
    "channel"
].values

# 9. Lead Status
# ========================================

# 不同渠道設定不同轉換狀態分布
status_options = [
    "New",
    "Contacted",
    "Qualified",
    "Converted",
    "Lost"
]

status_probabilities = {
    "Google Ads":   [0.20, 0.25, 0.20, 0.20, 0.15],
    "Facebook Ads": [0.22, 0.27, 0.18, 0.15, 0.18],
    "LINE":         [0.15, 0.22, 0.22, 0.25, 0.16],
    "官網":          [0.18, 0.22, 0.22, 0.25, 0.13],
    "電話":          [0.12, 0.23, 0.25, 0.27, 0.13],
    "Referral":     [0.10, 0.18, 0.25, 0.35, 0.12],
    "合作通路":       [0.12, 0.20, 0.24, 0.30, 0.14]
}


lead_status = []

for ch in lead_channel:

    status = np.random.choice(
        status_options,
        p=status_probabilities[ch]
    )

    lead_status.append(status)

# 10. Lead ID
# ========================================

lead_id = np.arange(
    1,
    num_leads + 1
)

# 11. 建立 DataFrame
# ========================================

df_leads = pd.DataFrame({
    "lead_id": lead_id,
    "customer_id": selected_customers,
    "campaign_id": selected_campaigns,
    "lead_date": lead_date,
    "channel": lead_channel,
    "status": lead_status
})

# 12. 日期格式
# ========================================

df_leads["lead_date"] = (
    df_leads["lead_date"]
    .dt.strftime("%Y-%m-%d")
)

# 13. 排序
# ========================================

df_leads = df_leads.sort_values(
    "lead_date"
).reset_index(drop=True)

# 14. 資料品質檢查
# ========================================

print("========== 前 10 筆 ==========")
print(df_leads.head(10))

print("\n========== 資料筆數 ==========")
print(len(df_leads))

print("\n========== PK 檢查 ==========")
print(
    "lead_id 是否有重複：",
    df_leads["lead_id"].duplicated().any()
)

print("\n========== 缺失值 ==========")
print(df_leads.isnull().sum())

print("\n========== Lead Status ==========")
print(
    df_leads["status"].value_counts()
)

print("\n========== Lead Channel ==========")
print(
    df_leads["channel"].value_counts()
)

print("\n========== Campaign FK 檢查 ==========")
print(
    "不存在的 campaign_id：",
    ~df_leads["campaign_id"].isin(
        campaigns["campaign_id"]
    ).any()
)

print("\n========== Customer FK 檢查 ==========")
print(
    "不存在的 customer_id：",
    ~df_leads["customer_id"].isin(
        customers["customer_id"]
    ).any()
)


# ========================================
# 15. 輸出 CSV
# ========================================

df_leads.to_csv(
    "C:/Project/finalproj/data/leads.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\n資料已輸出至：../data/leads.csv")
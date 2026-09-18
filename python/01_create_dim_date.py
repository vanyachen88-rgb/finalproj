import pandas as pd

# 設定資料日期範圍
start_date = "2024-01-01"
end_date = "2026-12-31"

# 建立每日日期
dates = pd.date_range(
    start=start_date,
    end=end_date,
    freq="D"
)

# 建立 DataFrame
df_date = pd.DataFrame({
    "full_date": dates
})

df_date["date_id"] = df_date["full_date"].dt.strftime("%Y%m%d").astype(int)
df_date["year"] = df_date["full_date"].dt.year
df_date["quarter"] = df_date["full_date"].dt.quarter
df_date["month"] = df_date["full_date"].dt.month
df_date["month_name"] = df_date["full_date"].dt.month_name()
df_date["week"] = df_date["full_date"].dt.isocalendar().week
df_date["day"] = df_date["full_date"].dt.day
df_date["day_of_week"] = df_date["full_date"].dt.dayofweek
df_date["day_name"] = df_date["full_date"].dt.day_name()
df_date = df_date[
    [
        "date_id",
        "full_date",
        "year",
        "quarter",
        "month",
        "month_name",
        "week",
        "day",
        "day_of_week",
        "day_name"
    ]
]

df_date.to_csv(
    "C:\\Project\\finalproj\\data\\dim_date.csv",
    index=False,
    encoding="utf-8-sig"
)

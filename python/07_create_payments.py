import pandas as pd
import numpy as np

# 1. 設定
# ========================================

np.random.seed(42)
data_end_date = pd.Timestamp("2026-12-31")

# 2. 讀取 Rentals
# ========================================

rentals = pd.read_csv(
    "C:/Project/finalproj//data/rentals.csv"
)

rentals["start_date"] = pd.to_datetime(
    rentals["start_date"]
)

rentals["end_date"] = pd.to_datetime(
    rentals["end_date"]
)

# 3. 產生付款資料
# ========================================

payment_records = []
payment_id = 1


for _, rental in rentals.iterrows():

    rental_id = rental["rental_id"]
    start_date = rental["start_date"]
    end_date = rental["end_date"]
    monthly_fee = rental["monthly_fee"]

    # 付款月份
    payment_dates = pd.date_range(
        start=start_date,
        end=min(end_date, data_end_date),
        freq="MS"
    )

    # 若開始日期不是每月 1 號，
    # 補上第一筆付款
    if len(payment_dates) == 0:

        payment_dates = pd.DatetimeIndex([
            start_date
        ])

    elif payment_dates[0] != start_date:

        payment_dates = payment_dates.insert(
            0,
            start_date
        )

    # 建立付款紀錄
    for payment_date in payment_dates:

        # 第一筆付款使用租賃開始日
        if payment_date == start_date:

            actual_payment_date = payment_date

        else:

            # 模擬正常付款日期落在應付款日前後
            payment_delay = np.random.choice(
                [-2, -1, 0, 0, 0, 1, 2, 3, 5, 7],
                p=[
                    0.03,
                    0.05,
                    0.30,
                    0.20,
                    0.15,
                    0.10,
                    0.07,
                    0.05,
                    0.03,
                    0.02
                ]
            )

            actual_payment_date = (
                payment_date
                + pd.Timedelta(
                    days=int(payment_delay)
                )
            )

        # 不超過資料截止日
        if actual_payment_date > data_end_date:
            actual_payment_date = data_end_date

        # ====================================
        # Payment Status
        # ====================================

        payment_status = np.random.choice(
            [
                "Paid",
                "Pending",
                "Overdue",
                "Failed"
            ],
            p=[
                0.82,
                0.07,
                0.08,
                0.03
            ]
        )

        # ====================================
        # Amount
        # ====================================

        amount = monthly_fee

        # ====================================
        # 建立一筆 Payment
        # ====================================

        payment_records.append({
            "payment_id": payment_id,
            "rental_id": rental_id,
            "payment_date": actual_payment_date,
            "amount": amount,
            "payment_status": payment_status
        })

        payment_id += 1


# ========================================
# 4. 建立 DataFrame
# ========================================

df_payments = pd.DataFrame(
    payment_records
)

# ========================================
# 5. 日期格式
# ========================================

df_payments["payment_date"] = (
    pd.to_datetime(
        df_payments["payment_date"]
    )
    .dt.strftime("%Y-%m-%d")
)


# ========================================
# 6. 排序
# ========================================

df_payments = df_payments.sort_values(
    [
        "rental_id",
        "payment_date"
    ]
).reset_index(drop=True)


# ========================================
# 7. 資料品質檢查
# ========================================

print("========== 前 10 筆 ==========")
print(df_payments.head(10))

print("\n========== 資料筆數 ==========")
print(len(df_payments))

print("\n========== PK 檢查 ==========")
print(
    "payment_id 是否有重複：",
    df_payments["payment_id"].duplicated().any()
)

print("\n========== 缺失值 ==========")
print(df_payments.isnull().sum())

print("\n========== Payment Status ==========")
print(
    df_payments["payment_status"].value_counts()
)

print("\n========== Amount 統計 ==========")
print(
    df_payments["amount"].describe()
)


# ========================================
# 8. FK 檢查
# ========================================

print("\n========== Rental FK 檢查 ==========")

invalid_rentals = ~df_payments[
    "rental_id"
].isin(
    rentals["rental_id"]
)

print(
    "不存在的 rental_id：",
    invalid_rentals.sum()
)


# ========================================
# 9. 日期檢查
# ========================================

print("\n========== Payment Date 檢查 ==========")

payment_dates = pd.to_datetime(
    df_payments["payment_date"]
)

print(
    "是否有超過資料截止日：",
    (payment_dates > data_end_date).sum()
)


# 10. 輸出 CSV
# ========================================

df_payments.to_csv(
    "C:/Project/finalproj/data/payments.csv",
    index=False,
    encoding="utf-8-sig"
)

print(
    "\n資料已輸出至："
    "../data/payments.csv"
)
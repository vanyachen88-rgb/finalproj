from pathlib import Path

# Clean Data 輸出位置
CLEAN_PATH = Path("C:/Project/finalproj/data/clean")

# 建立 Clean Data 資料夾
def create_clean_folder():
    CLEAN_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

# 儲存單一資料表
def save_table(df, table_clean):
    create_clean_folder()
    output_path = CLEAN_PATH / f"{table_clean}.csv"

    df.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"Saved: {output_path} "
        f"({len(df):,} rows)"
    )


# 儲存全部資料表
def load_all(data):

    create_clean_folder()

    print("\n")
    print("=" * 60)
    print("LOADING CLEAN DATA")
    print("=" * 60)

    for table_name, df in data.items():

        save_table(
            df,
            table_name
        )

    print("\n")
    print("=" * 60)
    print("LOAD COMPLETED")
    print("=" * 60)
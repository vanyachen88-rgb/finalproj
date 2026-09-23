# Rental Business Analytics & Data Engineering Project

以醫療設備租賃業務為情境建立的 End-to-End Data Engineering & Analytics 專案。

本專案從模擬業務資料開始，使用 Python 建立 ETL Pipeline，將清洗與驗證後的資料載入 Google Cloud SQL（SQL Server），再透過 SQL / Python 進行資料分析，最後使用 Streamlit 建立互動式商業分析 Dashboard。

> 本專案資料皆為模擬資料（Synthetic Data），不包含真實客戶或公司營運資料。

---

## Project Overview

本專案模擬一間醫療設備租賃公司的營運資料，整合：

- 客戶資料
- 行銷活動
- 潛在客戶（Leads）
- 設備資料
- 租賃紀錄
- 收款紀錄
- 維修紀錄
- 日期維度

主要目標是建立一套完整的資料流程：

**Data Generation → ETL → Data Validation → Cloud Database → SQL/Python Analytics → Streamlit Dashboard**

並透過 Dashboard 回答實際營運可能關注的問題，例如：

- 營收與租賃量如何變化？
- 哪些行銷渠道帶來較高的 Lead Conversion？
- 不同行銷活動的成效如何？
- 哪些設備型號貢獻較高營收？
- 設備維修成本與維修頻率如何？
- 客戶主要來自哪些 Acquisition Channels？

---

## Data Architecture

```text
Synthetic CSV Data
        │
        ▼
Python ETL Pipeline
        │
        ├── Extract
        ├── Transform
        ├── Validate
        └── Load
        │
        ▼
Google Cloud SQL
SQL Server 2022
        │
        ├── staging schema
        │
        └── production schema
        │
        ▼
SQL + Python Analytics
        │
        ▼
Streamlit Dashboard
```

---

## Tech Stack

| Category | Technology |
|---|---|
| Language | Python |
| Data Processing | Pandas, NumPy |
| ETL | Python |
| Database | Microsoft SQL Server 2022 |
| Cloud Database | Google Cloud SQL |
| Database Access | SQLAlchemy, pyodbc |
| Data Visualization | Plotly |
| Dashboard | Streamlit |
| Dependency Management | uv |
| Version Control | Git, GitHub |
| Development | VS Code |

---

## Dataset

本專案共建立 8 張主要業務資料表與 1 張日期維度表。

| Table | Rows | Description |
|---|---:|---|
| `Dim_Date` | 1,096 | 日期維度 |
| `Customers` | 4,000 | 客戶基本資料 |
| `Marketing_Campaigns` | 40 | 行銷活動 |
| `Leads` | 12,000 | 潛在客戶 / 銷售線索 |
| `Machines` | 400 | 租賃設備 |
| `Rentals` | 3,500 | 租賃紀錄 |
| `Payments` | 16,157 | 收款紀錄 |
| `Maintenance` | 2,500 | 設備維修紀錄 |

資料涵蓋期間：

**2024-01-01 ～ 2026-12-31**

---

## ETL Pipeline

ETL Pipeline 由 Python 模組化實作。

```text
etl/
├── extract.py
├── transform.py
├── validate.py
├── load.py
└── db.py
```

### Extract

從 CSV 讀取各業務資料表，建立後續 ETL 所需的 DataFrame。

### Transform

依照不同資料表執行：

- 日期格式標準化
- 欄位型態轉換
- 資料格式整理
- 資料庫欄位型態對應

### Validate

資料載入資料庫前執行品質檢查，包括：

- Duplicate validation
- NULL validation
- Data consistency checks
- Table-level validation

### Load

採用兩階段載入：

```text
CSV
 ↓
Staging Tables
 ↓
Production Tables
```

Staging tables 使用 `replace` 更新暫存資料，再透過 SQL Server Upsert / Merge 將資料寫入 Production tables。

資料庫欄位明確指定 SQL Data Type，文字欄位使用 `NVARCHAR`，確保中文資料在 SQL Server 中能正確儲存。

---

## Database Design

資料庫分為兩個 Schema：

```text
staging
production
```

### Staging Layer

用於 ETL 中間資料載入與驗證，例如：

```text
staging.stg_Customers
staging.stg_Leads
staging.stg_Rentals
staging.stg_Payments
...
```

### Production Layer

保存正式分析資料：

```text
production.Customers
production.Marketing_Campaigns
production.Leads
production.Machines
production.Rentals
production.Payments
production.Maintenance
production.Dim_Date
```

此設計將資料匯入流程與正式分析資料分離，避免直接操作 Production tables。

---

## Analytics

Python Analytics 模組：

```text
analytics/
├── db.py
├── queries.py
└── kpi.py
```

透過 SQLAlchemy 執行 SQL Query，再使用 Pandas 進行分析與 KPI 計算。

主要 KPI 包含：

| KPI | Result |
|---|---:|
| Customers | 4,000 |
| Leads | 12,000 |
| Rentals | 3,500 |
| Total Revenue | NT$ 43,647,100 |
| Avg. Monthly Rental Fee | NT$ 3,315 |
| Maintenance Cost | NT$ 6,096,754 |

---

## Lead Conversion Definition

本專案將 Lead Conversion 定義為：

> 同一個 `customer_id` 在 Lead 建立日期之後，至少產生一筆 Rental。

條件：

```text
Rental.start_date >= Lead.lead_date
```

Conversion Rate：

```text
Converted Unique Leads
──────────────────────── × 100%
Total Leads
```

藉此分析不同 Marketing Channels 與 Campaigns 的實際轉換表現。

---

## Streamlit Dashboard

Dashboard 分為四個主要分析頁面。

### Overview

提供整體營運概況：

- KPI Cards
- Revenue Trend
- Leads by Channel
- Rental Status
- Customer Acquisition

### Marketing

分析行銷與 Lead Conversion：

- Leads by Channel
- Channel Conversion Rate
- Campaign Performance
- Customer Acquisition Channel

### Revenue & Rentals

分析租賃與營收：

- Monthly Revenue Trend
- Monthly Rental Volume
- Revenue by Machine Model
- Rental Status

### Machines

分析設備營運狀況：

- Machine Status
- Maintenance Cost
- Maintenance Type
- Maintenance Trend
- Top Maintenance Machines

Dashboard 同時提供日期、Channel、Machine Model 等互動式篩選條件。

---

## Cloud Deployment

Database：

```text
Google Cloud SQL
└── SQL Server 2022
```

Dashboard：

```text
Streamlit Community Cloud
```

目前部署流程：

```text
GitHub Repository
       │
       ▼
Streamlit Community Cloud
       │
       ▼
Google Cloud SQL
       │
       ▼
SQL Server Production Data
```

Cloud SQL 使用 Public IP + Authorized Networks 控制資料庫來源連線，資料庫帳號等敏感資訊透過環境變數 / Streamlit Secrets 管理，不寫入 Git Repository。

---

## Project Structure

```text
finalproj/
│
├── app.py
├── main.py
├── pyproject.toml
├── uv.lock
│
├── etl/
│   ├── __init__.py
│   ├── db.py
│   ├── extract.py
│   ├── transform.py
│   ├── validate.py
│   └── load.py
│
├── analytics/
│   ├── __init__.py
│   ├── db.py
│   ├── queries.py
│   └── kpi.py
│
└── README.md
```

---

## Run Locally

### 1. Clone Repository

```bash
git clone https://github.com/vanyachen88-rgb/finalproj.git
cd finalproj
```

### 2. Install Dependencies

本專案使用 `uv` 管理 Python dependencies。

```bash
uv sync
```

### 3. Configure Environment Variables

建立本機 `.env`：

```env
DB_SERVER=YOUR_SERVER
DB_NAME=YOUR_DATABASE
DB_USER=YOUR_USERNAME
DB_PASSWORD=YOUR_PASSWORD
```

> `.env` 不應提交至 GitHub。

### 4. Run ETL

```bash
python main.py
```

Pipeline：

```text
[1/4] EXTRACT
[2/4] TRANSFORM
[3/4] VALIDATE
[4/4] LOAD
```

### 5. Run Dashboard

```bash
streamlit run app.py
```

---

## Key Engineering Features

本專案實作的主要 Data Engineering / Analytics 技術包括：

- End-to-End ETL Pipeline
- Modular Python Architecture
- Synthetic Business Data Generation
- Data Validation
- SQL Data Type Management
- Unicode / NVARCHAR Handling
- Staging & Production Database Architecture
- SQL Server Upsert / Merge
- Cloud SQL Deployment
- SQLAlchemy Database Integration
- SQL + Python Analytics
- Interactive Streamlit Dashboard
- Git / GitHub Version Control
- Cloud Application Deployment
- Environment Variable & Secret Management

---

## Future Improvements

後續可進一步擴充：

- Cloud SQL Python Connector / Auth Proxy
- IAM-based Cloud SQL Connection
- Automated ETL Scheduling
- Incremental Data Loading
- ETL Logging & Error Monitoring
- Data Quality Metrics
- CI/CD Pipeline
- Customer Cohort Analysis
- RFM Customer Segmentation
- Predictive Analytics / Machine Learning

---

## Author

**Vanya Chen**

GitHub: `vanyachen88-rgb`

---

## Disclaimer

This project is created for data engineering and analytics portfolio purposes.

All business data used in this repository is synthetically generated and does not represent actual customers, transactions, or company operations.
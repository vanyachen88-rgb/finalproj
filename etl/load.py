from sqlalchemy import text
from sqlalchemy import types as sql_types
from etl.db import engine


TABLE_ORDER = [
    "Dim_Date",
    "Customers",
    "Marketing_Campaigns",
    "Machines",
    "Leads",
    "Rentals",
    "Payments",
    "Maintenance"
]


STAGING_DTYPES = {

    "Dim_Date": {
        "date_id": sql_types.Integer(),
        "full_date": sql_types.Date(),
        "year": sql_types.SmallInteger(),
        "quarter": sql_types.SmallInteger(),
        "month": sql_types.SmallInteger(),
        "month_name": sql_types.NVARCHAR(20),
        "week": sql_types.SmallInteger(),
        "day": sql_types.SmallInteger(),
        "day_of_week": sql_types.SmallInteger(),
        "day_name": sql_types.NVARCHAR(20),
    },

    "Customers": {
        "customer_id": sql_types.Integer(),
        "gender": sql_types.CHAR(1),
        "age": sql_types.SmallInteger(),
        "city": sql_types.NVARCHAR(20),
        "register_date": sql_types.Date(),
        "acquisition_channel": sql_types.NVARCHAR(50),
    },

    "Marketing_Campaigns": {
        "campaign_id": sql_types.Integer(),
        "campaign_name": sql_types.NVARCHAR(100),
        "channel": sql_types.NVARCHAR(50),
        "start_date": sql_types.Date(),
        "end_date": sql_types.Date(),
        "budget": sql_types.Numeric(18, 2),
    },

    "Leads": {
        "lead_id": sql_types.Integer(),
        "customer_id": sql_types.Integer(),
        "campaign_id": sql_types.Integer(),
        "lead_date": sql_types.Date(),
        "channel": sql_types.NVARCHAR(50),
        "status": sql_types.NVARCHAR(20),
    },

    "Machines": {
        "machine_id": sql_types.Integer(),
        "model": sql_types.NVARCHAR(50),
        "purchase_date": sql_types.Date(),
        "purchase_cost": sql_types.Numeric(18, 2),
        "status": sql_types.NVARCHAR(20),
    },

    "Rentals": {
        "rental_id": sql_types.Integer(),
        "customer_id": sql_types.Integer(),
        "machine_id": sql_types.Integer(),
        "start_date": sql_types.Date(),
        "end_date": sql_types.Date(),
        "monthly_fee": sql_types.Numeric(18, 2),
        "status": sql_types.NVARCHAR(20),
    },

    "Payments": {
        "payment_id": sql_types.Integer(),
        "rental_id": sql_types.Integer(),
        "payment_date": sql_types.Date(),
        "amount": sql_types.Numeric(18, 2),
        "payment_status": sql_types.NVARCHAR(20),
    },

    "Maintenance": {
        "maintenance_id": sql_types.Integer(),
        "machine_id": sql_types.Integer(),
        "maintenance_date": sql_types.Date(),
        "maintenance_type": sql_types.NVARCHAR(20),
        "cost": sql_types.Numeric(18, 2),
    },
}
# ============================================================
# LOAD
# ============================================================
def load_all(data):

    print()
    print("=" * 60)
    print("LOAD → STAGING")
    print("=" * 60)
    # --------------------------------------------------------
    # STAGING
    # --------------------------------------------------------
for table_name in TABLE_ORDER:

    df = data[table_name]

    staging_table = f"stg_{table_name}"

    df.to_sql(
        staging_table,
        con=engine,
        schema="dbo",
        if_exists="replace",
        index=False,
        dtype=STAGING_DTYPES[table_name]
    )
    print("\n")
    print(
        f"Loaded {staging_table}: "
        f"{len(df):,} rows"
    )
    print("LOAD → STAGING")
    print("=" * 60)
# --------------------------------------------------------
   # PRODUCTION
# --------------------------------------------------------
    print("STAGING → PRODUCTION")
    print("=" * 60)

def load_production():

    print("\n")
    print("=" * 60)
    print("STAGING → PRODUCTION")
    print("=" * 60)

    with engine.begin() as conn:

        # =================================================
        # Dim_Date
        # =================================================

        conn.execute(text("""
            MERGE dbo.Dim_Date AS target
            USING dbo.stg_Dim_Date AS source
            ON target.date_id = source.date_id

            WHEN MATCHED THEN
                UPDATE SET
                    full_date = source.full_date,
                    year = source.year,
                    quarter = source.quarter,
                    month = source.month,
                    month_name = source.month_name,
                    week = source.week,
                    day = source.day,
                    day_of_week = source.day_of_week,
                    day_name = source.day_name

            WHEN NOT MATCHED THEN
                INSERT (
                    date_id,
                    full_date,
                    year,
                    quarter,
                    month,
                    month_name,
                    week,
                    day,
                    day_of_week,
                    day_name
                )
                VALUES (
                    source.date_id,
                    source.full_date,
                    source.year,
                    source.quarter,
                    source.month,
                    source.month_name,
                    source.week,
                    source.day,
                    source.day_of_week,
                    source.day_name
                );
        """))

        # =================================================
        # Customers
        # =================================================

        conn.execute(text("""
            MERGE dbo.Customers AS target
            USING dbo.stg_Customers AS source
            ON target.customer_id = source.customer_id

            WHEN MATCHED THEN
                UPDATE SET
                    gender = source.gender,
                    age = source.age,
                    city = source.city,
                    register_date = source.register_date,
                    acquisition_channel = source.acquisition_channel

            WHEN NOT MATCHED THEN
                INSERT (
                    customer_id,
                    gender,
                    age,
                    city,
                    register_date,
                    acquisition_channel
                )
                VALUES (
                    source.customer_id,
                    source.gender,
                    source.age,
                    source.city,
                    source.register_date,
                    source.acquisition_channel
                );
        """))

        # =================================================
        # Marketing_Campaigns
        # =================================================

        conn.execute(text("""
            MERGE dbo.Marketing_Campaigns AS target
            USING dbo.stg_Marketing_Campaigns AS source
            ON target.campaign_id = source.campaign_id

            WHEN MATCHED THEN
                UPDATE SET
                    campaign_name = source.campaign_name,
                    channel = source.channel,
                    start_date = source.start_date,
                    end_date = source.end_date,
                    budget = source.budget

            WHEN NOT MATCHED THEN
                INSERT (
                    campaign_id,
                    campaign_name,
                    channel,
                    start_date,
                    end_date,
                    budget
                )
                VALUES (
                    source.campaign_id,
                    source.campaign_name,
                    source.channel,
                    source.start_date,
                    source.end_date,
                    source.budget
                );
        """))

        # =================================================
        # Machines
        # =================================================

        conn.execute(text("""
            MERGE dbo.Machines AS target
            USING dbo.stg_Machines AS source
            ON target.machine_id = source.machine_id

            WHEN MATCHED THEN
                UPDATE SET
                    model = source.model,
                    purchase_date = source.purchase_date,
                    purchase_cost = source.purchase_cost,
                    status = source.status

            WHEN NOT MATCHED THEN
                INSERT (
                    machine_id,
                    model,
                    purchase_date,
                    purchase_cost,
                    status
                )
                VALUES (
                    source.machine_id,
                    source.model,
                    source.purchase_date,
                    source.purchase_cost,
                    source.status
                );
        """))

        # =================================================
        # Leads
        # =================================================

        conn.execute(text("""
            MERGE dbo.Leads AS target
            USING dbo.stg_Leads AS source
            ON target.lead_id = source.lead_id

            WHEN MATCHED THEN
                UPDATE SET
                    customer_id = source.customer_id,
                    campaign_id = source.campaign_id,
                    lead_date = source.lead_date,
                    channel = source.channel,
                    status = source.status

            WHEN NOT MATCHED THEN
                INSERT (
                    lead_id,
                    customer_id,
                    campaign_id,
                    lead_date,
                    channel,
                    status
                )
                VALUES (
                    source.lead_id,
                    source.customer_id,
                    source.campaign_id,
                    source.lead_date,
                    source.channel,
                    source.status
                );
        """))

        # =================================================
        # Rentals
        # =================================================

        conn.execute(text("""
            MERGE dbo.Rentals AS target
            USING dbo.stg_Rentals AS source
            ON target.rental_id = source.rental_id

            WHEN MATCHED THEN
                UPDATE SET
                    customer_id = source.customer_id,
                    machine_id = source.machine_id,
                    start_date = source.start_date,
                    end_date = source.end_date,
                    monthly_fee = source.monthly_fee,
                    status = source.status

            WHEN NOT MATCHED THEN
                INSERT (
                    rental_id,
                    customer_id,
                    machine_id,
                    start_date,
                    end_date,
                    monthly_fee,
                    status
                )
                VALUES (
                    source.rental_id,
                    source.customer_id,
                    source.machine_id,
                    source.start_date,
                    source.end_date,
                    source.monthly_fee,
                    source.status
                );
        """))

        # =================================================
        # Payments
        # =================================================

        conn.execute(text("""
            MERGE dbo.Payments AS target
            USING dbo.stg_Payments AS source
            ON target.payment_id = source.payment_id

            WHEN MATCHED THEN
                UPDATE SET
                    rental_id = source.rental_id,
                    payment_date = source.payment_date,
                    amount = source.amount,
                    payment_status = source.payment_status

            WHEN NOT MATCHED THEN
                INSERT (
                    payment_id,
                    rental_id,
                    payment_date,
                    amount,
                    payment_status
                )
                VALUES (
                    source.payment_id,
                    source.rental_id,
                    source.payment_date,
                    source.amount,
                    source.payment_status
                );
        """))

        # =================================================
        # Maintenance
        # =================================================

        conn.execute(text("""
            MERGE dbo.Maintenance AS target
            USING dbo.stg_Maintenance AS source
            ON target.maintenance_id = source.maintenance_id

            WHEN MATCHED THEN
                UPDATE SET
                    machine_id = source.machine_id,
                    maintenance_date = source.maintenance_date,
                    maintenance_type = source.maintenance_type,
                    cost = source.cost

            WHEN NOT MATCHED THEN
                INSERT (
                    maintenance_id,
                    machine_id,
                    maintenance_date,
                    maintenance_type,
                    cost
                )
                VALUES (
                    source.maintenance_id,
                    source.machine_id,
                    source.maintenance_date,
                    source.maintenance_type,
                    source.cost
                );
        """))

    print("Production Upsert completed.")


def load_all(data):

    load_staging(data)
    load_production()

    print("\n")
    print("=" * 60)
    print("LOAD COMPLETED")
    print("=" * 60)
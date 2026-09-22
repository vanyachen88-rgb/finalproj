from etl.extract import extract_data

from etl.transform import (
    transform_dim_date,
    transform_customers,
    transform_marketing_campaigns,
    transform_leads,
    transform_machines,
    transform_rentals,
    transform_payments,
    transform_maintenance
)

from etl.validate import validate_all

from etl.load_CSV import load_all


def main():

    print("\n")
    print("=" * 60)
    print("ETL PIPELINE START")
    print("=" * 60)

    # =====================================================
    # 1. EXTRACT
    # =====================================================

    print("\n[1/4] EXTRACT")

    data = extract_data()

    # =====================================================
    # 2. TRANSFORM
    # =====================================================

    print("\n[2/4] TRANSFORM")

    data["Dim_Date"] = transform_dim_date(
        data["Dim_Date"]
    )

    data["Customers"] = transform_customers(
        data["Customers"]
    )

    data["Marketing_Campaigns"] = transform_marketing_campaigns(
        data["Marketing_Campaigns"]
    )

    data["Leads"] = transform_leads(
        data["Leads"]
    )

    data["Machines"] = transform_machines(
        data["Machines"]
    )

    data["Rentals"] = transform_rentals(
        data["Rentals"]
    )

    data["Payments"] = transform_payments(
        data["Payments"]
    )

    data["Maintenance"] = transform_maintenance(
        data["Maintenance"]
    )

    # =====================================================
    # 3. VALIDATE
    # =====================================================

    print("\n[3/4] VALIDATE")

    validate_all(data)

    # =====================================================
    # 4. LOAD
    # =====================================================

    print("\n[4/4] LOAD")

    load_all(data)

    # =====================================================
    # 完成
    # =====================================================

    print("\n")
    print("=" * 60)
    print("ETL PIPELINE COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
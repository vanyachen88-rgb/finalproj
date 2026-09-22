from analytics.db import read_sql
from analytics.queries import (
    CUSTOMER_COUNT,
    LEAD_COUNT,
    RENTAL_COUNT,
    TOTAL_REVENUE,
    AVG_MONTHLY_FEE,
    TOTAL_MAINTENANCE_COST,
)


def get_kpis():

    customer_count = read_sql(
        CUSTOMER_COUNT
    ).iloc[0]["customer_count"]

    lead_count = read_sql(
        LEAD_COUNT
    ).iloc[0]["lead_count"]

    rental_count = read_sql(
        RENTAL_COUNT
    ).iloc[0]["rental_count"]

    total_revenue = read_sql(
        TOTAL_REVENUE
    ).iloc[0]["total_revenue"]

    avg_monthly_fee = read_sql(
        AVG_MONTHLY_FEE
    ).iloc[0]["avg_monthly_fee"]

    total_maintenance_cost = read_sql(
        TOTAL_MAINTENANCE_COST
    ).iloc[0]["total_maintenance_cost"]

    return {
        "customer_count": customer_count,
        "lead_count": lead_count,
        "rental_count": rental_count,
        "total_revenue": total_revenue,
        "avg_monthly_fee": avg_monthly_fee,
        "total_maintenance_cost": total_maintenance_cost,
    }


if __name__ == "__main__":

    print("=" * 60)
    print("PYTHON ANALYTICS")
    print("=" * 60)

    kpis = get_kpis()

    print()
    print(f"Customers              : {kpis['customer_count']:,}")
    print(f"Leads                  : {kpis['lead_count']:,}")
    print(f"Rentals                : {kpis['rental_count']:,}")
    print(f"Total Revenue          : {kpis['total_revenue']:,.2f}")
    print(f"Avg Monthly Fee        : {kpis['avg_monthly_fee']:,.2f}")
    print(
        f"Maintenance Cost       : "
        f"{kpis['total_maintenance_cost']:,.2f}"
    )
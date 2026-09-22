# ============================================================
# KPI 1：Customer Count
# ============================================================

CUSTOMER_COUNT = """
SELECT
    COUNT(*) AS customer_count
FROM dbo.Customers;
"""


# ============================================================
# KPI 2：Lead Count
# ============================================================

LEAD_COUNT = """
SELECT
    COUNT(*) AS lead_count
FROM dbo.Leads;
"""


# ============================================================
# KPI 3：Rental Count
# ============================================================

RENTAL_COUNT = """
SELECT
    COUNT(*) AS rental_count
FROM dbo.Rentals;
"""


# ============================================================
# KPI 4：Total Revenue
# ============================================================

TOTAL_REVENUE = """
SELECT
    SUM(amount) AS total_revenue
FROM dbo.Payments
WHERE payment_status = N'Paid';
"""


# ============================================================
# KPI 5：Average Monthly Rental Fee
# ============================================================

AVG_MONTHLY_FEE = """
SELECT
    AVG(monthly_fee) AS avg_monthly_fee
FROM dbo.Rentals
WHERE monthly_fee IS NOT NULL;
"""


# ============================================================
# KPI 6：Total Maintenance Cost
# ============================================================

TOTAL_MAINTENANCE_COST = """
SELECT
    SUM(cost) AS total_maintenance_cost
FROM dbo.Maintenance;
"""
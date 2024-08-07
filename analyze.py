import sqlite3
import pandas as pd

def run_query(query):
    conn = sqlite3.connect('github_issues.db')
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 1. Count of issues by state
query = """
SELECT state, COUNT(*) as issue_count
FROM issues
GROUP BY state;
"""
result = run_query(query)
print("Count of issues by state")
print(result)
# 2. Average time to close issues (in days)
query = """
SELECT AVG(JULIANDAY(closed_at) - JULIANDAY(created_at)) as avg_days_to_close
FROM issues
WHERE state = 'closed' AND closed_at IS NOT NULL;
"""
result = run_query(query)
print("Average time to close issues (in days)")
print(result)
# 3. Number of issues created per month
query = """
SELECT strftime('%Y-%m', created_at) as month, COUNT(*) as issue_count
FROM issues
GROUP BY month
ORDER BY month;
"""
result = run_query(query)
print("Number of issues created per month")
print(result)
# 4. Top 5 months with the most issues created
query = """
SELECT strftime('%Y-%m', created_at) as month, COUNT(*) as issue_count
FROM issues
GROUP BY month
ORDER BY issue_count DESC
LIMIT 5;
"""
result = run_query(query)
print("Top 5 months with the most issues created")
print(result)
# 5. Percentage of closed issues
query = """
SELECT 
    (COUNT(CASE WHEN state = 'closed' THEN 1 END) * 100.0 / COUNT(*)) as percent_closed
FROM issues;
"""
result = run_query(query)
print("Percentage of closed issues")
print(result)
# 6. Issues that were open for more than 30 days
query = """
SELECT id, created_at, closed_at, 
       (JULIANDAY(closed_at) - JULIANDAY(created_at)) as days_open
FROM issues
WHERE state = 'closed' AND (JULIANDAY(closed_at) - JULIANDAY(created_at)) > 30
ORDER BY days_open DESC;
"""
result = run_query(query)
print("Issues that were open for more than 30 days")
print(result)
# 7. Monthly closure rate (percentage of issues closed in the same month they were opened)
query = """
SELECT 
    strftime('%Y-%m', created_at) as month,
    COUNT(*) as total_issues,
    SUM(CASE WHEN state = 'closed' AND strftime('%Y-%m', closed_at) = strftime('%Y-%m', created_at) THEN 1 ELSE 0 END) as closed_same_month,
    (SUM(CASE WHEN state = 'closed' AND strftime('%Y-%m', closed_at) = strftime('%Y-%m', created_at) THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as closure_rate
FROM issues
GROUP BY month
ORDER BY month;
"""
result = run_query(query)
print("Monthly closure rate (percentage of issues closed in the same month they were opened)")
print(result)
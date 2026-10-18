import duckdb

con = duckdb.connect("olist.duckdb", read_only=True)


def run(title, sql):
    print("\n" + title)
    print(con.execute(sql).fetchdf())


run("Q1 delivered orders", "SELECT COUNT(*) AS delivered FROM orders WHERE order_status = 'delivered'")

run("Q2 orders per status", "SELECT order_status, COUNT(*) AS orders FROM orders GROUP BY order_status ORDER BY orders DESC")

run("Q3 total payment value", "SELECT ROUND(SUM(payment_value), 2) AS total_payment_value FROM order_payments")

run("Q4 top 5 categories by items sold", """
SELECT COALESCE(t.product_category_name_english, p.product_category_name) AS category,
       COUNT(*) AS items_sold
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN product_category_name_translation t ON p.product_category_name = t.product_category_name
GROUP BY category
ORDER BY items_sold DESC
LIMIT 5
""")

run("Q5 orders per month", """
SELECT strftime(CAST(order_purchase_timestamp AS TIMESTAMP), '%Y-%m') AS month,
       COUNT(*) AS orders
FROM orders
GROUP BY month
ORDER BY month
""")

run("Q6 average review score", "SELECT ROUND(AVG(review_score), 2) AS avg_review_score FROM order_reviews")

run("Q7 top 5 states by customers", """
SELECT customer_state, COUNT(DISTINCT customer_unique_id) AS customers
FROM customers
GROUP BY customer_state
ORDER BY customers DESC
LIMIT 5
""")

run("Q8 average order value", "SELECT ROUND(SUM(payment_value) / COUNT(DISTINCT order_id), 2) AS avg_order_value FROM order_payments")
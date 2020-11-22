SELECT product_id, SUM(store_sales - store_cost)/SUM(unit_sales) AS avg_gain
FROM sales_fact
GROUP BY product_id
ORDER BY avg_gain DESC


-- SELECT TOP(10) * FROM sales_fact ORDER BY product_id
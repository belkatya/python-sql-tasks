import psycopg2
from psycopg2.extras import DictCursor


conn = psycopg2.connect('postgresql://postgres:@localhost:5432/test_db')


# BEGIN (write your solution here)
def get_order_sum(conn, month) -> str:
    query = """
    SELECT 
        c.customer_name,
        SUM(o.total_amount)::INTEGER as total_sum
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE EXTRACT(MONTH FROM o.order_date) = %s
    GROUP BY c.customer_id, c.customer_name
    ORDER BY total_sum;
    """

    with conn.cursor() as cur:
        cur.execute(query, (month,)) 
        return "\n".join(
            f"Покупатель {name} совершил покупок на сумму {total}"
            for name, total in cur.fetchall()
        )
# END

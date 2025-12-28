import psycopg2
from psycopg2.extras import execute_values

conn = psycopg2.connect('postgresql://postgres:@localhost:5432/test_db')


# BEGIN (write your solution here)
def batch_insert(conn, products):
    insert_query = """
    INSERT INTO products (name, price, quantity) VALUES %s
    """
    template = "(%(name)s, %(price)s, %(quantity)s)"
    with conn.cursor() as cur:
        execute_values(cur, insert_query, products, template)
    conn.commit()

def get_all_products(conn):
    select_query = """
    SELECT * FROM products ORDER BY price DESC
    """
    with conn.cursor() as cur:
        cur.execute(select_query)
        return cur.fetchall()
# END

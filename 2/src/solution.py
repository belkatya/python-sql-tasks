import psycopg2

conn = psycopg2.connect('postgresql://postgres:@localhost:5432/test_db')


# BEGIN (write your solution here)
def make_cars_table(conn):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS cars (
        id SERIAL PRIMARY KEY,
        brand VARCHAR NOT NULL,
        model VARCHAR NOT NULL
    )
    """
    with conn.cursor() as cur:
        cur.execute(create_table_query)
    conn.commit()


def populate_cars_table(conn, cars):
    insert_query = """
    INSERT INTO cars (brand, model) VALUES (%s, %s)
    """
    with conn.cursor() as cur:
        for car in cars:
            cur.execute(insert_query, car)
    conn.commit()


def get_all_cars(conn):
    select_query = """SELECT * FROM cars ORDER BY brand ASC"""
    
    with conn.cursor() as cur:
        cur.execute(select_query)
        return cur.fetchall()
# END

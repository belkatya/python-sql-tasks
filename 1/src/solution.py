import psycopg2

conn = psycopg2.connect('postgresql://postgres:@localhost:5432/test_db')


# BEGIN (write your solution here)
def add_movies(conn):
    cursor = conn.cursor()
    try:
        query = """INSERT INTO movies (title, release_year, duration) VALUES (%s, %s, %s)"""
        
        cursor.execute(query, ('Godfather', 1972, 175))
        cursor.execute(query, ('The Green Mile', 1999, 189))
        
        conn.commit()
    finally:
        cursor.close()

def get_all_movies(conn):
    cursor = conn.cursor()
    
    try:
        select_query = "SELECT * FROM movies ORDER BY id"
        
        cursor.execute(select_query)
        movies = cursor.fetchall()
        return movies
    finally:
        cursor.close()
# END

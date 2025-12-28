import psycopg2
from psycopg2.extras import DictCursor


conn = psycopg2.connect('postgresql://postgres:@localhost:5432/test_db')


# BEGIN (write your solution here)
def create_post(conn, post):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO posts (title, content, author_id) VALUES (%s, %s, %s) RETURNING id", (post['title'], post['content'], post['author_id']))
        post_id = cur.fetchone()[0]
        conn.commit()
        return post_id
    
def add_comment(conn, comment):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO comments (post_id, author_id, content) VALUES (%s, %s, %s) RETURNING id", (comment['post_id'], comment['author_id'], comment['content']))
        comment_id = cur.fetchone()[0]
        conn.commit()
        return comment_id
    
def get_latest_posts(conn, limit):
    with conn.cursor(cursor_factory=DictCursor) as cur:
        query = """
        SELECT 
            p.id as post_id,
            p.title,
            p.content as post_content,
            p.author_id as post_author_id,
            p.created_at as post_created_at,
            c.id as comment_id,
            c.author_id as comment_author_id,
            c.content as comment_content,
            c.created_at as comment_created_at
        FROM (
            SELECT * FROM posts 
            ORDER BY created_at DESC 
            LIMIT %s
        ) p
        LEFT JOIN comments c ON p.id = c.post_id
        ORDER BY p.created_at DESC, c.created_at;
        """
        
        cur.execute(query, (limit,))
        rows = cur.fetchall()
        
        posts_dict = {}
        for row in rows:
            post_id = row['post_id']
            
            if post_id not in posts_dict:
                posts_dict[post_id] = {
                    'id': post_id,
                    'title': row['title'],
                    'content': row['post_content'],
                    'author_id': row['post_author_id'],
                    'created_at': row['post_created_at'],
                    'comments': []
                }
            
            if row['comment_id'] is not None:
                comment = {
                    'id': row['comment_id'],
                    'author_id': row['comment_author_id'],
                    'content': row['comment_content'],
                    'created_at': row['comment_created_at']
                }
                posts_dict[post_id]['comments'].append(comment)
        
        result = list(posts_dict.values())
        result.sort(key=lambda x: x['created_at'], reverse=True)
        
        return result
# END

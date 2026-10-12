import psycopg
from pgvector.psycopg import register_vector

with psycopg.connect("host=localhost dbname=postgres user=postgres") as conn:
    conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    register_vector(conn)

    with conn.cursor() as cur:
        cur.execute("CREATE TEMP TABLE documents (id serial PRIMARY KEY, content text, embedding vector(3));")

        items = [
            ("System architecture guide", [0.95, 0.10, 0.05]),
            ("Cooking recipe for pasta", [0.02, 0.88, 0.75]),
            ("WSL2 and Docker configuration", [0.91, 0.15, 0.12]),
        ]
        cur.executemany("INSERT INTO documents (content, embedding) VALUES (%s, %s);", items)

        query_vector = [0.90, 0.12, 0.08]
        cur.execute("""
            SELECT content, embedding <=> %s::vector AS distance
            FROM documents
            ORDER BY distance ASC
            LIMIT 2;
        """, (query_vector,))

        print("Top semantic matches (lowest cosine distance):")
        for content, distance in cur.fetchall():
            print(f" - {content} (distance: {distance:.4f})")

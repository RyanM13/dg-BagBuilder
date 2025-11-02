import psycopg2
import requests

# Database connection
conn = psycopg2.connect(
    dbname="Discs",
    user="postgres",
    password="MSUCOLT!",
    host="localhost",
    port="5432",
)
cur = conn.cursor()
print("✅ Connected to database")

API_URL = "https://discit-api.fly.dev/disc"

# Fetch the disc data
response = requests.get(API_URL)

if response.status_code == 200:
    data = response.json()

    for disc in data:
        name = disc.get("name", "Unknown")
        brand = disc.get("brand", "Unknown")
        speed = disc.get("speed", 0)
        glide = disc.get("glide", 0)
        turn = disc.get("turn", 0)
        fade = disc.get("fade", 0)

        print(
            f"Inserting: {name} ({brand}) - Speed {speed}, Glide {glide}, Turn {turn}, Fade {fade}"
        )

        insert_query = """
        INSERT INTO discs (name, brand, speed, glide, turn, fade)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (name) DO NOTHING;
        """

        try:
            cur.execute(insert_query, (name, brand, speed, glide, turn, fade))
            conn.commit()
        except Exception as e:
            print(f"❌ Error inserting {name}: {e}")
            conn.rollback()  # 🧹 Reset transaction state to keep going

else:
    print(f"❌ Failed to fetch data: {response.status_code}")

cur.close()
conn.close()
print("✅ Data insertion complete.")

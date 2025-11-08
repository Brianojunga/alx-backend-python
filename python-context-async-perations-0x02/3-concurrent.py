import asyncio
import aiosqlite

DB_PATH = "example.db"
# Setup database and table for demonstration
async def setup_database():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        """)
        await db.executemany(
            "INSERT OR IGNORE INTO users (id, name, age) VALUES (?, ?, ?)",
            [
                (1, "Alice", 25),
                (2, "Bob", 42),
                (3, "Charlie", 36),
                (4, "Diana", 55)
            ]
        )
        await db.commit()


# Fetch all users
async def async_fetch_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("\nAll Users:")
            for user in users:
                print(user)
            return users


# Fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            older_users = await cursor.fetchall()
            print("\nUsers older than 40:")
            for user in older_users:
                print(user)
            return older_users


# Run both concurrently
async def fetch_concurrently():
    await setup_database()  # Ensure table and data exist
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )


# Run the event loop
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())

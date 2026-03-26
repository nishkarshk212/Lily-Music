# Authored By Certified Coders © 2025
from pyrogram import Client

print("Starting Pyrogram Session Generator...")
print("Enter your API credentials below:\n")

API_ID = int(input("Enter API ID (e.g., 37176542): "))
API_HASH = input("Enter API HASH (e.g., 6545cdb8853f0e38aad24921ee992323): ")

async def main():
    async with Client(
        "SaregamaMusic",
        api_id=API_ID,
        api_hash=API_HASH
    ) as app:
        print("\n✅ Session generated successfully!")
        print(f"📝 Copy this session string and add it to your .env file:\n")
        print(f"STRING_SESSION={await app.export_session_string()}")
        print("\nAfter copying, run the bot with: python -m AnnieXMedia")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

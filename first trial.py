import logging
from telegram import Bot
from solana.rpc.async_api import AsyncClient
from aiohttp import ClientSession
import asyncio

# TG Bot token
TG_TOKEN = "7271322371:AAFwPsCM-uh9kMhT9uA_uPkz2FZ2OrcF--o"

# Solana RPC endpoint
SOLANA_RPC = "https://api.mainnet-beta.solana.com/"

# Wallet address to track
WALLET_ADDRESS = "TSLvdd1pWpHVjahSpsvCXUbgwsL3JAcvokwaKt1eokM"

# Bot logging
logging.basicConfig(level=logging.INFO)

# Initialize TG Bot
bot = Bot(token=TG_TOKEN)

# Initialize Solana client
async def init_solana_client():
    client = AsyncClient(SOLANA_RPC)
    return client

# Get latest transactions from wallet address
async def get_latest_transactions(wallet_address):
    solana_client = await init_solana_client()
    transactions = await solana_client.get_transactions(wallet_address)
    return transactions

# Check if transaction is a token creation
async def is_token_creation(transaction):
    if transaction["transaction"]["message"]["instructions"][0]["programId"] == "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA":
        return True
    return False

# Get token mint from transaction
async def get_token_mint(transaction):
    return transaction["transaction"]["message"]["instructions"][0]["accounts"][0]["pubkey"]

# Check if token has liquidity
async def has_liquidity(token_mint):
    solana_client = await init_solana_client()
    token_info = await solana_client.get_token_info(token_mint)
    return token_info["tokenAmount"]["amount"] > 0

# Snipe function
async def snipe(token_mint):
    # Implement your sniping logic here
    pass

# Real-time tracking function
async def track_wallet_address():
    while True:
        transactions = await get_latest_transactions(WALLET_ADDRESS)
        for transaction in transactions:
            if await is_token_creation(transaction):
                token_mint = await get_token_mint(transaction)
                if not await has_liquidity(token_mint):
                    await snipe(token_mint)
        await asyncio.sleep(60)  # Wait 1 minute before checking again

# TG Command handler
async def handle_command(update):
    message = update.message
    if message.text.startswith("/start"):
        # Start tracking wallet address
        await track_wallet_address()

# TG Bot main loop
async def main():
    async with ClientSession() as session:
        bot.add_handler(handle_command)
        await bot.start_polling()

if __name__ == "__main__":
    logging.info("Starting Solana sniping bot...")
    asyncio.run(main())


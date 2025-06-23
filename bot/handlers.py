from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.zero_ex_api import ZeroExAPI
from bot.base_web3 import get_web3
import logging
import os
from web3 import Web3

WETH_BASE = "0x4200000000000000000000000000000000000006"  # WETH officiel sur Base

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot 0x Swap prêt !\n"
        "Utilise la commande :\n"
        "/swap <token_address> <amount_eth> <max_fee_per_gas>\n"
        "pour acheter un token via 0x API sur Base."
        "\n\n⚠️ Tu dois avoir du WETH sur Base pour swapper !"
    )

async def swap_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) != 3:
            await update.message.reply_text("Usage : /swap <token_address> <amount_eth> <max_fee_per_gas>")
            return
        
        token_address, amount_eth, max_fee_per_gas = context.args
        
        # Validate inputs
        if not Web3.is_address(token_address):
            await update.message.reply_text("❌ Adresse de token invalide")
            return
        
        try:
            amount_eth = float(amount_eth)
            if amount_eth <= 0:
                await update.message.reply_text("❌ Le montant doit être positif")
                return
        except ValueError:
            await update.message.reply_text("❌ Montant ETH invalide")
            return
        
        try:
            max_fee_per_gas = int(max_fee_per_gas)
            if max_fee_per_gas <= 0:
                await update.message.reply_text("❌ Le max_fee_per_gas doit être positif")
                return
        except ValueError:
            await update.message.reply_text("❌ max_fee_per_gas invalide")
            return
        
        # Get private key from environment
        private_key = os.getenv('PRIVATE_KEY')
        if not private_key:
            await update.message.reply_text("❌ Clé privée non configurée")
            return
        
        # Initialize Web3 and 0x API
        web3 = get_web3()
        zero_ex = ZeroExAPI(web3)
        
        # Convert ETH amount to wei
        sell_amount_wei = Web3.to_wei(amount_eth, 'ether')
        
        # Execute swap (toujours WETH comme sell_token sur Base)
        await update.message.reply_text("🔄 Exécution du swap en cours...")
        
        tx_hash = zero_ex.execute_swap(
            private_key=private_key,
            sell_token=WETH_BASE,  # Utilise WETH de Base
            buy_token=token_address,  # Buying the specified token
            sell_amount=str(sell_amount_wei)
        )
        
        # Create Basescan URL
        basescan_url = f"https://basescan.org/tx/{tx_hash}"
        
        await update.message.reply_text(
            f"✅ Swap exécuté avec succès !\n"
            f"📊 Hash: `{tx_hash}`\n"
            f"🔗 [Voir sur Basescan]({basescan_url})\n"
            f"💰 Montant: {amount_eth} WETH"
        )
        
    except Exception as e:
        logging.exception("Erreur lors du swap :")
        await update.message.reply_text(f"❌ Erreur lors du swap : {str(e)}")

def register_handlers(app):
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("swap", swap_command)) 
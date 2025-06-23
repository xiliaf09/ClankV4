import os
import json
import logging
from typing import Dict, Any, Optional
import requests
from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_defunct

logger = logging.getLogger(__name__)

class ZeroExAPI:
    def __init__(self, web3: Web3):
        self.web3 = web3
        self.api_key = os.getenv('ZERO_EX_API_KEY')
        print(f"ZERO_EX_API_KEY lue: {self.api_key}")  # DEBUG Railway
        self.base_url = "https://api.0x.org"
        self.chain_id = 8453  # Base chain ID
        
        if not self.api_key:
            raise ValueError("ZERO_EX_API_KEY environment variable is required")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for 0x API requests"""
        return {
            "Content-Type": "application/json",
            "0x-api-key": self.api_key,
            "0x-version": "v2",
        }
    
    def get_swap_price(self, sell_token: str, buy_token: str, sell_amount: str, taker: str = None) -> Dict[str, Any]:
        """Get swap price quote from 0x API"""
        url = f"{self.base_url}/swap/permit2/price"
        
        params = {
            "chainId": self.chain_id,
            "sellToken": sell_token,
            "buyToken": buy_token,
            "sellAmount": sell_amount,
        }
        
        if taker:
            params["taker"] = taker
            
        try:
            response = requests.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Price quote received: {data}")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting swap price: {e}")
            raise
    
    def get_swap_quote(self, sell_token: str, buy_token: str, sell_amount: str, taker: str = None) -> Dict[str, Any]:
        """Get swap quote from 0x API"""
        url = f"{self.base_url}/swap/permit2/quote"
        
        params = {
            "chainId": self.chain_id,
            "sellToken": sell_token,
            "buyToken": buy_token,
            "sellAmount": sell_amount,
        }
        
        if taker:
            params["taker"] = taker
            
        try:
            response = requests.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Swap quote received: {data}")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting swap quote: {e}")
            raise
    
    def execute_swap(self, private_key: str, sell_token: str, buy_token: str, sell_amount: str) -> str:
        """Execute a swap using 0x API"""
        try:
            # Get account from private key
            account = Account.from_key(private_key)
            taker_address = account.address
            
            # Get swap quote
            quote = self.get_swap_quote(sell_token, buy_token, sell_amount, taker_address)
            
            # Prepare transaction
            tx_data = {
                "from": taker_address,
                "to": quote["to"],
                "data": quote["data"],
                "value": quote.get("value", "0"),
                "gas": int(quote["estimatedGas"] * 1.2),  # Add 20% buffer
                "nonce": self.web3.eth.get_transaction_count(taker_address),
                "chainId": self.chain_id,
            }
            
            # Get gas price
            gas_price = self.web3.eth.gas_price
            tx_data["gasPrice"] = gas_price
            
            # Sign transaction
            signed_tx = self.web3.eth.account.sign_transaction(tx_data, private_key)
            
            # Send transaction
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            tx_hash_hex = tx_hash.hex()
            
            logger.info(f"Swap transaction sent: {tx_hash_hex}")
            return tx_hash_hex
            
        except Exception as e:
            logger.error(f"Error executing swap: {e}")
            raise
    
    def get_token_info(self, token_address: str) -> Dict[str, Any]:
        """Get token information"""
        # For ETH, return special info
        if token_address.upper() == "ETH":
            return {
                "address": "ETH",
                "symbol": "ETH",
                "decimals": 18,
                "name": "Ethereum"
            }
        
        # For other tokens, you might want to call the token contract
        # This is a simplified version
        return {
            "address": token_address,
            "symbol": "UNKNOWN",
            "decimals": 18,
            "name": "Unknown Token"
        } 
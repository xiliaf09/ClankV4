# 0x Swap Telegram Bot

Ce bot Telegram permet d'acheter n'importe quel token sur la blockchain Base via l'API 0x.org avec une simple commande Telegram.

## Fonctionnalités principales
- Achat de tokens via la commande `/swap <token_address> <amount_eth> <max_fee_per_gas>`
- Utilisation de l'API 0x.org pour les meilleurs prix et liquidité
- Support de tous les tokens ERC-20 sur Base
- Affichage du hash de la transaction et d'un lien vers Basescan
- Gestion automatique des gas fees et optimisations

## Stack technique
- Python 3.10+
- python-telegram-bot
- web3.py
- 0x API
- Déploiement Railway

## Configuration
1. Cloner le repo
2. Créer un fichier `.env` avec les variables suivantes :
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   PRIVATE_KEY=your_private_key_here
   ZERO_EX_API_KEY=your_0x_api_key_here
   BASE_RPC_URL=https://mainnet.base.org
   ```
3. Installer les dépendances : `pip install -r requirements.txt`
4. Lancer le bot : `python main.py`

## Déploiement Railway
- Toutes les variables sensibles doivent être configurées dans Railway
- Obtenir une clé API gratuite sur [0x.org](https://0x.org/docs/api)

## Structure du projet
```
/0x-swap-bot/
│
├── bot/
│   ├── __init__.py
│   ├── handlers.py
│   ├── zero_ex_api.py
│   ├── base_web3.py
│   └── utils.py
├── requirements.txt
├── README.md
└── main.py
```

## Utilisation
1. Démarrer le bot avec `/start`
2. Utiliser la commande `/swap <token_address> <amount_eth> <max_fee_per_gas>`
   - `token_address` : Adresse du token à acheter
   - `amount_eth` : Montant d'ETH à vendre
   - `max_fee_per_gas` : Prix maximum du gas en wei

## Sécurité
Aucune donnée sensible ne doit être hardcodée dans le code source. Utilisez les variables d'environnement.

## Avantages de 0x API
- Meilleurs prix grâce à l'agrégation de plusieurs DEX
- Liquidité optimisée
- Support de tous les tokens ERC-20
- API simple et fiable 
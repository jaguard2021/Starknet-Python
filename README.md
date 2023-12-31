# StarkNet: All In One

This script is your ultimate companion for navigating the Starknet network effortlessly.
It offers a range of features that make working with Starknet a breeze, simplifies farm management,
and enables various network operations.

Documentation: https://starknet-aio.gitbook.io/starknet-aio/

## Requirements

```
1. Python 3.10+
2. WSL2 for Windows to run python.
3. Registered and activated starknet wallets (braavos or argent).
```

### Windows

For windows use WSL2: https://www.youtube.com/watch?v=Yq3YeLYYGNo
Install python on WSL2: https://www.cherryservers.com/blog/install-python-on-ubuntu

### Features:

- Check balances.
- Check transactions count.
- Exchange withdraw ETH.
- Transfer ETH to exchange.
- Orbiter bridge.
- Dmail: send random email.
- Swaps:
    - AVNU
    - JediSwap
    - MySwap
    - 10kSwap
    - SithSwap
    - Protoss
    - OpenOcean
    - RANDOM SWAP: ETH > Random Token > ETH / Random Dex
- NFT:
    - StarknetId
    - Starkverse
    - Unframed
    - Flex
    - StarkStars
    - Almanac
    - The Ninth
    - RANDOM: Call random NFT function
- ZkLend:
    - Deposit (supply)
    - Withdraw
    - Enable collateral
    - Disable collateral
    - Borrow
    - Repay
    - ROUTE: Deposit ETH > Enable collateral > Borrow random token > Repay token > Withdraw ETH
- Nostra:
    - Deposit
    - Withdraw
    - ROUTE: Deposit ETH > Withdraw ETH
- Deploy smart-contract
    - Token
    - NFT
- MULTIPLE Functions: make one or multiple random transactions.
- VOLUME: increase wallet tx volumes. Process step-by-step:
  Script withdraw ETH from OKX to your StarkNet wallet (amount include randomisation), then use zkLend to provide ETH as collateral and
  borrow USDC,
  proceed to execute multiple USDC/USDT swaps on AVNU/SithSwap/OpenOcean (the number of swaps can be configured in config/settings.py).
  Before each swap step there is 50% chance to call random function to build unique route.
  Then we repay the borrowed USDC (script can buy some USDC to fully cover the borrowed amount - it makes a swap in a random DEX)
  and withdraw the locked ETH from zkLend. The final step is to return the ETH to OKX,
  you can use OKX sub-accounts, script automatically move ETH to your main account and repeat this process for next wallet.
- Unused Contracts: Find and run unused contract for wallet.

**IMPORTANT: Use OKX sub-accounts for volume and transfers to OKX, don't mix your wallets!**

## Installation

```
python -m venv venv
source venv/bin/activate
pip3 install wheel
pip3 install -r requirements.txt
```

## Run

```
source venv/bin/activate
python main.py
```

## Configuration

1. Copy or rename "config_sample" directory to "config".
2. Edit config/.env file to configure work with OKX.
3. Edit config/settings.py file to suit your preferences.
4. To manage your wallet addresses and private keys, edit the config/wallets.csv file.
   We recommend using a Modern CSV editor: https://www.moderncsv.com/
5. Add proxy to config/proxies.txt file, format: http://login:password@ip:port
6. Optionally, you can customize routes by editing the config/routes.py file.

#### OKX Deposit (transfer from starkNet to OKX)

To facilitate deposits, create separate deposit wallets for each of your StarkNet wallets.
Make sure to include these deposit wallet addresses in the "okx_address" column of the config/wallets.csv file.

#### OKX Withdraw

For withdrawals from OKX, ensure that your wallets are included in the StarkNet channel's withdraw whitelist.
Add the relevant wallet addresses to the "starknet_address" column in the config/wallets.csv file.

#### Transactions Volume

To manage transaction volumes effectively, consider using OKX sub-accounts.
Our script supports this feature and can transfer funds to your main account.
To enable this feature, you need to include your sub-accounts' API information in the config/.env file.

#### Orbiter Bridge

If you need to transfer ETH from web3 (Arbitrum, Optimism, etc.) to StarkNet,
add your wallet's private key to the config/wallets.csv file under the "web3_private_key" column.

## IMPORTANT: Safety rules

1. Don't share your private keys and mnemonic phrases with anyone.
2. Test new features/protocols with small amounts first.
3. Update script regularly, we add new features and fix bugs.

## WARNING in common.py

optimism chain 
'rpc': 'YOUR_Alchemy RPC_URL',

linea chain
'rpc': 'YOUR_Infura RPC_URL',

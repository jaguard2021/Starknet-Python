import time
import random
import sys

from typing import Union, List
from loguru import logger
from starknet_py.cairo.felt import decode_shortstring
from starknet_py.contract import Contract
from starknet_py.hash.address import compute_address
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.account.account import Account
from starknet_py.net.client_models import Call
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.gateway_client import GatewayClient
from starknet_py.net.models import StarknetChainId, Invoke
from starknet_py.net.signer.stark_curve_signer import KeyPair
from helpers.retry import retry
from config.settings import *
from common import *
from helpers.common import int_to_wei, wei_to_int, get_min_balance_eth

MAX_RETRIES = 3


class Starknet:
    def __init__(self, _id: int, wallet_data) -> None:
        self._id = _id + 1
        self.private_key = wallet_data['starknet_private_key']
        self.key_pair = KeyPair.from_private_key(self.private_key)


        if len(CUSTOM_RPC) > 0:
            self.client = FullNodeClient(random.choice(RPC["starknet"]["rpc"]))
        else:
            self.client = GatewayClient("mainnet")

        self.address_original = wallet_data['starknet_address']



        self.address = self._create_account()

        self.account = Account(
            address =  self.address_original if  len(self.address_original) else self.address,
            client=self.client,
            key_pair=self.key_pair,
            chain=StarknetChainId.MAINNET,
        )

        self.address = self.account.address

        self.account.ESTIMATED_FEE_MULTIPLIER = WEB3_FEE_MULTIPLIER
        self.explorer = RPC["starknet"]["explorer"]
        if wallet_data['web3_private_key'] is not None and len(wallet_data['web3_private_key']) > 0:
            self.web3_private_key = wallet_data['web3_private_key']

    def _create_account(self) -> Union[int, None]:
        if TYPE_WALLET == "argent":
            return self._get_argent_address()
        elif TYPE_WALLET == "braavos":
            return self._get_braavos_account()
        else:
            logger.error("Type wallet error! Available values: argent or braavos")
            sys.exit()

    def _get_argent_address(self) -> int:
        if CAIRO_VERSION == 0:
            selector = get_selector_from_name("initialize")
            calldata = [self.key_pair.public_key, 0]
            address = compute_address(
                class_hash=ARGENTX_PROXY_CLASS_HASH,
                constructor_calldata=[ARGENTX_IMPLEMENTATION_CLASS_HASH, selector, len(calldata), *calldata],
                salt=self.key_pair.public_key,
            )
            return address
        else:
            address = compute_address(
                class_hash=ARGENTX_IMPLEMENTATION_CLASS_HASH_NEW,
                constructor_calldata=[self.key_pair.public_key, 0],
                salt=self.key_pair.public_key,
            )
            return address

    def _get_braavos_account(self) -> int:
        selector = get_selector_from_name("initializer")
        call_data = [self.key_pair.public_key]
        address = compute_address(
            class_hash=BRAAVOS_PROXY_CLASS_HASH,
            constructor_calldata=[BRAAVOS_IMPLEMENTATION_CLASS_HASH, selector, len(call_data), *call_data],
            salt=self.key_pair.public_key,
        )
        return address

    def get_contract(self, contract_address: int, abi: Union[dict, None] = None, cairo_version: int = 0):
        if abi is None:
            abi = ERC20_ABI

        contract = Contract(
            address=contract_address,
            abi=abi,
            provider=self.account,
            cairo_version=cairo_version
        )
        return contract

    @retry
    def get_eth_balance(self) -> int:
        return self.account.get_balance_sync(TOKEN_ADDRESS["ETH"])

    @retry
    def get_balance(self, contract_address: int) -> dict:
        contract = self.get_contract(contract_address)
        symbol_data = contract.functions["symbol"].call_sync()
        decimal = contract.functions["decimals"].call_sync()
        balance_wei = contract.functions["balanceOf"].call_sync(self.address)
        balance = balance_wei.balance / 10 ** decimal.decimals

        return {
            "balance_wei": balance_wei.balance,
            "balance": balance,
            "symbol": decode_shortstring(symbol_data.symbol),
            "decimal": decimal.decimals
        }

    def sign_transaction(self, calls: List[Call], repeat: int = 0):
        if repeat > MAX_RETRIES:
            raise Exception("Max retries reached")

        nonce = self.account.get_nonce_sync()
        try:
            transaction = self.account.sign_invoke_transaction_sync(
                calls=calls,
                auto_estimate=True,
                nonce=nonce
            )
        except Exception as error:
            if 'Server Error' in str(error) or 'Server disconnected' in str(error):
                time.sleep(10)
                return self.sign_transaction(calls, repeat + 1)
            else:
                raise Exception(str(error))

        return transaction

    def send_transaction(self, transaction: Invoke, _retry=0):
        try:
            return self.account.client.send_transaction_sync(transaction)
        except Exception as error:
            if ('Server Error' in str(error) or 'Server disconnected' in str(error)) and _retry < 3:
                time.sleep(10)
                return self.send_transaction(transaction, _retry + 1)
            else:
                logger.error(f"[{self._id}][{self.address_original}] {str(error)}")
                return False

    def wait_until_tx_finished(self, tx_hash: int, _retry=0):
        if _retry == 0:
            logger.info(f"Transaction: {self.explorer}{hex(tx_hash)}")

        try:
            self.account.client.wait_for_tx_sync(tx_hash, check_interval=10)
            logger.success(f"Transaction [{self._id}][{hex(self.address)}] SUCCESS!")
        except Exception as e:
            if _retry < 5:
                time.sleep(5)
                self.wait_until_tx_finished(tx_hash, _retry + 1)
            else:
                logger.error(f"[{self._id}][{hex(self.address)}] Error, max read retries reached.")
                raise Exception(str(e))

    @retry
    def get_swap_amount(self, from_token, amount: float) -> int:
        balance = self.account.get_balance_sync(from_token)
        decimals = 18
        if amount == 0:
            amount_wei = balance
            if from_token == TOKEN_ADDRESS["ETH"]:
                amount_wei = amount_wei - int_to_wei(get_min_balance_eth(), 18)
        else:
            token = self.get_contract(from_token).functions["decimals"].call_sync()
            amount_wei = int_to_wei(amount, token.decimals)
            decimals = token.decimals

        if amount_wei <= 0 or amount_wei > balance:
            if amount_wei <= 0:
                raise Exception(f"Not enough tokens to left on balance, check MIN_BALANCE_ETH setting")
            else:
                raise Exception(f"Insufficient balance: {wei_to_int(balance, decimals)} < {wei_to_int(amount_wei, decimals)}")
        return amount_wei

    def get_transaction(self, tx_hash: int):
        return self.account.client.get_transaction_receipt_sync(tx_hash)

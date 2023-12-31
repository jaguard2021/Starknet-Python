import requests
from loguru import logger
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.client_models import Call
from config.settings import *
from helpers.common import get_random_proxy
from helpers.starknet import Starknet
from modules.swaps.config import AVNU_CONTRACT


def get_quotes(from_token: int, to_token: int, amount: int):
    url = "https://starknet.api.avnu.fi/swap/v1/quotes"
    fees = hex(0x00860d7dd27b165979a5a5c0b1ca44fb53a756ed80848613931dacb6a58ff5a0)

    params = {
        "sellTokenAddress": hex(from_token),
        "buyTokenAddress": hex(to_token),
        "sellAmount": hex(amount),
        # "integratorFees": hex(2),
        # "integratorFeeRecipient": fees,
        "excludeSources": "Ekubo",
    }

    # if USE_REF:
    #     params['integratorFees'] = hex(3)
    #     params['integratorFeeRecipient'] = fees

    proxies = get_random_proxy()
    response = requests.get(url, params=params, proxies=proxies)
    response_data = response.json()
    return response_data[0]["quoteId"]


def build_transaction(quote_id: str, recipient: int, slippage: float):
    url = "https://starknet.api.avnu.fi/swap/v1/build"
    data = {
        "quoteId": quote_id,
        "takerAddress": hex(recipient),
        "slippage": float(slippage / 100),
    }

    proxies = get_random_proxy()
    response = requests.post(url, json=data, proxies=proxies)
    response_data = response.json()

    return response_data


def swap_token_avnu(account: Starknet, amount, from_token, to_token):
    logger.info(f"[{account._id}][{account.address_original}] Swap using AVNU")

    amount_wei = account.get_swap_amount(from_token, amount)
    if not amount_wei:
        return False

    quote_id = get_quotes(from_token, to_token, amount_wei)
    transaction_data = build_transaction(quote_id, account.address, SLIPPAGE_PCT)

    approve_contract = account.get_contract(from_token)
    approve_call = approve_contract.functions["approve"].prepare(
        AVNU_CONTRACT,
        amount_wei
    )

    call_data = [int(i, 16) for i in transaction_data["calldata"]]
    swap_call = Call(
        to_addr=AVNU_CONTRACT,
        selector=get_selector_from_name(transaction_data["entrypoint"]),
        calldata=call_data,
    )

    transaction = account.sign_transaction([approve_call, swap_call])
    transaction_response = account.send_transaction(transaction)
    if transaction_response:
        return transaction_response.transaction_hash

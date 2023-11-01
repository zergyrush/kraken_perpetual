from decimal import Decimal
from typing import Any, Dict, List, Tuple

from pydantic import Field, SecretStr

from hummingbot.client.config.config_data_types import BaseConnectorConfigMap, ClientFieldData
from hummingbot.connector.utils import split_hb_trading_pair
from hummingbot.core.data_type.trade_fee import TradeFeeSchema

# Bybit fees: https://help.bybit.com/hc/en-us/articles/360039261154
DEFAULT_FEES = TradeFeeSchema(
    maker_percent_fee_decimal=Decimal("0.0006"),
    taker_percent_fee_decimal=Decimal("0.0001"),
)

# Kraken Perp Symbols:
# Docs URL: https://support.kraken.com/hc/en-us/articles/360022835891-Ticker-symbols
# Ticker symbols are defined as:
# <Product Code>_<Currency Pair>_<Maturity Date (if applicable)>
#
# Ticker Code Segment and Explanation
# <Product Code>
# FI = Fixed Maturity Inverse Futures
# PI = Perpetual Inverse Futures
# FF = Fixed Maturity Linear Futures
# PF = Perpetual Linear Multi-Collateral Futures
# IN = Real Time Index
# RR = Reference Rate
#
# <Currency Pair>
# <Numerator Currency><Denominator Currency>
#
# <Maturity Date>
# <YYMMDD> (If Applicable)

CENTRALIZED = True

EXAMPLE_PAIR = "BTC-USD"


def is_exchange_information_valid(exchange_info: Dict[str, Any]) -> bool:
    """
    Verifies if a trading pair is enabled to operate with based on its exchange information

    :param exchange_info: the exchange information for a trading pair

    :return: True if the trading pair is enabled, False otherwise
    """
    suspended = exchange_info.get("suspended")
    symbol = exchange_info.get("symbol")
    sd = get_symbol_details(symbol)
    valid = all([
        suspended is not None,
        suspended is False,
        is_perpetual_inverse(sd["product_code"])
    ])
    return valid


def get_linear_non_linear_split(trading_pairs: List[str]) -> Tuple[List[str], List[str]]:
    linear_trading_pairs = []
    non_linear_trading_pairs = []
    for trading_pair in trading_pairs:
        if is_linear_perpetual(trading_pair):
            linear_trading_pairs.append(trading_pair)
        else:
            non_linear_trading_pairs.append(trading_pair)
    return linear_trading_pairs, non_linear_trading_pairs

def get_symbol_details(symbol: str) -> Dict[str, Any]:
    product_code = currency_pair = maturity_date = ""
    symbol_info = symbol.split("_")
    symbol_info_length = len(symbol_info)
    if symbol_info_length not in [3,2]:
        raise
    if symbol_info_length == 3:
        product_code = symbol_info[0]
        if not is_fixed_maturity(product_code):
           raise
        currency_pair = symbol_info[1]
        maturity_date = symbol_info[2]
    if symbol_info_length == 2:
        product_code = symbol_info[0]
        if not any([
            is_perpetual(product_code),
            is_realtime_index(product_code),
            is_reference_rate(product_code),
        ]):
           print(symbol)
           raise
        currency_pair = symbol_info[1]
        maturity_date = None
    return {
        "product_code": product_code,
        "currency_pair": currency_pair,
        "maturity_date": maturity_date,
    }


def is_perpetual(product_code: str) -> bool:
    return product_code in ["PI", "PF"]

def is_perpetual_inverse(product_code: str) -> bool:
    return product_code == "PI"

def is_perpetual_linear_multi_collateral_futures(product_code: str) -> bool:
    return product_code == "PF"

def is_fixed_maturity(product_code: str) -> bool:
    return product_code in ["FF", "FI"]

def is_realtime_index(product_code: str) -> bool:
    return product_code.upper() == "IN"

def is_reference_rate(product_code: str) -> bool:
    return product_code.upper() == "RR"

def is_linear_perpetual(trading_pair: str) -> bool:
    """
    Returns True if trading_pair is in USDT(Linear) Perpetual
    """
    _, quote_asset = split_hb_trading_pair(trading_pair)
    return quote_asset == "USDT"


def get_next_funding_timestamp(current_timestamp: float) -> float:
    # On ByBit Perpetuals, funding occurs every 8 hours at 00:00UTC, 08:00UTC and 16:00UTC.
    # Reference: https://help.bybit.com/hc/en-us/articles/360039261134-Funding-fee-calculation
    int_ts = int(current_timestamp)
    eight_hours = 8 * 60 * 60
    mod = int_ts % eight_hours
    return float(int_ts - mod + eight_hours)


class KrakenPerpetualConfigMap(BaseConnectorConfigMap):
    connector: str = Field(default="kraken_perpetual", client_data=None)
    kraken_perpetual_api_key: SecretStr = Field(
        default=...,
        client_data=ClientFieldData(
            prompt=lambda cm: "Enter your Kraken Perpetual API key",
            is_secure=True,
            is_connect_key=True,
            prompt_on_new=True,
        )
    )
    kraken_perpetual_secret_key: SecretStr = Field(
        default=...,
        client_data=ClientFieldData(
            prompt=lambda cm: "Enter your Kraken Perpetual secret key",
            is_secure=True,
            is_connect_key=True,
            prompt_on_new=True,
        )
    )

    class Config:
        title = "kraken_perpetual"


KEYS = KrakenPerpetualConfigMap.construct()

OTHER_DOMAINS = ["kraken_perpetual_testnet"]
OTHER_DOMAINS_PARAMETER = {"kraken_perpetual_testnet": "kraken_perpetual_testnet"}
OTHER_DOMAINS_EXAMPLE_PAIR = {"kraken_perpetual_testnet": "BTC-USDT"}
OTHER_DOMAINS_DEFAULT_FEES = {
    "kraken_perpetual_testnet": TradeFeeSchema(
        maker_percent_fee_decimal=Decimal("-0.00025"),
        taker_percent_fee_decimal=Decimal("0.00075"),
    )
}


class KrakenPerpetualTestnetConfigMap(BaseConnectorConfigMap):
    connector: str = Field(default="kraken_perpetual_testnet", client_data=None)
    kraken_perpetual_testnet_api_key: SecretStr = Field(
        default=...,
        client_data=ClientFieldData(
            prompt=lambda cm: "Enter your Kraken Perpetual Testnet API key",
            is_secure=True,
            is_connect_key=True,
            prompt_on_new=True,
        )
    )
    kraken_perpetual_testnet_secret_key: SecretStr = Field(
        default=...,
        client_data=ClientFieldData(
            prompt=lambda cm: "Enter your Kraken Perpetual Testnet secret key",
            is_secure=True,
            is_connect_key=True,
            prompt_on_new=True,
        )
    )

    class Config:
        title = "kraken_perpetual_testnet"


OTHER_DOMAINS_KEYS = {
    "kraken_perpetual_testnet": KrakenPerpetualTestnetConfigMap.construct()
}

from hummingbot.core.data_type.common import OrderType, PositionMode

from hummingbot.core.data_type.in_flight_order import OrderState

EXCHANGE_NAME = "kraken_perpetual"

DEFAULT_DOMAIN = "kraken_perpetual_main"

DEFAULT_TIME_IN_FORCE = "GoodTillCancel"
SERVER_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

REST_URLS = {
    "kraken_perpetual_main": "https://futures.kraken.com/derivatives/api/",
    "kraken_perpetual_testnet": "https://demo-futures.kraken.com/derivatives/api/",
}

REST_LINEAR_URLS = {
    "kraken_perpetual_main": "https://api.futures.kraken.com/",
    "kraken_perpetual_testnet": "https://api.demo-futures.kraken.com/",
}

WSS_NON_LINEAR_PUBLIC_URLS = {
    "kraken_perpetual_main": "wss://futures.kraken.com/ws/v1/",
    "kraken_perpetual_testnet": "wss://demo-futures.kraken.com/ws/v1/",
}
WSS_NON_LINEAR_PRIVATE_URLS = WSS_NON_LINEAR_PUBLIC_URLS

WSS_LINEAR_PUBLIC_URLS = {
    "kraken_perpetual_main": "wss://api.futures.kraken.com",
    "kraken_perpetual_testnet": "wss://api.demo-futures.kraken.com",
}
WSS_LINEAR_PRIVATE_URLS = WSS_LINEAR_PUBLIC_URLS

REST_API_VERSION = "v3"

HBOT_BROKER_ID = "Hummingbot"

MAX_ID_LEN = 36
SECONDS_TO_WAIT_TO_RECEIVE_MESSAGE = 30
POSITION_IDX_ONEWAY = 0
POSITION_IDX_HEDGE_BUY = 1
POSITION_IDX_HEDGE_SELL = 2

ORDER_TYPE_MAP = {
    OrderType.LIMIT: "Limit",
    OrderType.MARKET: "Market",
}

POSITION_MODE_API_ONEWAY = "MergedSingle"
POSITION_MODE_API_HEDGE = "BothSide"
POSITION_MODE_MAP = {
    PositionMode.ONEWAY: POSITION_MODE_API_ONEWAY,
    PositionMode.HEDGE: POSITION_MODE_API_HEDGE,
}

# REST API Public Endpoints
LINEAR_MARKET = "linear"
NON_LINEAR_MARKET = "non_linear"

LATEST_SYMBOL_INFORMATION_ENDPOINT = {
    LINEAR_MARKET: f"{REST_API_VERSION}/tickers",
    NON_LINEAR_MARKET: f"{REST_API_VERSION}/tickers",
}
QUERY_SYMBOL_ENDPOINT = {
    LINEAR_MARKET: f"{REST_API_VERSION}/tickers",
    NON_LINEAR_MARKET: f"{REST_API_VERSION}/tickers",
}
ORDER_BOOK_ENDPOINT = {
    LINEAR_MARKET: f"{REST_API_VERSION}/public/orderBook/L2",
    NON_LINEAR_MARKET: f"{REST_API_VERSION}/public/orderBook/L2",
}

# FIXME: Before finding the dedicated server_time API just use tickers
# You can also get "serverTime" from /tickers
SERVER_TIME_PATH_URL = {
    LINEAR_MARKET: f"{REST_API_VERSION}/tickers",
    NON_LINEAR_MARKET: f"{REST_API_VERSION}/tickers",
}

# REST API Private Endpoints
SET_LEVERAGE_PATH_URL = {
    LINEAR_MARKET: "private/linear/position/set-leverage",
    NON_LINEAR_MARKET: f"{REST_API_VERSION}/private/position/leverage/save",
}
GET_LAST_FUNDING_RATE_PATH_URL = {
    LINEAR_MARKET: "private/linear/funding/prev-funding",
    NON_LINEAR_MARKET: f"{REST_API_VERSION}/private/funding/prev-funding",
}
GET_PREDICTED_FUNDING_RATE_PATH_URL = {
    LINEAR_MARKET: "/private/linear/funding/predicted-funding",
    NON_LINEAR_MARKET: f"{REST_API_VERSION}/private/funding/predicted-funding",
}
GET_POSITIONS_PATH_URL = {
    LINEAR_MARKET: "private/linear/position/list",
    NON_LINEAR_MARKET: f"{REST_API_VERSION}/private/position/list",
}
PLACE_ACTIVE_ORDER_PATH_URL = {
    LINEAR_MARKET: "private/linear/order/create",
    NON_LINEAR_MARKET: f"{REST_API_VERSION}/private/order/create",
}
CANCEL_ACTIVE_ORDER_PATH_URL = {
    LINEAR_MARKET: "private/linear/order/cancel",
    NON_LINEAR_MARKET: f"{REST_API_VERSION}/private/order/cancel",
}
CANCEL_ALL_ACTIVE_ORDERS_PATH_URL = {
    LINEAR_MARKET: "private/linear/order/cancelAll",
    NON_LINEAR_MARKET: f"{REST_API_VERSION}/private/order/cancelAll",
}
QUERY_ACTIVE_ORDER_PATH_URL = {
    LINEAR_MARKET: "private/linear/order/search",
    NON_LINEAR_MARKET: f"{REST_API_VERSION}/private/order",
}
USER_TRADE_RECORDS_PATH_URL = {
    LINEAR_MARKET: "private/linear/trade/execution/list",
    NON_LINEAR_MARKET: f"{REST_API_VERSION}/private/execution/list",
}
GET_WALLET_BALANCE_PATH_URL = {
    LINEAR_MARKET: f"{REST_API_VERSION}/accounts",
    NON_LINEAR_MARKET: f"{REST_API_VERSION}/accounts",
}
SET_POSITION_MODE_URL = {LINEAR_MARKET: "private/linear/position/switch-mode"}

# Funding Settlement Time Span
FUNDING_SETTLEMENT_DURATION = (5, 5)  # seconds before snapshot, seconds after snapshot

# WebSocket Public Endpoints
WS_PING_REQUEST = "ping"
WS_ORDER_BOOK_EVENTS_TOPIC = "orderBook_200.100ms"
WS_TRADES_TOPIC = "trade"
WS_INSTRUMENTS_INFO_TOPIC = "instrument_info.100ms"
WS_AUTHENTICATE_USER_ENDPOINT_NAME = "auth"
WS_SUBSCRIPTION_POSITIONS_ENDPOINT_NAME = "position"
WS_SUBSCRIPTION_ORDERS_ENDPOINT_NAME = "order"
WS_SUBSCRIPTION_EXECUTIONS_ENDPOINT_NAME = "execution"
WS_SUBSCRIPTION_WALLET_ENDPOINT_NAME = "wallet"

# Order Statuses
ORDER_STATE = {
    "Created": OrderState.OPEN,
    "New": OrderState.OPEN,
    "Filled": OrderState.FILLED,
    "PartiallyFilled": OrderState.PARTIALLY_FILLED,
    "Cancelled": OrderState.CANCELED,
    "PendingCancel": OrderState.PENDING_CANCEL,
    "Rejected": OrderState.FAILED,
}

GET_LIMIT_ID = "GETLimit"
POST_LIMIT_ID = "POSTLimit"
GET_RATE = 49  # per second
POST_RATE = 19  # per second

NON_LINEAR_PRIVATE_BUCKET_100_LIMIT_ID = "NonLinearPrivateBucket100"
NON_LINEAR_PRIVATE_BUCKET_600_LIMIT_ID = "NonLinearPrivateBucket600"
NON_LINEAR_PRIVATE_BUCKET_75_LIMIT_ID = "NonLinearPrivateBucket75"
NON_LINEAR_PRIVATE_BUCKET_120_B_LIMIT_ID = "NonLinearPrivateBucket120B"
NON_LINEAR_PRIVATE_BUCKET_120_C_LIMIT_ID = "NonLinearPrivateBucket120C"

LINEAR_PRIVATE_BUCKET_100_LIMIT_ID = "LinearPrivateBucket100"
LINEAR_PRIVATE_BUCKET_600_LIMIT_ID = "LinearPrivateBucket600"
LINEAR_PRIVATE_BUCKET_75_LIMIT_ID = "LinearPrivateBucket75"
LINEAR_PRIVATE_BUCKET_120_A_LIMIT_ID = "LinearPrivateBucket120A"

# Request error codes
RET_CODE_OK = 0
RET_CODE_PARAMS_ERROR = 10001
RET_CODE_API_KEY_INVALID = 10003
RET_CODE_AUTH_TIMESTAMP_ERROR = 10021
RET_CODE_ORDER_NOT_EXISTS = 20001
RET_CODE_MODE_POSITION_NOT_EMPTY = 30082
RET_CODE_MODE_NOT_MODIFIED = 30083
RET_CODE_MODE_ORDER_NOT_EMPTY = 30086
RET_CODE_API_KEY_EXPIRED = 33004
RET_CODE_LEVERAGE_NOT_MODIFIED = 34036
RET_CODE_POSITION_ZERO = 130125

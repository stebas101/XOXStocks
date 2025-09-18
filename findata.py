import yfinance as yf
import requests_cache


# def get_session() -> object:
#     session = requests_cache.CachedSession('yfinance.cache')
#     session.headers['User-agent'] = 'xoxstocks/0.1'
    
#     return session


def get_stock_info(symbol: str) -> dict:
    # session = get_session()
    # ticker = yf.Ticker(symbol, session=session)
    ticker = yf.Ticker(symbol)
    info: dict = ticker.get_info()
    
    return {'name'      : info.get('shortName'),
            'sector'    : info.get('sector'),
            'industry'  : info.get('industry'),
            'exchange'  : info.get('exchange'),
            }
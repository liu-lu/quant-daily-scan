import pandas as pd
from xbbg import blp
from datetime import datetime, timedelta
import sys

class BloombergProvider:
    """
    Data Access Object (DAO) for Bloomberg.
    Handles connection, fetching, and basic cleaning.
    """
    def __init__(self, lookback_days=90):
        self.lookback_days = lookback_days

    def fetch_history(self, ticker_list: list) -> pd.DataFrame:
        """
        批量获取历史数据。
        为了通用性，同时拉取价格(PX_LAST)和收益率(YLD_YTM_MID)。
        """
        start_date = datetime.now().date() - timedelta(days=self.lookback_days)
        print(f"   [Data] Fetching history for {len(ticker_list)} assets from Bloomberg...")

        try:
            # 尝试同时获取不同字段，xbbg会自动处理有效性
            df = blp.bdh(
                tickers=ticker_list,
                flds=['PX_LAST', 'YLD_YTM_MID', 'OAS_SPREAD_BID'],
                start_date=start_date,
                end_date=datetime.now().date()
            )
            
            if df.empty:
                print("   [Error] Bloomberg returned empty data. Check tickers or connection.")
                return pd.DataFrame()
                
            return df
            
        except Exception as e:
            print(f"   [Critical Error] BBG API Failure: {e}")
            sys.exit(1)
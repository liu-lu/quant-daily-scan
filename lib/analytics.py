import pandas as pd
import numpy as np

class MarketAnalyzer:
    """
    Business Logic Layer.
    """
    def __init__(self, z_score_window=30):
        self.window = z_score_window

    def process_portfolio(self, config_data: dict, raw_data: pd.DataFrame) -> pd.DataFrame:
        results = []
        
        for group in config_data['portfolio']:
            category = group['category']
            
            for asset in group['assets']:
                ticker = asset['ticker']
                name = asset['name']
                asset_type = asset['type']
                
                # 1. 智能选择最佳数据列 (修复了空数据问题)
                series = self._get_best_series(raw_data, ticker, asset_type)
                
                if series is None or len(series) < self.window:
                    # 仅在调试时打印跳过信息，保持界面整洁
                    # print(f"   [Skip] {name}: Insufficient history") 
                    continue

                # 2. 计算核心指标
                curr_val = series.iloc[-1]
                prev_val = series.iloc[-2]
                
                # Yield/Spread 用 bps, Price 用 %
                if asset_type in ['YIELD', 'SPREAD']:
                    # 对于利率，PX_LAST 通常已经是 % (如 4.25)，变动 0.01 是 1bp
                    change_1d = (curr_val - prev_val) * 100 
                    diff_series = series.diff()
                    unit = "bps"
                else:
                    change_1d = (curr_val / prev_val - 1) * 100
                    diff_series = series.pct_change()
                    unit = "%"
                
                # 3. Z-Score 计算
                rolling_window = diff_series.tail(self.window)
                mu = rolling_window.mean()
                sigma = rolling_window.std()
                
                z_score = (diff_series.iloc[-1] - mu) / sigma if sigma != 0 else 0
                
                # 4. 趋势判断 (用于生成 Emoji)
                trend = "FLAT"
                if z_score > 1: trend = "UP"
                elif z_score < -1: trend = "DOWN"

                results.append({
                    'Category': category,
                    'Ticker': ticker,
                    'Name': name,
                    'Last': curr_val,
                    'Chg_1D': change_1d,
                    'Unit': unit,
                    'Z_Score': z_score,
                    'Trend': trend
                })
        
        return pd.DataFrame(results)

    def _get_best_series(self, df, ticker, asset_type):
        """
        Extract the correct column. 
        Critical Fix: Check if data is actually present, not just if column exists.
        """
        # 优先级：利率优先找 YLD，找不到找 PX_LAST
        field_priority = {
            'YIELD': ['YLD_YTM_MID', 'PX_LAST', 'px_last'],
            'SPREAD': ['OAS_SPREAD_BID', 'PX_LAST', 'px_last'],
            'PRICE': ['PX_LAST', 'px_last']
        }
        
        target_fields = field_priority.get(asset_type, ['PX_LAST'])
        
        for fld in target_fields:
            if (ticker, fld) in df.columns:
                series = df[(ticker, fld)].dropna()
                # [Fix] 必须确保 Series 不为空，且长度足够
                if not series.empty and len(series) > 5:
                    return series
        return None
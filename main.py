import yaml
import sys
from lib.data_loader import BloombergProvider
from lib.analytics import MarketAnalyzer
from lib.reporter import NotionRenderer

CONFIG_FILE = 'config.yaml'

def load_config(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"[Error] Failed to load config file: {e}")
        sys.exit(1)

def main():
    print(">>> Starting Daily Market Scan...")
    
    # 1. Load Configuration
    config = load_config(CONFIG_FILE)
    
    # Extract just the ticker list
    all_tickers = []
    for group in config['portfolio']:
        for asset in group['assets']:
            all_tickers.append(asset['ticker'])
            
    # 2. Fetch Data (90天回溯，确保数据足够)
    provider = BloombergProvider(lookback_days=90)
    raw_data = provider.fetch_history(all_tickers)
    
    # 3. Analyze Data
    analyzer = MarketAnalyzer(z_score_window=30)
    metrics_df = analyzer.process_portfolio(config, raw_data)
    
    # 4. Generate & Save Report
    NotionRenderer.render(metrics_df)

if __name__ == "__main__":
    main()
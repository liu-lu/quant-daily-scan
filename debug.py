from lib.data_loader import BloombergProvider
import yaml
import pandas as pd

# 强制显示所有列，防止被省略
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.width', 1000)

def debug_run():
    print(">>> 🛠️ Starting Debug Mode...")

    # 1. 模拟加载配置 (取前两个作为测试)
    tickers = ['USGG10YR Index', 'EURUSD Curncy'] 
    print(f"1. Target Tickers: {tickers}")

    # 2. 尝试抓取数据
    provider = BloombergProvider(lookback_days=10)
    df = provider.fetch_history(tickers)

    # 3. 诊断输出
    print("\n" + "="*30)
    print("DATA DIAGNOSTICS")
    print("="*30)
    
    if df.empty:
        print("❌ RAW DATA IS EMPTY! (Check connection or permissions)")
    else:
        print("✅ Raw Data Fetched Successfully!")
        print(f"Shape: {df.shape}")
        
        print("\n--- [CRITICAL] Column Names Check ---")
        # 打印列名元组，检查大小写
        print(df.columns.tolist()) 
        
        print("\n--- Data Head (First 3 rows) ---")
        print(df.head(3))
        
        print("\n--- Data Tail (Last 3 rows) ---")
        print(df.tail(3))
        
        # 4. 模拟匹配测试
        print("\n--- [TEST] Matching Logic ---")
        test_col_upper = ('USGG10YR Index', 'PX_LAST')
        test_col_lower = ('USGG10YR Index', 'px_last')
        
        if test_col_upper in df.columns:
            print(f"✅ Found exact match: {test_col_upper}")
        elif test_col_lower in df.columns:
            print(f"⚠️ Found lowercase match: {test_col_lower} (Code needs update!)")
        else:
            print(f"❌ Match Failed for both. Available keys: {[x[1] for x in df.columns if x[0] == 'USGG10YR Index']}")

if __name__ == "__main__":
    debug_run()
import pandas as pd
from datetime import datetime

class NotionRenderer:
    """
    Presentation Layer.
    Formats the data into Markdown for Notion.
    """
    @staticmethod
    def render(df: pd.DataFrame):
        if df.empty:
            print("No data to render.")
            return

        print("\n" + "="*50)
        print(f"🚀 DAILY MARKET SCAN | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("="*50 + "\n")
        
        # 1. 异常高亮区 (Dislocations)
        # 筛选 Z-Score 绝对值 > 1.96 的资产
        dislocations = df[df['Z_Score'].abs() > 1.96].copy()
        
        print("### 🚨 High Volatility Alerts (2-Sigma)")
        if not dislocations.empty:
            dislocations = dislocations.sort_values(by='Z_Score', ascending=False)
            print("| Asset | Level | 1D Change | Z-Score | Status |")
            print("|---|---|---|---|---|")
            for _, row in dislocations.iterrows():
                icon = "🔥" if row['Z_Score'] > 0 else "❄️" # 火热上涨 or 急剧下跌
                chg_str = f"{row['Chg_1D']:+.1f} {row['Unit']}"
                print(f"| {row['Name']} | {row['Last']:.4f} | {chg_str} | **{row['Z_Score']:.2f}** | {icon} |")
        else:
            print("> *No significant dislocations detected (>2σ).*")

        # 2. 全景监控区 (Market Overview)
        print("\n### 📋 Sector Overview")
        grouped = df.groupby('Category')
        
        for name, group in grouped:
            print(f"\n**{name}**")
            print("| Asset | Level | 1D Change | Z-Score |")
            print("|---|---|---|---|")
            for _, row in group.iterrows():
                chg_str = f"{row['Chg_1D']:+.1f} {row['Unit']}"
                z_str = f"{row['Z_Score']:.2f}"
                # 如果是小异常(1-2 sigma)，稍微加粗提示
                if abs(row['Z_Score']) > 1: z_str = f"*{z_str}*" 
                
                print(f"| {row['Name']} | {row['Last']:.2f} | {chg_str} | {z_str} |")
        
        print("\n" + "="*50)
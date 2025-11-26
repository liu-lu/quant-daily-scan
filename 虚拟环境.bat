# 1. 创建环境，同时安装所有基础包，并强制锁定 NumPy 版本
conda create -n quant_scan python=3.10 "numpy=1.26.4" "pandas<2.2" pyyaml openpyxl tabulate -y

# 2. 激活环境
conda activate quant_scan

# 3. 安装 Bloomberg API (blpapi) - 这一步使用官方源
# 注意：增加 --no-deps 参数，防止它自作主张去更新 numpy
python -m pip install --index-url=https://blpapi.bloomberg.com/repository/releases/python/simple/ blpapi --no-deps

# 4. 安装 xbbg - 这一步最关键
# 我们告诉 pip：安装 xbbg，但不要升级 numpy
pip install xbbg --no-build-isolation
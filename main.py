# 这是一个示例 Python 脚本。

import numpy as np
import pandas as pd

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    df = pd.read_excel("20230429193515_均重导出数据.xlsx",sheet_name="基础数据")
    writer = pd.ExcelWriter("英德公司-均重导出数据.xlsx",engine='xlsxwriter')
    


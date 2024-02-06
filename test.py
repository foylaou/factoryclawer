import pandas as pd
import os

# 设置包含.xls文件的目录
directory = r'D:\Users\user\Downloads\factoty'

# 用于存储每个文件数据的列表
dataframes = []

# 遍历目录中的每个文件
for filename in os.listdir(directory):
    if filename.endswith('.xls'):
        # 构建完整的文件路径
        filepath = os.path.join(directory, filename)
        # 读取.xls文件
        df = pd.read_excel(filepath)
        # 将读取的DataFrame添加到列表中
        dataframes.append(df)

# 合并所有DataFrame
merged_df = pd.concat(dataframes, ignore_index=True)

# （可选）保存合并后的DataFrame到新文件
output_file = 'total.xlsx'
merged_df.to_excel(output_file, index=False)

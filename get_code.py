import glob
import re

# 定位本地所有的 Loop_21 pkl 文件
pkl_files = glob.glob('log/*/Loop_21/**/*.pkl', recursive=True)
print(f"🔍 找到 {len(pkl_files)} 个 Loop 21 的数据文件，正在进行二进制深度扫描...\n")

code_blocks = set()

for file_path in pkl_files:
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            # 利用正则匹配：从 import pandas 开始，到 return result 结束的代码块
            matches = re.finditer(rb'(import pandas.*?def calculate_[a-zA-Z0-9_]+\(.*?(?:return result|print\(result\)))', data, re.DOTALL)
            
            for match in matches:
                # 提取并过滤掉乱码
                code = match.group(1).decode('utf-8', 'ignore')
                code_blocks.add(code)
    except Exception as e:
        pass

if not code_blocks:
    print("❌ 未能在文件中找到完整的源码特征，请确认文件是否完整。")
else:
    for i, code in enumerate(code_blocks):
        print(f"{'='*50}\n【原生源码提取成功 - 模块 {i+1}】\n{'='*50}")
        print(code)
        print("\n")

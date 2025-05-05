from bs4 import BeautifulSoup
import pandas as pd

# 读取你的 HTML 文件
with open('DataLoader\TP.HTML', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 用 BeautifulSoup 解析
soup = BeautifulSoup(html_content, 'lxml')

# 找出所有 <nobr> 标签
nobr_tags = soup.find_all('nobr')

# 提取 Technischer Platz 和 Beschreibung
data = []
current_number = None

for tag in nobr_tags:
    text = tag.get_text(strip=True)
    if not text:
        continue

    # Technischer Platz编号：一般是数字开头或者带"-"（比如6200-GB-EUR）
    if text[0].isdigit():
        current_number = text
    elif current_number:
        # 当前有编号且读到了描述
        data.append((current_number, text))
        current_number = None  # 匹配一次，清空等待下一个

# 转成 DataFrame
df = pd.DataFrame(data, columns=["Technischer Platz", "Beschreibung"])

# 输出查看
print(df.head(100))

# 可保存成Excel
df.to_excel('exported_tplnr_list.xlsx', index=False)

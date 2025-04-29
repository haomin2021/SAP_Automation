import os
import ssl
from transformers import pipeline
import torch
import urllib3

# 跳过证书验证（适用于 requests + urllib3）
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings()

# 禁用 transformers 中的 SSL 校验
os.environ["TRUSTSTORE_DISABLE"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "info"
os.environ["HF_HUB_DISABLE_SSL_VERIFICATION"] = "1"

# 创建摘要生成器
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

text = """
Transportbänder auf Verschleiß geprüft, ggf. als offene Reperatur aufgenommen.
Magnet am Plunger gereinigt, Führungsstangen gereinigt und gefettet,
bei sichtbaren Verschleispuren die Führungstangen ausbauen und um 180° gedreht wieder einbauen.
Über die eingebaute Zentralschmierung komplette Anlage abgeschmiert, Restfettmengen mit Lappen abgerieben.
"""

# 生成摘要
summary = summarizer(text, max_length=60, min_length=20, do_sample=False)

print(summary[0]['summary_text'])

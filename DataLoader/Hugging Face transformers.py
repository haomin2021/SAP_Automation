from transformers import pipeline

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

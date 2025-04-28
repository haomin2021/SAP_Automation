from keybert import KeyBERT

kw_model = KeyBERT(model="thenlper/gte-small")

text = """
Transportbänder auf Verschleiß geprüft, ggf. als offene Reperatur aufgenommen. 		
Magnet am Plunger gereinigt, Führungsstangen gereinigt und gefettet, bei sichtbaren Verschleispuren die Führungstangen ausbauen und um 180° gedreht wieder einbauen,		
Über die eingebaute Zentralschmierung komplette Anlage abgeschmiert, Restfettmengen mit Lappen abgerieben,		
"""

# 提取前5个关键词组
keywords = kw_model.extract_keywords(text, top_n=5)

for kw in keywords:
    print(kw)

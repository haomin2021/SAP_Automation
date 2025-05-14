import tkinter as tk
from tkinter import filedialog, ttk
from bs4 import BeautifulSoup
import pandas as pd

def parse_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')
    nobr_tags = soup.find_all('nobr')

    data = []
    current_number = None
    for tag in nobr_tags:
        text = tag.get_text(strip=True)
        if not text:
            continue
        if text[0].isdigit():
            current_number = text
        elif current_number:
            data.append((current_number, text))
            current_number = None
    return data

def browse_html():
    filepath = filedialog.askopenfilename(filetypes=[("HTML files", "*.html *.htm")])
    if not filepath:
        return

    # 解析 HTML 内容
    records = parse_html_file(filepath)

    # 清空旧树
    tree.delete(*tree.get_children())

    # 加载树结构
    for platz, beschreibung in records:
        parent = tree.insert("", "end", text=platz, values=(beschreibung,))
        # 如果你希望每个 Technischer Platz 下有子描述（可展开），可以添加：
        # tree.insert(parent, "end", text=beschreibung)

def on_tree_select(event):
    selected = tree.focus()
    values = tree.item(selected, "values")
    platz = tree.item(selected, "text")
    if values:
        beschr = values[0]
        entry_tplnr.delete(0, tk.END)
        entry_tplnr.insert(0, platz)
        entry_beschr.delete(0, tk.END)
        entry_beschr.insert(0, beschr)

# UI
root = tk.Tk()
root.title("Technischer Platz Parser")

# 按钮
frame_top = tk.Frame(root)
frame_top.pack(pady=5)

btn_browse = tk.Button(frame_top, text="Browse HTML", command=browse_html)
btn_browse.pack()

# Treeview
tree = ttk.Treeview(root, columns=("Beschreibung",), show="tree headings")
tree.heading("#0", text="Technischer Platz")
tree.heading("Beschreibung", text="Beschreibung")
tree.pack(padx=10, pady=5, fill="both", expand=True)
tree.bind("<<TreeviewSelect>>", on_tree_select)

# Entry 显示选中项
frame_entry = tk.Frame(root)
frame_entry.pack(pady=5)

tk.Label(frame_entry, text="Technischer Platz:").grid(row=0, column=0, sticky="w")
entry_tplnr = tk.Entry(frame_entry, width=40)
entry_tplnr.grid(row=0, column=1, padx=5)

tk.Label(frame_entry, text="Beschreibung:").grid(row=1, column=0, sticky="w")
entry_beschr = tk.Entry(frame_entry, width=40)
entry_beschr.grid(row=1, column=1, padx=5)

root.mainloop()

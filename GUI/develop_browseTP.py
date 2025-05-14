import tkinter as tk
from tkinter import ttk, filedialog
from bs4 import BeautifulSoup


class HierarchyTreeBuilder:
    def __init__(self):
        self.tree = {}

    def insert(self, full_code, description):
        parts = full_code.split("-")
        node = self.tree
        for i, part in enumerate(parts):
            key = "-".join(parts[:i+1])
            if key not in node:
                node[key] = {"children": {}, "desc": ""}
            if i == len(parts) - 1:
                node[key]["desc"] = description
            node = node[key]["children"]

    def get_tree(self):
        return self.tree


class TechnischerPlatzViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Technischer Platz Tree - Tkinter")
        self.geometry("800x600")

        self.button = tk.Button(self, text="Load HTML", command=self.load_html)
        self.button.pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("Beschreibung",), show="tree headings")
        self.tree.heading("#0", text="Technischer Platz")
        self.tree.heading("Beschreibung", text="Beschreibung")
        self.tree.pack(expand=True, fill="both")

        # 设置可滚动
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def load_html(self):
        path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html *.htm")])
        if not path:
            return

        platz_data = self.parse_html(path)
        builder = HierarchyTreeBuilder()
        for code, desc in platz_data:
            builder.insert(code, desc)

        self.tree.delete(*self.tree.get_children())
        self.populate_tree(builder.get_tree(), "")

    def parse_html(self, filepath):
        with open(filepath, encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'lxml')

        nobr_tags = soup.find_all('nobr')
        data = []
        current_code = None
        for tag in nobr_tags:
            text = tag.get_text(strip=True)
            if not text:
                continue
            if text[0].isdigit():
                current_code = text
            elif current_code:
                data.append((current_code, text))
                current_code = None
        return data

    def populate_tree(self, node_dict, parent_id):
        for key, value in node_dict.items():
            desc = value["desc"]
            children = value["children"]
            item_id = self.tree.insert(parent_id, "end", text=key, values=(desc,))
            self.populate_tree(children, item_id)


if __name__ == '__main__':
    app = TechnischerPlatzViewer()
    app.mainloop()

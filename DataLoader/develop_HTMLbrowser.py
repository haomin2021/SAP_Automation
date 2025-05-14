from PyQt5.QtWidgets import (
    QApplication, QTreeWidget, QTreeWidgetItem, QFileDialog,
    QWidget, QVBoxLayout, QPushButton, QHeaderView
)
import sys
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
                node[key] = {"children": {}, "desc": None}
            node = node[key]["children"]
        node["_leaf"] = True
        node["_desc"] = description

    def get_tree(self):
        return self.tree


class TechnischerPlatzViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Technischer Platz Tree - SAP Style")
        self.resize(800, 600)

        layout = QVBoxLayout(self)

        self.load_button = QPushButton("Load HTML")
        self.load_button.clicked.connect(self.load_html)
        layout.addWidget(self.load_button)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Technischer Platz", "Beschreibung"])
        self.tree.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        layout.addWidget(self.tree)

    def load_html(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open HTML", "", "HTML Files (*.html *.htm)")
        if not path:
            return

        platz_data = self.parse_html(path)

        builder = HierarchyTreeBuilder()
        for code, desc in platz_data:
            builder.insert(code, desc)

        self.tree.clear()
        self.populate_tree(builder.get_tree(), self.tree.invisibleRootItem())

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

    def populate_tree(self, node_dict, parent_item):
        for key, value in node_dict.items():
            if key.startswith("_"):
                continue

            desc = ""
            if "_desc" in value["children"]:
                desc = value["children"]["_desc"]

            # 判断是否为叶子节点
            is_leaf = "_leaf" in value["children"]
            final_desc = value["children"].get("_desc") if is_leaf else ""

            item = QTreeWidgetItem([key, final_desc or ""])
            item.setCheckState(0, 0)
            parent_item.addChild(item)

            self.populate_tree(value["children"], item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = TechnischerPlatzViewer()
    viewer.show()
    sys.exit(app.exec_())

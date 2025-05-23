import tkinter as tk
from tkinter import ttk, messagebox
from bs4 import BeautifulSoup
import os
import datetime

# Helper class to build a hierarchical tree from Technischer Platz codes
class HierarchyTreeBuilder:
    def __init__(self):
        self.tree = {}  # Root of the tree

    def insert(self, full_code, description):
        # Split the code into hierarchical parts
        parts = full_code.split("-")
        node = self.tree
        for i, part in enumerate(parts):
            key = "-".join(parts[:i+1])  # Rebuild the hierarchical key step by step
            if key not in node:
                node[key] = {"children": {}, "desc": ""}
            if i == len(parts) - 1:
                node[key]["desc"] = description  # Set description at leaf node
            node = node[key]["children"]  # Traverse deeper into the tree

    def get_tree(self):
        return self.tree  # Return the full tree structure


# Main GUI class for viewing the Technischer Platz hierarchy
class TechnischerPlatzViewer(tk.Toplevel):
    def __init__(self, master=None, on_select=None, html_path=""):
        super().__init__(master)
        self.on_select = on_select  # Optional callback when an item is selected
        self.html_path = html_path  # Path to the HTML file
        self.title("Select Technischer Platz")
        self.geometry("800x600")

        # Label to display HTML file timestamp
        self.file_info_label = tk.Label(self, text="", fg='grey')
        self.file_info_label.pack(pady=(5, 0))

        # Button to load an HTML file
        self.button = tk.Button(self, text="Reload Data from SAP", command=self.refresh_data)
        self.button.pack(pady=(0, 8))

        # TreeView widget with one additional column for description
        self.tree = ttk.Treeview(self, columns=("Beschreibung",), show="tree headings")
        self.tree.heading("#0", text="Technischer Platz")  # Main tree column
        self.tree.heading("Beschreibung", text="Beschreibung")  # Description column
        self.tree.pack(expand=True, fill="both")

        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Bind double-click event to item selection
        self.tree.bind("<Double-1>", self.on_item_select)

        # Load initial data
        if not os.path.exists(self.html_path):
            messagebox.showwarning("File Not Found", f"HTML file not found at {self.html_path}\nReloading data from SAP.")
            self.refresh_data()
        else:
            self.load_from_file(self.html_path)

        # Update file info label with last modified time
        self.update_file_info()

    def load_from_file(self, path):
        # Parse and build the hierarchy
        platz_data = self.parse_html(path)
        builder = HierarchyTreeBuilder()
        for code, desc in platz_data:
            builder.insert(code, desc)

        # Clear current tree and populate with new data
        self.tree.delete(*self.tree.get_children())
        self.populate_tree(builder.get_tree(), "")

        self.update_file_info()  # Update the file info label

    # Get the last modified time of the HTML file
    def update_file_info(self):
        if os.path.exists(self.html_path):
            last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(self.html_path))
            self.file_info_label.config(text=f"Last updated: {last_modified.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            self.file_info_label.config(text="File not found.")

    def refresh_data(self):
        from SAP.sap_interface import SAPSession
        from SAP.IH01 import IH01Transaction
        # Ask for confirmation before reloading
        if not messagebox.askyesno("Confirm Refresh", "This will overwrite the current data file.\nDo you want to continue?"):
            return

        try:
            # Refresh data from SAP
            sap = SAPSession()
            ih01 = IH01Transaction(sap.session)
            ih01.export_html(
                save_dir=os.path.dirname(os.path.abspath(self.html_path)),
                tplnr="6200",  # Example Technischer Platz
                filename=os.path.basename(self.html_path)
            )
            self.load_from_file(self.html_path)  # Reload the data into the tree
            self.update_file_info()  # Update the file info label
            messagebox.showinfo("Info", "Data reloaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reload data:\n{str(e)}")

    def parse_html(self, filepath):
        # Parse the HTML file to extract Technischer Platz and Beschreibung
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
                current_code = text  # Likely a Technischer Platz code
            elif current_code:
                data.append((current_code, text))  # Pair with the following description
                current_code = None  # Reset for next pair
        return data

    def populate_tree(self, node_dict, parent_id):
        # Recursively populate the TreeView with hierarchical data
        for key, value in node_dict.items():
            desc = value["desc"]
            children = value["children"]
            item_id = self.tree.insert(parent_id, "end", text=key, values=(desc,))
            self.populate_tree(children, item_id)

    def on_item_select(self, event):
        # Handle double-click event to select a Technischer Platz
        item_id = self.tree.selection()
        if not item_id:
            return
        item_id = item_id[0]
        tp_code = self.tree.item(item_id, "text")
        if self.on_select:
            self.on_select(tp_code)  # Call the callback with the selected code
        self.destroy()  # Close the viewer window

def get_tp_html_path():
    # Get the path to the HTML file
    current_dir = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(current_dir, "..", "Resources", "TechnischerPlatz", "TP_data.html"))


#################### Example Usage ####################
if __name__ == '__main__':
    def on_platz_selected(tp_code):
        print(f"✅ Selected Technischer Platz: {tp_code}")

    html_file = get_tp_html_path()
    app = TechnischerPlatzViewer(on_select=on_platz_selected, html_path=html_file)
    app.mainloop()
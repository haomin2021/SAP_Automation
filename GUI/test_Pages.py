import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("多页面示例")

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.pages = {}

        for PageClass in (HomePage, ConfigPage):
            page = PageClass(self.container, self)
            self.pages[PageClass] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_page(HomePage)

    def show_page(self, page_class):
        page = self.pages[page_class]
        page.tkraise()

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="这是首页").pack(pady=10)
        tk.Button(self, text="跳转到设置页", command=lambda: controller.show_page(ConfigPage)).pack()

class ConfigPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="这是设置页").pack(pady=10)
        tk.Button(self, text="返回首页", command=lambda: controller.show_page(HomePage)).pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()
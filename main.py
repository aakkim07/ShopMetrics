import tkinter as tk
from tkinter import ttk
import random
import statistics
import math

BG = '#f5f6fa'
WHITE = '#ffffff'
TEXT = '#253047'
GRAY = '#69758a'
BLUE = '#5278d8'
GREEN = '#38a789'
BORDER = '#dfe4ed'


def calculate_discount(price):
    return price * 0.8


def generate_prices():
    prices = [round(random.uniform(10, 250), 2) for _ in range(50)]
    prices.sort()
    return prices


class ShopMetrics(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('ShopMetrics - Analýza cien')
        self.geometry('950x700')
        self.minsize(800, 620)
        self.configure(bg=BG)
        self.prices = []
        self.new_prices = []
        self.create_interface()
        self.generate()

    def create_interface(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TEntry', padding=7, font=('Segoe UI', 11))

        container = tk.Frame(self, bg=BG, padx=25, pady=20)
        container.pack(fill='both', expand=True)

        header = tk.Frame(container, bg=BG)
        header.pack(fill='x', pady=(0, 16))
        tk.Label(header, text='ShopMetrics', font=('Segoe UI', 22, 'bold'), bg=BG, fg=TEXT).pack(anchor='w')
        tk.Label(header, text='Jednoduchá analýza cien produktov', font=('Segoe UI', 11), bg=BG, fg=GRAY).pack(anchor='w', pady=(3, 0))

        statistics_frame = tk.LabelFrame(container, text=' Štatistika cien ', font=('Segoe UI', 11, 'bold'), bg=WHITE, fg=TEXT, padx=15, pady=12, bd=1, relief='solid')
        statistics_frame.pack(fill='x', pady=(0, 12))
        for i in range(4):
            statistics_frame.columnconfigure(i, weight=1)

        self.stat_labels = []
        titles = ['Počet produktov', 'Najnižšia cena', 'Najvyššia cena', 'Priemerná cena']
        for i, title in enumerate(titles):
            tk.Label(statistics_frame, text=title, font=('Segoe UI', 10), bg=WHITE, fg=GRAY).grid(row=0, column=i, pady=(0, 5))
            value = tk.Label(statistics_frame, text='-', font=('Segoe UI', 17, 'bold'), bg=WHITE, fg=BLUE)
            value.grid(row=1, column=i)
            self.stat_labels.append(value)

        button_frame = tk.Frame(container, bg=BG)
        button_frame.pack(fill='x', pady=(0, 10))
        tk.Button(button_frame, text='Generovať nové ceny', command=self.generate, font=('Segoe UI', 10, 'bold'), bg=BLUE, fg=WHITE, activebackground='#4165c0', activeforeground=WHITE, relief='flat', padx=18, pady=8, cursor='hand2').pack(side='left')
        tk.Label(button_frame, text='50 náhodných cien od 10 € do 250 €', font=('Segoe UI', 10), bg=BG, fg=GRAY).pack(side='right')

        calculator = tk.LabelFrame(container, text=' Kalkulačka zľavy ', font=('Segoe UI', 11, 'bold'), bg=WHITE, fg=TEXT, padx=15, pady=11, bd=1, relief='solid')
        calculator.pack(side='bottom', fill='x')

        row = tk.Frame(calculator, bg=WHITE)
        row.pack(fill='x')
        tk.Label(row, text='Cena produktu (€):', font=('Segoe UI', 11), bg=WHITE, fg=TEXT).pack(side='left', padx=(0, 12))
        self.entry = ttk.Entry(row, width=17, font=('Segoe UI', 12))
        self.entry.pack(side='left', ipady=4)
        self.entry.bind('<Return>', lambda event: self.calculate())
        tk.Button(row, text='Vypočítať', command=self.calculate, font=('Segoe UI', 10, 'bold'), bg=BLUE, fg=WHITE, activebackground='#4165c0', activeforeground=WHITE, relief='flat', padx=20, pady=9, cursor='hand2').pack(side='left', padx=15)

        self.result = tk.Label(calculator, text='', font=('Segoe UI', 12, 'bold'), bg=WHITE, fg=GREEN)
        self.result.pack(anchor='w', pady=(9, 0))
        self.savings = tk.Label(calculator, text='', font=('Segoe UI', 11), bg=WHITE, fg=TEXT)
        self.savings.pack(anchor='w', pady=(2, 0))
        tk.Label(calculator, text='Vzorec: Cena po zľave = Cena × 0,8', font=('Segoe UI', 9), bg=WHITE, fg=GRAY).pack(anchor='w', pady=(6, 0))

        graph_frame = tk.LabelFrame(container, text=' Graf porovnania cien ', font=('Segoe UI', 11, 'bold'), bg=WHITE, fg=TEXT, padx=12, pady=8, bd=1, relief='solid')
        graph_frame.pack(fill='both', expand=True, pady=(0, 12))
        legend = tk.Frame(graph_frame, bg=WHITE)
        legend.pack(fill='x')
        tk.Label(legend, text='● Pôvodná cena', font=('Segoe UI', 10), bg=WHITE, fg=BLUE).pack(side='left', padx=(5, 20))
        tk.Label(legend, text='● Cena po zľave 20 %', font=('Segoe UI', 10), bg=WHITE, fg=GREEN).pack(side='left')
        self.canvas = tk.Canvas(graph_frame, bg=WHITE, highlightthickness=0, height=200)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.bind('<Configure>', lambda event: self.draw_graph())

    def generate(self):
        self.prices = generate_prices()
        self.new_prices = [calculate_discount(price) for price in self.prices]
        values = [str(len(self.prices)), f'{min(self.prices):.2f} €', f'{max(self.prices):.2f} €', f'{statistics.mean(self.prices):.2f} €']
        for label, value in zip(self.stat_labels, values):
            label.config(text=value)
        self.draw_graph()

    def calculate(self):
        try:
            price = float(self.entry.get().strip().replace(',', '.'))
            if not math.isfinite(price) or price < 0:
                raise ValueError
            new_price = calculate_discount(price)
            savings = price - new_price
            if not math.isfinite(new_price) or not math.isfinite(savings):
                raise ValueError
            self.result.config(text=f'Cena po zľave: {new_price:.2f} €', fg=GREEN)
            self.savings.config(text=f'Ušetríte: {savings:.2f} € (20 %)')
        except (ValueError, OverflowError):
            self.result.config(text='Zadajte platnú cenu', fg='#d9534f')
            self.savings.config(text='')

    def draw_graph(self):
        if not self.prices:
            return
        canvas = self.canvas
        canvas.delete('all')
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        if width < 150 or height < 100:
            return
        left, right, top, bottom = 48, width - 15, 15, height - 35
        maximum = 300

        def get_y(value):
            return bottom - (value / maximum * (bottom - top))

        for value in range(0, 301, 50):
            y = get_y(value)
            canvas.create_line(left, y, right, y, fill='#e8ebf0')
            canvas.create_text(left - 10, y, text=str(value), fill=GRAY, anchor='e', font=('Segoe UI', 9))

        step = (right - left) / len(self.prices)
        bar_width = max(2, step * 0.3)
        for i, (old, new) in enumerate(zip(self.prices, self.new_prices)):
            x = left + i * step + step / 2
            canvas.create_rectangle(x - bar_width - 1, get_y(old), x - 1, bottom, fill=BLUE, outline='')
            canvas.create_rectangle(x + 1, get_y(new), x + bar_width + 1, bottom, fill=GREEN, outline='')

        for index in (0, 9, 19, 29, 39, 49):
            x = left + index * step + step / 2
            canvas.create_text(x, bottom + 13, text=str(index + 1), fill=GRAY, font=('Segoe UI', 9))
        canvas.create_text((left + right) / 2, height - 8, text='Produkty zoradené podľa ceny', fill=GRAY, font=('Segoe UI', 9))


if __name__ == '__main__':
    ShopMetrics().mainloop()

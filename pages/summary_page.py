import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from datetime import date
from tkinter import messagebox
import json

class SummaryPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.current_book = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Canvas + scrollbar
        canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Scrollable frame
        self.scrollable_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")

        self.scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Center wrapper
        wrapper = ttk.Frame(self.scrollable_frame, padding=30)
        wrapper.pack(expand=True)

        self.title_label = ttk.Label(wrapper, text="", font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=(10, 20))

        form_frame = ttk.Frame(wrapper)
        form_frame.pack(fill="x", expand=True)

        self.chapter_entry = ttk.Entry(form_frame)
        self.chapter_entry.insert(0, "Chapter X: Title")
        self.chapter_entry.pack(fill="x", pady=5)

        self.date_entry = ttk.Entry(form_frame)
        self.date_entry.insert(0, date.today().strftime("%d/%m/%Y"))
        self.date_entry.pack(fill="x", pady=5)

        labels = [
            "1. Key Events & Operations",
            "2. Key Figures & Agents",
            "3. Tactics & Strategies Used",
            "4. Historical & Political Context",
            "5. Notable Quotes",
            "6. Personal Insights & Questions",
            "7. Rating/Importance (Optional)"
        ]

        self.text_fields = {}

        for label in labels:
            lbl = ttk.Label(form_frame, text=label, font=("Helvetica", 11, "bold"))
            lbl.pack(anchor="w", pady=(15, 2))
            txt = tk.Text(form_frame, height=5, wrap="word", font=("Helvetica", 10))
            txt.pack(fill="both", expand=True)
            self.text_fields[label] = txt

        button_frame = ttk.Frame(wrapper)
        button_frame.pack(pady=25)

        self.save_button = ttk.Button(button_frame, text="💾 Save Entry", bootstyle="success", command=self.save_entry)
        self.save_button.pack(side="left", padx=10)

        self.back_button = ttk.Button(button_frame, text="← Back to Books", bootstyle="secondary",
                                      command=lambda: controller.show_frame("BookSelectPage"))
        self.back_button.pack(side="left", padx=10)

    def load_book(self, book):
        self.current_book = book
        self.title_label.config(text=f"📘 {book['title']}")
        self.chapter_entry.delete(0, tk.END)
        self.chapter_entry.insert(0, "Chapter X: Title")
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, date.today().strftime("%d/%m/%Y"))
        for txt in self.text_fields.values():
            txt.delete("1.0", tk.END)

    def save_entry(self):
        chapter = self.chapter_entry.get()
        date_read = self.date_entry.get()

        if not chapter:
            messagebox.showerror("Error", "Please fill the chapter title")
            return

        entry = {
            "book": self.current_book['title'],
            "date": date_read,
            "chapter": chapter
        }

        for label, txt in self.text_fields.items():
            entry[label] = txt.get("1.0", tk.END).strip()

        try:
            with open("data/summaries.json", "r") as f:
                summaries = json.load(f)
        except:
            summaries = []

        summaries.append(entry)
        with open("data/summaries.json", "w") as f:
            json.dump(summaries, f, indent=4)

        messagebox.showinfo("Saved", "✅ Summary saved!")
        self.load_book(self.current_book)

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import json

class BookSelectPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.books = self.load_books()
        self.book_images = {}

        # Title
        title = ttk.Label(self, text="📚 Select or Add a Book", font=("Helvetica", 22, "bold"))
        title.pack(pady=(30, 10))

        # Add Book Button Section
        add_btn = ttk.Button(self, text="➕ Add New Book", bootstyle="primary outline", command=self.open_add_book)
        add_btn.pack(pady=(0, 20))

        # Book Display Area (Scrollable Frame)
        self.canvas = ttk.Canvas(self, highlightthickness=0)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.scroll_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.render_books()

    def load_books(self):
        try:
            with open("data/books.json", "r") as f:
                return json.load(f)
        except:
            return []

    def save_books(self):
        with open("data/books.json", "w") as f:
            json.dump(self.books, f, indent=4)

    def render_books(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for book in self.books:
            frame = ttk.Frame(self.scrollable_frame, padding=15)
            frame.pack(pady=10, padx=20, fill="x", expand=True)

            container = ttk.Frame(frame)
            container.pack(anchor="center")

            image_path = book.get("image", "")
        try:
            img = Image.open(image_path)
            img = img.resize((140, 200))
            photo = ImageTk.PhotoImage(img)
            self.book_images[book['title']] = photo

            img_label = ttk.Label(container, image=photo)
            img_label.pack(side="left", padx=(0, 20))
        except:
            img_label = ttk.Label(container, text="[No Image]", bootstyle="secondary")
            img_label.pack(side="left", padx=(0, 20))

        title_btn = ttk.Button(
            container,
            text=book['title'],
            width=25,
            bootstyle="info outline",
            command=lambda b=book: self.controller.open_summary_page(b)
        )
        title_btn.pack(side="left", ipadx=5, ipady=5)
        chapters = self.get_chapters_for_book(book['title'])

        for chapter in chapters:
            chapter_button = ttk.Button(
                frame,
                text=chapter["chapter"],
                width=35,
                bootstyle="primary outline",
                command=lambda c=chapter: self.controller.open_summary_page(c, is_existing=True)
            )
            chapter_button.pack(anchor="w", padx=40, pady=2)


    def open_add_book(self):
        def add_book():
            title = title_entry.get()
            image = image_path.get()

            if not title or not image:
                messagebox.showerror("Error", "Please provide both title and image.")
                return

            new_book = {"title": title, "image": image}
            self.books.append(new_book)
            self.save_books()
            top.destroy()
            self.render_books()

        top = ttk.Toplevel(self)
        top.title("Add New Book")
        top.geometry("400x200")
        top.resizable(False, False)

        ttk.Label(top, text="Book Title:", font=("Helvetica", 10)).pack(pady=(10, 0))
        title_entry = ttk.Entry(top)
        title_entry.pack(padx=20, pady=5, fill="x")

        ttk.Label(top, text="Cover Image:", font=("Helvetica", 10)).pack(pady=(10, 0))
        image_path = ttk.StringVar()
        image_frame = ttk.Frame(top)
        image_frame.pack(padx=20, pady=5, fill="x")

        image_entry = ttk.Entry(image_frame, textvariable=image_path)
        image_entry.pack(side="left", expand=True, fill="x")

        browse_btn = ttk.Button(image_frame, text="Browse", command=lambda: image_path.set(filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])))
        browse_btn.pack(side="left", padx=5)

        ttk.Button(top, text="Add Book", bootstyle="success", command=add_book).pack(pady=15)

    def get_chapters_for_book(self, book_title):
        try:
            with open("data/summaries.json", "r") as f:
                data = json.load(f)
            return [entry for entry in data if entry['book'] == book_title]
        except:
            return []

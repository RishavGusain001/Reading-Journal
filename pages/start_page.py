import tkinter as tk
from tkinter import PhotoImage
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

class StartPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Full-screen background image
        self.bg_image = None
        try:
            image = Image.open("assets/background.jpg")  # your background image path
            image = image.resize((1920, 1080))  # Resize for fullscreen
            self.bg_image = ImageTk.PhotoImage(image)

            bg_label = tk.Label(self, image=self.bg_image)
            bg_label.place(relwidth=1, relheight=1)
        except:
            self.configure(style="primary.TFrame")  # fallback solid background

        # Center frame
        content_frame = ttk.Frame(self, padding=30)
        content_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        title = ttk.Label(
            content_frame,
            text="📖 Reading Journal",
            font=("Helvetica", 28, "bold"),
            foreground="black",
        )
        title.pack(pady=(10, 5))

        # Subtitle
        subtitle = ttk.Label(
            content_frame,
            text="Track your literary journey with beautiful notes",
            font=("Helvetica", 14),
            foreground="black",
        )
        subtitle.pack(pady=(0, 20))

        # Button
        start_button = ttk.Button(
            content_frame,
            text="📅 Begin Reading",
            bootstyle="success",
            width=20,
            command=lambda: controller.show_frame("BookSelectPage")
        )
        start_button.pack(pady=20)

        # Footer quote
        footer_frame = ttk.Frame(self)
        footer_frame.place(relx=0.5, rely=0.93, anchor="center")

        quote = ttk.Label(
            footer_frame,
            text="Every book is a new adventure...",
            font=("Helvetica", 10, "italic"),
            foreground="black",
        )
        quote.pack()

    def animate(self, index):
        frame = self.frames[index]
        self.anim_label.configure(image=frame)
        self.after(100, self.animate, (index + 1) % len(self.frames))

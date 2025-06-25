import os 
import json
from datetime import date
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class SummaryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.current_book = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        canvas.configure(yscrollcommand=scrollbar.set)

        self.scrollable_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")

        self.scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        self.content_wrapper = ttk.Frame(self.scrollable_frame, padding=20)
        self.content_wrapper.pack(anchor="n", expand=True)

        self.title_label = ttk.Label(
            self.content_wrapper, text="", font=("Helvetica", 20, "bold"), anchor="center"
        )
        self.title_label.pack(pady=(10, 20))

        form_frame = ttk.Frame(self.content_wrapper)
        form_frame.pack(fill="x", expand=True)

        self.chapter_entry = ttk.Entry(form_frame)
        self.chapter_entry.insert(0, "Chapter X: Title")
        self.chapter_entry.pack(fill="x", pady=5)

        self.date_entry = ttk.Entry(form_frame)
        self.date_entry.insert(0, date.today().strftime("%d/%m/%Y"))
        self.date_entry.pack(fill="x", pady=5)

        labels_with_images = [
            "1. Key Events & Operations",
            "2. Key Figures & Agents",
            "3. Tactics & Strategies Used",
            "4. Historical & Political Context"
        ]

        labels_no_images = [
            "5. Notable Quotes",
            "6. Personal Insights & Questions",
            "7. Rating/Importance (Optional)"
        ]

        self.text_fields = {}
        self.image_labels = {}

        for label in labels_with_images:
            lbl = ttk.Label(form_frame, text=label, font=("Helvetica", 11, "bold"))
            lbl.pack(anchor="w", pady=(15, 2))

            txt = tk.Text(form_frame, height=5, wrap="word", font=("Helvetica", 10))
            txt.pack(fill="both", expand=True)
            self.text_fields[label] = txt

            image_frame = ttk.Frame(form_frame)
            image_frame.pack(anchor="w", fill="x")
            self.image_labels[label] = {
                "frame": image_frame,
                "images": []
            }

            img_btn = ttk.Button(form_frame, text="📷 Add Image", command=lambda l=label: self.add_image(l))
            img_btn.pack(pady=(2, 5))

        for label in labels_no_images:
            lbl = ttk.Label(form_frame, text=label, font=("Helvetica", 11, "bold"))
            lbl.pack(anchor="w", pady=(15, 2))

            txt = tk.Text(form_frame, height=5, wrap="word", font=("Helvetica", 10))
            txt.pack(fill="both", expand=True)
            self.text_fields[label] = txt

            image_frame = ttk.Frame(form_frame)
            image_frame.pack(anchor="w", fill="x")
            self.image_labels[label] = {
                "frame": image_frame,
                "images": []
            }

        button_frame = ttk.Frame(self.content_wrapper)
        button_frame.pack(pady=25)

        self.save_button = ttk.Button(button_frame, text="💾 Save Entry", bootstyle="success", command=self.save_entry)
        self.save_button.pack(side="left", padx=10)

        self.back_button = ttk.Button(button_frame, text="← Back to Books", bootstyle="secondary",
                                      command=lambda: controller.show_frame("BookSelectPage"))
        self.back_button.pack(side="left", padx=10)

        self.delete_button = ttk.Button(button_frame, text="🗑️ Delete Chapter", bootstyle="danger",command=self.delete_entry)
        self.delete_button.pack(side="left", padx=10)

    def add_image(self, section_label):
        filepaths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        for filepath in filepaths:
            img = Image.open(filepath)
            img.thumbnail((200, 150))
            photo = ImageTk.PhotoImage(img)

            wrapper = ttk.Frame(self.image_labels[section_label]["frame"])
            wrapper.pack(side="left", padx=5, pady=5)

            img_label = ttk.Label(wrapper, image=photo)
            img_label.image = photo
            img_label.pack()

            caption_entry = ttk.Entry(wrapper, width=25)
            caption_entry.insert(0, "Caption here...")
            caption_entry.pack(pady=(2, 0))

            delete_btn = ttk.Button(wrapper, text="❌", bootstyle="danger-outline", width=3,
                                    command=lambda w=wrapper, l=section_label: self.remove_image(w, l))
            delete_btn.pack(pady=2)

            self.image_labels[section_label]["images"].append({
                "frame": wrapper,
                "image_path": filepath,
                "caption": caption_entry
            })

    def remove_image(self, frame, label):
        frame.destroy()
        self.image_labels[label]["images"] = [
            img for img in self.image_labels[label]["images"]
            if img["frame"] != frame
        ]

    def load_book(self, book):
        self.current_book = book
        self.title_label.config(text=f"📘 {book['title']}")
        self.chapter_entry.delete(0, tk.END)
        self.chapter_entry.insert(0, "Chapter X: Title")
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, date.today().strftime("%d/%m/%Y"))
        for txt in self.text_fields.values():
            txt.delete("1.0", tk.END)
        for label in self.image_labels:
            for img_data in self.image_labels[label]["images"]:
                img_data["frame"].destroy()
            self.image_labels[label]["images"] = []

    def save_entry(self):
        chapter = self.chapter_entry.get()
        date_read = self.date_entry.get()

        if not chapter:
            tk.messagebox.showerror("Error", "Please fill the chapter title")
            return

        # Create new summary entry
        entry = {
            "book": self.current_book['title'],
            "date": date_read,
            "chapter": chapter,
            "sections": {}
        }

        for label, txt in self.text_fields.items():
            section_data = {
                "text": txt.get("1.0", tk.END).strip(),
                "images": [
                    {
                        "path": img["image_path"],
                        "caption": img["caption"].get()
                    } for img in self.image_labels[label]["images"]
                ]
            }
            entry["sections"][label] = section_data

        # Load existing summaries
        try:
            with open("data/summaries.json", "r") as f:
                summaries = json.load(f)
        except:
            summaries = []

        # Check if summary for this book + chapter already exists
        updated = False
        for i, existing in enumerate(summaries):
            if existing["book"] == entry["book"] and existing["chapter"] == entry["chapter"]:
                summaries[i] = entry  # Overwrite
                updated = True
                break

        if not updated:
            summaries.append(entry)

        with open("data/summaries.json", "w") as f:
            json.dump(summaries, f, indent=4)

        self.controller.frames["BookSelectPage"].load_books()
        tk.messagebox.showinfo("Saved", "✅ Summary saved!")
        self.controller.show_frame("BookSelectPage")

    def delete_entry(self):
        chapter = self.chapter_entry.get()
        book_title = self.current_book['title']

        if not chapter:
            tk.messagebox.showerror("Error", "No chapter selected to delete.")
            return

        confirm = tk.messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete:\n📘 {book_title}\n📖 {chapter}?")
        if not confirm:
            return

        try:
            with open("data/summaries.json", "r") as f:
                summaries = json.load(f)
        except:
            tk.messagebox.showerror("Error", "Summary file not found.")
            return

        # Filter out the chapter
        summaries = [
            entry for entry in summaries
            if not (entry["book"] == book_title and entry["chapter"] == chapter)
        ]

        # Save updated summaries
        with open("data/summaries.json", "w") as f:
            json.dump(summaries, f, indent=4)

        tk.messagebox.showinfo("Deleted", f"❌ Chapter '{chapter}' deleted.")
        self.controller.frames["BookSelectPage"].load_books()
        self.controller.show_frame("BookSelectPage")

    def load_existing_entry(self, entry):
        self.current_book = {"title": entry["book"]}
        self.title_label.config(text=f"📘 {entry['book']}")

        self.chapter_entry.delete(0, tk.END)
        self.chapter_entry.insert(0, entry["chapter"])

        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, entry["date"])

        # Clear all text fields
        for label, txt in self.text_fields.items():
            txt.delete("1.0", tk.END)
            txt.insert("1.0", entry["sections"].get(label, {}).get("text", ""))

        # Clear old images
        for label in self.image_labels:
            for img_data in self.image_labels[label]["images"]:
                img_data["frame"].destroy()
            self.image_labels[label]["images"] = []

        # Clear old image references to avoid garbage issues
        self.image_refs = {}

        # Load saved images
        for label in self.image_labels:
            for img in entry["sections"].get(label, {}).get("images", []):
                if os.path.exists(img["path"]):
                    image = Image.open(img["path"])
                    image.thumbnail((200, 150))
                    photo = ImageTk.PhotoImage(image)

                    # Keep strong reference
                    if label not in self.image_refs:
                        self.image_refs[label] = []
                    self.image_refs[label].append(photo)

                    wrapper = ttk.Frame(self.image_labels[label]["frame"])
                    wrapper.pack(side="left", padx=5, pady=5)

                    img_label = ttk.Label(wrapper, image=photo)
                    img_label.image = photo
                    img_label.pack()

                    caption_entry = ttk.Entry(wrapper, width=25)
                    caption_entry.insert(0, img.get("caption", ""))
                    caption_entry.pack(pady=(2, 0))

                    delete_btn = ttk.Button(wrapper, text="❌", bootstyle="danger-outline", width=3,
                                            command=lambda w=wrapper, l=label: self.remove_image(w, l))
                    delete_btn.pack(pady=2)

                    self.image_labels[label]["images"].append({
                        "frame": wrapper,
                        "image_path": img["path"],
                        "caption": caption_entry
                    })

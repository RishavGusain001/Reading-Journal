# 📖 Reading Journal App

A beautifully designed desktop application to help you **track your reading journey**, write **daily summaries**, and save insights chapter-by-chapter. Ideal for book lovers who want to make notes, store thoughts, and reflect on their learning.

---

## 🌟 Features

- 🎬 **Animated start page** with background and GIF
- 📚 **Add books with cover image**
- 📝 **Write structured summaries** per chapter:
  - Key events
  - Characters & agents
  - Tactics and strategy
  - Historical & political context
  - Quotes
  - Personal insights
- 💾 **Save summaries** locally as JSON
- 🔄 **Daily reset** of entries
- 🖼️ Fully responsive with scroll support and fullscreen mode
- 💄 Built using `ttkbootstrap` for a modern and clean UI

---
## 📸 Screenshots

> ![image](https://github.com/user-attachments/assets/03938d41-e911-4193-9ee3-37f3a5fe975c)
> ![image](https://github.com/user-attachments/assets/c21a658a-c17a-4548-ba88-bcbe8cd272d3)
> ![image](https://github.com/user-attachments/assets/56db38de-1d8b-4a89-9ffb-a4c86a4b6b0e)

---

## 📁 Project Structure

BookNotes/
├── assets/
│ ├── background.jpg
│ └── book.gif
├── data/
│ ├── books.json
│ └── summaries.json
├── pages/
│ ├── start_page.py
│ ├── book_select_page.py
│ └── summary_page.py
├── utils/
│ └── helpers.py (optional)
├── main.py
└── README.md

---

🚀 How to Run

1. **Install requirements**  
   *(ttkbootstrap will auto-install most dependencies)*
   pip install ttkbootstrap pillow
2. Run the app
   python main.py

--- 

🛠 Technologies Used
-> Python 3.x
-> tkinter
-> ttkbootstrap
-> Pillow (PIL) for image handling
-> JSON for data storage

---

👨‍💻 Author
Rishav Gusain
rishavgusain001@gmail.com
📍 Uttarakhand, India

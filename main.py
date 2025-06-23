import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from pages.start_page import StartPage
from pages.book_select_page import BookSelectPage
from pages.summary_page import SummaryPage

class ReadingJournalApp(ttk.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title("📚 Reading Journal")
        self.state('zoomed')  # Fullscreen

        self.iconbitmap("assets/icon.ico")
        # Main container WITHOUT background color
        container = ttk.Frame(self, style="TFrame")  # <- important change: neutral base frame
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, BookSelectPage, SummaryPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def open_summary_page(self, book):
        summary_frame = self.frames["SummaryPage"]
        summary_frame.load_book(book)
        self.show_frame("SummaryPage")

if __name__ == "__main__":
    app = ReadingJournalApp(themename="flatly")  
    app.mainloop()

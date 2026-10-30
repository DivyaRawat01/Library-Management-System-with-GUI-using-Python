import tkinter as tk
from tkinter import ttk, messagebox

from project import (
    LibraryCatalog,
    FictionBook,
    NonFictionBook,
    ReferenceBook,
    load_sample_data
)


class LibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Catalog Management System")
        self.root.geometry("1100x680")
        self.root.minsize(900, 580)

        self.catalog = LibraryCatalog()
        load_sample_data(self.catalog)

        self.setup_style()
        self.create_layout()
        self.refresh_books()

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Title.TLabel", font=("Arial", 20, "bold"))
        style.configure("Heading.TLabel", font=("Arial", 12, "bold"))
        style.configure("Treeview", rowheight=28, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Action.TButton", padding=7)

    def create_layout(self):
        header = ttk.Frame(self.root, padding=(18, 14))
        header.pack(fill="x")

        ttk.Label(
            header,
            text="Library Catalog Management System",
            style="Title.TLabel"
        ).pack(side="left")

        self.stats_label = ttk.Label(header, text="", font=("Arial", 10))
        self.stats_label.pack(side="right", padx=5)

        main = ttk.Frame(self.root, padding=(15, 5, 15, 15))
        main.pack(fill="both", expand=True)

        form_frame = ttk.LabelFrame(main, text="Book Information", padding=12)
        form_frame.pack(side="left", fill="y", padx=(0, 12))

        ttk.Label(form_frame, text="Book Type").grid(row=0, column=0, sticky="w", pady=5)
        self.type_var = tk.StringVar(value="Fiction")
        self.type_combo = ttk.Combobox(
            form_frame,
            textvariable=self.type_var,
            values=["Fiction", "Non-Fiction", "Reference"],
            state="readonly",
            width=23
        )
        self.type_combo.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        self.type_combo.bind("<<ComboboxSelected>>", self.update_extra_label)

        ttk.Label(form_frame, text="Title").grid(row=2, column=0, sticky="w", pady=5)
        self.title_entry = ttk.Entry(form_frame, width=27)
        self.title_entry.grid(row=3, column=0, sticky="ew", pady=(0, 8))

        ttk.Label(form_frame, text="Author").grid(row=4, column=0, sticky="w", pady=5)
        self.author_entry = ttk.Entry(form_frame, width=27)
        self.author_entry.grid(row=5, column=0, sticky="ew", pady=(0, 8))

        self.extra_label = ttk.Label(form_frame, text="Sub-genre")
        self.extra_label.grid(row=6, column=0, sticky="w", pady=5)
        self.extra_entry = ttk.Entry(form_frame, width=27)
        self.extra_entry.grid(row=7, column=0, sticky="ew", pady=(0, 12))

        ttk.Button(
            form_frame, text="Add Book", style="Action.TButton",
            command=self.add_book
        ).grid(row=8, column=0, sticky="ew", pady=4)

        ttk.Separator(form_frame).grid(row=9, column=0, sticky="ew", pady=12)

        ttk.Label(form_frame, text="Book ID").grid(row=10, column=0, sticky="w", pady=5)
        self.id_entry = ttk.Entry(form_frame, width=27)
        self.id_entry.grid(row=11, column=0, sticky="ew", pady=(0, 8))

        ttk.Button(
            form_frame, text="Borrow Book", style="Action.TButton",
            command=self.borrow_book
        ).grid(row=12, column=0, sticky="ew", pady=4)

        ttk.Button(
            form_frame, text="Return Book", style="Action.TButton",
            command=self.return_book
        ).grid(row=13, column=0, sticky="ew", pady=4)

        ttk.Button(
            form_frame, text="Remove Book", style="Action.TButton",
            command=self.remove_book
        ).grid(row=14, column=0, sticky="ew", pady=4)

        ttk.Button(
            form_frame, text="Show Details", style="Action.TButton",
            command=self.show_details
        ).grid(row=15, column=0, sticky="ew", pady=4)

        right_frame = ttk.Frame(main)
        right_frame.pack(side="right", fill="both", expand=True)

        search_frame = ttk.LabelFrame(right_frame, text="Search Books", padding=10)
        search_frame.pack(fill="x", pady=(0, 10))

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.search_entry.bind("<Return>", lambda event: self.search_books())

        self.search_by_var = tk.StringVar(value="Title")
        ttk.Combobox(
            search_frame,
            textvariable=self.search_by_var,
            values=["Title", "Author"],
            state="readonly",
            width=10
        ).pack(side="left", padx=(0, 8))

        ttk.Button(search_frame, text="Search", command=self.search_books).pack(side="left")
        ttk.Button(search_frame, text="Show All", command=self.refresh_books).pack(side="left", padx=(8, 0))
        ttk.Button(search_frame, text="Available Only", command=self.show_available).pack(side="left", padx=(8, 0))

        table_frame = ttk.LabelFrame(right_frame, text="Book Catalog", padding=8)
        table_frame.pack(fill="both", expand=True)

        columns = ("id", "title", "author", "type", "extra", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        headings = {
            "id": ("ID", 55),
            "title": ("Title", 190),
            "author": ("Author", 150),
            "type": ("Type", 105),
            "extra": ("Sub-genre / Subject / Edition", 170),
            "status": ("Status", 100)
        }

        for column, (heading, width) in headings.items():
            self.tree.heading(column, text=heading)
            self.tree.column(column, width=width, anchor="center" if column in ("id", "status") else "w")

        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        self.tree.pack(side="top", fill="both", expand=True)
        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")
        self.tree.bind("<<TreeviewSelect>>", self.select_book)

        footer = ttk.Label(
            right_frame,
            text="Select a book in the table to load its ID into the Book ID field.",
            foreground="gray"
        )
        footer.pack(anchor="w", pady=(8, 0))

    def update_extra_label(self, event=None):
        labels = {
            "Fiction": "Sub-genre",
            "Non-Fiction": "Subject",
            "Reference": "Edition"
        }
        self.extra_label.config(text=labels.get(self.type_var.get(), "Extra information"))

    def get_extra_value(self, book):
        if isinstance(book, FictionBook):
            return book.sub_genre
        if isinstance(book, NonFictionBook):
            return book.subject
        if isinstance(book, ReferenceBook):
            return book.edition
        return ""

    def refresh_books(self, books=None):
        if books is None:
            books = list(self.catalog.books.values())

        for item in self.tree.get_children():
            self.tree.delete(item)

        for book in books:
            status = "Available" if book.check_availability() else "Borrowed"
            self.tree.insert(
                "", "end", iid=str(book.book_id),
                values=(
                    book.book_id,
                    book.title,
                    book.author,
                    book.book_type(),
                    self.get_extra_value(book),
                    status
                )
            )

        total = len(self.catalog.books)
        available = sum(book.check_availability() for book in self.catalog.books.values())
        self.stats_label.config(
            text=f"Total books: {total}   |   Available: {available}   |   Borrowed: {total - available}"
        )

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        extra = self.extra_entry.get().strip()
        book_type = self.type_var.get()

        if not title or not author or not extra:
            messagebox.showwarning("Missing Information", "Please fill in all book information fields.")
            return

        book_id = self.catalog.generate_id()

        if book_type == "Fiction":
            book = FictionBook(book_id, title, author, extra)
        elif book_type == "Non-Fiction":
            book = NonFictionBook(book_id, title, author, extra)
        else:
            book = ReferenceBook(book_id, title, author, extra)

        self.catalog.add_book(book)
        self.refresh_books()
        self.clear_form()
        messagebox.showinfo("Success", f"'{title}' has been added successfully.")

    def get_selected_id(self):
        value = self.id_entry.get().strip()
        if not value:
            selected = self.tree.selection()
            if selected:
                value = selected[0]

        try:
            return int(value)
        except ValueError:
            messagebox.showwarning("Invalid Book ID", "Enter a valid Book ID or select a book from the table.")
            return None

    def select_book(self, event=None):
        selected = self.tree.selection()
        if selected:
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, selected[0])

    def borrow_book(self):
        book_id = self.get_selected_id()
        if book_id is None:
            return

        book = self.catalog.find_by_id(book_id)
        if book is None:
            messagebox.showerror("Not Found", "Book not found.")
        elif not book.can_be_borrowed():
            messagebox.showwarning("Cannot Borrow", "Reference books are for in-library use only.")
        elif not book.check_availability():
            messagebox.showwarning("Already Borrowed", f"'{book.title}' is already borrowed.")
        else:
            self.catalog.borrow_book(book_id)
            messagebox.showinfo("Success", f"You have borrowed '{book.title}'.")
            self.refresh_books()

    def return_book(self):
        book_id = self.get_selected_id()
        if book_id is None:
            return

        book = self.catalog.find_by_id(book_id)
        if book is None:
            messagebox.showerror("Not Found", "Book not found.")
        elif book.check_availability():
            messagebox.showwarning("Not Borrowed", f"'{book.title}' is already marked as available.")
        else:
            self.catalog.return_book(book_id)
            messagebox.showinfo("Success", f"'{book.title}' has been returned.")
            self.refresh_books()

    def remove_book(self):
        book_id = self.get_selected_id()
        if book_id is None:
            return

        book = self.catalog.find_by_id(book_id)
        if book is None:
            messagebox.showerror("Not Found", "Book not found.")
            return

        confirm = messagebox.askyesno("Confirm Removal", f"Remove '{book.title}' from the catalog?")
        if confirm:
            self.catalog.remove_book(book_id)
            self.refresh_books()
            self.id_entry.delete(0, tk.END)
            messagebox.showinfo("Removed", "Book removed successfully.")

    def search_books(self):
        keyword = self.search_var.get().strip()
        if not keyword:
            self.refresh_books()
            return

        if self.search_by_var.get() == "Title":
            results = self.catalog.search_by_title(keyword)
        else:
            results = self.catalog.search_by_author(keyword)

        self.refresh_books(results)

    def show_available(self):
        available = [
            book for book in self.catalog.books.values()
            if book.check_availability()
        ]
        self.refresh_books(available)

    def show_details(self):
        book_id = self.get_selected_id()
        if book_id is None:
            return

        book = self.catalog.find_by_id(book_id)
        if book is None:
            messagebox.showerror("Not Found", "Book not found.")
            return

        details = [
            f"Book ID: {book.book_id}",
            f"Title: {book.title}",
            f"Author: {book.author}",
            f"Type: {book.book_type()}",
            f"Status: {'Available' if book.check_availability() else 'Borrowed'}"
        ]

        if isinstance(book, FictionBook):
            details.append(f"Sub-genre: {book.sub_genre}")
        elif isinstance(book, NonFictionBook):
            details.append(f"Subject: {book.subject}")
        elif isinstance(book, ReferenceBook):
            details.extend([
                f"Edition: {book.edition}",
                "Note: In-library use only; cannot be borrowed."
            ])

        messagebox.showinfo("Book Details", "\n".join(details))

    def clear_form(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.extra_entry.delete(0, tk.END)
        self.type_var.set("Fiction")
        self.update_extra_label()


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()

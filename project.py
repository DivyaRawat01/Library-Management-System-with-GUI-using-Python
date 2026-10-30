
class Book:
    """Parent class holding the attributes common to every book."""

    def __init__(self, book_id, title, author, genre, available=True):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.available = available

    def display_details(self):
        """Print all details of the book."""
        print(f"  ID        : {self.book_id}")
        print(f"  Title     : {self.title}")
        print(f"  Author    : {self.author}")
        print(f"  Genre     : {self.genre}")
        print(f"  Type      : {self.book_type()}")
        print(f"  Status    : {'Available' if self.available else 'Borrowed'}")

    def check_availability(self):
        """Return True if the book can currently be borrowed."""
        return self.available

    def update_availability(self, status):
        """Set availability status (True = available, False = borrowed)."""
        self.available = status

    def book_type(self):
        return "General Book"

    def can_be_borrowed(self):
        """Most books can be borrowed; subclasses may override."""
        return True

    def __str__(self):
        status = "Available" if self.available else "Borrowed"
        return f"[{self.book_id}] {self.title} by {self.author} ({self.book_type()}) - {status}"


# ---------------------------------------------------------------------------
# 2. INHERITANCE
# ---------------------------------------------------------------------------
class FictionBook(Book):
    """Fiction books: add a sub-genre (e.g. Fantasy, Mystery, Sci-Fi)."""

    def __init__(self, book_id, title, author, sub_genre, available=True):
        super().__init__(book_id, title, author, "Fiction", available)
        self.sub_genre = sub_genre

    def book_type(self):
        return "Fiction"

    def display_details(self):
        super().display_details()
        print(f"  Sub-genre : {self.sub_genre}")


class NonFictionBook(Book):
    """Non-fiction books: add a subject area (e.g. History, Science)."""

    def __init__(self, book_id, title, author, subject, available=True):
        super().__init__(book_id, title, author, "Non-Fiction", available)
        self.subject = subject

    def book_type(self):
        return "Non-Fiction"

    def display_details(self):
        super().display_details()
        print(f"  Subject   : {self.subject}")


class ReferenceBook(Book):
    """Reference books (dictionaries, encyclopedias): in-library use only."""

    def __init__(self, book_id, title, author, edition, available=True):
        super().__init__(book_id, title, author, "Reference", available)
        self.edition = edition

    def book_type(self):
        return "Reference"

    def can_be_borrowed(self):
        return False  # overridden: reference books never leave the library

    def display_details(self):
        super().display_details()
        print(f"  Edition   : {self.edition}")
        print("  Note      : In-library use only (cannot be borrowed)")


# ---------------------------------------------------------------------------
# 3. CATALOG MANAGER
# ---------------------------------------------------------------------------
class LibraryCatalog:
    """Manages the collection of books."""

    def __init__(self):
        self.books = {}      # book_id -> Book object
        self._next_id = 1

    def generate_id(self):
        book_id = self._next_id
        self._next_id += 1
        return book_id

    def add_book(self, book):
        self.books[book.book_id] = book
        print(f"\nAdded: {book}")

    def remove_book(self, book_id):
        book = self.books.pop(book_id, None)
        if book:
            print(f"\nRemoved: {book.title}")
            return True
        print("\nBook not found.")
        return False

    def find_by_id(self, book_id):
        return self.books.get(book_id)

    def search_by_title(self, keyword):
        keyword = keyword.lower()
        return [b for b in self.books.values() if keyword in b.title.lower()]

    def search_by_author(self, keyword):
        keyword = keyword.lower()
        return [b for b in self.books.values() if keyword in b.author.lower()]

    def display_available_books(self):
        available = [b for b in self.books.values() if b.check_availability()]
        if not available:
            print("\nNo books are currently available.")
            return
        print("\n--- Available Books ---")
        for b in available:
            print(b)

    def display_all_books(self):
        if not self.books:
            print("\nThe catalog is empty.")
            return
        print("\n--- Full Catalog ---")
        for b in self.books.values():
            print(b)

    def borrow_book(self, book_id):
        book = self.find_by_id(book_id)
        if book is None:
            print("\nBook not found.")
        elif not book.can_be_borrowed():
            print(f"\n'{book.title}' is a reference book and cannot be borrowed.")
        elif not book.check_availability():
            print(f"\nSorry, '{book.title}' is already borrowed.")
        else:
            book.update_availability(False)
            print(f"\nYou have borrowed '{book.title}'. Enjoy reading!")

    def return_book(self, book_id):
        book = self.find_by_id(book_id)
        if book is None:
            print("\nBook not found.")
        elif book.check_availability():
            print(f"\n'{book.title}' was not borrowed.")
        else:
            book.update_availability(True)
            print(f"\nThank you for returning '{book.title}'.")


# ---------------------------------------------------------------------------
# 4. COMMAND-LINE INTERFACE
# ---------------------------------------------------------------------------
def read_int(prompt):
    """Keep asking until the user enters a valid whole number."""
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Please enter a valid number.")


def read_text(prompt):
    """Keep asking until the user enters non-empty text."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def add_book_menu(catalog):
    print("\nBook type:  1) Fiction   2) Non-Fiction   3) Reference")
    choice = read_int("Choose type: ")
    title = read_text("Title: ")
    author = read_text("Author: ")
    book_id = catalog.generate_id()

    if choice == 1:
        sub_genre = read_text("Sub-genre (e.g. Fantasy, Mystery): ")
        book = FictionBook(book_id, title, author, sub_genre)
    elif choice == 2:
        subject = read_text("Subject (e.g. History, Science): ")
        book = NonFictionBook(book_id, title, author, subject)
    elif choice == 3:
        edition = read_text("Edition (e.g. 5th): ")
        book = ReferenceBook(book_id, title, author, edition)
    else:
        print("Invalid type.")
        return
    catalog.add_book(book)


def search_menu(catalog):
    print("\nSearch by:  1) Title   2) Author")
    choice = read_int("Choose: ")
    keyword = read_text("Enter search text: ")
    if choice == 1:
        results = catalog.search_by_title(keyword)
    elif choice == 2:
        results = catalog.search_by_author(keyword)
    else:
        print("Invalid choice.")
        return

    if not results:
        print("\nNo matching books found.")
        return
    print(f"\n{len(results)} result(s) found:")
    for book in results:
        print()
        book.display_details()


def check_availability_menu(catalog):
    book = catalog.find_by_id(read_int("Enter book ID: "))
    if book is None:
        print("\nBook not found.")
        return
    state = "available" if book.check_availability() else "currently borrowed"
    print(f"\n'{book.title}' is {state}.")


def load_sample_data(catalog):
    """Pre-load a few books so the system can be tried immediately."""
    catalog.books[1] = FictionBook(1, "Harry Potter", "J.K. Rowling", "Fantasy")
    catalog.books[2] = NonFictionBook(2, "Sapiens", "Yuval Noah Harari", "History")
    catalog.books[3] = ReferenceBook(3, "Oxford English Dictionary", "Oxford Press", "2nd")
    catalog.books[4] = FictionBook(4, "The Da Vinci Code", "Dan Brown", "Mystery")
    catalog._next_id = 5


MENU = """
==========================================
        LIBRARY CATALOG SYSTEM
==========================================
 1. Add a new book
 2. Remove a book
 3. Search for a book
 4. Check availability
 5. Display available books
 6. Display full catalog
 7. Borrow a book
 8. Return a book
 9. Show book details
 0. Exit
------------------------------------------"""


def main():
    catalog = LibraryCatalog()
    load_sample_data(catalog)

    while True:
        print(MENU)
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_book_menu(catalog)
        elif choice == "2":
            catalog.remove_book(read_int("Enter book ID to remove: "))
        elif choice == "3":
            search_menu(catalog)
        elif choice == "4":
            check_availability_menu(catalog)
        elif choice == "5":
            catalog.display_available_books()
        elif choice == "6":
            catalog.display_all_books()
        elif choice == "7":
            catalog.borrow_book(read_int("Enter book ID to borrow: "))
        elif choice == "8":
            catalog.return_book(read_int("Enter book ID to return: "))
        elif choice == "9":
            book = catalog.find_by_id(read_int("Enter book ID: "))
            print()
            book.display_details() if book else print("Book not found.")
        elif choice == "0":
            print("\nThank you for using the Library Catalog System. Goodbye!")
            break
        else:
            print("\nInvalid choice, please try again.")


if __name__ == "__main__":
    main()
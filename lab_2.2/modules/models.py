class Book:
    def __init__(self, book_id, title, author, pages, publish_year, status=0, book_type="Base"):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.pages = pages
        self.publish_year = publish_year
        self.status = status 
        self.book_type = book_type

    def get_status_text(self):
        status_map = {0: "Có sẵn", 1: "Đã mượn", 2: "Trạng thái khác"}
        return status_map.get(self.status, "Không xác định")

class Novel(Book):
    def __init__(self, book_id, title, author, pages, publish_year, status=0, genre=""):
        super().__init__(book_id, title, author, pages, publish_year, status, "Novel")
        self.genre = genre

    def __str__(self):
        return f"[Novel] ID: {self.book_id:<8} | Title: {self.title:<20} | Genre: {self.genre:<12} | Status: {self.get_status_text()}"

class Textbook(Book):
    def __init__(self, book_id, title, author, pages, publish_year, status=0, subject="", grade_level=""):
        super().__init__(book_id, title, author, pages, publish_year, status, "Textbook")
        self.subject = subject
        self.grade_level = grade_level

    def __str__(self):
        return f"[Textbook] ID: {self.book_id:<5} | Title: {self.title:<20} | Subject: {self.subject} ({self.grade_level}) | Status: {self.get_status_text()}"

class ScienceBook(Book):
    def __init__(self, book_id, title, author, pages, publish_year, status=0, field=""):
        super().__init__(book_id, title, author, pages, publish_year, status, "Science")
        self.field = field

    def __str__(self):
        return f"[Science] ID: {self.book_id:<8} | Title: {self.title:<20} | Field: {self.field:<12} | Status: {self.get_status_text()}"

class Member:
    def __init__(self, member_id, full_name):
        self.member_id = member_id
        self.full_name = full_name

    def __str__(self):
        return f"Member ID: {self.member_id:<10} | Full Name: {self.full_name}"

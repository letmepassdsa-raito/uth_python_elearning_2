from .db_connection import DatabaseConnection
from .models import Novel, Textbook, ScienceBook, Member
from datetime import datetime, timedelta

class BookDAO:
    @staticmethod
    def map_row_to_object(row):
        if not row: return None
        b_id, title, author, pages, year, status, b_type, genre, subject, grade, field = row
        if b_type == "Novel":
            return Novel(b_id, title, author, pages, year, status, genre)
        elif b_type == "Textbook":
            return Textbook(b_id, title, author, pages, year, status, subject, grade)
        elif b_type == "Science":
            return ScienceBook(b_id, title, author, pages, year, status, field)
        return None

    @staticmethod
    def add(book):
        connection = DatabaseConnection.get_connection()
        
        # CHẨN ĐOÁN 1: Kiểm tra xem có lấy được kết nối không
        if not connection: 
            print("\n[HỆ THỐNG CHẨN ĐOÁN LỖI]: ❌ KHÔNG KẾT NỐI ĐƯỢC CƠ SỞ DỮ LIỆU!")
            print("👉 Hướng xử lý: Hãy kiểm tra lại file config.ini (sai pass, sai tên DB library_management hoặc PostgreSQL chưa bật).")
            return False
            
        try:
            with connection.cursor() as cursor:
                query = """
                INSERT INTO books (book_id, title, author, pages, publish_year, status, book_type, genre, subject, grade_level, field)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    book.book_id, book.title, book.author, book.pages, book.publish_year, book.status, book.book_type,
                    getattr(book, 'genre', None), getattr(book, 'subject', None), getattr(book, 'grade_level', None), getattr(book, 'field', None)
                ))
            connection.commit()
            return True
            
        # CHẨN ĐOÁN 2: Nếu kết nối OK nhưng câu lệnh SQL lỗi
        except Exception as e:
            print(f"\n[HỆ THỐNG CHẨN ĐOÁN LỖI]: ❌ LỖI SQL THỰC THI -> {e}")
            print("👉 Hướng xử lý: Chạy file database để tạo bảng books hoặc nhập mã ID trùng thật.")
            connection.rollback()
            return False
        finally: 
            if connection: connection.close()

    @staticmethod
    def get_all():
        connection = DatabaseConnection.get_connection()
        if not connection: return []
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM books ORDER BY book_id")
                return [BookDAO.map_row_to_object(row) for row in cursor.fetchall()]
        except Exception: return []
        finally: connection.close()

    @staticmethod
    def update(book):
        connection = DatabaseConnection.get_connection()
        if not connection: return False
        try:
            with connection.cursor() as cursor:
                query = """
                UPDATE books SET title=%s, author=%s, pages=%s, publish_year=%s, status=%s, 
                                 genre=%s, subject=%s, grade_level=%s, field=%s WHERE book_id=%s
                """
                cursor.execute(query, (
                    book.title, book.author, book.pages, book.publish_year, book.status,
                    getattr(book, 'genre', None), getattr(book, 'subject', None), getattr(book, 'grade_level', None), getattr(book, 'field', None),
                    book.book_id
                ))
            connection.commit()
            return True
        except Exception: return False
        finally: connection.close()

    @staticmethod
    def delete(book_id):
        connection = DatabaseConnection.get_connection()
        if not connection: return False
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM books WHERE book_id=%s", (book_id,))
                return cursor.rowcount > 0
            connection.commit()
        except Exception: return False
        finally: connection.close()

    @staticmethod
    def search(keyword):
        connection = DatabaseConnection.get_connection()
        if not connection: return []
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM books WHERE book_id ILIKE %s OR title ILIKE %s", (f"%{keyword}%", f"%{keyword}%"))
                return [BookDAO.map_row_to_object(row) for row in cursor.fetchall()]
        except Exception: return []
        finally: connection.close()


class MemberDAO:
    @staticmethod
    def add(member):
        connection = DatabaseConnection.get_connection()
        if not connection: return False
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO members (member_id, full_name) VALUES (%s, %s)", (member.member_id, member.full_name))
            connection.commit()
            return True
        except Exception: return False
        finally: connection.close()

    @staticmethod
    def get_all():
        connection = DatabaseConnection.get_connection()
        if not connection: return []
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM members ORDER BY member_id")
                return [Member(*row) for row in cursor.fetchall()]
        except Exception: return []
        finally: connection.close()

    @staticmethod
    def update(member):
        connection = DatabaseConnection.get_connection()
        if not connection: return False
        try:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE members SET full_name=%s WHERE member_id=%s", (member.full_name, member.member_id))
            connection.commit()
            return True
        except Exception: return False
        finally: connection.close()

    @staticmethod
    def delete(member_id):
        connection = DatabaseConnection.get_connection()
        if not connection: return False
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM members WHERE member_id=%s", (member_id,))
                return cursor.rowcount > 0
            connection.commit()
        except Exception: return False
        finally: connection.close()

    @staticmethod
    def search(keyword):
        connection = DatabaseConnection.get_connection()
        if not connection: return []
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM members WHERE member_id ILIKE %s OR full_name ILIKE %s", (f"%{keyword}%", f"%{keyword}%"))
                return [Member(*row) for row in cursor.fetchall()]
        except Exception: return []
        finally: connection.close()


class BorrowDAO:
    @staticmethod
    def borrow_book(member_id, book_id, days=14):
        connection = DatabaseConnection.get_connection()
        if not connection: return False
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT status FROM books WHERE book_id=%s", (book_id,))
                res = cursor.fetchone()
                if not res or res[0] != 0: return False 
                
                due_date = datetime.now().date() + timedelta(days=days)
                cursor.execute("INSERT INTO borrow_records (member_id, book_id, due_date) VALUES (%s, %s, %s)", (member_id, book_id, due_date))
                cursor.execute("UPDATE books SET status=1 WHERE book_id=%s", (book_id,))
            connection.commit()
            return True
        except Exception:
            connection.rollback()
            return False
        finally: connection.close()

    @staticmethod
    def return_book(member_id, book_id):
        connection = DatabaseConnection.get_connection()
        if not connection: return False
        try:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE borrow_records SET return_date=CURRENT_DATE WHERE member_id=%s AND book_id=%s AND return_date IS NULL", (member_id, book_id))
                if cursor.rowcount == 0: return False
                cursor.execute("UPDATE books SET status=0 WHERE book_id=%s", (book_id,))
            connection.commit()
            return True
        except Exception:
            connection.rollback()
            return False
        finally: connection.close()

    @staticmethod
    def get_overdue_records():
        connection = DatabaseConnection.get_connection()
        if not connection: return []
        try:
            with connection.cursor() as cursor:
                query = """
                SELECT r.record_id, m.member_id, m.full_name, b.book_id, b.title, r.borrow_date, r.due_date
                FROM borrow_records r
                JOIN members m ON r.member_id = m.member_id
                JOIN books b ON r.book_id = b.book_id
                WHERE r.return_date IS NULL AND r.due_date < CURRENT_DATE
                """
                cursor.execute(query)
                return cursor.fetchall()
        except Exception: return []
        finally: connection.close()

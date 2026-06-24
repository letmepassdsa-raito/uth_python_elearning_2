from modules.db_connection import DatabaseConnection
from modules.models import Student, Course

class StudentDAO:
    @staticmethod
    def add(student):
        connection = DatabaseConnection.get_connection()
        if not connection: return False
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO students (student_id, full_name, dob, email, phone, address) VALUES (%s, %s, %s, %s, %s, %s)",
                    (student.student_id, student.full_name, student.dob, student.email, student.phone, student.address)
                )
            connection.commit()
            return True
        except Exception:
            connection.rollback()
            return False
        finally: connection.close()

    @staticmethod
    def get_all():
        connection = DatabaseConnection.get_connection()
        if not connection: return []
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM students ORDER BY student_id")
                return [Student(*row) for row in cursor.fetchall()]
        except Exception: return []
        finally: connection.close()

    @staticmethod
    def update(student):
        connection = DatabaseConnection.get_connection()
        if not connection: return False
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE students SET full_name=%s, dob=%s, email=%s, phone=%s, address=%s WHERE student_id=%s",
                    (student.full_name, student.dob, student.email, student.phone, student.address, student.student_id)
                )
            connection.commit()
            return True
        except Exception:
            connection.rollback()
            return False
        finally: connection.close()

    @staticmethod
    def delete(student_id):
        connection = DatabaseConnection.get_connection()
        if not connection: return False
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM students WHERE student_id=%s", (student_id,))
                if cursor.rowcount == 0: return False
            connection.commit()
            return True
        except Exception:
            connection.rollback()
            return False
        finally: connection.close()

    @staticmethod
    def search(keyword):
        connection = DatabaseConnection.get_connection()
        if not connection: return []
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM students WHERE student_id ILIKE %s OR full_name ILIKE %s", (f"%{keyword}%", f"%{keyword}%"))
                return [Student(*row) for row in cursor.fetchall()]
        except Exception: return []
        finally: connection.close()


class CourseDAO:
    @staticmethod
    def add(course):
        connection = DatabaseConnection.get_connection()
        if not connection: return False
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO courses (course_id, course_name, description, credits) VALUES (%s, %s, %s, %s)",
                    (course.course_id, course.course_name, course.description, course.credits)
                )
            connection.commit()
            return True
        except Exception:
            connection.rollback()
            return False
        finally: connection.close()

    @staticmethod
    def get_all():
        connection = DatabaseConnection.get_connection()
        if not connection: return []
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM courses ORDER BY course_id")
                return [Course(*row) for row in cursor.fetchall()]
        except Exception: return []
        finally: connection.close()

    @staticmethod
    def update(course):
        connection = DatabaseConnection.get_connection()
        if not connection: return False
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE courses SET course_name=%s, description=%s, credits=%s WHERE course_id=%s",
                    (course.course_name, course.description, course.credits, course.course_id)
                )
            connection.commit()
            return True
        except Exception:
            connection.rollback()
            return False
        finally: connection.close()

    @staticmethod
    def delete(course_id):
        connection = DatabaseConnection.get_connection()
        if not connection: return False
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM courses WHERE course_id=%s", (course_id,))
                if cursor.rowcount == 0: return False
            connection.commit()
            return True
        except Exception:
            connection.rollback()
            return False
        finally: connection.close()

    @staticmethod
    def search(keyword):
        connection = DatabaseConnection.get_connection()
        if not connection: return []
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM courses WHERE course_id ILIKE %s OR course_name ILIKE %s", (f"%{keyword}%", f"%{keyword}%"))
                return [Course(*row) for row in cursor.fetchall()]
        except Exception: return []
        finally: connection.close()


class EnrollmentDAO:
    @staticmethod
    def add(student_id, course_id):
        connection = DatabaseConnection.get_connection()
        if not connection: return False
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO enrollment (student_id, course_id) VALUES (%s, %s)", (student_id, course_id))
            connection.commit()
            return True
        except Exception:
            connection.rollback()
            return False
        finally: connection.close()

    @staticmethod
    def delete(student_id, course_id):
        connection = DatabaseConnection.get_connection()
        if not connection: return False
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM enrollment WHERE student_id=%s AND course_id=%s", (student_id, course_id))
                if cursor.rowcount == 0: return False
            connection.commit()
            return True
        except Exception:
            connection.rollback()
            return False
        finally: connection.close()

    @staticmethod
    def search_by_student(student_id):
        connection = DatabaseConnection.get_connection()
        if not connection: return []
        try:
            with connection.cursor() as cursor:
                query = """
                SELECT e.enrollment_id, s.student_id, s.full_name, c.course_id, c.course_name, e.enrollment_date
                FROM enrollment e
                JOIN students s ON e.student_id = s.student_id
                JOIN courses c ON e.course_id = c.course_id
                WHERE e.student_id = %s
                """
                cursor.execute(query, (student_id,))
                return cursor.fetchall()
        except Exception: return []
        finally: connection.close()

    @staticmethod
    def search_by_course(course_id):
        connection = DatabaseConnection.get_connection()
        if not connection: return []
        try:
            with connection.cursor() as cursor:
                query = """
                SELECT e.enrollment_id, s.student_id, s.full_name, c.course_id, c.course_name, e.enrollment_date
                FROM enrollment e
                JOIN students s ON e.student_id = s.student_id
                JOIN courses c ON e.course_id = c.course_id
                WHERE e.course_id = %s
                """
                cursor.execute(query, (course_id,))
                return cursor.fetchall()
        except Exception: return []
        finally: connection.close()
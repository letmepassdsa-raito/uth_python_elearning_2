from modules.models import Student, Course
from modules.dao import StudentDAO, CourseDAO, EnrollmentDAO

class AppUI:
    @staticmethod
    def menu_main():
        while True:
            print("\n" + "="*55)
            print("   HỆ THỐNG QUẢN LÝ ĐĂNG KÝ KHÓA HỌC SINH VIÊN   ")
            print("="*55)
            print("1. Quản lý thông tin Sinh viên")
            print("2. Quản lý thông tin Khóa học")
            print("3. Quản lý Đăng ký khóa học (Học phần)")
            print("0. Thoát chương trình")
            print("="*55)
            choice = input("Nhập lựa chọn của bạn (0-3): ").strip()
            
            if choice == "1": AppUI.menu_student()
            elif choice == "2": AppUI.menu_course()
            elif choice == "3": AppUI.menu_enrollment()
            elif choice == "0":
                print("\nCảm ơn bạn đã sử dụng hệ thống! Tạm biệt.")
                break
            else:
                print("[!] Lựa chọn không hợp lệ, vui lòng thử lại.")

    @staticmethod
    def menu_student():
        while True:
            print("\n--- QUẢN LÝ SINH VIÊN ---")
            print("1. Hiển thị danh sách sinh viên")
            print("2. Thêm sinh viên mới")
            print("3. Sửa thông tin sinh viên")
            print("4. Xóa sinh viên")
            print("5. Tìm kiếm sinh viên")
            print("0. Quay lại menu chính")
            choice = input("Nhập lựa chọn (0-5): ").strip()

            if choice == "1":
                students = StudentDAO.get_all()
                if not students: print("Danh sách sinh viên trống.")
                for student in students: print(student)
            elif choice == "2":
                student_id = input("Nhập MSSV: ").strip()
                full_name = input("Nhập họ tên: ").strip()
                dob = input("Nhập ngày sinh (YYYY-MM-DD) hoặc bỏ trống: ").strip()
                email = input("Nhập email: ").strip()
                phone = input("Nhập số điện thoại: ").strip()
                address = input("Nhập địa chỉ: ").strip()
                
                if student_id and full_name:
                    student = Student(student_id, full_name, dob if dob else None, email, phone, address)
                    if StudentDAO.add(student): print("[THÀNH CÔNG]: Đã thêm sinh viên vào hệ thống.")
                    else: print("[THẤT BẠI]: MSSV đã tồn tại hoặc định dạng ngày sai.")
                else: print("[!] MSSV và Họ tên bắt buộc phải điền.")
            elif choice == "3":
                student_id = input("Nhập MSSV cần sửa: ").strip()
                results = StudentDAO.search(student_id)
                exists = [s for s in results if s.student_id == student_id]
                if not exists:
                    print("[!] Không tìm thấy sinh viên có MSSV này."); continue
                
                current = exists[0]
                full_name = input(f"Tên mới (Trống nếu giữ nguyên '{current.full_name}'): ").strip()
                dob = input(f"Ngày sinh mới (Trống nếu giữ nguyên '{current.dob}'): ").strip()
                email = input(f"Email mới (Trống nếu giữ nguyên '{current.email}'): ").strip()
                phone = input(f"SĐT mới (Trống nếu giữ nguyên '{current.phone}'): ").strip()
                address = input(f"Địa chỉ mới (Trống nếu giữ nguyên '{current.address}'): ").strip()
                
                student_updated = Student(
                    student_id,
                    full_name if full_name else current.full_name,
                    dob if dob else current.dob,
                    email if email else current.email,
                    phone if phone else current.phone,
                    address if address else current.address
                )
                if StudentDAO.update(student_updated): print("[THÀNH CÔNG]: Cập nhật hoàn tất.")
                else: print("[THẤT BẠI]: Lỗi đồng bộ dữ liệu.")
            elif choice == "4":
                student_id = input("Nhập MSSV cần xóa: ").strip()
                if StudentDAO.delete(student_id): print("[THÀNH CÔNG]: Đã xóa sinh viên.")
                else: print("[THẤT BẠI]: Không tìm thấy sinh viên.")
            elif choice == "5":
                keyword = input("Nhập MSSV hoặc tên cần tìm: ").strip()
                for student in StudentDAO.search(keyword): print(student)
            elif choice == "0": break

    @staticmethod
    def menu_course():
        while True:
            print("\n--- QUẢN LÝ KHÓA HỌC ---")
            print("1. Hiển thị danh sách khóa học")
            print("2. Thêm khóa học mới")
            print("3. Sửa thông tin khóa học")
            print("4. Xóa khóa học")
            print("5. Tìm kiếm khóa học")
            print("0. Quay lại menu chính")
            choice = input("Nhập lựa chọn (0-5): ").strip()

            if choice == "1":
                courses = CourseDAO.get_all()
                if not courses: print("Danh sách khóa học trống.")
                for course in courses: print(course)
            elif choice == "2":
                course_id = input("Nhập Mã khóa học: ").strip()
                course_name = input("Nhập Tên khóa học: ").strip()
                description = input("Mô tả: ").strip()
                credits = input("Số tín chỉ: ").strip()
                if course_id and course_name:
                    course = Course(course_id, course_name, description, int(credits) if credits.isdigit() else 3)
                    if CourseDAO.add(course): print("[THÀNH CÔNG]: Đã thêm khóa học.")
                    else: print("[THẤT BẠI]: Mã môn học đã tồn tại.")
                else: print("[!] Mã và Tên môn học không được để trống.")
            elif choice == "3":
                course_id = input("Nhập Mã khóa học cần sửa: ").strip()
                results = CourseDAO.search(course_id)
                exists = [c for c in results if c.course_id == course_id]
                if not exists: print("[!] Không tìm thấy môn học."); continue
                
                current = exists[0]
                course_name = input(f"Tên môn mới (Trống nếu giữ '{current.course_name}'): ").strip()
                description = input(f"Mô tả mới (Trống nếu giữ '{current.description}'): ").strip()
                credits = input(f"Số tín chỉ mới (Trống nếu giữ '{current.credits}'): ").strip()
                
                course_updated = Course(
                    course_id,
                    course_name if course_name else current.course_name,
                    description if description else current.description,
                    int(credits) if credits.isdigit() else current.credits
                )
                if CourseDAO.update(course_updated): print("[THÀNH CÔNG]: Đã sửa thông tin môn học.")
                else: print("[THẤT BẠI]: Cập nhật lỗi.")
            elif choice == "4":
                course_id = input("Nhập Mã khóa học cần xóa: ").strip()
                if CourseDAO.delete(course_id): print("[THÀNH CÔNG]: Đã xóa khóa học.")
                else: print("[THẤT BẠI]: Mã môn không tồn tại.")
            elif choice == "5":
                keyword = input("Nhập Mã hoặc Tên môn cần tìm: ").strip()
                for course in CourseDAO.search(keyword): print(course)
            elif choice == "0": break

    @staticmethod
    def menu_enrollment():
        while True:
            print("\n--- QUẢN LÝ ĐĂNG KÝ HỌC PHẦN ---")
            print("1. Đăng ký môn học mới cho Sinh viên")
            print("2. Hủy đăng ký môn học (Xóa)")
            print("3. Tra cứu danh sách môn học của 1 Sinh viên")
            print("4. Tra cứu danh sách lớp học của 1 Môn học")
            print("0. Quay lại menu chính")
            choice = input("Nhập lựa chọn (0-4): ").strip()

            if choice == "1":
                student_id = input("Nhập MSSV: ").strip()
                course_id = input("Nhập Mã khóa học: ").strip()
                if EnrollmentDAO.add(student_id, course_id): print("[THÀNH CÔNG]: Sinh viên đăng ký môn học thành công.")
                else: print("[THẤT BẠI]: Lỗi (SV đã đăng ký môn này trước đó hoặc sai thông tin định danh).")
            elif choice == "2":
                student_id = input("Nhập MSSV: ").strip()
                course_id = input("Nhập Mã khóa học cần hủy: ").strip()
                if EnrollmentDAO.delete(student_id, course_id): print("[THÀNH CÔNG]: Đã hủy đăng ký môn học.")
                else: print("[THẤT BẠI]: Bản ghi đăng ký không tồn tại.")
            elif choice == "3":
                student_id = input("Nhập MSSV cần tra cứu: ").strip()
                records = EnrollmentDAO.search_by_student(student_id)
                print(f"\n>> Các môn SV {student_id} đăng ký:")
                for r in records: print(f"Mã ĐK: {r[0]} | Môn: {r[3]} - {r[4]} | Ngày đăng ký: {r[5]}")
            elif choice == "4":
                course_id = input("Nhập Mã môn cần tra cứu danh sách lớp: ").strip()
                records = EnrollmentDAO.search_by_course(course_id)
                print(f"\n>> Danh sách SV học lớp {course_id}:")
                for r in records: print(f"Mã ĐK: {r[0]} | SV: {r[1]} - {r[2]} | Ngày đăng ký: {r[5]}")
            elif choice == "0": break

if __name__ == "__main__":
    AppUI.menu_main()
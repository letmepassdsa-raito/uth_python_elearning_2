from modules.models import Novel, Textbook, ScienceBook, Member
from modules.dao import BookDAO, MemberDAO, BorrowDAO

class LibraryUI:
    @staticmethod
    def menu_main():
        while True:
            print("\n" + "="*55)
            print("         HỆ THỐNG QUẢN LÝ THƯ VIỆN ĐẠI HỌC         ")
            print("="*55)
            print("1. Quản lý danh mục Sách")
            print("2. Quản lý Thành viên thư viện")
            print("3. Nghiệp vụ Mượn sách")
            print("4. Nghiệp vụ Trả sách")
            print("5. Thống kê danh sách sách MƯỢN QUÁ HẠN")
            print("0. Thoát chương trình")
            print("="*55)
            choice = input("Nhập lựa chọn (0-5): ").strip()
            
            if choice == "1": LibraryUI.menu_books()
            elif choice == "2": LibraryUI.menu_members()
            elif choice == "3":
                m_id = input("Nhập mã thành viên mượn: ").strip()
                b_id = input("Nhập mã sách cần mượn: ").strip()
                if BorrowDAO.borrow_book(m_id, b_id): print("[THÀNH CÔNG]: Sách đã được ghi nhận mượn.")
                else: print("[THẤT BẠI]: Sách không có sẵn hoặc thông tin sai.")
            elif choice == "4":
                m_id = input("Nhập mã thành viên trả: ").strip()
                b_id = input("Nhập mã sách cần trả: ").strip()
                if BorrowDAO.return_book(m_id, b_id): print("[THÀNH CÔNG]: Trả sách thành công.")
                else: print("[THẤT BẠI]: Không tìm thấy lịch sử mượn phù hợp.")
            elif choice == "5":
                records = BorrowDAO.get_overdue_records()
                print("\n>>> DANH SÁCH ĐÃ QUÁ HẠN TRẢ <<<")
                if not records: print("Hiện không có cuốn sách nào quá hạn.")
                for r in records:
                    print(f"Mã TV: {r[1]} | Tên: {r[2]} | Mã Sách: {r[3]} | Tên Sách: {r[4]} | Hạn Trả: {r[6]}")
            elif choice == "0": break

    @staticmethod
    def menu_books():
        while True:
            print("\n--- QUẢN LÝ DANH MỤC SÁCH ---")
            print("1. Hiển thị tất cả sách")
            print("2. Thêm sách mới")
            print("3. Sửa thông tin sách")
            print("4. Xóa sách khỏi hệ thống")
            print("5. Tìm kiếm sách")
            print("0. Quay lại Menu chính")
            choice = input("Chọn chức năng (0-5): ").strip()

            if choice == "1":
                books = BookDAO.get_all()
                if not books: print("Tủ sách hiện tại đang trống.")
                for b in books: print(b)
            elif choice == "2":
                b_id = input("Mã sách: ").strip()
                title = input("Tên sách: ").strip()
                author = input("Tác giả: ").strip()
                pages = int(input("Số trang: ").strip() or 0)
                year = int(input("Năm xuất bản: ").strip() or 2026)
                print("Chủng loại: 1. Tiểu thuyết | 2. Sách giáo khoa | 3. Sách khoa học")
                t = input("Chọn (1-3): ").strip()
                
                book = None
                if t == "1":
                    genre = input("Thể loại (lãng mạn, kinh dị,...): ").strip()
                    book = Novel(b_id, title, author, pages, year, 0, genre)
                elif t == "2":
                    sub = input("Môn học (Toán, Văn,...): ").strip()
                    grade = input("Cấp độ (Tiểu học, THCS, THPT): ").strip()
                    book = Textbook(b_id, title, author, pages, year, 0, sub, grade)
                elif t == "3":
                    field = input("Lĩnh vực (CNTT, Điện tử,...): ").strip()
                    book = ScienceBook(b_id, title, author, pages, year, 0, field)
                
                if book and BookDAO.add(book): print("[THÀNH CÔNG]: Thêm sách hoàn tất.")
                else: print("[THẤT BẠI]: Mã sách đã tồn tại.")
            elif choice == "3":
                b_id = input("Nhập mã sách cần sửa: ").strip()
                results = BookDAO.search(b_id)
                exists = [b for b in results if b.book_id == b_id]
                if not exists: print("[!] Không tìm thấy cuốn sách này."); continue
                current = exists[0]
                
                title = input(f"Tên mới (Trống nếu giữ '{current.title}'): ").strip()
                author = input(f"Tác giả mới (Trống nếu giữ '{current.author}'): ").strip()
                status = input(f"Trạng thái mới (0: Có sẵn, 1: Mượn, 2: Khác - Hiện tại '{current.status}'): ").strip()
                
                current.title = title if title else current.title
                current.author = author if author else current.author
                current.status = int(status) if status else current.status
                
                if isinstance(current, Novel):
                    g = input(f"Thể loại mới (Trống nếu giữ '{current.genre}'): ").strip()
                    current.genre = g if g else current.genre
                elif isinstance(current, Textbook):
                    sub = input(f"Môn học mới (Trống nếu giữ '{current.subject}'): ").strip()
                    grade = input(f"Cấp mới (Trống nếu giữ '{current.grade_level}'): ").strip()
                    current.subject = sub if sub else current.subject
                    current.grade_level = grade if grade else current.grade_level
                elif isinstance(current, ScienceBook):
                    f = input(f"Lĩnh vực mới (Trống nếu giữ '{current.field}'): ").strip()
                    current.field = f if f else current.field

                if BookDAO.update(current): print("[THÀNH CÔNG]: Đã cập nhật thông tin sách.")
                else: print("[THẤT BẠI]: Cập nhật lỗi.")
            elif choice == "4":
                b_id = input("Nhập mã sách cần xóa: ").strip()
                if BookDAO.delete(b_id): print("[THÀNH CÔNG]: Đã xóa sách khỏi thư viện.")
                else: print("[THẤT BẠI]: Không tìm thấy mã sách.")
            elif choice == "5":
                keyword = input("Nhập mã sách hoặc tên sách cần tìm: ").strip()
                for b in BookDAO.search(keyword): print(b)
            elif choice == "0": break

    @staticmethod
    def menu_members():
        while True:
            print("\n--- QUẢN LÝ THÀNH VIÊN ---")
            print("1. Danh sách tất cả thành viên")
            print("2. Đăng ký thành viên mới")
            print("3. Sửa thông tin thành viên")
            print("4. Xóa tài khoản thành viên")
            print("5. Tìm kiếm thành viên")
            print("0. Quay lại Menu chính")
            choice = input("Chọn chức năng (0-5): ").strip()

            if choice == "1":
                members = MemberDAO.get_all()
                if not members: print("Danh sách thành viên trống.")
                for m in members: print(m)
            elif choice == "2":
                m_id = input("Mã thành viên: ").strip()
                name = input("Họ và tên: ").strip()
                if m_id and name:
                    if MemberDAO.add(Member(m_id, name)): print("[THÀNH CÔNG]: Đã thêm thành viên.")
                    else: print("[THẤT BẠI]: Mã thành viên bị trùng.")
                else: print("[!] Không được bỏ trống các trường bắt buộc.")
            elif choice == "3":
                m_id = input("Nhập mã thành viên cần sửa: ").strip()
                results = MemberDAO.search(m_id)
                exists = [m for m in results if m.member_id == m_id]
                if not exists: print("[!] Không tìm thấy thành viên."); continue
                name = input(f"Họ tên mới (Trống nếu giữ '{exists[0].full_name}'): ").strip()
                if name:
                    exists[0].full_name = name
                    if MemberDAO.update(exists[0]): print("[THÀNH CÔNG]: Đã sửa đổi thông tin.")
                    else: print("[THẤT BẠI]: Lỗi cập nhật cơ sở dữ liệu.")
            elif choice == "4":
                m_id = input("Nhập mã thành viên muốn xóa: ").strip()
                if MemberDAO.delete(m_id): print("[THÀNH CÔNG]: Đã xóa thành viên.")
                else: print("[THẤT BẠI]: Mã thành viên không tồn tại.")
            elif choice == "5":
                keyword = input("Nhập mã hoặc họ tên cần tìm: ").strip()
                for m in MemberDAO.search(keyword): print(m)
            elif choice == "0": break

if __name__ == "__main__":
    LibraryUI.menu_main()

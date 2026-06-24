CREATE TABLE members (
    member_id VARCHAR(20) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL
);

CREATE TABLE books (
    book_id VARCHAR(20) PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    author VARCHAR(100),
    pages INT,
    publish_year INT,
    status INT DEFAULT 0,          -- 0: Có sẵn, 1: Đã mượn, 2: Trạng thái khác
    book_type VARCHAR(30) NOT NULL, -- 'Novel', 'Textbook', 'Science'
    genre VARCHAR(50),              -- Riêng cho Tiểu thuyết
    subject VARCHAR(50),            -- Riêng cho Sách giáo khoa
    grade_level VARCHAR(20),        -- Riêng cho Sách giáo khoa
    field VARCHAR(50)               -- Riêng cho Sách khoa học
);

CREATE TABLE borrow_records (
    record_id SERIAL PRIMARY KEY,
    member_id VARCHAR(20) REFERENCES members(member_id) ON DELETE CASCADE,
    book_id VARCHAR(20) REFERENCES books(book_id) ON DELETE CASCADE,
    borrow_date DATE DEFAULT CURRENT_DATE,
    due_date DATE NOT NULL,
    return_date DATE DEFAULT NULL   -- NULL nghĩa là chưa trả sách
);

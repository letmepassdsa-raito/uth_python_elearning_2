CREATE TABLE students (
    student_id VARCHAR(20) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    dob DATE,
    email VARCHAR(100),
    phone VARCHAR(15),
    address TEXT
);

CREATE TABLE courses (
    course_id VARCHAR(20) PRIMARY KEY,
    course_name VARCHAR(150) NOT NULL,
    description TEXT,
    credits INT CHECK (credits > 0)
);

CREATE TABLE enrollment (
    enrollment_id SERIAL PRIMARY KEY,
    student_id VARCHAR(20) REFERENCES students(student_id) ON DELETE CASCADE,
    course_id VARCHAR(20) REFERENCES courses(course_id) ON DELETE CASCADE,
    enrollment_date DATE DEFAULT CURRENT_DATE,
    CONSTRAINT unique_student_course UNIQUE (student_id, course_id)
);



class Student:
    def __init__(self, student_id, full_name, dob, email, phone, address):
        self.student_id = student_id
        self.full_name = full_name
        self.dob = dob  # Date of birth
        self.email = email
        self.phone = phone
        self.address = address

    def __str__(self):
        return f"ID: {self.student_id:<10} | Name: {self.full_name:<20} | DOB: {str(self.dob):<12} | Email: {self.email}"

class Course:
    def __init__(self, course_id, course_name, description, credits):
        self.course_id = course_id
        self.course_name = course_name
        self.description = description
        self.credits = credits

    def __str__(self):
        return f"Course ID: {self.course_id:<10} | Name: {self.course_name:<25} | Credits: {self.credits}"
    
    
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Student

class StudentDatabase:
    def init(self, session_factory):
        self.Session = session_factory

    def insert_students(self, students):
        session = self.Session()
        session.add_all(students)
        session.commit()
        session.close()

    def load_data_from_csv(self, file_path):
        df = pd.read_csv(file_path)
        students = [
            Student(last_name=row['Фамилия'],
                    first_name=row['Имя'],
                    faculty=row['Факультет'],
                    course=row['Курс'],
                    grade=row['Оценка'])
            for _, row in df.iterrows()
        ]
        self.insert_students(students)

    def get_students_by_faculty(self, faculty_name):
        session = self.Session()
        students = session.query(Student).filter(Student.faculty == faculty_name).all()
        session.close()
        return students

    def get_unique_courses(self):
        session = self.Session()
        courses = session.query(Student.course).distinct().all()

        session.close()
        return [course[0] for course in courses]

    def get_average_grade_by_faculty(self, faculty_name):
        session = self.Session()
        average_grade = session.query(func.avg(Student.grade)).filter(Student.faculty == faculty_name).scalar()
        session.close()
        return average_grade

    def create_student(self, last_name, first_name, faculty, course, grade):
        session = self.Session()
        student = Student(last_name=last_name, first_name=first_name, faculty=faculty, course=course, grade=grade)
        session.add(student)
        session.commit()
        session.refresh(student)
        session.close()
        return student

    def update_student(self, student_id, last_name, first_name, faculty, course, grade):
        session = self.Session()
        student = session.query(Student).filter(Student.id == student_id).first()
        if student:
            student.last_name = last_name
            student.first_name = first_name
            student.faculty = faculty
            student.course = course
            student.grade = grade
            session.commit()
            session.refresh(student)
        session.close()
        return student

    def delete_student(self, student_id):
        session = self.Session()
        student = session.query(Student).filter(Student.id == student_id).first()
        if student:
            session.delete(student)
            session.commit()
        session.close()
        return student

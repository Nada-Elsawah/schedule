from typing import List, Tuple, Dict

class Lecturer:
    def __init__(self, name: str, availability: List[Tuple[str, str, str]]):
        self.name = name
        self.availability = availability

class Student:
    def __init__(self, name: str, courses: List[str], availability: List[Tuple[str, str, str]]):
        self.name = name
        self.courses = courses
        self.availability = availability

class Classroom:
    def __init__(self, name: str, capacity: int, availability: List[Tuple[str, str, str]]):
        self.name = name
        self.capacity = capacity
        self.availability = availability

class Course:
    def __init__(self, name: str, lecturer: str, students: List[str], classroom: str):
        self.name = name
        self.lecturer = lecturer
        self.students = students
        self.classroom = classroom

class TimeSlot:
    def __init__(self, day: str, start_time: str, end_time: str):
        self.day = day
        self.start_time = start_time
        self.end_time = end_time

class Schedule:
    def __init__(self, course: str, lecturer: str, classroom: str, day: str, start_time: str, end_time: str):
        self.course = course
        self.lecturer = lecturer
        self.classroom = classroom
        self.day = day
        self.start_time = start_time
        self.end_time = end_time

def is_available(availability: List[Tuple[str, str, str]], day: str, start: str, end: str) -> bool:
    return (day, start, end) in availability

def find_student(students: List[Student], name: str) -> Student:
    for student in students:
        if student.name == name:
            return student
    return None

def assign_courses(courses: List[Course], lecturers: List[Lecturer], students: List[Student], classrooms: List[Classroom], time_slots: List[TimeSlot]) -> List[Schedule]:
    schedule = []

    for course in courses:
        lecturer = next((l for l in lecturers if l.name == course.lecturer), None)
        classroom = next((c for c in classrooms if c.name == course.classroom), None)

        if lecturer and classroom:
            for time_slot in time_slots:
                if is_available(lecturer.availability, time_slot.day, time_slot.start_time, time_slot.end_time) and \
                   is_available(classroom.availability, time_slot.day, time_slot.start_time, time_slot.end_time):
                    all_available = True
                    for student_name in course.students:
                        student = find_student(students, student_name)
                        if student and not is_available(student.availability, time_slot.day, time_slot.start_time, time_slot.end_time):
                            all_available = False
                            break

                    if all_available:
                        conflict = False
                        for s in schedule:
                            if (s.day == time_slot.day and s.start_time == time_slot.start_time and s.end_time == time_slot.end_time) and \
                               (s.lecturer == lecturer.name or s.classroom == classroom.name or s.course == course.name):
                                conflict = True
                                break

                        if not conflict:
                            schedule.append(Schedule(course.name, lecturer.name, classroom.name, time_slot.day, time_slot.start_time, time_slot.end_time))
                            break

    return schedule

def print_schedule(schedule: List[Schedule]):
    for s in schedule:
        print(f"Assigned course: {s.course} to {s.lecturer} in {s.classroom} at {s.day} {s.start_time}-{s.end_time}")

def print_student_schedule(schedule: List[Schedule], students: List[Student]):
    student_schedules: Dict[str, List[Schedule]] = {student.name: [] for student in students}

    for s in schedule:
        for student in students:
            if s.course in student.courses:
                student_schedules[student.name].append(s)

    for student_name, courses in student_schedules.items():
        print(f"Schedule for {student_name}:")
        for s in courses:
            print(f"  Course: {s.course}, Lecturer: {s.lecturer}, Classroom: {s.classroom}, Day: {s.day}, Time: {s.start_time}-{s.end_time}")
        print()

def print_lecturer_schedule(schedule: List[Schedule], lecturers: List[Lecturer]):
    lecturer_schedules: Dict[str, List[Schedule]] = {lecturer.name: [] for lecturer in lecturers}

    for s in schedule:
        for lecturer in lecturers:
            if s.lecturer == lecturer.name:
                lecturer_schedules[lecturer.name].append(s)

    for lecturer_name, courses in lecturer_schedules.items():
        print(f"Schedule for {lecturer_name}:")
        for s in courses:
            print(f"  Course: {s.course}, Classroom: {s.classroom}, Day: {s.day}, Time: {s.start_time}-{s.end_time}")
        print()

def print_course_schedule(schedule: List[Schedule]):
    course_schedules: Dict[str, List[Schedule]] = {}

    for s in schedule:
        if s.course not in course_schedules:
            course_schedules[s.course] = []
        course_schedules[s.course].append(s)

    for course_name, times in course_schedules.items():
        print(f"Schedule for course {course_name}:")
        for s in times:
            print(f"  Lecturer: {s.lecturer}, Classroom: {s.classroom}, Day: {s.day}, Time: {s.start_time}-{s.end_time}")
        print()

# Example usage
lecturers = [
    Lecturer("Dr. Ahmed", [("Monday", "9:00", "11:00"), ("Wednesday", "9:00", "11:00")]),
    Lecturer("Prof. Sara", [("Tuesday", "10:00", "12:00"), ("Thursday", "10:00", "12:00")])
]

students = [
    Student("Nada", "Algorithms ", [("Monday", "9:00", "11:00"), ("Wednesday", "11:00", "1:00")]),

    Student("Nada", "Bioinformatics", [("Tuesday", "10:00", "12:00"), ("Thursday", "10:00", "12:00")]),
    Student("Nagwa", "Algorithms " , [("Monday", "9:00", "11:00") ,("Wednesday", "10:00", "12:00") ]),
    Student("Nagwa", "Advanced AI" , [("Tuesday", "10:00", "12:00"), ("Thursday", "10:00", "12:00") ]),

]

classrooms = [
    Classroom("Room1", 30, [("Monday", "9:00", "11:00"),("Tuesday", "11:00", "1:00") ]),
    Classroom("Room3", 30, [("Monday", "9:00", "11:00"), ("Wednesday", "9:00", "11:00"),("Tuesday", "11:00", "1:00"), ("Tuesday", "10:00", "12:00"), ("Thursday", "10:00", "12:00")]),
    Classroom("Room5", 30, [("Monday", "9:00", "11:00"),("Tuesday", "11:00", "1:00") , ("Wednesday", "9:00", "11:00"),("Tuesday", "10:00", "12:00"), ("Thursday", "10:00", "12:00")]),

]

courses = [
    Course("Algorithms ", "Dr. Ahmed", "Nagwa", "Room1" ),
    Course("Algorithms ", "Dr. Ahmed", "Nada",  "Room1" ),
    Course("Bioinformatics" , "Prof. Sara", "Nada" , "Room3"),
    Course("Advanced AI", "Prof. Sara" , "Nagwa", "Room5")
]

time_slots = [
    TimeSlot("Monday", "9:00", "11:00"),
    TimeSlot("Tuesday", "10:00", "12:00"),
    TimeSlot("Wednesday", "9:00", "11:00"),
    TimeSlot("Thursday", "10:00", "12:00"),
    TimeSlot("Tuesday", "11:00", "1:00"),
]

schedule = assign_courses(courses, lecturers, students, classrooms, time_slots)

print("Overall Schedule:")
print_schedule(schedule)
print()


print("Lecturer Schedules:")
print_lecturer_schedule(schedule, lecturers)
print()

print("Student Schedules:")
print_student_schedule(schedule, students)
print()

print("Course Schedules:")
print_course_schedule(schedule)

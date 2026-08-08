from faker import Faker


class student:
    def __init__(self, name, age, address, student_id):
        self.name = name
        self.age = age
        self.address = address
        self.student_id = student_id


class student_sorter:
    def __init__(self, students):
        self.students = students

    def sort(self):
        return sorted(self.students, key=lambda student: student.age)


def init():
    mode = input(
        "Input a student generation mode, 1 - manual input, 2 - random generation "
    )

    students = []

    if mode == "1":
        while True:
            name = input("Enter student name (or 'done' to finish): ")
            if name.lower() == "done":
                break
            age = int(input("Enter student age: "))
            address = input("Enter student address: ")
            student_id = input("Enter student ID: ")
            students.append(student(name, age, address, student_id))
    if mode == "2":
        fake = Faker()
        student_amount = input("Enter student amount: ")
        for _ in range(int(student_amount)): 
            name = fake.name()
            age = fake.random_int(min=18, max=55)
            address = fake.address()
            student_id = fake.uuid4()
            students.append(student(name, age, address, student_id))

    for s in student_sorter(students).sort():
        print("====================================")
        print(f"Name: {s.name}, Age: {s.age}, Address: {s.address}, ID: {s.student_id}")
        print("====================================")

if __name__ == "__main__":
    init()

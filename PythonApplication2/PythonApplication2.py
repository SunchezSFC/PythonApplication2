import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Treeview
from tkinter import simpledialog
import json

class Employee:
    def __init__(self, employee_id, name, surname, patronymic, gender, birth_date, position, salary):
        self.employee_id = employee_id
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.gender = gender
        self.birth_date = birth_date
        self.position = position
        self.salary = salary

class EmployeeManager:
    def __init__(self):
        self.employees = []
        self.load_from_file('employees.json')

    def add_employee(self, employee):
        self.employees.append(employee)
        self.save_to_file('employees.json')

    def delete_employee(self, employee_id):
        self.employees = [emp for emp in self.employees if emp.employee_id!= employee_id]
        self.save_to_file('employees.json')

    def calculate_average_salary(self):
        total_salary = sum(emp.salary for emp in self.employees)
        average_salary = total_salary / len(self.employees) if self.employees else 0
        return average_salary

    def filter_employees_by_attribute(self, attribute, value):
        return [emp for emp in self.employees if getattr(emp, attribute) == value]

    def save_to_file(self, file_name):
        with open(file_name, 'w') as file:
            json.dump([employee.__dict__ for employee in self.employees], file)

    def load_from_file(self, file_name):
        try:
            with open(file_name, 'r') as file:
                data = json.load(file)
                for employee_data in data:
                    self.add_employee(Employee(**employee_data))
        except FileNotFoundError:
            print("���� �� ������.")

    def export_to_text_file(self, file_name):
        with open(file_name, 'w') as file:
            for employee in self.employees:
                file.write(f"ID: {employee.employee_id}, ���: {employee.name}, �������: {employee.surname}, ��������: {employee.patronymic}, ���: {employee.gender}, ���� ��������: {employee.birth_date}, ���������: {employee.position}, ��������: {employee.salary}\n")

def create_gui():
    root = tk.Tk()
    root.title("���������� ������������")

    employees_tree = Treeview(root, columns=("ID", "���", "�������", "���������"), show="headings")
    employees_tree.heading("ID", text="ID")
    employees_tree.heading("���", text="���")
    employees_tree.heading("�������", text="�������")
    employees_tree.heading("���������", text="���������")
    employees_tree.pack()

    manager = EmployeeManager()

    def add_employee():
        id = int(simpledialog.askinteger("���������� ����������", "������� ID ����������"))
        name = simpledialog.askstring("���������� ����������", "������� ��� ����������")
        surname = simpledialog.askstring("���������� ����������", "������� ������� ����������")
        patronymic = simpledialog.askstring("���������� ����������", "������� �������� ����������")
        gender = simpledialog.askstring("���������� ����������", "������� ��� ����������")
        birth_date = simpledialog.askstring("���������� ����������", "������� ���� �������� ����������")
        position = simpledialog.askstring("���������� ����������", "������� ��������� ����������")
        salary = int(simpledialog.askinteger("���������� ����������", "������� �������� ����������"))
        manager.add_employee(Employee(id, name, surname, patronymic, gender, birth_date, position, salary))
        display_employees()

    def delete_employee():
        selected_item = employees_tree.selection()[0]
        employee_id = employees_tree.item(selected_item, "text")["ID"]
        manager.delete_employee(employee_id)
        display_employees()

    def display_employees():
        employees_tree.delete(*employees_tree.get_children())
        for employee in manager.employees:
            employees_tree.insert("", "end", text=employee.employee_id, values=(employee.employee_id, employee.name, employee.surname, employee.position))

    def calculate_average_salary():
        average_salary = manager.calculate_average_salary()
        messagebox.showinfo("������� ��������", f"������� ��������: {average_salary}")

    def filter_employees():
        attribute = simpledialog.askstring("���������� �����������", "������� ������� ��� ���������� (name, surname, position)")
        value = simpledialog.askstring("���������� �����������", "������� �������� ��������")
        filtered_employees = manager.filter_employees_by_attribute(attribute, value)
        messagebox.showinfo("��������������� ����������", "\n".join([f"{emp.employee_id}: {emp.name} {emp.surname}" for emp in filtered_employees]))

    def export_to_txt():
        manager.export_to_text_file('employees.txt')

    add_button = tk.Button(root, text="�������� ����������", command=add_employee)
    add_button.pack()

    delete_button = tk.Button(root, text="������� ����������", command=delete_employee)
    delete_button.pack()

    average_salary_button = tk.Button(root, text="�������� ������� ��������", command=calculate_average_salary)
    average_salary_button.pack()

    filter_button = tk.Button(root, text="����������� �����������", command=filter_employees)
    filter_button.pack()

    export_button = tk.Button(root, text="������� � TXT", command=export_to_txt)
    export_button.pack()

    display_employees()

    root.mainloop()

if __name__ == "__main__":
    create_gui()


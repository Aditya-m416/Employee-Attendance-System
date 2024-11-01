import csv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *

# Define CSV file name
filename = "attendance_records.csv"

# Initialize attendance records if the file doesn't exist
def initialize_csv():
    try:
        with open(filename, 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Employee ID", "Name", "Check In", "Check Out", "Date"])
    except FileExistsError:
        pass

# Record check-in time
def check_in(employee_id, name):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        check_in_time = datetime.now().strftime("%H:%M:%S")
        date = datetime.now().strftime("%Y-%m-%d")
        writer.writerow([employee_id, name, check_in_time, "", date])
    messagebox.showinfo("Check In", f"{name} (ID: {employee_id}) checked in at {check_in_time}.")

# Record check-out time
def check_out(employee_id):
    records = []
    found = False
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            if row[0] == employee_id and row[3] == "":
                row[3] = datetime.now().strftime("%H:%M:%S")
                found = True
                messagebox.showinfo("Check Out", f"{row[1]} (ID: {employee_id}) checked out at {row[3]}.")
            records.append(row)
    
    if found:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(records)
    else:
        messagebox.showwarning("Check Out", "No check-in record found or already checked out.")

# View all attendance records
def view_records():
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            records_text.delete("1.0", tk.END)
            for row in reader:
                records_text.insert(tk.END, f"{' | '.join(row)}\n")
    except FileNotFoundError:
        messagebox.showerror("Error", "No attendance records found.")

# Main application
def run_app():
    initialize_csv()

    root = tk.Tk()
    img=PhotoImage(file='C:/Users/91830/Desktop/INTERNSHIP/att.png')
    root.iconphoto(False,img)
    root.title("Employee Attendance System")
    root.geometry("500x400")

    # Check-in section
    tk.Label(root, text="Check In", font=("Arial", 14)).pack(pady=10)
    tk.Label(root, text="Employee ID").pack()
    employee_id_in = tk.Entry(root)
    employee_id_in.pack()
    tk.Label(root, text="Employee Name").pack()
    employee_name_in = tk.Entry(root)
    employee_name_in.pack()

    def handle_check_in():
        emp_id = employee_id_in.get()
        emp_name = employee_name_in.get()
        if emp_id and emp_name:
            check_in(emp_id, emp_name)
            employee_id_in.delete(0, tk.END)
            employee_name_in.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter both Employee ID and Name.")

    tk.Button(root, text="Check In", command=handle_check_in).pack(pady=5)

    # Check-out section
    tk.Label(root, text="Check Out", font=("Arial", 14)).pack(pady=10)
    tk.Label(root, text="Employee ID").pack()
    employee_id_out = tk.Entry(root)
    employee_id_out.pack()

    def handle_check_out():
        emp_id = employee_id_out.get()
        if emp_id:
            check_out(emp_id)
            employee_id_out.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter Employee ID.")

    tk.Button(root, text="Check Out", command=handle_check_out).pack(pady=5)

    # View records section
    tk.Label(root, text="Attendance Records", font=("Arial", 14)).pack(pady=10)
    records_text = tk.Text(root, width=60, height=10)
    records_text.pack()

    tk.Button(root, text="View Records", command=view_records).pack(pady=5)

    root.mainloop()

# Run the application
run_app()

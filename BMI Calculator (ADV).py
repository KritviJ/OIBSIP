import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt

# Database setup
def setup_database():
    try:
        conn = sqlite3.connect('bmi_data.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                weight REAL,
                height REAL,
                bmi REAL,
                category TEXT,
                feedback TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        return conn, c
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")
        return None, None

def calculate_bmi(weight, height):
    try:
        bmi = weight / (height ** 2)
        return bmi
    except ZeroDivisionError:
        messagebox.showerror("Calculation Error", "Height must be greater than zero.")
        return None

def classify_bmi(bmi, age):
    if bmi is None:
        return None
    try:
        if age < 18:
            if bmi < 14:
                return "Underweight"
            elif 14 <= bmi < 20:
                return "Normal weight"
            elif 20 <= bmi < 25:
                return "Overweight"
            else:
                return "Obesity"
        elif 18 <= age < 65:
            if bmi < 18.5:
                return "Underweight"
            elif 18.5 <= bmi < 24.9:
                return "Normal weight"
            elif 25 <= bmi < 29.9:
                return "Overweight"
            else:
                return "Obesity"
        else:
            if bmi < 23:
                return "Underweight"
            elif 23 <= bmi < 29:
                return "Normal weight"
            elif 29 <= bmi < 35:
                return "Overweight"
            else:
                return "Obesity"
    except Exception as e:
        messagebox.showerror("Classification Error", f"Error classifying BMI: {e}")
        return None

def save_bmi_data(conn, c, name, age, weight, height, bmi, category, feedback):
    try:
        with conn:
            c.execute("INSERT INTO bmi_records (name, age, weight, height, bmi, category, feedback) VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (name, age, weight, height, bmi, category, feedback))
            conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error saving data to database: {e}")

def on_calculate(conn, c, name_entry, age_entry, weight_entry, height_entry, feedback_entry, result_label, weight_unit_var, height_unit_var):
    try:
        name = name_entry.get()
        age = int(age_entry.get())
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        feedback = feedback_entry.get()

        weight_unit = weight_unit_var.get()
        height_unit = height_unit_var.get()

        if weight_unit == "pounds":
            weight = weight * 0.453592
        if height_unit == "inches":
            height = height * 0.0254

        if age <= 0 or weight <= 0 or height <= 0:
            raise ValueError("Age, weight, and height must be positive values.")

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
        return

    bmi = calculate_bmi(weight, height)
    category = classify_bmi(bmi, age)

    if category:
        result_label.config(text=f"BMI: {bmi:.2f}\nCategory: {category}")
        save_bmi_data(conn, c, name, age, weight, height, bmi, category, feedback)

def view_data(conn, c):
    try:
        c.execute("SELECT id, name, age, weight, height, bmi, category, timestamp FROM bmi_records")
        records = c.fetchall()

        # Create a new window to display the data
        data_window = tk.Toplevel(app)
        data_window.title("BMI Records")

        text = tk.Text(data_window, wrap='word')
        text.pack(expand=True, fill='both')

        for record in records:
            text.insert(tk.END, f"ID: {record[0]}, Name: {record[1]}, Age: {record[2]}, Weight: {record[3]}, Height: {record[4]}, "
                                f"BMI: {record[5]:.2f}, Category: {record[6]}, Timestamp: {record[7]}\n")
            text.insert(tk.END, '\n')
        text.config(state=tk.DISABLED)
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error retrieving data from database: {e}")

def view_feedback(conn, c):
    try:
        c.execute("SELECT id, name, feedback, timestamp FROM bmi_records WHERE feedback IS NOT NULL AND feedback != ''")
        feedbacks = c.fetchall()

        # Create a new window to display the feedback
        feedback_window = tk.Toplevel(app)
        feedback_window.title("Customer Feedback")

        text = tk.Text(feedback_window, wrap='word')
        text.pack(expand=True, fill='both')

        text.tag_config('bold_large', font=('TkDefaultFont', 12, 'bold'))

        for feedback in feedbacks:
            text.insert(tk.END, f"ID: {feedback[0]}, Name: {feedback[1]}, Timestamp: {feedback[3]}\n")
            text.insert(tk.END, f"Feedback: {feedback[2]}\n", 'bold_large')
            text.insert(tk.END, '\n')  # Add a blank line for separation
        text.config(state=tk.DISABLED)
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error retrieving feedback from database: {e}")

def plot_data(conn, c):
    try:
        c.execute("SELECT name, bmi FROM bmi_records")
        data = c.fetchall()

        if not data:
            messagebox.showinfo("No Data", "No data available.")
            return

        names = [record[0] for record in data]
        bmis = [record[1] for record in data]

        plt.figure()
        plt.plot(names, bmis, marker='o')
        plt.xlabel('Name')
        plt.ylabel('BMI')
        plt.title('BMI Records')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error retrieving data from database: {e}")

# Main application setup
conn, c = setup_database()

app = tk.Tk()
app.title("BMI Calculator")

# Layout configuration
labels = ["Name", "Age", "Weight", "Height", "Feedback"]
for i, label in enumerate(labels):
    tk.Label(app, text=label).grid(row=i, column=0, padx=10, pady=5)

name_entry = tk.Entry(app)
age_entry = tk.Entry(app)
weight_entry = tk.Entry(app)
height_entry = tk.Entry(app)
feedback_entry = tk.Entry(app)

entries = [name_entry, age_entry, weight_entry, height_entry, feedback_entry]
for i, entry in enumerate(entries):
    entry.grid(row=i, column=1, padx=10, pady=5)

# Weight and height unit selection
weight_unit_var = tk.StringVar(value="kg")
height_unit_var = tk.StringVar(value="meters")

weight_units = ["kg", "pounds"]
height_units = ["meters", "inches"]

weight_unit_menu = tk.OptionMenu(app, weight_unit_var, *weight_units)
height_unit_menu = tk.OptionMenu(app, height_unit_var, *height_units)

weight_unit_menu.grid(row=2, column=2, padx=10, pady=5)
height_unit_menu.grid(row=3, column=2, padx=10, pady=5)

calculate_button = tk.Button(app, text="Calculate BMI", command=lambda: on_calculate(conn, c, name_entry, age_entry, weight_entry, height_entry, feedback_entry, result_label, weight_unit_var, height_unit_var))
calculate_button.grid(row=5, columnspan=3, pady=10)

result_label = tk.Label(app, text="")
result_label.grid(row=6, columnspan=3, pady=5)

view_button = tk.Button(app, text="View Data", command=lambda: view_data(conn, c))
view_button.grid(row=7, column=0, pady=10)

plot_button = tk.Button(app, text="Plot Data", command=lambda: plot_data(conn, c))
plot_button.grid(row=7, column=1, pady=10)

feedback_button = tk.Button(app, text="View Feedback", command=lambda: view_feedback(conn, c))
feedback_button.grid(row=8, columnspan=3, pady=10)

app.mainloop()

# Close the database connection
if conn:
    try:
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error closing the database connection: {e}")

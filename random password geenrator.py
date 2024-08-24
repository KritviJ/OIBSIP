import tkinter as tk
from tkinter import messagebox
import random
import pyperclip

def generate_password():
    try:
        length = int(length_entry.get())
        if length <= 0:
            raise ValueError("Password length must be positive.")
        
        use_letters = letters_var.get()
        use_numbers = numbers_var.get()
        use_symbols = symbols_var.get()
        exclude_chars = exclude_entry.get()

        letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        numbers = "0123456789"
        symbols = "_@#$"

        character_set = ""
        if use_letters:
            character_set += letters
        if use_numbers:
            character_set += numbers

        if use_symbols:
            character_set += symbols

        character_set = ''.join(c for c in character_set if c not in exclude_chars)

        if not character_set:
            raise ValueError("At least one character type must be selected and should have remaining characters after exclusion.")

        first_last_set = ''.join(c for c in (letters + numbers) if c not in exclude_chars) if (use_letters or use_numbers) else character_set

        middle_length = length - 2 if length > 2 else 0
        middle_password = ''.join(random.choice(character_set) for _ in range(middle_length))
        
        first_char = random.choice(first_last_set)
        last_char = random.choice(first_last_set)
        
        password = first_char + middle_password + last_char
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

def copy_to_clipboard():
    pyperclip.copy(password_entry.get())
    messagebox.showinfo("Clipboard", "Password copied to clipboard")

def clear_fields():
    length_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    exclude_entry.delete(0, tk.END)
    letters_var.set(True)
    numbers_var.set(True)
    symbols_var.set(True)

app = tk.Tk()
app.title("Advanced Password Generator")
app.geometry("400x300")

tk.Label(app, text="Password Length:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
length_entry = tk.Entry(app)
length_entry.grid(row=0, column=1, padx=10, pady=5)

letters_var = tk.BooleanVar(value=True)
tk.Checkbutton(app, text="Include Letters", variable=letters_var).grid(row=1, column=0, columnspan=2, sticky='w', padx=10)

numbers_var = tk.BooleanVar(value=True)
tk.Checkbutton(app, text="Include Numbers", variable=numbers_var).grid(row=2, column=0, columnspan=2, sticky='w', padx=10)

symbols_var = tk.BooleanVar(value=True)
tk.Checkbutton(app, text="Include Symbols (@_#$)", variable=symbols_var).grid(row=3, column=0, columnspan=2, sticky='w', padx=10)

tk.Label(app, text="Exclude Specific Characters:").grid(row=5, column=0, padx=10, pady=5, sticky='e')
exclude_entry = tk.Entry(app)
exclude_entry.grid(row=5, column=1, padx=10, pady=5)

generate_button = tk.Button(app, text="Generate Password", command=generate_password)
generate_button.grid(row=6, column=0, columnspan=2, pady=10)

password_entry = tk.Entry(app, width=40)
password_entry.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

clipboard_button = tk.Button(app, text="Copy to Clipboard", command=copy_to_clipboard)
clipboard_button.grid(row=8, column=0, columnspan=1, pady=10, padx=5, sticky='e')

clear_button = tk.Button(app, text="Clear Fields", command=clear_fields)
clear_button.grid(row=8, column=1, columnspan=1, pady=10, padx=5, sticky='w')

app.mainloop()

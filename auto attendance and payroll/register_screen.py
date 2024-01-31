import tkinter as tk
from tkinter import ttk, messagebox

def register():
    username = entry_username.get()
    password = entry_password.get()
    selected_role = role_var.get()

    if username and password and selected_role:
        # Add your registration logic here (e.g., store in a database)
        messagebox.showinfo("Registration Successful", f"You have been registered as {selected_role} successfully!")
    else:
        messagebox.showwarning("Registration Error", "Please enter both username, password, and select a role.")

# Create the main window
root = tk.Tk()
root.title("Role-based Registration Page")
root.geometry("400x300")  # Set the window size

# Create labels, entry widgets, and buttons with enhanced visual appearance
label_username = tk.Label(root, text="Username:", font=("Helvetica", 12, "bold"))
label_password = tk.Label(root, text="Password:", font=("Helvetica", 12, "bold"))
label_role = tk.Label(root, text="Role:", font=("Helvetica", 12, "bold"))

entry_username = tk.Entry(root, font=("Helvetica", 12))
entry_password = tk.Entry(root, show="*", font=("Helvetica", 12))

# Create a dropdown menu for role selection
roles = ["Admin", "Employee"]
role_var = tk.StringVar()
role_var.set(roles[0])  # Default role is "Admin"
role_dropdown = ttk.Combobox(root, textvariable=role_var, values=roles, font=("Helvetica", 12))

button_register = tk.Button(root, text="Register", command=register, font=("Helvetica", 12, "bold"))

# Place labels, entry widgets, dropdown, and button in the window
label_username.grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_username.grid(row=0, column=1, padx=10, pady=10, sticky="w")
label_password.grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_password.grid(row=1, column=1, padx=10, pady=10, sticky="w")
label_role.grid(row=2, column=0, padx=10, pady=10, sticky="e")
role_dropdown.grid(row=2, column=1, padx=10, pady=10, sticky="w")
button_register.grid(row=3, column=0, columnspan=2, pady=20)

# Run the application
root.mainloop()

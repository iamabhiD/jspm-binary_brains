from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import sqlite3
import subprocess
import bcrypt  # Import bcrypt for password hashing and verification

class Login_System:
    def __init__(self, root):  # Corrected constructor
        self.root = root
        self.root.title("Login System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#fafafa")

        # Login frame
        login_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        login_frame.place(x=650, y=90, width=350, height=460)

        # Title
        title = Label(login_frame, text="Login System", font=("Elephant", 30, "bold"), bg="white")
        title.place(x=0, y=30, relwidth=1)

        # Username Label and Entry
        lbl_user = Label(login_frame, text="Employee ID", font=("Andalus", 15), bg="white", fg="#767171")
        lbl_user.place(x=50, y=100)
        self.employee_id = StringVar()
        txt_employee_id = Entry(login_frame, textvariable=self.employee_id, font=("times new roman", 15), bg="#ECECEC")
        txt_employee_id.place(x=50, y=140, width=250)

        # Password Label and Entry
        lbl_pass = Label(login_frame, text="Password", font=("Andalus", 15), bg="white", fg="#767171")
        lbl_pass.place(x=50, y=190)
        self.password = StringVar()
        txt_pass = Entry(login_frame, textvariable=self.password, show="*", font=("times new roman", 15), bg="#ECECEC")
        txt_pass.place(x=50, y=240, width=250)

        # Login Button
        btn_login = Button(
            login_frame, command=self.login, text="Log In",
            font=("Arial Rounded MT Bold", 15), bg="#00B0F0",
            activebackground="#00B0F0", fg="white", activeforeground="white", cursor="hand2"
        )
        btn_login.place(x=50, y=300, width=250, height=35)

        # Separator Line
        hr = Label(login_frame, bg="lightgray")
        hr.place(x=50, y=370, width=250, height=2)

        # Forget Password Button
        btn_forget = Button(
            login_frame, text="Forget Password?", font=("times new roman", 13),
            bg="white", fg="#00759E", bd=0, cursor="hand2"
        )
        btn_forget.place(x=100, y=390)

    def login(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.employee_id.get() == "" or self.password.get() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                cur.execute("SELECT pass FROM employee WHERE eid=?", (self.employee_id.get(),))
                user = cur.fetchone()
                if user is None:
                    messagebox.showerror("Error", "Invalid Username or Password", parent=self.root)
                else:
                    stored_hashed_password = user[0]
                    # Verify the password using bcrypt
                    if bcrypt.checkpw(self.password.get().encode('utf-8'), stored_hashed_password.encode('utf-8')):
                        messagebox.showinfo("Success", "Login Successful!", parent=self.root)
                        self.root.destroy()  # Close the login window

                        # Replace the below path with the absolute path to your dashboard.py
                        subprocess.Popen(["python", r"C:\Users\shashank zende\OneDrive\Documents\clone\Inventory-Management-System\dashboard.py"])
                    else:
                        messagebox.showerror("Error", "Invalid Username or Password", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()


if __name__ == "__main__":  # Corrected the if condition for the main block
    root = Tk()
    obj = Login_System(root)
    root.mainloop()

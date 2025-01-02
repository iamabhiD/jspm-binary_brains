from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import time
import sqlite3
import os
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass

class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+110+80")
        self.root.title("Inventory Management System")
        self.root.config(bg="#f4f4f4")

        # Title Bar
        self.icon_title = PhotoImage(file="Inventory-Management-System/images/logo1.png")
        title = Label(self.root, text="Inventory Management System", image=self.icon_title, compound=LEFT,
                      font=("Verdana", 30, "bold"), bg="#2c3e50", fg="white", anchor="w", padx=20)
        title.place(x=0, y=0, relwidth=1, height=70)

        # Logout Button
        btn_logout = Button(self.root, text="Logout", font=("Verdana", 15, "bold"), bg="#e74c3c", fg="white",
                            cursor="hand2", command=self.logout)
        btn_logout.place(x=1150, y=10, height=50, width=150)
        self.add_hover_effect(btn_logout, "#c0392b", "#e74c3c")  

        # Clock
        self.lbl_clock = Label(self.root, text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",
                               font=("Verdana", 12), bg="#34495e", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # Horizontal Menu Bar
        menu_frame = Frame(self.root, bg="#1abc9c")
        menu_frame.place(x=0, y=100, relwidth=1, height=50)

        self.icon_side = PhotoImage(file="Inventory-Management-System/images/side.png")

        menu_buttons = [
            {"text": "Employee", "command": self.employee},
            {"text": "Supplier", "command": self.supplier},
            {"text": "Category", "command": self.category},
            {"text": "Products", "command": self.product},
            {"text": "Sales", "command": self.sales},
            {"text": "Exit", "command": self.exit}
        ]

        total_buttons = len(menu_buttons)
        for i, item in enumerate(menu_buttons):
            btn = Button(menu_frame, text=item["text"], image=self.icon_side, compound=LEFT, padx=5,
                         anchor="w", font=("Verdana", 14, "bold"), bg="#1abc9c", fg="white", bd=0, cursor="hand2",
                         command=item["command"])
            btn.place(relx=i / total_buttons, rely=0.05, relwidth=1 / total_buttons, relheight=0.9)
            self.add_hover_effect(btn, "#16a085", "#1abc9c")  # Hover shadow effect

        # Dashboard Widgets
        colors = ["#3498db", "#e74c3c", "#2ecc71", "#9b59b6", "#f1c40f"]
        labels = [
            {"text": "Total Employee\n{ 0 }"},
            {"text": "Total Supplier\n{ 0 }"},
            {"text": "Total Category\n{ 0 }"},
            {"text": "Total Product\n{ 0 }"},
            {"text": "Total Sales\n{ 0 }"}
        ]

        self.dashboard_labels = []
        for i, label in enumerate(labels):
            x_pos = (i % 3) * (1 / 3) + 0.05
            y_pos = (i // 3) * 0.35 + 0.25

            lbl = Label(self.root, text=label["text"], bd=5, relief=RIDGE,
                        bg=colors[i], fg="white", font=("Verdana", 16, "bold"))
            lbl.place(relx=x_pos, rely=y_pos, relwidth=0.27, relheight=0.25)
            self.add_hover_effect(lbl, self.darker_color(colors[i]), colors[i])  # Hover shadow effect
            self.dashboard_labels.append(lbl)

        # Footer
        lbl_footer = Label(self.root, text="IMS - Inventory Management System | Developed by Binary Brains \nFor any Technical Issues Contact: 8767440456",
                           font=("Verdana", 10), bg="#34495e", fg="white")
        lbl_footer.pack(side=BOTTOM, fill=X)

        self.update_content()

    # Functions
    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = employeeClass(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = supplierClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryClass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productClass(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = salesClass(self.new_win)

    def exit(self):
        self.root.destroy()

    def logout(self):
        messagebox.showinfo("Logout", "You have logged out successfully.", parent=self.root)

    def update_content(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product")
            product = cur.fetchall()
            self.dashboard_labels[3].config(text=f"Total Product\n[ {str(len(product))} ]")

            cur.execute("SELECT * FROM category")
            category = cur.fetchall()
            self.dashboard_labels[2].config(text=f"Total Category\n[ {str(len(category))} ]")

            cur.execute("SELECT * FROM employee")
            employee = cur.fetchall()
            self.dashboard_labels[0].config(text=f"Total Employee\n[ {str(len(employee))} ]")

            cur.execute("SELECT * FROM supplier")
            supplier = cur.fetchall()
            self.dashboard_labels[1].config(text=f"Total Supplier\n[ {str(len(supplier))} ]")

            bill = len(os.listdir("Inventory-Management-System/bill"))
            self.dashboard_labels[4].config(text=f"Total Sales\n[ {str(bill)} ]")

            time_ = time.strftime("%I:%M:%S %p")
            date_ = time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {date_}\t\t Time: {time_}")
            self.lbl_clock.after(1000, self.update_content)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def add_hover_effect(self, widget, hover_color, original_color):
        """Add hover effects with shadow simulation."""
        def on_enter(e):
            widget.config(bg=hover_color)

        def on_leave(e):
            widget.config(bg=original_color)

        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def darker_color(self, color):
        """Generate a slightly darker shade of the given hex color."""
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
        return f"#{max(r - 20, 0):02x}{max(g - 20, 0):02x}{max(b - 20, 0):02x}"

if __name__ == "__main__":
    root = Tk()
    app = IMS(root)
    root.mainloop()

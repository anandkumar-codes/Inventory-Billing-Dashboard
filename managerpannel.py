from tkinter import *
import time
from PIL import Image, ImageTk
import os
from promanagement import ProductManagement
from billing import BillingSection
from attendance import AttendanceSection



class ManagerSection:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System | Manager Section")
        self.root.geometry("1345x700+5+50")
        self.root.config(bg="#efffb5")
        self.root.resizable(False, False)
        self.root.focus_force()
        self.root.grab_set()


        # ==================== Image Handling ====================
        img_path1 = r"images/logo1.png"
        def load_image(path, size, placeholder_color):
            """Load an image or return a placeholder if missing."""
            try:
                if os.path.exists(path):
                    return ImageTk.PhotoImage(Image.open(path).resize(size, Image.LANCZOS))
                else:
                    raise FileNotFoundError
            except (FileNotFoundError, IOError):
                print(f"Warning: {path} not found. Using placeholder.")
                return ImageTk.PhotoImage(Image.new("RGB", size, placeholder_color))

        self.img1 = load_image(img_path1, (60, 60), "#c1ffe4")

        img_path2 = r"images/pro.png"
        def load_image(path, size, placeholder_color):
            """Load an image or return a placeholder if missing."""
            try:
                if os.path.exists(path):
                    return ImageTk.PhotoImage(Image.open(path).resize(size, Image.LANCZOS))
                else:
                    raise FileNotFoundError
            except (FileNotFoundError, IOError):
                print(f"Warning: {path} not found. Using placeholder.")
                return ImageTk.PhotoImage(Image.new("RGB", size, placeholder_color))

        self.img2 = load_image(img_path2, (150, 150), "#c1ffe4")

        img_path3 = r"images/bill.png"
        def load_image(path, size, placeholder_color):
            """Load an image or return a placeholder if missing."""
            try:
                if os.path.exists(path):
                    return ImageTk.PhotoImage(Image.open(path).resize(size, Image.LANCZOS))
                else:
                    raise FileNotFoundError
            except (FileNotFoundError, IOError):
                print(f"Warning: {path} not found. Using placeholder.")
                return ImageTk.PhotoImage(Image.new("RGB", size, placeholder_color))

        self.img3 = load_image(img_path3, (150, 150), "#c1ffe4")

        img_path4 = r"images/attend.png"
        def load_image(path, size, placeholder_color):
            """Load an image or return a placeholder if missing."""
            try:
                if os.path.exists(path):
                    return ImageTk.PhotoImage(Image.open(path).resize(size, Image.LANCZOS))
                else:
                    raise FileNotFoundError
            except (FileNotFoundError, IOError):
                print(f"Warning: {path} not found. Using placeholder.")
                return ImageTk.PhotoImage(Image.new("RGB", size, placeholder_color))

        self.img4 = load_image(img_path4, (150, 150), "#c1ffe4")

        # ====================== Main Title =====================
        self.lblTitle = Label(
            self.root, text="Inventory Management System (Manager Section)",
            image=self.img1, compound=LEFT, font=("Verdana", 25, "bold"),
            fg="black", bg="#c1ffe4", relief=SOLID, padx=10
        )
        self.lblTitle.place(x=5, y=20, width=1350)

        # ====================== Date and Time========================
        self.lbldateTime=Label(self.root,font=("times new roman",15,"bold"),fg="white",bg="#125f36")
        self.lbldateTime.place(x=0,y=130,relwidth=1)

        # Product
        btnPro=Button(self.root,command=self.product_management,image=self.img2,cursor="hand2",bd=0)
        btnPro.place(x=400,y=200)

        # Billing
        btnBilling=Button(self.root,command=self.product_billing,image=self.img3,cursor="hand2",bd=0)
        btnBilling.place(x=750,y=200)

        # Attendance
        btnAttendance=Button(self.root,command=self.attendance_section,image=self.img4,cursor="hand2",bd=0)
        btnAttendance.place(x=1100,y=200)

        self.datetime_update()

# ===================================== Functionality ======================================

    def datetime_update(self):
        date_=time.strftime("%d-%m-%Y (%A)")
        time_=time.strftime("%r")
        self.lbldateTime.config(text=f"Date: {str(date_)}\t\t\t\tTime: {str(time_)}")
        self.lbldateTime.after(200,self.datetime_update)

    def product_management(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=ProductManagement(self.new_win)

    def product_billing(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=BillingSection(self.new_win)

    def attendance_section(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=AttendanceSection(self.new_win)











if __name__ == "__main__":
    root = Tk()
    app = ManagerSection(root)
    root.mainloop()

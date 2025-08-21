from tkinter import *
from PIL import Image,ImageTk
import time
from promanagement import ProductManagement
from billing import BillingSection
from reports import ReportSection
from users import UserSection
from attendance import AttendanceSection
from salary import SalarySection

class InventoryManagementSystem:
    def __init__(self,root):
        self.root=root
        self.root.title("Inventory Management System | Dashboard")
        self.root.geometry("1366x700+0+0")
        self.root.config(bg="#fdedec")
        self.root.resizable(False,False)
        self.root.focus_force()

        
        # ================ Image ======================
        # img1
        self.img1=Image.open(r"images/logo1.png")
        self.img1=self.img1.resize((90,90), Image.Resampling.LANCZOS)
        self.img1=ImageTk.PhotoImage(self.img1)

        # img2
        self.img2=Image.open(r"images/machine.png")
        self.img2=self.img2.resize((500,450), Image.Resampling.LANCZOS)
        self.img2=ImageTk.PhotoImage(self.img2)

        # img3
        self.img3=Image.open(r"images/pro.png")
        self.img3=self.img3.resize((150,150), Image.Resampling.LANCZOS)
        self.img3=ImageTk.PhotoImage(self.img3)

        # img4
        self.img4=Image.open(r"images/bill.png")
        self.img4=self.img4.resize((150,150), Image.Resampling.LANCZOS)
        self.img4=ImageTk.PhotoImage(self.img4)

        # img5
        self.img5=Image.open(r"images/repo.png")
        self.img5=self.img5.resize((150,150), Image.Resampling.LANCZOS)
        self.img5=ImageTk.PhotoImage(self.img5)

        # img6
        self.img6=Image.open(r"images/user.png")
        self.img6=self.img6.resize((150,150), Image.Resampling.LANCZOS)
        self.img6=ImageTk.PhotoImage(self.img6)

        # img7
        self.img7=Image.open(r"images/attend.png")
        self.img7=self.img7.resize((150,150), Image.Resampling.LANCZOS)
        self.img7=ImageTk.PhotoImage(self.img7)

        # img8
        self.img8=Image.open(r"images/salar.png")
        self.img8=self.img8.resize((150,150), Image.Resampling.LANCZOS)
        self.img8=ImageTk.PhotoImage(self.img8)


        # ====================== Main Title========================
        self.lblTitle=Label(self.root,text="Inventory Management System",image=self.img1,compound=LEFT,font=("verdana",30,"bold"),fg="black",bg="#f9e79f",relief=SOLID)
        self.lblTitle.place(x=5,y=20,width=1350)

        self.dashImage=Label(self.root,image=self.img2,bg="#fdedec")
        self.dashImage.place(x=5,y=200)

        # ====================== Date and Time========================
        self.lbldateTime=Label(self.root,font=("times new roman",15,"bold"),fg="white",bg="#125f36")
        self.lbldateTime.place(x=0,y=130,relwidth=1)

        # ============================== Buttons ======================================

        # Product
        btnPro=Button(self.root,image=self.img3,command=self.product_management,cursor="hand2",bd=0)
        btnPro.place(x=550,y=200)

        # Billing
        btnBilling=Button(self.root,image=self.img4,command=self.product_billing,cursor="hand2",bd=0)
        btnBilling.place(x=750,y=200)

        # Sales
        btnSales=Button(self.root,image=self.img5,command=self.bill_reports,cursor="hand2",bd=0)
        btnSales.place(x=950,y=200)

        # User
        btnUser=Button(self.root,command=self.user_section,image=self.img6,cursor="hand2",bd=0)
        btnUser.place(x=1150,y=200)

        # Attendance
        btnAttendance=Button(self.root,command=self.attendance_section,image=self.img7,cursor="hand2",bd=0)
        btnAttendance.place(x=650,y=400)

        # Salary
        btnSalay=Button(self.root,command=self.salary_section,image=self.img8,cursor="hand2",bd=0)
        btnSalay.place(x=900,y=400)


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

    def bill_reports(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=ReportSection(self.new_win)

    def user_section(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=UserSection(self.new_win)

    def attendance_section(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=AttendanceSection(self.new_win)

    def salary_section(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=SalarySection(self.new_win)


if __name__=="__main__":
    root=Tk()
    object=InventoryManagementSystem(root)
    root.mainloop()
from tkinter import ttk
from tkinter import *
from PIL import Image,ImageTk
import time
from tkinter import messagebox
import sqlite3
import os


class LoginClass:
    def __init__(self,root):
        self.root=root
        self.root.title("Inventory Management System | Login")
        self.root.geometry("1360x700+0+0")
        self.root.config(bg="white")
        self.root.resizable(0,0)

        # ================Images=================

        img2=Image.open(r"images\mobile.png")
        img2=img2.resize((250,500),Image.Resampling.LANCZOS)
        self.photoimg2=ImageTk.PhotoImage(img2)
        b1=Button(self.root,image=self.photoimg2,borderwidth=0,bd=0)
        b1.place(x=850,y=150)

        # ==================== Image Handling ====================
        img_path1 = r"images/cat2.jpg"
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

        self.img1 = load_image(img_path1, (700, 500), "#c1ffe4")

        # ================ Variables Login ================
        self.mobile_var=StringVar()
        self.pass_var=StringVar()
        self.role_var=StringVar()

        # ================ Variables Forgot ================
        self.question_var=StringVar()
        self.answer_var=StringVar()
        self.new_pass_var=StringVar()

        # Title
        mainTitle=Label(self.root,text="INVENTORY MANAGEMENT SYSTEM\nLOGIN",font=("constantia",30,"bold"),bg="#17a589",fg="white")
        mainTitle.place(x=0,y=0,relwidth=1)

        # Date & Time 
        self.date_time=Label(self.root,text="Date: [DD-MM-YYYY]\t\t\t\t Time: [HH:MM:SS]",font=("times new roman",15,"bold"),bg="#de6544",fg="white")
        self.date_time.place(x=0,y=110,relwidth=1)
        self.Update_date_time()

        # mainLogo
        btnmainLogo=Button(self.root,image=self.img1,cursor="hand2",bd=0)
        btnmainLogo.place(x=100,y=200)

        # ================== Labels & Frames===============

        # Login
        lblLogin=Label(self.root,text="LOGIN HERE",font=("goudy old style",20,"bold",UNDERLINE),fg="black")
        lblLogin.place(x=890,y=190)

        # Mobile
        lblMobile=Label(self.root,text="Mobile*",font=("goudy old style",15,"bold"),fg="black")
        lblMobile.place(x=870,y=230)

        entryMobile=Entry(self.root,textvariable=self.mobile_var,font=("goudy old style",12,"bold"),relief=GROOVE,bd=2,fg="black",bg="white",width=25)
        entryMobile.place(x=870,y=260)

        # Password
        lblPassword=Label(self.root,text="Password",font=("goudy old style",15,"bold"),fg="black")
        lblPassword.place(x=870,y=300)

        entryPassword=Entry(self.root,textvariable=self.pass_var,font=("goudy old style",12,"bold"),relief=GROOVE,bd=2,fg="black",bg="white",width=25,show="*")
        entryPassword.place(x=870,y=330)

        # Role
        lblRole=Label(self.root,text="Role",font=("goudy old style",15,"bold"),fg="black")
        lblRole.place(x=870,y=360)

        entryRole=ttk.Combobox(self.root,textvariable=self.role_var,font=("goudy old style",12,"bold"),width=23,state="readonly")
        entryRole["values"]=("Admin","Manager","Cashier")
        entryRole.place(x=870,y=390)

        # Login BUtton
        lblLogin=Button(self.root,command=self.login,text="Log In",bd=0,font=("times new roman",12,"bold"),cursor="hand2",fg="black",bg="#27AE60")
        lblLogin.place(x=900,y=430,width=150)

        # Register
        self.lblRegister=Button(self.root,command=self.register_new,text="Register New Account?",font=("goudy old style",12,"bold"),bd=0,cursor="hand2",fg="#6C3483")
        self.lblRegister.place(x=890,y=490)

        # Forgot Password
        self.lblFrogotP=Button(self.root,command=self.forgot_password_window,text="Forgot Password",font=("goudy old style",12,"bold"),bd=0,cursor="hand2",fg="#26104C")
        self.lblFrogotP.place(x=915,y=530)


# =================== Functionality ==================

    def Update_date_time(self):
        current_time = time.strftime("%d-%m-%Y(%a) %H:%M:%S(%p)")
        self.date_time.config(text=f"Date: {current_time.split()[0]} \t\t Time: {current_time.split()[1]}")
        self.root.after(1000, self.Update_date_time)  # Auto-refresh every second

    def change_password(self):
        if self.question_var.get()=="Select" or self.answer_var.get()=="" or self.new_pass_var.get()=="":
            messagebox.showerror("Error","All fields are Required",parent=self.root2)
        else:
            try:
                con=sqlite3.connect(database=r'inventory.db')
                cur=con.cursor()
                cur.execute("select * from register where Mobile=? and SecurityQ=? and SecurityA=?",(self.mobile_var.get(),self.question_var.get(),self.answer_var.get()))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Please Select Valid Security Question / Answer",parent=self.root2)
                else:
                    cur.execute("update register set Password=? where Mobile=?",(self.new_pass_var.get(),self.mobile_var.get()))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success","Password Changed Successfully,\n\nPlease Login with New Password",parent=self.root2)
                    self.clear()
                    self.root2.destroy()
            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)


    def forgot_password_window(self):
        if self.mobile_var.get()=="":
            messagebox.showerror("Error","Please enter Mobile Number",parent=self.root)
        else:
            try:
                con=sqlite3.connect(database=r'inventory.db')
                cur=con.cursor()
                cur.execute("select * from register where Mobile=?",(self.mobile_var.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Please Enter a Valid Mobile to Reset Password",parent=self.root)
                else:
                    con.close()
                    self.root2=Toplevel()
                    self.root2.title("Inventory Management System | Forgot Password")
                    self.root2.geometry("500x300+450+200")
                    self.root2.config(bg="white")
                    self.root2.focus_force()
                    self.root2.grab_set()

                    lblForgot=Label(self.root2,text="FORGOT PASSWORD",font=("times new roman",12,"bold"),cursor="hand2",fg="white",bg="#E74C3C")
                    lblForgot.place(x=0,y=5,relwidth=1)

                    # Security Question
                    lblsq=Label(self.root2,text="Security Question",font=("goudy old style",12,"bold"),fg="black",bg="white")
                    lblsq.place(x=30,y=50)

                    combosq=ttk.Combobox(self.root2,textvariable=self.question_var,font=("goudy old style",12,"bold"),justify=CENTER,width=23,state="readonly")
                    combosq["values"]=("Select","Best Teacher","Fav Food","First School Name")
                    combosq.current(0)
                    combosq.place(x=160,y=50)

                    # Security Answer
                    lblsa=Label(self.root2,text="Security Answer",font=("goudy old style",12,"bold"),fg="black",bg="white")
                    lblsa.place(x=30,y=100)

                    entrysa=Entry(self.root2,textvariable=self.answer_var,font=("goudy old style",12,"bold"),relief=GROOVE,bd=2,fg="black",bg="white",width=25)
                    entrysa.place(x=160,y=100)

                    # New Password
                    lblnewpswd=Label(self.root2,text="New Password",font=("goudy old style",12,"bold"),fg="black",bg="white")
                    lblnewpswd.place(x=30,y=150)

                    entrypswd=Entry(self.root2,textvariable=self.new_pass_var,font=("goudy old style",12,"bold"),relief=GROOVE,bd=2,fg="black",bg="white",width=25,show="*")
                    entrypswd.place(x=160,y=150)

                    # Change Password
                    lblChangePswd=Button(self.root2,command=self.change_password,text="Change Password",bd=0,font=("times new roman",12,"bold"),cursor="hand2",fg="black",bg="#27AE60")
                    lblChangePswd.place(x=190,y=220)
            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)

    def login(self):
        try:
            # Check if fields are empty
            if self.mobile_var.get() == "" or self.pass_var.get() == "" or self.role_var.get() == "":
                messagebox.showerror("Error", "Mobile Number, Password, and Role must be provided", parent=self.root)
                return
            
            # Database Connection
            con = sqlite3.connect(database=r'inventory.db')
            cur = con.cursor()

            # Query to check user credentials
            cur.execute("SELECT * FROM register WHERE Mobile=? AND Password=? AND Role=?", 
                        (self.mobile_var.get(), self.pass_var.get(), self.role_var.get()))
            row = cur.fetchone()
            con.close()

            if row is None:
                messagebox.showerror("Error", "Invalid Mobile Number, Password, or Role", parent=self.root)
            else:
                messagebox.showinfo("Success", f"Welcome {self.mobile_var.get()}", parent=self.root)
                self.root.destroy()

                # Open respective dashboard based on role
                if self.role_var.get() == "Admin":
                    os.system("python dashboard.py")
                elif self.role_var.get() == "Manager":
                    os.system("python managerpannel.py")
                elif self.role_var.get() == "Cashier":
                    os.system("python billing.py")
                else:
                    messagebox.showerror("Error", "Invalid Role Assigned!", parent=self.root)

        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def register_new(self):
        from register import RegisterClass
        self.new_win=Toplevel(self.root)
        self.new_obj=RegisterClass(self.new_win)

    def clear(self):
        self.question_var.set("Select")
        self.answer_var.set("")
        self.new_pass_var.set("")




if __name__=="__main__":
    root=Tk()
    object=LoginClass(root)
    root.mainloop()
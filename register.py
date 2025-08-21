import sqlite3
from tkinter import *
from tkinter import ttk
import time
from PIL import Image,ImageTk
from tkinter import messagebox
import os


class RegisterClass:
    def __init__(self,root):
        self.root=root
        self.root.title("Inventory Management System | Register")
        self.root.geometry("1200x550+75+75")
        self.root.config(bg="white")
        self.root.focus_force()
        self.root.resizable(0,0)
        self.root.grab_set()

        # ================== Image ====================
        img1=Image.open(r"images\register.jpg")
        img1=img1.resize((400,350),Image.Resampling.LANCZOS)
        self.photoimage1=ImageTk.PhotoImage(img1)
        b1=Button(self.root,image=self.photoimage1,borderwidth=0)
        b1.place(x=50,y=120)

        # ==================== Variables ======================
        self.uid_var=StringVar()
        self.name_var=StringVar()
        self.role_var=StringVar()
        self.mobile_var=StringVar()
        self.DOJ_var=StringVar()
        self.sq_var=StringVar()
        self.sa_var=StringVar()
        self.password_var=StringVar()
        self.cpassword_var=StringVar()
        
        # ====================== Main Title========================
        lblTitle=Label(self.root,text="NEW USER REGISTRATION",font=("verdana",20,"bold"),bg="#17A589",fg="#D7DBDD")
        lblTitle.place(x=0,y=0,relwidth=1)

        # Date & Time 
        self.date_time=Label(self.root,text="Date: [DD-MM-YYYY]\t\t\t\t Time: [HH:MM:SS]",font=("times new roman",15,"bold"),bg="#1E8449",fg="white")
        self.date_time.place(x=0,y=40,relwidth=1)
        self.Update_date_time()

        # ============================= Labels and Entries ==================

        register_win=Label(self.root,text="\t\tREGISTER HERE",font=("goudy old style",20,"bold"),bg="#E74C3C",fg="white")
        register_win.place(x=0,y=72,relwidth=1)

        # User ID
        lbluserid=Label(self.root,text="*User ID",font=("goudy old style",12,"bold"),fg="red",bg="white")
        lbluserid.place(x=700,y=120)

        entryuserid=Entry(self.root,textvariable=self.uid_var,font=("goudy old style",12,"bold"),relief=GROOVE,bd=2)
        entryuserid.place(x=660,y=150,width=150,height=20)
        
        # Name
        lblname=Label(self.root,text="Name",font=("goudy old style",12,"bold"),fg="black",bg="white")
        lblname.place(x=550,y=170)

        entryname=Entry(self.root,textvariable=self.name_var,font=("goudy old style",12,"bold"),relief=GROOVE,bd=2,fg="black",bg="white",state="readonly")
        entryname.place(x=550,y=200,width=150,height=20)

        # Role
        lblRole=Label(self.root,text="Role",font=("goudy old style",12,"bold"),fg="black",bg="white")
        lblRole.place(x=770,y=170)

        entryRole=Entry(self.root,textvariable=self.role_var,font=("goudy old style",12,"bold"),relief=GROOVE,bd=2,fg="black",bg="white",state="readonly")
        entryRole.place(x=770,y=200,width=150,height=20)

        # Mobile
        lblMobile=Label(self.root,text="Mobile",font=("goudy old style",12,"bold"),fg="black",bg="white")
        lblMobile.place(x=550,y=220)

        entryMobile=Entry(self.root,textvariable=self.mobile_var,font=("goudy old style",12,"bold"),relief=GROOVE,bd=2,fg="black",bg="white",state="readonly")
        entryMobile.place(x=550,y=250,width=150,height=20)

        # DOJ
        lblDOJ=Label(self.root,text="DOJ",font=("goudy old style",12,"bold"),fg="black",bg="white")
        lblDOJ.place(x=770,y=220)

        entryDOJ=Entry(self.root,textvariable=self.DOJ_var,font=("goudy old style",12,"bold"),relief=GROOVE,bd=2,fg="black",bg="white",state="readonly")
        entryDOJ.place(x=770,y=250,width=150,height=20)

        # Security Question
        lblsq=Label(self.root,text="Security Question",font=("goudy old style",12,"bold"),fg="black",bg="white")
        lblsq.place(x=550,y=280)

        combosq=ttk.Combobox(self.root,textvariable=self.sq_var,font=("goudy old style",12,"bold"),justify=CENTER,state="readonly")
        combosq["values"]=("Select","Best Teacher","Fav Food","First School Name")
        combosq.current(0)
        combosq.place(x=550,y=310,width=150,height=20)

        # Security Answer
        lblsa=Label(self.root,text="Security Answer",font=("goudy old style",12,"bold"),fg="black",bg="white")
        lblsa.place(x=770,y=280)

        entrysa=Entry(self.root,textvariable=self.sa_var,font=("goudy old style",12,"bold"),relief=GROOVE,bd=2,fg="black",bg="white")
        entrysa.place(x=770,y=310,width=150,height=20)

        # Password
        lblPassword=Label(self.root,text="Password",font=("goudy old style",12,"bold"),fg="black",bg="white")
        lblPassword.place(x=550,y=340)

        entryPassword=Entry(self.root,textvariable=self.password_var,font=("goudy old style",12,"bold"),relief=GROOVE,bd=2,fg="black",bg="white",show="*")
        entryPassword.place(x=550,y=370,width=150,height=20)

        # Confirm Password
        lblCPassword=Label(self.root,text="Confirm Password",font=("goudy old style",12,"bold"),fg="black",bg="white")
        lblCPassword.place(x=770,y=340)

        entryCPassword=Entry(self.root,textvariable=self.cpassword_var,font=("goudy old style",12,"bold"),relief=GROOVE,bd=2,fg="black",bg="white",show="*")
        entryCPassword.place(x=770,y=370,width=150,height=20)

        # Check Button
        self.chk_var=IntVar()
        chk_btn=Checkbutton(self.root,variable=self.chk_var,text="Accept Terms & Conditions*",onvalue=1,offvalue=0,font=("goudy old style",12,"bold"),activeforeground="#641E16",fg="#641E16",bg="white")
        chk_btn.place(x=550,y=390)

        # ======================== Register Button =================

        # ================== Image ===================

        img2=Image.open(r"images\register.png")
        img2=img2.resize((180,40),Image.Resampling.LANCZOS)
        self.photoimage2=ImageTk.PhotoImage(img2)

        lblregister=Button(self.root,command=self.register,text="Register",image=self.photoimage2,bd=0,font=("goudy old style",12,"bold"),cursor="hand2",fg="black",bg="white")
        lblregister.place(x=650,y=430)

        # img3=Image.open(r"images\signin.png")
        # img3=img3.resize((120,40),Image.Resampling.LANCZOS)
        # self.photoimage3=ImageTk.PhotoImage(img3)

        lblfetch=Button(self.root,text="Fetch",command=self.fetch_data,font=("goudy old style",10,"bold"),cursor="hand2",fg="white",bg="green",relief=SOLID,bd=1)
        lblfetch.place(x=850,y=150,width=100,height=20)

        # lblsignin=Button(self.root,command=self.login,text="Signin",image=self.photoimage3,bd=0,font=("goudy old style",12,"bold"),cursor="hand2",fg="black",bg="white")
        # lblsignin.place(x=800,y=430)


# =================== Functionality ==================

    def fetch_data(self):
        con = sqlite3.connect(database=r'inventory.db')
        cur = con.cursor()
        try:
            cur.execute(
                "SELECT User_Name, Role, Mobile, DOJ FROM usersdata WHERE User_ID=?",
                (self.uid_var.get(),)
            )
            row = cur.fetchone()
            if row is not None:
                # Set the text variables with fetched data
                self.name_var.set(row[0])
                self.role_var.set(row[1])
                self.mobile_var.set(row[2])
                self.DOJ_var.set(row[3])
            else:
                messagebox.showerror("Error", "No record found", parent=self.root)
                self.clear()
        except Exception as es:
            messagebox.showerror("Error", f"Error Due To: {str(es)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.uid_var.set("")
        self.name_var.set("")
        self.role_var.set("")
        self.mobile_var.set("")
        self.DOJ_var.set("")

    def clear_all(self):
        self.uid_var.set("")
        self.name_var.set("")
        self.role_var.set("")
        self.mobile_var.set("")
        self.DOJ_var.set("")
        self.sq_var.set("Select")
        self.sa_var.set("")
        self.password_var.set("")
        self.cpassword_var.set("")

    def Update_date_time(self):
        time_=time.strftime("%I:%M:%S %p")
        date_=time.strftime("%d-%m-%Y %a")
        self.date_time.config(text=f"Date: {str(date_)}\t\t\t\t Time: {str(time_)}")
        self.date_time.after(200,self.Update_date_time)

    def register(self):
        # Validation Checks
        if not all([
            self.uid_var.get(),
            self.name_var.get(),
            self.role_var.get(),
            self.mobile_var.get(),
            self.DOJ_var.get(),
            self.sq_var.get(),
            self.sa_var.get(),
            self.password_var.get()
        ]):
            messagebox.showerror("Error", "All fields are Required", parent=self.root)
            return

        if self.sq_var.get() == "Select":
            messagebox.showerror("Error", "Please Select Security Question", parent=self.root)
            return

        if self.password_var.get() != self.cpassword_var.get():
            messagebox.showerror("Error", "Password Doesn't Match, Please Try Again", parent=self.root)
            return

        if self.chk_var.get() == 0:
            messagebox.showerror("Error", "Please Accept Our Terms & Conditions", parent=self.root)
            return

        try:
            with sqlite3.connect(database=r'inventory.db') as con:
                cur = con.cursor()
                
                # Check if User ID already exists
                cur.execute("SELECT RUser_ID FROM register WHERE RUser_ID = ?", (self.uid_var.get(),))
                existing_user = cur.fetchone()

                if existing_user:
                    messagebox.showwarning("Warning", "User ID already exists. Please use a different User ID.", parent=self.root)
                    return  # Stop registration process

                # Confirmation before registration
                register = messagebox.askyesno("Register", f"Are You Sure To Register {self.name_var.get()}?", parent=self.root)
                if not register:
                    return

                # Insert new user
                cur.execute("""
                    INSERT INTO register (RUser_ID, Name, Role, Mobile, DOJ, SecurityQ, SecurityA, Password) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    self.uid_var.get(),
                    self.name_var.get(),
                    self.role_var.get(),
                    self.mobile_var.get(),
                    self.DOJ_var.get(),
                    self.sq_var.get(),
                    self.sa_var.get(),
                    self.password_var.get()
                ))
                con.commit()

            # Success Message
            messagebox.showinfo("Success", f"{self.name_var.get()} Registered Successfully", parent=self.root)
            self.clear_all()
        except sqlite3.Error as db_err:
            messagebox.showerror("Database Error", f"Error: {db_err}", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(ex)}", parent=self.root)

    # def login(self):
    #     self.root.destroy()
    #     os.system("python login.py")













if __name__=="__main__":
    root=Tk()
    object=RegisterClass(root)
    root.mainloop()
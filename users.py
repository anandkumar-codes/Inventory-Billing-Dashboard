from tkinter import *
import time
from tkinter import messagebox,ttk
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import os
from datetime import datetime
import sqlite3


class UserSection:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System | User")
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

        # ====================== Main Title =====================
        self.lblTitle = Label(
            self.root, text="Inventory Management System (User Registration)",
            image=self.img1, compound=LEFT, font=("Verdana", 25, "bold"),
            fg="black", bg="#c1ffe4", relief=SOLID, padx=10
        )
        self.lblTitle.place(x=5, y=20, width=1350)


        # ======================= Labels and Entries==========================

        # User Details

        # User
        self.userid_var=StringVar()
        lblUser = Label(self.root, text="*User ID", font=("Constantia", 11, "bold"), bg="#efffb5",fg="#dd2f00")
        lblUser.place(x=10, y=100)

        entryUser = Entry(self.root,textvariable=self.userid_var,justify=CENTER, font=("times new roman", 10, "bold"),
                                       relief=SOLID, bd=1, width=19, fg="#10106E",state="readonly")
        entryUser.place(x=80, y=100, width=130)

        # Name
        self.name_var=StringVar()
        # Trace StringVars for real-time capitalization
        self.name_var.trace("w", lambda *args: self.capitalize_name(self.name_var))
        lblName = Label(self.root, text="Name", font=("Constantia", 11, "bold"), bg="#efffb5")
        lblName.place(x=230, y=100)

        entryName = Entry(self.root,textvariable=self.name_var,justify=CENTER, font=("times new roman", 10, "bold"),
                                       relief=SOLID, bd=1, width=19, fg="#10106E")
        entryName.place(x=280, y=100, width=180)

        # Role
        self.role_var=StringVar()
        lblRole = Label(self.root, text="Role", font=("Constantia", 11, "bold"), bg="#efffb5")
        lblRole.place(x=480, y=100)

        entryRole = ttk.Combobox(self.root,textvariable=self.role_var,justify=CENTER, font=("times new roman", 10, "bold"),
                                    width=19,state="readonly")
        entryRole['values']=("Select","Admin","Manager","Cashier")
        entryRole.place(x=520, y=100, width=180)
        entryRole.current(0)

        # Gender
        self.gender_var=StringVar()
        lblGender = Label(self.root, text="Gender", font=("Constantia", 11, "bold"), bg="#efffb5")
        lblGender.place(x=720, y=100)

        entryGender = ttk.Combobox(self.root,textvariable=self.gender_var,justify=CENTER, font=("times new roman", 10, "bold"),
                                    width=19,state="readonly")
        entryGender['values']=("Select","Male","Female","Others")
        entryGender.place(x=790, y=100, width=100)
        entryGender.current(0)

        # Date of Birth
        lblDateOfBirth = Label(self.root, text="Date of Birth", font=("Constantia", 11, "bold"), bg="#efffb5")
        lblDateOfBirth.place(x=910, y=100)

        self.entryDateDOB = DateEntry(self.root, width=19, background='darkblue', foreground='white',
                               font=("times new roman", 10, "bold"), date_pattern='dd-mm-yyyy',justify=CENTER)
        self.entryDateDOB.place(x=1020, y=100, width=100)
        self.entryDateDOB.set_date("01-01-2000")

        # ID Type
        self.idtype_var=StringVar()
        lblIDType = Label(self.root, text="ID Type", font=("Constantia", 11, "bold"), bg="#efffb5")
        lblIDType.place(x=1140, y=100)

        entryIDType = ttk.Combobox(self.root,textvariable=self.idtype_var,justify=CENTER, font=("times new roman", 10, "bold"),
                                    width=19,state="readonly")
        entryIDType['values']=("Select","Aadhar Card","PAN Card","Driving License","Voter ID","Passport")
        entryIDType.place(x=1210, y=100, width=100)
        entryIDType.current(0)

        # IDNum
        self.idnum_var=StringVar()
        lblIDNum = Label(self.root, text="ID Number", font=("Constantia", 11, "bold"), bg="#efffb5")
        lblIDNum.place(x=10, y=140)

        entryIDNum = Entry(self.root,textvariable=self.idnum_var,justify=CENTER, font=("times new roman", 10, "bold"),
                                       relief=SOLID, bd=1, width=19, fg="#10106E")
        entryIDNum.place(x=100, y=140, width=150)

        # Mobile
        self.mobile_var=StringVar()
        vcmd = (self.root.register(self.validate_mobile_input), '%P')
        lblMobile = Label(self.root, text="Mobile", font=("Constantia", 11, "bold"), bg="#efffb5")
        lblMobile.place(x=270, y=140)

        self.entryMobile = Entry(self.root,textvariable=self.mobile_var,justify=CENTER, font=("times new roman", 10, "bold"),validate="key", validatecommand=vcmd,
                                       relief=SOLID, bd=1, width=19, fg="#10106E")
        self.entryMobile.place(x=330, y=140, width=130)

        # Date of Joining
        lblDateOfJoining = Label(self.root, text="Date of Joining", font=("Constantia", 11, "bold"), bg="#efffb5")
        lblDateOfJoining.place(x=480, y=140)

        self.entryDateDOJ = DateEntry(self.root, width=19, background='darkblue', foreground='white',
                               font=("times new roman", 10, "bold"), date_pattern='dd-mm-yyyy',justify=CENTER)
        self.entryDateDOJ.place(x=600, y=140, width=100)

        # Salary
        self.salary_var=StringVar()
        lblSalary = Label(self.root, text="Salary", font=("Constantia", 11, "bold"), bg="#efffb5")
        lblSalary.place(x=730, y=140)

        entrySalary = Entry(self.root,textvariable=self.salary_var,justify=CENTER, font=("times new roman", 10, "bold"),
                                       relief=SOLID, bd=1, width=19, fg="#10106E")
        entrySalary.place(x=790, y=140, width=100)

        # Marital status
        self.marital_var=StringVar()
        lblMarital = Label(self.root, text="Marital Status", font=("Constantia", 11, "bold"), bg="#efffb5")
        lblMarital.place(x=910, y=140)

        entryMarital = ttk.Combobox(self.root,textvariable=self.marital_var,justify=CENTER, font=("times new roman", 10, "bold"),
                                    width=19,state="readonly")
        entryMarital['values']=("Select","Unmarried","Married","Divorced")
        entryMarital.place(x=1020, y=140, width=100)
        entryMarital.current(0)

        #status
        self.status_var=StringVar()
        lblStatus = Label(self.root, text="Status", font=("Constantia", 11, "bold"), bg="#efffb5")
        lblStatus.place(x=1150, y=140)

        entryStatus = ttk.Combobox(self.root,textvariable=self.status_var,justify=CENTER, font=("times new roman", 10, "bold"),
                                    width=19,state="readonly")
        entryStatus['values']=("Select","Active","Inactive")
        entryStatus.place(x=1210, y=140, width=100)
        entryStatus.current(0)

        # ======================= Buttons ==========================
        # Calculate button width dynamically
        window_width = 1325
        button_width = (window_width - 50) // 4  # Distribute width equally among 4 buttons with spacing

        # Buttons Placement
        self.btnAdd = Button(self.root,command=self.add_user, text="Add", font=("times new roman", 12, "bold"),
                        relief=SOLID, bd=1, bg="#4CAF50", fg="white",cursor="hand2")
        self.btnAdd.place(x=20, y=180, width=button_width, height=30)

        self.btnUpdate = Button(self.root,command=self.update_user, text="Update", font=("times new roman", 12, "bold"),
                           relief=SOLID, bd=1, bg="#FF9800", fg="white",cursor="hand2",state=DISABLED)
        self.btnUpdate.place(x=20 + button_width + 10, y=180, width=button_width, height=30)

        self.btnDelete = Button(self.root,command=self.delete_user, text="Delete", font=("times new roman", 12, "bold"),
                           relief=SOLID, bd=1, bg="#f44336", fg="white",cursor="hand2",state=DISABLED)
        self.btnDelete.place(x=20 + 2 * (button_width + 10), y=180, width=button_width, height=30)

        self.btnClear = Button(self.root,command=self.clear_records, text="Clear", font=("times new roman", 12, "bold"),
                          relief=SOLID, bd=1, bg="#607D8B", fg="white",cursor="hand2")
        self.btnClear.place(x=20 + 3 * (button_width + 10), y=180, width=button_width, height=30)


        # ===================== Treeview Table ========================

        treeFrame=Frame(self.root,relief=RIDGE,bd=2,bg="white")
        treeFrame.place(x=5,y=220,width=1340,height=350)

        self.lblTitle=Label(treeFrame,text=f"All Users Details[]",font=("verdana",11,"bold"),bg="#2A2A3A",fg="white",anchor=W)
        self.lblTitle.pack(side=TOP,fill=X)


        scrollx=ttk.Scrollbar(treeFrame,orient=HORIZONTAL)
        scrolly=ttk.Scrollbar(treeFrame,orient=VERTICAL)

        self.userRegister=ttk.Treeview(treeFrame,columns=("uid","name","role","gender","dob","idtype","idnum","mobile","doj","salary","mstatus","status"),xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)

        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)

        scrollx.config(command=self.userRegister.xview)
        scrolly.config(command=self.userRegister.yview)

        self.userRegister.heading("uid",text="User ID")
        self.userRegister.heading("name",text="User Name")
        self.userRegister.heading("role",text="Role")
        self.userRegister.heading("gender",text="Gender")
        self.userRegister.heading("dob",text="Date of Birth")
        self.userRegister.heading("idtype",text="ID Type")
        self.userRegister.heading("idnum",text="ID Number")
        self.userRegister.heading("mobile",text="Mobile")
        self.userRegister.heading("doj",text="Date of Joining")
        self.userRegister.heading("salary",text="Salary")
        self.userRegister.heading("mstatus",text="Marital Status")
        self.userRegister.heading("status",text="Status")

        self.userRegister["show"]="headings"

        self.userRegister.column("uid",width=100)
        self.userRegister.column("name",width=100)
        self.userRegister.column("role",width=100)
        self.userRegister.column("gender",width=100)
        self.userRegister.column("dob",width=100)
        self.userRegister.column("idtype",width=100)
        self.userRegister.column("idnum",width=100)
        self.userRegister.column("mobile",width=100)
        self.userRegister.column("doj",width=100)
        self.userRegister.column("salary",width=100)
        self.userRegister.column("mstatus",width=100)
        self.userRegister.column("status",width=100)

        self.userRegister.pack(fill=BOTH,expand=1)

        self.userRegister.bind("<ButtonRelease-1>", self.get_cursor)




        self.user_ID()
        self.show_data()
# ======================================== Functionality ===========================================
    def user_ID(self):
        a=str("UID")
        b=int(time.strftime("%I%M%S"))
        c=int(time.strftime("%d%m%Y"))
        self.d=str(a+str(b+c))
        self.userid_var.set(self.d)

    def capitalize_name(self, var):
        current_value = var.get()
        
        # Allow only alphabetic characters and spaces, limit to 30 characters
        filtered_value = ''.join(char for char in current_value if char.isalpha() or char.isspace())
        
        if len(filtered_value) > 30:
            # Display a message box if the input exceeds 30 characters
            messagebox.showinfo("Input Limit", "Only 30 Characters are Allowed.",parent=self.root)
            # Truncate the value to 30 characters
            filtered_value = filtered_value[:30]
        
        # Capitalize each word
        capitalized_value = filtered_value.title()
        
        # Update the variable
        var.set(capitalized_value)

    def validate_mobile_input(self, P):
        # Ensure only digits are entered and limit to 10 characters
        if P == "":
            return True  # Allow clearing the field
        if P.isdigit() and len(P) <= 10:
            return True
        return False


    # Add
    def add_user(self):
        if self.name_var.get()=="":
            messagebox.showerror("Error","Please Enter the Name",parent=self.root)
        elif self.role_var.get()=="Select":
            messagebox.showerror("Error","Please Select Role",parent=self.root)
        elif self.gender_var.get()=="Select":
            messagebox.showerror("Error","Please Select the Gender",parent=self.root)
        elif self.entryDateDOB.get()=="01-01-2000":
            messagebox.showerror("Error","Select the Date of Birth",parent=self.root)
        elif self.idtype_var.get()=="Select":
            messagebox.showerror("Error","Please Select the ID Type",parent=self.root)
        elif self.idnum_var.get()=="":
            messagebox.showerror("Error","Please Enter ID Number",parent=self.root)
        elif self.mobile_var.get()=="":
            messagebox.showerror("Error","Please Enter Mobile Number",parent=self.root)
        elif self.entryDateDOJ.get()=="":
            messagebox.showerror("Error","Please Select the Joining Date",parent=self.root)
        elif self.salary_var.get()=="":
            messagebox.showerror("Error","Please Enter the Salary",parent=self.root)
        elif self.marital_var.get()=="Select":
            messagebox.showerror("Error","Please Select the Marital Status",parent=self.root)
        elif self.status_var.get()=="Select":
            messagebox.showerror("Error","Please Select the Status",parent=self.root)
        else:
            try:
                add=messagebox.askyesno("Add User",f"Are you sure to Add {self.name_var.get()} with User ID {self.userid_var.get()} to the list?",parent=self.root)
                if add>0:
                    con=sqlite3.connect(database=r'inventory.db')
                    cur=con.cursor()
                    cur.execute("insert into usersdata(User_ID,User_Name,Role,Gender,DOB,ID_Type,ID_Number,Mobile,DOJ,Salary,Marital_Status,Status) values(?,?,?,?,?,?,?,?,?,?,?,?)",(

                                                        self.userid_var.get(),
                                                        self.name_var.get(),
                                                        self.role_var.get(),
                                                        self.gender_var.get(),
                                                        self.entryDateDOB.get(),
                                                        self.idtype_var.get(),
                                                        self.idnum_var.get(),
                                                        self.mobile_var.get(),
                                                        self.entryDateDOJ.get(),
                                                        self.salary_var.get(),
                                                        self.marital_var.get(),
                                                        self.status_var.get()

                                                                            ))
                else:
                    if not add:
                        return
                con.commit()
                con.close()
                self.show_data()
                messagebox.showinfo("Success",f"Product ID {self.userid_var.get()} with the Name {self.name_var.get()} Added Successfully",parent=self.root)
                self.clear_records()
            except Exception as es:
                messagebox.showerror("Error",f"Error Due To:{str(es)}",parent=self.root)
    # Update Data
    def update_user(self):
        if self.name_var.get()=="":
            messagebox.showerror("Error","Please Enter the Name",parent=self.root)
        elif self.role_var.get()=="Select":
            messagebox.showerror("Error","Please Select Role",parent=self.root)
        elif self.gender_var.get()=="Select":
            messagebox.showerror("Error","Please Select the Gender",parent=self.root)
        elif self.entryDateDOB.get()=="01-01-2000":
            messagebox.showerror("Error","Select the Date of Birth",parent=self.root)
        elif self.idtype_var.get()=="Select":
            messagebox.showerror("Error","Please Select the ID Type",parent=self.root)
        elif self.idnum_var.get()=="":
            messagebox.showerror("Error","Please Enter ID Number",parent=self.root)
        elif self.mobile_var.get()=="":
            messagebox.showerror("Error","Please Enter Mobile Number",parent=self.root)
        elif self.entryDateDOJ.get()=="":
            messagebox.showerror("Error","Please Select the Joining Date",parent=self.root)
        elif self.salary_var.get()=="":
            messagebox.showerror("Error","Please Enter the Salary",parent=self.root)
        elif self.marital_var.get()=="Select":
            messagebox.showerror("Error","Please Select the Marital Status",parent=self.root)
        elif self.status_var.get()=="Select":
            messagebox.showerror("Error","Please Select the Status",parent=self.root)
        else:
            try:
                con=sqlite3.connect(database=r'inventory.db')
                cur=con.cursor()
                update=messagebox.askyesno("Update",f"Are you sure to Update Information of '{self.userid_var.get()}' ?",parent=self.root)
                if update>0:
                    cur.execute("update usersdata set User_Name=?,Role=?,Gender=?,DOB=?,ID_Type=?,ID_Number=?,Mobile=?,DOJ=?,Salary=?,Marital_Status=?,Status=? where User_ID=?",(


                                                    self.name_var.get(),
                                                    self.role_var.get(),
                                                    self.gender_var.get(),
                                                    self.entryDateDOB.get(),
                                                    self.idtype_var.get(),
                                                    self.idnum_var.get(),
                                                    self.mobile_var.get(),
                                                    self.entryDateDOJ.get(),
                                                    self.salary_var.get(),
                                                    self.marital_var.get(),
                                                    self.status_var.get(),
                                                    self.userid_var.get()


                                                                ))
                else:
                    if not update:
                        return
                con.commit()
                con.close()
                self.show_data()
                messagebox.showinfo("Updated","Information Updated Successfully",parent=self.root)
                self.clear_records()
            except Exception as es:
                    messagebox.showerror("Error",f"Error Due To:{str(es)}",parent=self.root)

    # Delete Data
    def delete_user(self):
        if self.name_var.get()=="":
            messagebox.showerror("Error","Please Enter the Name",parent=self.root)
        elif self.role_var.get()=="Select":
            messagebox.showerror("Error","Please Select Role",parent=self.root)
        elif self.gender_var.get()=="Select":
            messagebox.showerror("Error","Please Select the Gender",parent=self.root)
        elif self.entryDateDOB.get()=="01-01-2000":
            messagebox.showerror("Error","Select the Date of Birth",parent=self.root)
        elif self.idtype_var.get()=="Select":
            messagebox.showerror("Error","Please Select the ID Type",parent=self.root)
        elif self.idnum_var.get()=="":
            messagebox.showerror("Error","Please Enter ID Number",parent=self.root)
        elif self.mobile_var.get()=="":
            messagebox.showerror("Error","Please Enter Mobile Number",parent=self.root)
        elif self.entryDateDOJ.get()=="":
            messagebox.showerror("Error","Please Select the Joining Date",parent=self.root)
        elif self.salary_var.get()=="":
            messagebox.showerror("Error","Please Enter the Salary",parent=self.root)
        elif self.marital_var.get()=="Select":
            messagebox.showerror("Error","Please Select the Marital Status",parent=self.root)
        elif self.status_var.get()=="Select":
            messagebox.showerror("Error","Please Select the Status",parent=self.root)
        else:
            try:
                con=sqlite3.connect(database=r'inventory.db')
                cur=con.cursor()
                cur.execute("select * from usersdata where User_ID=?",(self.userid_var.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showwarning("Error","No Product User ID Present with the provided Number",parent=self.root)
                else:
                    delete=messagebox.askyesno("Delete",f"Are you sure to Delete the Information of '{self.userid_var.get()}'",parent=self.root)
                    if delete>0:
                        sql=("delete from usersdata where User_ID=?")
                        val=(self.userid_var.get(),)
                        cur.execute(sql,val)
                        messagebox.showinfo("Success",f"User ID '{self.userid_var.get()}' with Name '{self.name_var.get()}' Deleted Successfully",parent=self.root)
                    else:
                        if not delete:
                            return
                    con.commit()
                    con.close()
                    self.show_data()
                    self.clear_records()
            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)

    # Show Data
    def show_data(self):
        con=sqlite3.connect(database=r'inventory.db')
        cur=con.cursor()
        try:
            cur.execute("select * from usersdata")
            data=cur.fetchall()
            if len(data)!=0:
                self.userRegister.delete(*self.userRegister.get_children())
                for i in data:
                    self.userRegister.insert("",END,values=i)
                    con.commit()
                con.close()
                self.lblTitle.config(text=f"All Users Details[{str(len(self.userRegister.get_children()))}]")
        except Exception as es:
                messagebox.showerror("Error",f"Error Due To:{str(es)}",parent=self.root)

    # Get Cursor
    def get_cursor(self, event=""):
        row = self.userRegister.focus()  # Get the selected row
        content = self.userRegister.item(row)  # Get row data
        data = content.get("values", [])  # Ensure we get a list, even if empty

        if not data:  # If data is empty, return without setting values
            return
        
        # Ensure the data has the expected number of elements
        if len(data) < 12:  # Adjust based on the number of expected columns
            return

        self.userid_var.set(data[0])
        self.name_var.set(data[1])
        self.role_var.set(data[2])
        self.gender_var.set(data[3])
        self.entryDateDOB.set_date(data[4])
        self.idtype_var.set(data[5])
        self.idnum_var.set(data[6])
        self.mobile_var.set(data[7])
        self.entryDateDOJ.set_date(data[8])
        self.salary_var.set(data[9])
        self.marital_var.set(data[10])
        self.status_var.set(data[11])

        self.btnAdd.config(state="disabled")
        self.btnUpdate.config(state="normal")
        self.btnDelete.config(state="normal")


    def clear_records(self):
        try:
            a=str("UID")
            b=int(time.strftime("%I%M%S"))
            c=int(time.strftime("%d%m%Y"))
            self.d=str(a+str(b+c))
            self.userid_var.set(self.d)

            self.name_var.set("")
            self.role_var.set("Select")
            self.gender_var.set("Select")
            
            # Resetting date fields to default values
            if hasattr(self.entryDateDOB, 'set_date'):
                self.entryDateDOB.set_date("01-01-2000")
            
            self.idtype_var.set('Select')
            self.idnum_var.set("")
            self.mobile_var.set("")
            
            # Check for valid method for entryDateDOJ
            today_date = datetime.today().strftime('%d-%m-%Y')
            if hasattr(self.entryDateDOJ, 'set_date'):
                self.entryDateDOJ.set_date(today_date)
            
            self.salary_var.set("")
            self.marital_var.set("Select")
            self.status_var.set("Select")

            self.btnAdd.config(state="normal")
            self.btnUpdate.config(state=DISABLED)
            self.btnDelete.config(state=DISABLED)
            self.show_data()
        except Exception as es:
            messagebox.showerror("Error", f"Error Due To: {str(es)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    app = UserSection(root)
    root.mainloop()

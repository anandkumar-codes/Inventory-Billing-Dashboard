import sqlite3
from tkinter import *
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime
import os
import time
from PIL import Image, ImageTk

class AttendanceSection:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Management")
        self.root.geometry("1350x650+0+0")
        self.root.config(bg="#efffb5")
        self.root.resizable(False, False)
        self.root.focus_force()
        self.root.grab_set()

        # ==================== Image Handling ====================
        img_path1 = r"images/plogo.png"
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
            self.root, text="Attendance Management System",
            image=self.img1, compound=LEFT, font=("Verdana", 25, "bold"),
            fg="black", bg="#c1ffe4", relief=SOLID, padx=10
        )
        self.lblTitle.place(x=5, y=20, width=1350)

        # ====================== Date and Time========================
        self.lbldateTime=Label(self.root,font=("times new roman",15,"bold"),fg="white",bg="#125f36")
        self.lbldateTime.place(x=0,y=100,relwidth=1)

        # =============== Labels and Entries ==========================
        # staffID
        self.staffid_var=StringVar()
        lblstaffID=Label(self.root,text="*Staff ID",font=("Constantia",12,"bold"),bg="#efffb5")
        lblstaffID.place(x=10,y=150)

        entrystaffID=Entry(self.root,textvariable=self.staffid_var,font=("times new roman",11,"bold"),relief=SOLID,justify=CENTER,state="readonly")
        entrystaffID.place(x=90,y=150,width=100,height=20)

        # Name
        self.name_var=StringVar()
        lblName=Label(self.root,text="Name",font=("Constantia",12,"bold"),bg="#efffb5")
        lblName.place(x=210,y=150)

        entryName=Entry(self.root,textvariable=self.name_var,font=("times new roman",11,"bold"),relief=SOLID,justify=CENTER,state="readonly")
        entryName.place(x=270,y=150,width=240,height=20)

        # Status
        self.status_var=StringVar()
        lblStatus = Label(self.root, text="Status", font=("Constantia", 11, "bold"), bg="#efffb5")
        lblStatus.place(x=550, y=150)

        entryStatus=ttk.Combobox(self.root,textvariable=self.status_var,font=("times new roman",10,"bold"),justify=CENTER,state="readonly")
        entryStatus['values']=("Select","Present","Absent","Leave","Holiday")
        entryStatus.current(0)
        entryStatus.place(x=615,y=150,width=100,height=20)
        entryStatus.bind("<<ComboboxSelected>>", self.update_reason_state)

        # Reason
        self.reason_var=StringVar()
        lblReason=Label(self.root,text="Reason",font=("Constantia",12,"bold"),bg="#efffb5")
        lblReason.place(x=750,y=150)

        self.entryReason=Entry(self.root,textvariable=self.reason_var,font=("times new roman",11,"bold"),relief=SOLID,justify=CENTER,state="readonly")
        self.entryReason.place(x=830,y=150,width=240,height=20)

        # ======================== Buttons ==============================
        # Buttons Placement
        self.btnAdd = Button(self.root,command=self.add_attendance, text="Add Attendance", font=("times new roman", 10, "bold"),
                        relief=SOLID, bd=1, bg="green", fg="white",cursor="hand2")
        self.btnAdd.place(x=1100,y=150,height=20,width=230)

        # ====================== Search Frame ===========================
        search_frame=Frame(self.root,relief=SOLID,bd=1,bg="white")
        search_frame.place(x=520,y=190,width=820,height=40)

        # Search By StaffID
        searchLabelStaffID=Label(search_frame,text="Search By | Staff ID",font=("verdana",10,"bold"),bg="white")
        searchLabelStaffID.place(x=5,y=8)

        self.var_search_StaffID=StringVar()
        entrySearchByStaffID=Entry(search_frame,textvariable=self.var_search_StaffID,font=("verdana",10),bd=1,relief=SOLID,width=15)
        entrySearchByStaffID.place(x=160,y=9)
        entrySearchByStaffID.bind("<Key>",self.search_staffID)

        # Search By Name
        searchLabelName=Label(search_frame,text="Name",font=("verdana",10,"bold"),bg="white")
        searchLabelName.place(x=290,y=8)

        self.var_search_Name=StringVar()
        entrySearchByName=Entry(search_frame,textvariable=self.var_search_Name,font=("verdana",10),bd=1,relief=SOLID,width=15)
        entrySearchByName.place(x=350,y=9)
        entrySearchByName.bind("<Key>",self.search_name)

        # Search By Date
        today_date = datetime.today().date()
        searchLabelDate=Label(search_frame,text="Date",font=("verdana",10,"bold"),bg="white")
        searchLabelDate.place(x=480,y=8)

        self.entrySearchDate = DateEntry(search_frame, width=19, background='darkblue', foreground='white',
                               font=("times new roman", 10, "bold"), date_pattern='yyyy-mm-dd',justify=CENTER,maxdate=today_date)
        self.entrySearchDate.place(x=530, y=8, width=100)
        self.entrySearchDate.bind("<Key>",self.search_date)

        # Show All
        btnClear=Button(search_frame,command=self.show_data_recorded,text="Show All",font=("verdana",8,"bold"),border=0,relief=RIDGE,bd=0,activebackground="#34495E",bg="#34495E",fg="white",cursor="hand2")
        btnClear.place(x=650,y=9,width=150,height=20)

        # ===================== Treeview Table for CHecking Attendance List========================

        treeFrame=Frame(self.root,relief=RIDGE,bd=2,bg="white")
        treeFrame.place(x=520,y=240,width=820,height=400)

        self.lblTitle=Label(treeFrame,text="ALL ATTENDANCE RECORD",font=("verdana",10,"bold"),bg="#27AE60",fg="white")
        self.lblTitle.pack(side=TOP,fill=X)

        scrollx=ttk.Scrollbar(treeFrame,orient=HORIZONTAL)
        scrolly=ttk.Scrollbar(treeFrame,orient=VERTICAL)

        self.recordedAttendance=ttk.Treeview(treeFrame,columns=("date","staff","name","status","reason"),xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)

        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)

        scrollx.config(command=self.recordedAttendance.xview)
        scrolly.config(command=self.recordedAttendance.yview)

        self.recordedAttendance.heading("date",text="Date")
        self.recordedAttendance.heading("staff",text="Staff ID")
        self.recordedAttendance.heading("name",text="Staff Name")
        self.recordedAttendance.heading("status",text="Status")
        self.recordedAttendance.heading("reason",text="Reason")


        self.recordedAttendance["show"]="headings"

        self.recordedAttendance.column("date",width=100)
        self.recordedAttendance.column("staff",width=100)
        self.recordedAttendance.column("name",width=100)
        self.recordedAttendance.column("status",width=100)
        self.recordedAttendance.column("reason",width=100)

        self.recordedAttendance.pack(fill=BOTH,expand=1)

        # ===================== Treeview Table Main========================

        treeFrame=Frame(self.root,relief=RIDGE,bd=2,bg="white")
        treeFrame.place(x=5,y=190,width=500,height=450)

        # Date
        today_date = datetime.today().date()
        lblDate = Label(treeFrame, text="Date", font=("Constantia", 11, "bold"), bg="#efffb5",background="white")
        lblDate.pack(side=TOP, anchor=W, padx=10, pady=5)

        self.entryDate = DateEntry(treeFrame, width=19, background='darkblue', foreground='white',
                               font=("times new roman", 10, "bold"), date_pattern='yyyy-mm-dd',justify=CENTER,maxdate=today_date)
        self.entryDate.place(x=60, y=6, width=100)
        self.entryDate.bind("<<DateEntrySelected>>", lambda e: self.show_data())
        self.entryDate.bind("<KeyRelease>", lambda e: self.handle_date_cleared())  # Detect manual clearing


        scrollx=ttk.Scrollbar(treeFrame,orient=HORIZONTAL)
        scrolly=ttk.Scrollbar(treeFrame,orient=VERTICAL)

        self.userAttendance=ttk.Treeview(treeFrame,columns=("uid","name","mobile"),xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)

        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)

        scrollx.config(command=self.userAttendance.xview)
        scrolly.config(command=self.userAttendance.yview)

        self.userAttendance.heading("uid",text="Staff ID")
        self.userAttendance.heading("name",text="Staff Name")
        self.userAttendance.heading("mobile",text="Mobile")


        self.userAttendance["show"]="headings"

        self.userAttendance.column("uid",width=100)
        self.userAttendance.column("name",width=100)
        self.userAttendance.column("mobile",width=100)


        self.userAttendance.pack(fill=BOTH,expand=1)

        self.userAttendance.bind("<ButtonRelease-1>", self.get_cursor)

        self.show_data()

        self.datetime_update()

        self.show_data_recorded()

# =========================== Functionality===========================

    def datetime_update(self):
        date_=time.strftime("%d-%m-%Y (%A)")
        time_=time.strftime("%r")
        self.lbldateTime.config(text=f"Date: {str(date_)}\t\t\t\tTime: {str(time_)}")
        self.lbldateTime.after(200,self.datetime_update)

    def update_reason_state(self, event=None):
        """Enable or disable reason entry based on status selection."""
        if self.status_var.get() in ["Leave", "Holiday"]:
            self.entryReason.config(state=NORMAL)  # Enable entry
        else:
            self.entryReason.config(state=DISABLED)  # Disable entry

    # Show Data - Only Staff who have NOT marked attendance for the selected date
    def show_data(self):
        date = self.entryDate.get().strip()  # Get selected date

        if not date:  # If DateEntry is cleared, reset the table
            self.userAttendance.delete(*self.userAttendance.get_children())
            return

        con = sqlite3.connect(database=r'inventory.db')
        cur = con.cursor()
        try:
            # Get all staff from usersdata
            cur.execute("SELECT User_ID, User_Name, Mobile FROM usersdata where Status='Active'")
            all_staff = cur.fetchall()

            # Get staff who have already marked attendance on the selected date
            cur.execute("SELECT Staff_ID FROM attendance WHERE Date=?", (date,))
            attended_staff = {row[0] for row in cur.fetchall()}  # Convert to a set for quick lookup

            # Filter staff who have NOT marked attendance
            absent_staff = [staff for staff in all_staff if staff[0] not in attended_staff]

            # Clear existing treeview data
            self.userAttendance.delete(*self.userAttendance.get_children())

            # Insert absent staff into the treeview
            for staff in absent_staff:
                self.userAttendance.insert("", END, values=staff)

            con.commit()
        except Exception as es:
            messagebox.showerror("Error", f"Error Due To: {str(es)}", parent=self.root)
        finally:
            con.close()

    def handle_date_cleared(self):
        if not self.entryDate.get().strip():  # If DateEntry is empty
            self.userAttendance.delete(*self.userAttendance.get_children())  # Clear table


# Get Cursor
    def get_cursor(self, event=""):
        row = self.userAttendance.focus()  # Get the selected row
        content = self.userAttendance.item(row)  # Get row data
        data = content.get("values", [])  # Ensure we get a list, even if empty

        if not data:  # If data is empty, return without setting values
            return

        # Ensure the data has the expected number of elements
        if len(data) < 3:  # Adjust based on the number of expected columns
            return

        self.staffid_var.set(data[0])
        self.name_var.set(data[1])
        self.show_data()

    def add_attendance(self):
        date = self.entryDate.get()
        staff_id = self.staffid_var.get().strip()  # Ensure no extra spaces
        name = self.name_var.get().strip()
        status = self.status_var.get()
        reason = self.reason_var.get().strip()

        # === Input Validations ===
        if not staff_id:
            messagebox.showerror("Error", "Please select a staff member!", parent=self.root)
            return
        if status == "Select":
            messagebox.showerror("Error", "Please select an attendance status!", parent=self.root)
            return
        if status in ["Leave", "Holiday"] and not reason:
            messagebox.showerror("Error", f"Reason is required for {status}!", parent=self.root)
            return

        # === Database Operations with Exception Handling ===
        try:
            with sqlite3.connect(r'inventory.db') as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO attendance (Date, Staff_ID, Name, Status, Reason) VALUES (?, ?, ?, ?, ?)",
                    (date, staff_id, name, status, reason),
                )
                con.commit()

            messagebox.showinfo("Success", "Attendance recorded successfully!", parent=self.root)
            self.clear()
            self.show_data_recorded()

            # === Remove staff from Treeview ===
            for item in self.userAttendance.get_children():
                row_data = self.userAttendance.item(item, "values")
                if row_data and row_data[0] == staff_id:
                    self.userAttendance.delete(item)
                    break  # Exit loop after deletion

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}", parent=self.root)

    def clear(self):
        self.staffid_var.set("")
        self.name_var.set("")
        self.status_var.set("Select")
        self.reason_var.set("")

    def clear_search(self):
        self.var_search_StaffID.set("")
        self.var_search_Name.set("")
        self.root.focus_set()

    # Show Data
    def show_data_recorded(self):
        con=sqlite3.connect(database=r'inventory.db')
        cur=con.cursor()
        try:
            cur.execute("select * from attendance")
            data=cur.fetchall()
            if len(data)!=0:
                self.recordedAttendance.delete(*self.recordedAttendance.get_children())
                for i in data:
                    self.recordedAttendance.insert("",END,values=i)
                    con.commit()
                con.close()
                self.clear_search()
        except Exception as es:
                messagebox.showerror("Error",f"Error Due To:{str(es)}",parent=self.root)

    # ====================== Search ========================
    # Search Staff ID
    def search_staffID(self,ev):
        con=sqlite3.connect(database=r'inventory.db')
        cur=con.cursor()
        try:
            cur.execute("select * from attendance where Staff_ID LIKE '%"+self.var_search_StaffID.get()+"%'")
            row=cur.fetchall()
            if len(row)>0:
                self.recordedAttendance.delete(*self.recordedAttendance.get_children())
                for i in row:
                    self.recordedAttendance.insert("",END,values=i)
            else:
                self.recordedAttendance.delete(*self.recordedAttendance.get_children())
        except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)

    # Search Name
    def search_name(self,ev):
        con=sqlite3.connect(database=r'inventory.db')
        cur=con.cursor()
        try:
            cur.execute("select * from attendance where Name LIKE '%"+self.var_search_Name.get()+"%'")
            row=cur.fetchall()
            if len(row)>0:
                self.recordedAttendance.delete(*self.recordedAttendance.get_children())
                for i in row:
                    self.recordedAttendance.insert("",END,values=i)
            else:
                self.recordedAttendance.delete(*self.recordedAttendance.get_children())
        except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)

    # Search Date
    def search_date(self,ev):
        con=sqlite3.connect(database=r'inventory.db')
        cur=con.cursor()
        try:
            cur.execute("select * from attendance where Date LIKE '%"+self.entrySearchDate.get()+"%'")
            row=cur.fetchall()
            if len(row)>0:
                self.recordedAttendance.delete(*self.recordedAttendance.get_children())
                for i in row:
                    self.recordedAttendance.insert("",END,values=i)
            else:
                self.recordedAttendance.delete(*self.recordedAttendance.get_children())
        except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)






if __name__ == "__main__":
    root = Tk()
    app = AttendanceSection(root)
    root.mainloop()
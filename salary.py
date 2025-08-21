from tkinter import *
import time
from tkinter import messagebox,ttk
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import os
from datetime import datetime
import sqlite3
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
from datetime import datetime
from num2words import num2words


class SalarySection:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System | Salary")
        self.root.geometry("1340x650+0+50")
        self.root.config(bg="#ddf3ef")
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
            self.root, text="Inventory Management System (Salary Section)",
            image=self.img1, compound=LEFT, font=("Verdana", 25, "bold"),
            fg="black", bg="#ffe2fa", relief=SOLID, padx=10
        )
        self.lblTitle.place(x=5, y=20, width=1340)


        # ======================= Labels and Entries==========================

        # Staff
        self.Staffid_var=StringVar()
        lblStaff = Label(self.root, text="*Staff ID", font=("Constantia", 11, "bold"), bg="#ddf3ef",fg="#dd2f00")
        lblStaff.place(x=500, y=100)

        self.entryStaff = Entry(self.root,textvariable=self.Staffid_var,justify=CENTER, font=("times new roman", 10, "bold"),
                                       relief=SOLID, bd=1, width=19, fg="#10106E")
        self.entryStaff.place(x=580, y=100, width=200)

        # Name
        self.Nameid_var=StringVar()
        lblName = Label(self.root, text="Name", font=("Constantia", 11, "bold"), bg="#ddf3ef")
        lblName.place(x=10, y=130)

        entryName = Entry(self.root,textvariable=self.Nameid_var,justify=CENTER, font=("times new roman", 10, "bold"),
                                       relief=SOLID, bd=1, width=19, fg="#10106E",state="readonly")
        entryName.place(x=70, y=130, width=200)

        # Role
        self.Roleid_var=StringVar()
        lblRole = Label(self.root, text="Role", font=("Constantia", 11, "bold"), bg="#ddf3ef")
        lblRole.place(x=300, y=130)

        entryRole = Entry(self.root,textvariable=self.Roleid_var,justify=CENTER, font=("times new roman", 10, "bold"),
                                       relief=SOLID, bd=1, width=19, fg="#10106E",state="readonly")
        entryRole.place(x=350, y=130, width=200)

        # Mobile
        self.Mobileid_var=StringVar()
        lblMobile = Label(self.root, text="Mobile", font=("Constantia", 11, "bold"), bg="#ddf3ef")
        lblMobile.place(x=580, y=130)

        entryMobile = Entry(self.root,textvariable=self.Mobileid_var,justify=CENTER, font=("times new roman", 10, "bold"),
                                       relief=SOLID, bd=1, width=19, fg="#10106E",state="readonly")
        entryMobile.place(x=660, y=130, width=200)

        # salary
        self.salaryid_var=StringVar()
        lblsalary = Label(self.root, text="Actual Salary", font=("Constantia", 11, "bold"), bg="#ddf3ef")
        lblsalary.place(x=900, y=130)

        entrysalary = Entry(self.root,textvariable=self.salaryid_var,justify=CENTER, font=("times new roman", 10, "bold"),
                                       relief=SOLID, bd=1, width=19, fg="#10106E",state="readonly")
        entrysalary.place(x=1030, y=130, width=200)

        # From Date
        today_date = datetime.today().date()
        lblfromDate=Label(self.root,text="From Date",font=("Constantia",10,"bold"),bg="#f07cd7")
        lblfromDate.place(x=450,y=160)

        self.fromDate = DateEntry(self.root, width=19, background='darkblue', foreground='white',
                               font=("times new roman", 10, "bold"), date_pattern='yyyy-mm-dd',justify=CENTER,maxdate=today_date)
        self.fromDate.place(x=530, y=160, width=100)

        # To Date
        today_date = datetime.today().date()
        lbltoDate=Label(self.root,text="To Date",font=("Constantia",10,"bold"),bg="#f07cd7")
        lbltoDate.place(x=650,y=160)

        self.toDate = DateEntry(self.root, width=19, background='darkblue', foreground='white',
                               font=("times new roman", 10, "bold"), date_pattern='yyyy-mm-dd',justify=CENTER)
        self.toDate.place(x=720, y=160, width=100)

        # total days
        self.tdays_var=StringVar()
        lbltdays = Label(self.root, text="Total Days", font=("Constantia", 11, "bold"), bg="#ddf3ef")
        lbltdays.place(x=10, y=190)

        entrytdays = Entry(self.root,textvariable=self.tdays_var,justify=CENTER, font=("times new roman", 10, "bold"),
                                       relief=SOLID, bd=1, width=19, fg="#10106E",state="readonly")
        entrytdays.place(x=110, y=190, width=160)

        # Present
        self.present_var=StringVar()
        lblpresent = Label(self.root, text="Present", font=("Constantia", 11, "bold"), bg="#ddf3ef")
        lblpresent.place(x=300, y=190)

        entrypresent = Entry(self.root,textvariable=self.present_var,justify=CENTER, font=("times new roman", 10, "bold"),
                                       relief=SOLID, bd=1, width=19, fg="#10106E",state="readonly")
        entrypresent.place(x=380, y=190, width=50)

        # Absent
        self.Absent_var=StringVar()
        lblabsent = Label(self.root, text="Absent", font=("Constantia", 11, "bold"), bg="#ddf3ef")
        lblabsent.place(x=450, y=190)

        entryabsent = Entry(self.root,textvariable=self.Absent_var,justify=CENTER, font=("times new roman", 10, "bold"),
                                       relief=SOLID, bd=1, width=19, fg="#10106E",state="readonly")
        entryabsent.place(x=520, y=190, width=50)

        # Non Working
        self.ndays_var=StringVar()
        lblndays = Label(self.root, text="Non-Working Days", font=("Constantia", 11, "bold"), bg="#ddf3ef")
        lblndays.place(x=600, y=190)

        entryndays = Entry(self.root,textvariable=self.ndays_var,justify=CENTER, font=("times new roman", 10, "bold"),
                                       relief=SOLID, bd=1, width=19, fg="#10106E",state="readonly")
        entryndays.place(x=760, y=190, width=40)

        # Salary(Deductions)
        self.dsalary_var=StringVar()
        lbldsalary = Label(self.root, text="Salary(-Deductions)", font=("Constantia", 11, "bold"), bg="#ddf3ef")
        lbldsalary.place(x=10, y=220)

        entrydsalary = Entry(self.root,textvariable=self.dsalary_var,justify=CENTER, font=("times new roman", 10, "bold"),
                                       relief=SOLID, bd=1, width=19, fg="#10106E",state="readonly")
        entrydsalary.place(x=170, y=220, width=100)

        # Present Salary
        self.psalary_var=StringVar()
        lbldsalary = Label(self.root, text="Present Pay", font=("Constantia", 11, "bold"), bg="#ddf3ef")
        lbldsalary.place(x=300, y=220)

        entrydsalary = Entry(self.root,textvariable=self.psalary_var,justify=CENTER, font=("times new roman", 10, "bold"),
                                       relief=SOLID, bd=1, width=19, fg="#10106E",state="readonly")
        entrydsalary.place(x=400, y=220, width=100)

        # Absent Deducations
        self.absentdeductions_var=StringVar()
        lbldsalary = Label(self.root, text="Absent Deductions", font=("Constantia", 11, "bold"), bg="#ddf3ef")
        lbldsalary.place(x=530, y=220)

        entrydsalary = Entry(self.root,textvariable=self.absentdeductions_var,justify=CENTER, font=("times new roman", 10, "bold"),
                                       relief=SOLID, bd=1, width=19, fg="#10106E",state="readonly")
        entrydsalary.place(x=680, y=220, width=100)

        # ====================== deductions frame ================
        deductions_frame= LabelFrame(self.root,text="Deduction", font=("Constantia", 9, "bold",UNDERLINE), fg="white", bg="#c86b50")
        deductions_frame.place(x=830,y=190,width=400,height=50)

        # ESI
        lblesi=Label(deductions_frame,text="ESI", font=("Constantia", 9, "bold"), bg="#c86b50",fg="white")
        lblesi.place(x=5,y=5)

        self.esi_var=StringVar()
        entryesi=Entry(deductions_frame,textvariable=self.esi_var,justify=CENTER, font=("times new roman", 10, "bold"),fg="black",state="readonly")
        entryesi.place(x=30,y=5,width=50)

        # PF
        lblPF=Label(deductions_frame,text="PF", font=("Constantia", 9, "bold"), bg="#c86b50",fg="white")
        lblPF.place(x=100,y=5)

        self.PF_var=StringVar()
        entryPF=Entry(deductions_frame,textvariable=self.PF_var,justify=CENTER, font=("times new roman", 10, "bold"),fg="black",state="readonly")
        entryPF.place(x=130,y=5,width=50)

        # TA
        lblTA=Label(deductions_frame,text="TA", font=("Constantia", 9, "bold"), bg="#c86b50",fg="white")
        lblTA.place(x=200,y=5)

        self.TA_var=StringVar()
        entryTA=Entry(deductions_frame,textvariable=self.TA_var,justify=CENTER, font=("times new roman", 10, "bold"),fg="black",state="readonly")
        entryTA.place(x=230,y=5,width=50)

        # DA
        lblDA=Label(deductions_frame,text="DA", font=("Constantia", 9, "bold"), bg="#c86b50",fg="white")
        lblDA.place(x=300,y=5)

        self.DA_var=StringVar()
        entryDA=Entry(deductions_frame,textvariable=self.DA_var,justify=CENTER, font=("times new roman", 10, "bold"),fg="black",state="readonly")
        entryDA.place(x=330,y=5,width=50)


        # ======================================== Buttons -==============================

        # Buttons Placement
        # Fetch Details
        self.btnFetch = Button(self.root, text="Fetch Details", command=self.fetch_data, font=("times new roman", 10, "bold"),
                        relief=SOLID, bd=1, bg="green", fg="white",cursor="hand2")
        self.btnFetch.place(x=800,y=100,height=20,width=230)

        # Fetch Record
        self.btnRecord = Button(self.root, text="Fetch Record", command=self.fetch_record, font=("times new roman", 10, "bold"),
                        relief=SOLID, bd=1, bg="green", fg="white",cursor="hand2")
        self.btnRecord.place(x=860,y=160,height=20,width=230)

        # Fetch Record
        self.btnGeneratew = Button(self.root, text="Generate Pay Slip", command=self.generate_salary_pdf, font=("times new roman", 10, "bold"),
                        relief=SOLID, bd=1, bg="#17a589", fg="white",cursor="hand2")
        self.btnGeneratew.place(x=500,y=250,height=20,width=230)

# ============================= Functionality ============================

    def fetch_data(self):
        con = sqlite3.connect(database=r'inventory.db')
        cur = con.cursor()
        try:
            cur.execute(
                "SELECT User_Name, Role, Mobile, Salary FROM usersdata WHERE User_ID=?",
                (self.Staffid_var.get(),)
            )
            row = cur.fetchone()
            if row is not None:
                # Set the text variables with fetched data
                self.Nameid_var.set(row[0])
                self.Roleid_var.set(row[1])
                self.Mobileid_var.set(row[2])
                self.salaryid_var.set(row[3])
                self.entryStaff.config(state="readonly")
            else:
                messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Error Due To: {str(es)}", parent=self.root)
        finally:
            con.close()

    def fetch_record(self):
        con = sqlite3.connect(database=r'inventory.db')
        cur = con.cursor()
        try:
            from_date = self.fromDate.get_date()
            to_date = self.toDate.get_date()
            staff_id = self.Staffid_var.get()
            name = self.Nameid_var.get()

            if not staff_id:
                messagebox.showerror("Error", "Please enter Staff ID first!", parent=self.root)
                return
            
            if not name:
                messagebox.showerror("Error", "Please Click the Fetcht Details Button", parent=self.root)
                return

            # Calculate Total Days (Difference between from_date and to_date)
            total_days = (to_date - from_date).days + 1  # +1 to include both start and end date

            # Fetch attendance records within the given date range
            cur.execute(
                "SELECT Date, Status FROM attendance WHERE Staff_ID=? AND Date BETWEEN ? AND ?",
                (staff_id, from_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d"))
            )
            records = cur.fetchall()

            # Count attendance types
            present_days = sum(1 for record in records if record[1] == "Present")
            absent_days = sum(1 for record in records if record[1] == "Absent")
            non_working_days = sum(1 for record in records if record[1] in ["Leave", "Holiday"])

            # Ensure the sum of counted days equals total_days
            counted_days = present_days + absent_days + non_working_days
            if counted_days < total_days:
                missing_days = total_days - counted_days
                absent_days += missing_days  # Add missing days to absent count

            # Update the entry fields
            self.tdays_var.set(total_days)
            self.present_var.set(present_days)
            self.Absent_var.set(absent_days)
            self.ndays_var.set(non_working_days)

            # Fetch the actual salary
            actual_salary = float(self.salaryid_var.get()) if self.salaryid_var.get() else 0.0

            # **Calculate deductions**
            esi = round((3 / 100) * actual_salary, 2)
            pf = round((3.5 / 100) * actual_salary, 2)
            ta = round((2 / 100) * actual_salary, 2)
            da = round((2.5 / 100) * actual_salary, 2)

            # **Update deduction entry fields**
            self.esi_var.set(esi)
            self.PF_var.set(pf)
            self.TA_var.set(ta)
            self.DA_var.set(da)

            # **Calculate final salary after deductions**
            total_deductions = esi + pf + ta + da
            final_salary = round(actual_salary - total_deductions, 2)
            self.dsalary_var.set(final_salary)

            # **Calculate Per Day Salary**
            per_day_salary = round(final_salary / total_days, 2) if total_days > 0 else 0

            # **Calculate Present Salary (including Non-Working Days)**
            present_salary = round((present_days + non_working_days) * per_day_salary, 2)
            self.psalary_var.set(present_salary)

            # **Calculate Absent Deductions**
            absent_deductions = round(absent_days * per_day_salary, 2)
            self.absentdeductions_var.set(absent_deductions)

        except Exception as es:
            messagebox.showerror("Error", f"Error Due To: {str(es)}", parent=self.root)
        finally:
            con.close()



    def generate_salary_pdf(self):
        """Generates a PDF of the salary slip and saves it in the 'Salary Slips' directory."""
        
        if self.PF_var.get()=="":
            messagebox.showwarning("Warning","Please Fetch the salary for Certain Period")
            return

        # Create folder if it doesn't exist
        folder_path = "Salary Slips"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        try:
            # Fetching Data
            staff_id = self.Staffid_var.get()
            staff_name = self.Nameid_var.get()
            role = self.Roleid_var.get()
            mobile = self.Mobileid_var.get()
            actual_salary = float(self.salaryid_var.get() or 0)
            total_days = int(self.tdays_var.get() or 0)
            present_days = int(self.present_var.get() or 0)
            absent_days = int(self.Absent_var.get() or 0)
            non_working_days = int(self.ndays_var.get() or 0)

            esi = float(self.esi_var.get() or 0)
            pf = float(self.PF_var.get() or 0)
            ta = float(self.TA_var.get() or 0)
            da = float(self.DA_var.get() or 0)
            absent_deductions = float(self.absentdeductions_var.get() or 0)

            # Salary Calculations
            total_fixed_deductions = esi + pf + ta + da
            salary_after_deductions = actual_salary - total_fixed_deductions
            net_salary = round(salary_after_deductions - absent_deductions)

            # Convert Net Salary to Words
            net_salary_words = num2words(net_salary, lang='en').title() + " Only"

            # Fetch current date
            fetch_date = datetime.now().strftime("%Y-%m-%d")
            filename_date = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Salary Period (Replace with actual input if needed)
            from_date = self.fromDate.get_date()
            to_date = self.toDate.get_date()

            # PDF file path
            pdf_filename = f"{folder_path}/SalarySlip_{staff_id}_{filename_date}.pdf"

            # PDF Document Setup
            pdf = SimpleDocTemplate(pdf_filename, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
            elements = []
            styles = getSampleStyleSheet()

            # Company Details
            company_details = Paragraph(
                "<b>INDIAN ELECTRONICS</b><br/>123 Tech Street, New Delhi, India<br/>"
                "Phone: +91-9876543210 | Email: support@indianelectronics.com",
                styles["Normal"]
            )
            elements.append(company_details)
            elements.append(Spacer(1, 10))

            # Title
            title = Paragraph("<b>Salary Slip</b>", styles["Title"])
            elements.append(title)
            elements.append(Spacer(1, 10))

            # Date and Salary Period
            elements.append(Paragraph(f"<b>Generated On:</b> {fetch_date}", styles["Normal"]))
            elements.append(Paragraph(f"<b>Salary Period:</b> {from_date} to {to_date}", styles["Normal"]))
            elements.append(Spacer(1, 10))

            # Employee Details Table
            emp_details = [
                ["Employee ID:", staff_id, "Role:", role],
                ["Employee Name:", staff_name, "Mobile:", mobile],
                ["Total Days:", total_days, "Present Days:", present_days],
                ["Absent Days:", absent_days, "Non-Working Days:", non_working_days]
            ]
            emp_table = Table(emp_details, colWidths=[100, 150, 100, 150])
            emp_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
                ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
            ]))
            elements.append(emp_table)
            elements.append(Spacer(1, 10))

            # Salary Breakdown Title
            elements.append(Paragraph("<b>Salary Breakdown</b>", styles["Heading2"]))
            elements.append(Spacer(1, 10))

            # Salary Breakdown Table
            earnings_deductions = [
                ["Earnings", "Amount", "Deductions", "Amount"],
                ["Basic Salary", actual_salary, "", ""],
                ["", "", "Fixed Deductions", ""],  # Label for Fixed Deductions
                ["", "", "ESI", esi],
                ["", "", "PF", pf],
                ["", "", "TA", ta],
                ["", "", "DA", da],
                ["", "", "Total Fixed Deductions", f"{total_fixed_deductions}"],  
                ["Salary After Fixed Deductions", salary_after_deductions, "Absent Deductions", absent_deductions],
                ["", "", "Final Net Salary", f"{net_salary}"]
            ]

            salary_table = Table(earnings_deductions, colWidths=[150, 100, 150, 100])
            salary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('FONTNAME', (2, 2), (2, 2), 'Helvetica-Bold'),  # Fixed Deductions Label
                ('BACKGROUND', (2, 2), (3, 2), colors.lightgrey),
                ('FONTNAME', (2, 7), (2, 7), 'Helvetica-Bold'),  # Total Fixed Deductions
                ('FONTNAME', (2, 9), (2, 9), 'Helvetica-Bold')  # Final Net Salary
            ]))

            elements.append(salary_table)
            elements.append(Spacer(1, 10))

            # Final Salary in Words
            elements.append(Paragraph(f"<b>Net Salary (In Words):</b> {net_salary_words}", styles["Normal"]))

            # Build PDF
            pdf.build(elements)

            # Show success message
            messagebox.showinfo("Success", f"Salary slip generated successfully!\nSaved at: {pdf_filename}", parent=self.root)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate salary slip.\nError: {str(e)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    app = SalarySection(root)
    root.mainloop()
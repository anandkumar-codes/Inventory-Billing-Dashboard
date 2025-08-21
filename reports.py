from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import os
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime

class ReportSection:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System | Reports")
        self.root.geometry("1345x700+5+50")
        self.root.config(bg="#e1ffda")
        self.root.resizable(False, False)
        self.root.focus_force()
        self.root.grab_set()

        # ================ Image Handling ======================
        image_path = os.path.join(os.path.dirname(__file__), "images/logo1.png")
        try:
            img = Image.open(image_path).resize((60, 60), Image.Resampling.LANCZOS)
            self.img1 = ImageTk.PhotoImage(img)
        except FileNotFoundError:
            messagebox.showwarning("Warning", "Image not found! Using default logo.")
            self.img1 = None  # Placeholder

        # ====================== Main Title =====================
        self.lblTitle = Label(
            self.root, text="Inventory Management System (Reports Section)",
            image=self.img1, compound=LEFT, font=("Verdana", 25, "bold"),
            fg="black", bg="#f9ecff", relief=SOLID, padx=10
        )
        self.lblTitle.place(x=5, y=20, width=1350)

        # ====================== Search Section =====================
        lbl_search = Label(self.root, text="Enter Bill ID:", font=("Verdana", 10, "bold"), bg="#e1ffda")
        lbl_search.place(x=10, y=100)

        self.entry_bill_id = Entry(self.root, font=("Verdana", 10), relief=SOLID, justify=CENTER)
        self.entry_bill_id.place(x=120, y=100, width=150, height=22)

        # Fetch Button
        btn_search = Button(self.root, text="Search", command=self.fetch_bill,
                            font=("constantia", 10, "bold"), bg="#077400", fg="white",
                            relief=SOLID, bd=1, cursor="hand2")
        btn_search.place(x=300, y=98, width=110, height=25)

        # Clear Button (Newly Added)
        btn_clear = Button(self.root, text="Clear", command=self.clear_bill_check,
                        font=("constantia", 10, "bold"), bg="#bb2d2d", fg="white",
                        relief=SOLID, bd=1, cursor="hand2")
        btn_clear.place(x=300, y=130, width=110, height=25)

        # Bill Details
        lbl_billDetails = Label(self.root, text="Bill Details Section",
                                font=("constantia", 17, "bold", "underline"),
                                bg="#e1ffda", fg="#001b45")
        lbl_billDetails.place(x=80, y=130)

        # ====================== Text Area for Bill Details =====================
        self.text_area = Text(self.root, font=("Verdana", 7), wrap=WORD, relief=SOLID, state=DISABLED)
        self.text_area.place(x=10, y=170, width=400, height=460)

        # ========================== Report Section ===============================
        reportFrame = LabelFrame(self.root, text="Report Section", font=("constantia", 10, "bold", UNDERLINE), relief=SOLID, bd=1, bg="#e1ffda")
        reportFrame.place(x=420, y=100, width=920, height=200)

        # From Date and To Date for Report Generation
        lbl_from = Label(reportFrame, text="From Date:", font=("Verdana", 10, "bold"), bg="#e1ffda")
        lbl_from.place(x=10, y=20)
        
        self.from_date = DateEntry(reportFrame, width=15, background="darkblue", foreground="white", borderwidth=2, justify=CENTER, date_pattern="dd-mm-yyyy",state="readonly")
        self.from_date.place(x=100, y=20)

        lbl_to = Label(reportFrame, text="To Date:", font=("Verdana", 10, "bold"), bg="#e1ffda")
        lbl_to.place(x=230, y=20)

        self.to_date = DateEntry(reportFrame, width=15, background="darkblue", foreground="white", borderwidth=2, justify=CENTER, date_pattern="dd-mm-yyyy",state="readonly")
        self.to_date.place(x=300, y=20)

        # Generate Report Button
        btn_generate_report = Button(reportFrame, text="Generate Report", command=self.generate_report,
                                      font=("Verdana", 8, "bold"), bg="#bb5aa1", fg="white",
                                      relief=SOLID, bd=1, cursor="hand2")
        btn_generate_report.place(x=450, y=20,height=20)

    # ========================================= Functionality ============================================

    def clear_bill_check(self):
        """Clears the bill ID input field and resets the bill details text area."""
        self.entry_bill_id.delete(0, END)  # Clear the input field
        self.text_area.config(state=NORMAL)  # Enable text area for editing
        self.text_area.delete("1.0", END)  # Clear text field
        self.text_area.config(state=DISABLED)  # Make it read-only


    def fetch_bill(self):
        """Fetch the bill details from the 'bills' folder and display them."""
        bill_id = self.entry_bill_id.get().strip()  # Get user input & remove spaces

        if not bill_id:
            messagebox.showwarning("Warning", "Please enter a Bill ID!",parent=self.root)
            return

        bill_path = os.path.join(os.path.dirname(__file__), f"bills/{bill_id}.txt")

        if os.path.exists(bill_path):
            try:
                with open(bill_path, "r", encoding="utf-8") as file:
                    bill_data = file.read()

                self.text_area.config(state=NORMAL)  # Enable text area
                self.text_area.delete("1.0", END)  # Clear previous content
                self.text_area.insert(END, bill_data)  # Insert fetched data
                self.text_area.config(state=DISABLED)  # Make it read-only
            except Exception as e:
                messagebox.showerror("Error", f"Error reading bill file: {str(e)}",parent=self.root)
        else:
            messagebox.showerror("Error", f"Bill ID '{bill_id}' not found in records!",parent=self.root)
            self.text_area.config(state=NORMAL)
            self.text_area.delete("1.0", END)  # Clear text field in case of error
            self.text_area.config(state=DISABLED)

    def generate_report(self):
        """Generate a PDF report based on selected date range."""
        from_date = self.from_date.get()
        to_date = self.to_date.get()

        if not from_date or not to_date:
            messagebox.showwarning("Warning", "Please select both 'From' and 'To' dates.",parent=self.root)
            return

        try:
            conn = sqlite3.connect('inventory.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM bills WHERE Date BETWEEN ? AND ?", (from_date, to_date))
            bills = cursor.fetchall()
            conn.close()

            if not bills:
                messagebox.showwarning("No Data", "No bills found for the selected date range.",parent=self.root)
                return

            file_name = f"reports/INVOICE_REPORT_{from_date}_to_{to_date}.pdf"
            pdf = canvas.Canvas(file_name, pagesize=letter)
            width, height = letter

            margin = 50  # Proper margin for readability
            content_width = width - 2 * margin
            content_height = height - 2 * margin

            # Draw the border inside margins
            pdf.setStrokeColorRGB(0, 0, 0)
            pdf.setLineWidth(1)
            pdf.rect(margin, margin, content_width, content_height)

            # Title
            title = "INDIAN ELECTRONICS"
            pdf.setFont("Helvetica-Bold", 18)
            title_width = pdf.stringWidth(title, "Helvetica-Bold", 18)
            title_x = (width - title_width) / 2
            pdf.drawString(title_x, height - margin - 30, title)

            # Underline title
            pdf.setLineWidth(1)
            pdf.line(title_x, height - margin - 35, title_x + title_width, height - margin - 35)

            # Report Date and Time
            today_date = datetime.today().strftime("%d-%m-%Y")
            current_time = datetime.now().strftime("%I:%M:%S %p")
            pdf.setFont("Helvetica", 10)
            pdf.drawString(margin + 10, height - margin - 50, f"Report Date: {from_date} to {to_date}")
            pdf.drawString(width - margin - 170, height - margin - 50, f"Generated: {today_date} {current_time}")

            pdf.line(margin, height - margin - 55, width - margin, height - margin - 55)

            # Column headers
            column_headers = ["Bill ID", "Mobile", "Date", "Qty", "Total", "Mode"]
            column_widths = [60, 90, 90, 50, 70, 70]  # Adjusted column widths
            header_height = height - margin - 80
            pdf.setFont("Helvetica-Bold", 10)
            pdf.setFillColor(colors.black)
            x_pos = margin + 10

            for i, header in enumerate(column_headers):
                pdf.drawString(x_pos, header_height, header)
                x_pos += column_widths[i]

            pdf.line(margin, header_height - 5, width - margin, header_height - 5)

            # Bill Records (No lines between rows)
            pdf.setFont("Helvetica", 9)
            y_pos = header_height - 20

            for i, bill in enumerate(bills):
                x_pos = margin + 10

                # Alternate row color for readability (light gray background)
                if i % 2 == 0:
                    pdf.setFillColorRGB(0.9, 0.9, 0.9)
                    pdf.rect(margin, y_pos - 2, content_width, 13, fill=1)

                pdf.setFillColor(colors.black)  # Ensure text color is black

                for j, field in enumerate(bill):
                    pdf.drawString(x_pos, y_pos, str(field))
                    x_pos += column_widths[j]

                y_pos -= 15  # Move to next row

                # Page break handling
                if y_pos < margin + 50:
                    pdf.showPage()
                    y_pos = height - margin - 80

                    # Reprint headers on new page
                    pdf.setFont("Helvetica-Bold", 10)
                    x_pos = margin + 10
                    for header in column_headers:
                        pdf.drawString(x_pos, y_pos, header)
                        x_pos += column_widths[i]
                    y_pos -= 15
                    pdf.line(margin, y_pos, width - margin, y_pos)

            # Footer
            pdf.setFont("Helvetica", 8)
            pdf.setFillColor(colors.black)
            pdf.drawString(margin + 10, margin + 10, f"Report generated for: {from_date} to {to_date}")

            pdf.save()
            messagebox.showinfo("Success", f"Report generated: {file_name}",parent=self.root)

        except Exception as e:
            messagebox.showerror("Error", f"Error generating the report: {str(e)}",parent=self.root)





if __name__ == "__main__":
    root = Tk()
    app = ReportSection(root)
    root.mainloop()

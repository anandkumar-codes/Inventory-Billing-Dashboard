# Inventory-Billing-Dashboard (Python + Sqlite3)  

# Feature of the Project  
1. Login into the Application with the credentials.
2. Product management which deals with Supplier and Stock along CRUD operations.
3. Billing and generating invoices for individual bills.
4. Reports and Statistics section which deals with searching bill deatails of the past purchases and generating report for the given period of time(PDF).
5. User management which details with users assigned to access the application to certain limit(Authorization).
6. Attendance of the user which is useful for calculating the Salary.
7. Finally there will be a salary section which calculates the salary of the User(Employee) from the attendance record and a PDF report will be generated.

# Installation  
- Make sure Python is installed on your PC.
- Register the user in User Management and generate a password for login.
- run login.py to start the application.

# Dependencies  
- Import tkinter, PIL, time
- from tkinter import messagebox, ttk
- import sqlite3
- from tkcalendar import DateEntry
- import os
- import qrcode
- import reportlab
- from num2words import num2words
- from datetime import datetime

from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
import time
import sqlite3
from tkinter import messagebox


class ProductManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System | Product Management")
        self.root.geometry("1345x700+5+50")
        self.root.config(bg="#d1fff4")
        self.root.resizable(False, False)
        self.root.focus_force()
        self.root.grab_set()

        # ==================== Text Variable for Supplier====================
        self.supplierID_var = StringVar()
        self.supplier_name_var = StringVar()

        # ================ Image ======================
        # img1
        self.img1 = Image.open(r"images/logo1.png")
        self.img1 = self.img1.resize((60, 60), Image.Resampling.LANCZOS)
        self.img1 = ImageTk.PhotoImage(self.img1)

        # img2
        self.img2 = Image.open(r"images/warehouse.png")
        self.img2 = self.img2.resize((550, 450), Image.Resampling.LANCZOS)
        self.img2 = ImageTk.PhotoImage(self.img2)

        # ====================== Date and Time========================
        self.lbldateTime = Label(self.root, font=("times new roman", 15, "bold"), fg="white", bg="#e74c3c")
        self.lbldateTime.place(x=0, y=100, relwidth=1)

        # ====================== Main Title========================
        self.lblTitle = Label(self.root, text="Inventory Management System(Product & Stock)", image=self.img1, compound=LEFT,
                              font=("verdana", 30, "bold"), fg="black", bg="#7bc5b5", relief=SOLID)
        self.lblTitle.place(x=5, y=20, width=1350)

        self.dashImage = Label(self.root, image=self.img2, bg="#d1fff4")
        self.dashImage.place(x=5, y=130)

        # ======================= Labels and Entries==========================

        # Supplier Details

        # Supplier ID
        lblSupplierID = Label(self.root, text="Supplier ID", font=("Constantia", 11, "bold"), bg="#d1fff4")
        lblSupplierID.place(x=40, y=150)

        vcmd = (self.root.register(self.validate_supplierid_input), '%P')
        self.entrySupplierID = Entry(self.root, textvariable=self.supplierID_var,justify=CENTER, font=("times new roman", 10, "bold"),
                                     relief=SOLID, bd=1, width=19, fg="#10106E", validate="key",
                                     validatecommand=vcmd)
        self.entrySupplierID.place(x=160, y=150, width=250)
        self.entrySupplierID.bind("<FocusOut>", lambda event: self.validate_supplierid_on_focusout(event))

        # Supplier
        lblSupplier = Label(self.root, text="Supplier Name", font=("Constantia", 11, "bold"), bg="#d1fff4")
        lblSupplier.place(x=40, y=180)

        self.entrySupplierName = Entry(self.root, textvariable=self.supplier_name_var,justify=CENTER, font=("times new roman", 10, "bold"),
                                       relief=SOLID, bd=1, width=19, fg="#10106E")
        self.entrySupplierName.place(x=160, y=180, width=250)

        # =================================== Buttons for Suppliers =========================

        # Save
        self.btnSave = Button(self.root, text="Save Details", command=self.save_Supplier, font=("Constantia", 10, "bold"),
                              relief=RIDGE, bd=2, bg="#068206", fg="white", cursor="hand2")
        self.btnSave.place(x=430, y=180, width=100, height=20)

        # Update
        self.btnUpdate = Button(self.root, text="Update Details", command=self.update_supplier,
                                font=("Constantia", 10, "bold"), relief=RIDGE, bd=2, bg="#f7f73c", fg="black",
                                cursor="hand2", state=DISABLED)
        self.btnUpdate.place(x=40, y=210, width=150, height=20)

        # Delete
        self.btnDelete = Button(self.root, text="Delete Details", command=self.delete_supplier,
                                font=("Constantia", 10, "bold"), relief=RIDGE, bd=2, bg="#f71801", fg="white",
                                cursor="hand2", state=DISABLED)
        self.btnDelete.place(x=210, y=210, width=150, height=20)

        # Clear
        self.btnClear = Button(self.root, text="Clear Section", command=self.clear_supplier,
                               font=("Constantia", 10, "bold"), relief=RIDGE, bd=2, bg="#6c6c6c", fg="white",
                               cursor="hand2")
        self.btnClear.place(x=380, y=210, width=150, height=20)

        # ============================ Treeview for Suppliers =================================

        treeFrame = Frame(self.root, relief=RIDGE, bd=2, bg="white")
        treeFrame.place(x=10, y=510, width=530, height=120)

        lblTitle = Label(treeFrame, text="Supplier Details", font=("verdana", 10, "bold"), bg="#000000", fg="white")
        lblTitle.pack(side=TOP, fill=X)

        scrollx = ttk.Scrollbar(treeFrame, orient=HORIZONTAL)
        scrolly = ttk.Scrollbar(treeFrame, orient=VERTICAL)

        self.supplierTable = ttk.Treeview(treeFrame, columns=("sid", "Suppliername"), xscrollcommand=scrollx.set,
                                          yscrollcommand=scrolly.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)

        self.supplierTable.heading("sid", text="Supplier ID")
        self.supplierTable.heading("Suppliername", text="Supplier Name")

        self.supplierTable["show"] = "headings"

        self.supplierTable.column("sid", width=10)
        self.supplierTable.column("Suppliername", width=100)

        self.supplierTable.pack(fill=BOTH, expand=1)

        self.supplierTable.bind("<ButtonRelease-1>", self.get_cursor_supplier)

        # ================================= Stock ======================================================

        self.suppliername_inlist_var=StringVar()
        self.productid_var=StringVar()
        self.productname_var=StringVar()
        self.category_var=StringVar()
        self.costpunit_var=StringVar()
        self.totalunits_var=StringVar()

        self.supplierName_list=[]
        self.fetch_supplierName()


        stockFrame=LabelFrame(self.root,text="Stock Entry & Details",font=("times new roman",10,"bold",UNDERLINE),relief=SOLID,bd=1,bg="#ffeeed")
        stockFrame.place(x=550,y=150,width=780,height=480)

        # Stock Details

        # Supplier
        lblSupplierStock=Label(stockFrame,text="Supplier Name",font=("Constantia",11,"bold"),bg="#ffeeed")
        lblSupplierStock.place(x=10,y=10 )

        entrySupplierStock=ttk.Combobox(stockFrame,textvariable=self.suppliername_inlist_var,values=self.supplierName_list,font=("times new roman",10,"bold"),width=19,state="readonly",justify=CENTER)
        entrySupplierStock.place(x=130,y=10,width=250)
        self.suppliername_inlist_var.set("Select")

        # Product
        lblProductID=Label(stockFrame,text="Product ID",font=("Constantia",11,"bold"),bg="#ffeeed")
        lblProductID.place(x=400,y=10)

        self.entryProductID=Entry(stockFrame,textvariable=self.productid_var,font=("times new roman",10,"bold"),width=19,justify=CENTER,relief=SOLID)
        self.entryProductID.place(x=500,y=10,width=250)

        # Product Name
        lblProductName=Label(stockFrame,text="Product Name",font=("Constantia",11,"bold"),bg="#ffeeed")
        lblProductName.place(x=10,y=40)

        entryProductName=Entry(stockFrame,textvariable=self.productname_var,font=("times new roman",10,"bold"),width=19,justify=CENTER,relief=SOLID)
        entryProductName.place(x=130,y=40,width=250)

        # Category
        lblCategory=Label(stockFrame,text="Category",font=("Constantia",11,"bold"),bg="#ffeeed")
        lblCategory.place(x=400,y=40)

        entryCategory=Entry(stockFrame,textvariable=self.category_var,font=("times new roman",10,"bold"),width=19,justify=CENTER,relief=SOLID)
        entryCategory.place(x=500,y=40,width=250)


        # Cost
        lblCost=Label(stockFrame,text="Cost per Unit",font=("Constantia",11,"bold"),bg="#ffeeed")
        lblCost.place(x=10,y=70)

        entryCost=Entry(stockFrame,textvariable=self.costpunit_var,font=("times new roman",10,"bold"),width=19,justify=CENTER,relief=SOLID)
        entryCost.place(x=130,y=70,width=250)

        # Units
        lblUnits=Label(stockFrame,text="Total Units",font=("Constantia",11,"bold"),bg="#ffeeed")
        lblUnits.place(x=400,y=70)

        entryUnits=Entry(stockFrame,textvariable=self.totalunits_var,font=("times new roman",10,"bold"),width=19,justify=CENTER,relief=SOLID)
        entryUnits.place(x=500,y=70,width=250)

        # =================================== Buttons for Stock =========================

        # Save
        self.btnSaveStock = Button(stockFrame, text="Save Stock", command=self.add_stock, font=("Constantia", 10, "bold"),
                              relief=RIDGE, bd=2, bg="#068206", disabledforeground="black", cursor="hand2")
        self.btnSaveStock.place(x=10, y=100, width=160, height=30)

        # Update
        self.btnUpdateStock = Button(stockFrame, text="Update Stock", command=self.update_stock,
                                font=("Constantia", 10, "bold"), relief=RIDGE, bd=2, bg="#158069", disabledforeground="black",state=DISABLED)
        self.btnUpdateStock.place(x=200, y=100, width=160, height=30)

        # Delete
        self.btnDeleteStock = Button(stockFrame, text="Delete Details", command=self.delete_stock,
                                font=("Constantia", 10, "bold"), relief=RIDGE, bd=2, bg="#f71801", disabledforeground="black",state=DISABLED)
        self.btnDeleteStock.place(x=390, y=100, width=160, height=30)

        # Clear
        self.btnClearStock = Button(stockFrame, text="Clear Section",command=self.clear_stock_data,
                               font=("Constantia", 10, "bold"), relief=RIDGE, bd=2, bg="#89578e", fg="white",
                               cursor="hand2")
        self.btnClearStock.place(x=580, y=100, width=160, height=30)

# ============================ Treeview for Suppliers =================================

        stocktreeFrame = Frame(stockFrame, relief=RIDGE, bd=2, bg="white")
        stocktreeFrame.place(x=10, y=200, width=750, height=250)
        self.lblTitleStock = Label(stocktreeFrame, text="TOTAL STOCK DETAILS[]", font=("verdana", 10, "bold"), bg="#000000", fg="white")
        self.lblTitleStock.pack(side=TOP, fill=X)

        scrollx = ttk.Scrollbar(stocktreeFrame, orient=HORIZONTAL)
        scrolly = ttk.Scrollbar(stocktreeFrame, orient=VERTICAL)

        self.stockTable = ttk.Treeview(stocktreeFrame, columns=("pid", "sname", "pname", "category","costpunit","totalunits"), xscrollcommand=scrollx.set,
                                          yscrollcommand=scrolly.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        scrollx.config(command=self.stockTable.xview)
        scrolly.config(command=self.stockTable.yview)

        self.stockTable.heading("pid", text="Product ID")
        self.stockTable.heading("sname", text="Supplier Name")
        self.stockTable.heading("pname", text="Product Name")
        self.stockTable.heading("category", text="Categoty")
        self.stockTable.heading("costpunit", text="Cost Per Unit")
        self.stockTable.heading("totalunits", text="Total Units")

        self.stockTable["show"] = "headings"
        
        self.stockTable.column("pid", width=40)
        self.stockTable.column("sname", width=200)
        self.stockTable.column("pname", width=100)
        self.stockTable.column("category", width=100)
        self.stockTable.column("costpunit", width=50)
        self.stockTable.column("totalunits", width=40)


        self.stockTable.pack(fill=BOTH, expand=1)
        self.stockTable.bind("<ButtonRelease-1>", self.get_cursor_stock)

        # Search Frame
        # ====================== Search Frame =====================
        search_frame=Frame(stockFrame,relief=SOLID,bd=1,bg="white")
        search_frame.place(x=10,y=150,width=750,height=40)

        # Search By Product ID
        searchLabelProductID=Label(search_frame,text="Product ID",font=("verdana",10,"bold"),bg="white")
        searchLabelProductID.place(x=5,y=8)

        self.var_search_productid=StringVar()
        entrySearchByLicense=Entry(search_frame,textvariable=self.var_search_productid,font=("verdana",10),bd=1,relief=SOLID,width=10)
        entrySearchByLicense.place(x=100,y=9)
        entrySearchByLicense.bind("<Key>",self.search_ProductID)

        # Search By Name
        searchLabelName=Label(search_frame,text="Name",font=("verdana",10,"bold"),bg="white")
        searchLabelName.place(x=190,y=8)

        self.var_search_Name=StringVar()
        entrySearchByName=Entry(search_frame,textvariable=self.var_search_Name,font=("verdana",10),bd=1,relief=SOLID,width=10)
        entrySearchByName.place(x=250,y=9)
        entrySearchByName.bind("<Key>",self.search_ProductName)

        # Search By Supplier
        searchLabelSupplier=Label(search_frame,text="Supplier",font=("verdana",10,"bold"),bg="white")
        searchLabelSupplier.place(x=350,y=8)

        self.var_search_Supplier=StringVar()
        entrySearchBySupplier=Entry(search_frame,textvariable=self.var_search_Supplier,font=("verdana",10),bd=1,relief=SOLID,width=10)
        entrySearchBySupplier.place(x=420,y=9)
        entrySearchBySupplier.bind("<Key>",self.search_Supplier)

        # Search By Category
        searchLabelCategory=Label(search_frame,text="Category",font=("verdana",10,"bold"),bg="white")
        searchLabelCategory.place(x=520,y=8)

        self.var_search_Category=StringVar()
        entrySearchByCategory=Entry(search_frame,textvariable=self.var_search_Category,font=("verdana",10),bd=1,relief=SOLID,width=10)
        entrySearchByCategory.place(x=600,y=9)
        entrySearchByCategory.bind("<Key>",self.search_Category)

        # Show All
        btnClear=Button(search_frame,text="Show\nAll",command=self.clear_search,font=("verdana",7,"bold"),border=0,relief=RIDGE,bd=0,activebackground="#34495E",bg="#34495E",fg="white",cursor="hand2")
        btnClear.place(x=690,y=4,width=50,height=30)

        self.datetime_update()
        self.show_data_supplier()
        self.show_data_stock()

# ===================================== Functionality SUpplier==================================

    def validate_supplierid_input(self, P):
        # Ensure only digits are entered and limit to 6 characters
        if P == "":
            return True  # Allow clearing the field
        if P.isdigit() and len(P) <= 6:
            return True
        return False

    def validate_supplierid_on_focusout(self, event):
        supplier_ID = self.supplierID_var.get()
        if len(supplier_ID) != 6 or not supplier_ID.isdigit():
            messagebox.showerror("Invalid Supplier ID", "Supplier ID should be exactly 6 digits.", parent=self.root)
            self.entrySupplierID.focus()  # Keep focus on the Supplier field
            return "break"  # Prevent moving out of the field
        return True

    def datetime_update(self):
        date_ = time.strftime("%d-%m-%Y (%A)")
        time_ = time.strftime("%r")
        self.lbldateTime.config(text=f"Date: {str(date_)}\t\t\t\tTime: {str(time_)}")
        self.lbldateTime.after(200, self.datetime_update)

    def fetch_supplierName(self):
        con = sqlite3.connect(database=r'inventory.db')
        cur = con.cursor()
        try:
            cur.execute("select Supplier_Name from supplier")
            rows = cur.fetchall()
            if len(rows) > 0:
                for i in rows:
                    self.supplierName_list.append(i[0])
        except Exception as es:
            messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    def show_data_supplier(self):
        con = sqlite3.connect(database=r'inventory.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM supplier")
            data = cur.fetchall()
            if len(data) != 0:
                self.supplierTable.delete(*self.supplierTable.get_children())
                for record in data:
                    s_id = record[0]
                    supplier_name = record[1]
                    self.supplierTable.insert("", END, values=(s_id, supplier_name))
                con.commit()
            con.close()
        except Exception as es:
            messagebox.showerror("Error", f"Error Due To: {str(es)}", parent=self.root)

    def get_cursor_supplier(self, event=""):
        row = self.supplierTable.focus()
        content = self.supplierTable.item(row)
        data = content.get("values")

        if data:  # Ensure a valid row is selected
            self.supplierID_var.set(data[0])
            self.supplier_name_var.set(data[1])  # Set selected Supplier Name in Entry

            # Disable "Save" and Enable "Update" & "Delete"
            self.btnSave.config(state=DISABLED)
            self.btnUpdate.config(state=NORMAL)
            self.btnDelete.config(state=NORMAL)
            self.entrySupplierID.config(state="readonly")

    # Save Supplier
    def save_Supplier(self):
        if self.supplierID_var.get() == "":
            messagebox.showerror("Error", "Please Enter the Supplier ID", parent=self.root)
        elif self.supplier_name_var.get() == "":
            messagebox.showerror("Error", "Please Enter the Supplier Name", parent=self.root)
        else:
            try:
                con = sqlite3.connect(database=r'inventory.db')
                cur = con.cursor()
                # Check if supplier already exists
                cur.execute("SELECT * FROM supplier WHERE Supplier_ID=?", (self.supplierID_var.get(),))
                row = cur.fetchone()
                if row:
                    messagebox.showerror("Error", f"Supplier '{self.supplierID_var.get()}' already exists with the Name '{self.supplier_name_var.get()}'", parent=self.root)
                    con.close()
                    return

                # If not exists, insert new supplier
                add = messagebox.askyesno("Add Supplier", f"Are you sure to add '{self.supplier_name_var.get()}'?", parent=self.root)
                if add:
                    cur.execute("INSERT INTO supplier (Supplier_ID,Supplier_Name) VALUES (?,?)", (self.supplierID_var.get(), self.supplier_name_var.get()))
                    con.commit()
                    messagebox.showinfo("Success", f"Supplier '{self.supplier_name_var.get()}' Added successfully!", parent=self.root)
                    self.show_data_supplier()
                    self.clear_supplier()
                con.close()
            except Exception as es:
                messagebox.showerror("Error", f"Error Due To: {str(es)}", parent=self.root)

    def update_supplier(self):
        if self.supplier_name_var.get() == "":
            messagebox.showerror("Error", "Please Enter the Supplier Name", parent=self.root)
        else:
            try:
                con = sqlite3.connect(database=r'inventory.db')
                cur = con.cursor()

                # Check if the supplier exists
                cur.execute("SELECT * FROM supplier WHERE Supplier_ID=?", (self.supplierID_var.get(),))
                row = cur.fetchone()

                if row is None:
                    messagebox.showerror("Error", "Supplier ID does not exist!", parent=self.root)
                    con.close()
                    return

                # Confirm update action
                update = messagebox.askyesno("Update", f"Are you sure you want to update supplier '{self.supplierID_var.get()}'?", parent=self.root)
                if update:
                    cur.execute("UPDATE supplier SET Supplier_Name=? WHERE Supplier_ID=?", 
                                (self.supplier_name_var.get(), self.supplierID_var.get()))
                    con.commit()
                    messagebox.showinfo("Success", "Supplier Updated Successfully", parent=self.root)
                    self.show_data_supplier()
                    self.clear_supplier()

                con.close()
            except Exception as es:
                messagebox.showerror("Error", f"Error Due To: {str(es)}", parent=self.root)


    def delete_supplier(self):
        if self.supplierID_var.get() == "" or self.supplier_name_var.get() == "":
            messagebox.showerror("Error", "Missing Supplier Information", parent=self.root)
        else:
            try:
                delete = messagebox.askyesno("Delete", f"Are you sure to Delete the Information of {self.supplierID_var.get()}", parent=self.root)
                if delete > 0:
                    con = sqlite3.connect(database=r'inventory.db')
                    cur = con.cursor()
                    sql = ("delete from supplier where Supplier_ID=?")
                    val = (self.supplierID_var.get(),)
                    cur.execute(sql, val)
                    messagebox.showinfo("Success", f"Supplier ID {self.supplierID_var.get()} Deleted Successfully", parent=self.root)
                else:
                    if not delete:
                        return
                con.commit()
                self.clear_supplier()
                self.show_data_supplier()
                con.close()
            except Exception as es:
                messagebox.showerror("Error", f"Due To:{str(es)}", parent=self.root)

    def clear_supplier(self):
        self.supplierID_var.set("")
        self.supplier_name_var.set("")  # Clear entry field

        # Enable "Save" and Disable "Update" & "Delete"
        self.btnSave.config(state=NORMAL)
        self.btnUpdate.config(state=DISABLED)
        self.btnDelete.config(state=DISABLED)
        self.entrySupplierID.config(state=NORMAL)
        self.show_data_supplier()

# ======================================= Functionality Stock ========================================


    # Add
    def add_stock(self):
        if self.suppliername_inlist_var.get()=="Select":
            messagebox.showerror("Error","Please Select the Supplier",parent=self.root)
        elif self.productid_var.get()=="":
            messagebox.showerror("Error","Product ID is Required",parent=self.root)
        elif self.productname_var.get()=="":
            messagebox.showerror("Error","Please Enter the Product Name",parent=self.root)
        elif self.category_var.get()=="":
            messagebox.showerror("Error","Please Enter the Category of the Product",parent=self.root)
        elif self.costpunit_var.get()=="":
            messagebox.showerror("Error","Please Enter the Cost Per Unit of the Product",parent=self.root)
        elif self.totalunits_var.get()=="":
            messagebox.showerror("Error","Please Enter Number of Units",parent=self.root)
        else:
            try:
                add=messagebox.askyesno("Add Stock",f"Are you sure to Add {self.productname_var.get()} with Product ID {self.productid_var.get()} to the Stock list?",parent=self.root)
                if add>0:
                    con=sqlite3.connect(database=r'inventory.db')
                    cur=con.cursor()
                    cur.execute("insert into stock(Product_ID,Supplier_Name,Product_Name,Category,Cost,Total_Units) values(?,?,?,?,?,?)",(

                                                        self.productid_var.get(),
                                                        self.suppliername_inlist_var.get(),
                                                        self.productname_var.get(),
                                                        self.category_var.get(),
                                                        self.costpunit_var.get(),
                                                        self.totalunits_var.get()

                                                                            ))
                else:
                    if not add:
                        return
                con.commit()
                con.close()
                messagebox.showinfo("Success",f"Product ID {self.productid_var.get()} with the Name {self.productname_var.get()} Added Successfully",parent=self.root)
                self.show_data_stock()
                self.clear_stock_data()
            except Exception as es:
                messagebox.showerror("Error",f"Error Due To:{str(es)}",parent=self.root)

    # Update Data
    def update_stock(self):
        if self.productid_var.get()=="":
            messagebox.showerror("Error","Please Enter Product ID",parent=self.root)
        elif self.productname_var.get()=="":
            messagebox.showerror("Error","Please Enter the Product Name",parent=self.root)
        elif self.category_var.get()=="":
            messagebox.showerror("Error","Please Enter the Category",parent=self.root)
        elif self.costpunit_var.get()=="":
            messagebox.showerror("Error","Please Enter the Cost per Unit of the Product",parent=self.root)
        elif self.totalunits_var.get()=="":
            messagebox.showerror("Error","Please Enter the Total Units",parent=self.root)
        else:
            try:
                con=sqlite3.connect(database=r'inventory.db')
                cur=con.cursor()
                update=messagebox.askyesno("Update",f"Are you sure to Update Information of '{self.productid_var.get()}' ?",parent=self.root)
                if update>0:
                    cur.execute("update stock set Supplier_Name=?,Product_Name=?,Category=?,Cost=?,Total_Units=? where Product_ID=?",(


                                                    self.suppliername_inlist_var.get(),
                                                    self.productname_var.get(),
                                                    self.category_var.get(),
                                                    self.costpunit_var.get(),
                                                    self.totalunits_var.get(),
                                                    self.productid_var.get()


                                                                ))
                else:
                    if not update:
                        return
                con.commit()
                con.close()
                messagebox.showinfo("Updated","Information Updated Successfully",parent=self.root)
                self.show_data_stock()
                self.clear_stock_data()
            except Exception as es:
                    messagebox.showerror("Error",f"Error Due To:{str(es)}",parent=self.root)

    # Delete Data
    def delete_stock(self):
        if self.productid_var.get()=="":
            messagebox.showerror("Error","Please Enter Product ID",parent=self.root)
        elif self.productname_var.get()=="":
            messagebox.showerror("Error","Please Enter the Product Name",parent=self.root)
        elif self.category_var.get()=="":
            messagebox.showerror("Error","Please Enter the Category",parent=self.root)
        elif self.costpunit_var.get()=="":
            messagebox.showerror("Error","Please Enter the Cost per Unit of the Product",parent=self.root)
        elif self.totalunits_var.get()=="":
            messagebox.showerror("Error","Please Enter the Total Units",parent=self.root)
        else:
            try:
                con=sqlite3.connect(database=r'inventory.db')
                cur=con.cursor()
                cur.execute("select * from stock where Product_ID=?",(self.productid_var.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showwarning("Error","No Product ID Present with the provided Number",parent=self.root)
                else:
                    delete=messagebox.askyesno("Delete",f"Are you sure to Delete the Information of '{self.productid_var.get()}'",parent=self.root)
                    if delete>0:
                        sql=("delete from stock where Product_ID=?")
                        val=(self.productid_var.get(),)
                        cur.execute(sql,val)
                        messagebox.showinfo("Success",f"Product ID '{self.productid_var.get()}' with Name '{self.productname_var.get()}' Deleted Successfully",parent=self.root)
                    else:
                        if not delete:
                            return
                    con.commit()
                    self.show_data_stock()
                    self.clear_stock_data()
                    con.close()
            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)


    # Show Data
    def show_data_stock(self):
        con=sqlite3.connect(database=r'inventory.db')
        cur=con.cursor()
        try:
            cur.execute("select * from stock")
            data=cur.fetchall()
            if len(data)!=0:
                self.stockTable.delete(*self.stockTable.get_children())
                for i in data:
                    self.stockTable.insert("",END,values=i)
                    con.commit()
                con.close()
                self.lblTitleStock.config(text=f"TOTAL STOCK DETAILS[{str(len(self.stockTable.get_children()))}]")
        except Exception as es:
                messagebox.showerror("Error",f"Error Due To:{str(es)}",parent=self.root)
        

    # Get Cursor
    def get_cursor_stock(self,event=""):
        row=self.stockTable.focus()
        content=self.stockTable.item(row)
        data=content["values"]

        self.productid_var.set(data[0])
        self.suppliername_inlist_var.set(data[1])
        self.productname_var.set(data[2])
        self.category_var.set(data[3])
        self.costpunit_var.set(data[4])
        self.totalunits_var.set(data[5])

        self.btnSaveStock.config(state=DISABLED,cursor="arrow")
        self.btnUpdateStock.config(state=NORMAL,cursor="hand2")
        self.btnDeleteStock.config(state=NORMAL,cursor="hand2")
        self.entryProductID.config(state="readonly")

    # Clear Stock Data
    def clear_stock_data(self):
        self.suppliername_inlist_var.set("Select")
        self.productid_var.set("")
        self.productname_var.set("")
        self.category_var.set("")
        self.costpunit_var.set("")
        self.totalunits_var.set("")
        self.show_data_stock()
        self.btnSaveStock.config(state=NORMAL,cursor="hand2")
        self.btnUpdateStock.config(state=DISABLED,cursor="arrow")
        self.btnDeleteStock.config(state=DISABLED,cursor="arrow")
        self.entryProductID.config(state=NORMAL)

# ================================== Search in Stock Treeview =============================

# ====================== Search ========================
    # Search ProductID
    def search_ProductID(self,ev):
        con=sqlite3.connect(database=r'inventory.db')
        cur=con.cursor()
        try:
            cur.execute("select * from stock where Product_ID LIKE '%"+self.var_search_productid.get()+"%'")
            row=cur.fetchall()
            if len(row)>0:
                self.stockTable.delete(*self.stockTable.get_children())
                for i in row:
                    self.stockTable.insert("",END,values=i)
            else:
                self.stockTable.delete(*self.stockTable.get_children())
        except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)
                

    # Search ProductName
    def search_ProductName(self,ev):
        con=sqlite3.connect(database=r'inventory.db')
        cur=con.cursor()
        try:
            cur.execute("select * from stock where Product_Name LIKE '%"+self.var_search_Name.get()+"%'")
            row=cur.fetchall()
            if len(row)>0:
                self.stockTable.delete(*self.stockTable.get_children())
                for i in row:
                    self.stockTable.insert("",END,values=i)
            else:
                self.stockTable.delete(*self.stockTable.get_children())
        except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)
    
    # Search Supplier
    def search_Supplier(self,ev):
        con=sqlite3.connect(database=r'inventory.db')
        cur=con.cursor()
        try:
            cur.execute("select * from stock where Supplier_Name LIKE '%"+self.var_search_Supplier.get()+"%'")
            row=cur.fetchall()
            if len(row)>0:
                self.stockTable.delete(*self.stockTable.get_children())
                for i in row:
                    self.stockTable.insert("",END,values=i)
            else:
                self.stockTable.delete(*self.stockTable.get_children())
        except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)


    # Search Category
    def search_Category(self,ev):
        con=sqlite3.connect(database=r'inventory.db')
        cur=con.cursor()
        try:
            cur.execute("select * from stock where Category LIKE '%"+self.var_search_Category.get()+"%'")
            row=cur.fetchall()
            if len(row)>0:
                self.stockTable.delete(*self.stockTable.get_children())
                for i in row:
                    self.stockTable.insert("",END,values=i)
            else:
                self.stockTable.delete(*self.stockTable.get_children())
        except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)


    def clear_search(self):
        self.var_search_productid.set("")
        self.var_search_Name.set("")
        self.var_search_Supplier.set("")
        self.var_search_Category.set("")
        self.show_data_stock()



if __name__=="__main__":
    root=Tk()
    object=ProductManagement(root)
    root.mainloop()
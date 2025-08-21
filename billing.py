from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
import time
import sqlite3
from tkinter import messagebox
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,Image
from reportlab.lib.styles import getSampleStyleSheet
from num2words import num2words
from datetime import datetime



class BillingSection:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System | Billing Section")
        self.root.geometry("1345x700+5+50")
        self.root.config(bg="#fef9e7")
        self.root.resizable(False, False)
        self.root.focus_force()
        self.root.grab_set()

        self.cart_items_spinbox = {}  # Dictionary to store Spinboxes by cart item
        self.spinbox_dict = {}  # Dictionary to store Spinbox references for each cart item
        
        # Calling database connection
        self.creat_db()

        # ================ Image ======================
        # img1
        image_path = os.path.join(os.path.dirname(__file__), "images/logo1.png")
        try:
            self.img1 = Image.open(r"images/logo1.png").resize((60, 60), Image.Resampling.LANCZOS)
            self.img1 = ImageTk.PhotoImage(self.img1)
        except Exception as e:
            self.img1 = None  # Assign a default image or handle the error
            print(f"Error loading image: {e}")


        # ====================== Date and Time========================
        self.lbldateTime = Label(self.root, font=("times new roman", 15, "bold"), fg="black", bg="#f39c12")
        self.lbldateTime.place(x=0, y=100, relwidth=1)

        # ====================== Main Title========================
        self.lblTitle = Label(self.root, text="Inventory Management System(Billing Section)", image=self.img1, compound=LEFT,
                              font=("verdana", 30, "bold"), fg="white", bg="#239b56", relief=SOLID)
        self.lblTitle.place(x=5, y=20, width=1350)

        # ===================== Customer Details Frame =======================================
        customerFrame=LabelFrame(self.root,text="Customer Details",font=("constantia", 8, "bold",UNDERLINE),bg="white",relief=SOLID,bd=1)
        customerFrame.place(x=550,y=140,width=780,height=60)

        # Bill ID
        self.billID_var=StringVar()
        lblBillID=Label(customerFrame,text="*Bill ID",font=("constantia", 11, "bold"), fg="red",bg="white")
        lblBillID.place(x=10,y=10)

        entryBillID=Entry(customerFrame,textvariable=self.billID_var,font=("verdana", 9, "bold"), fg="black",bg="white",relief=SOLID,state="readonly",justify=CENTER)
        entryBillID.place(x=80,y=10,width=120)

        # Mobile
        self.mobile_var=StringVar()
        lblMobile=Label(customerFrame,text="Mobile",font=("constantia", 11, "bold"), fg="black",bg="white")
        lblMobile.place(x=210,y=10)

        entryMobile=Entry(customerFrame,textvariable=self.mobile_var,font=("verdana", 10, "bold"), fg="black",bg="white",relief=SOLID,justify=CENTER)
        entryMobile.place(x=280,y=10,width=120)

        # Name
        self.cname_var=StringVar()
        lblName=Label(customerFrame,text="Name/Email",font=("constantia", 11, "bold"), fg="black",bg="white")
        lblName.place(x=410,y=10)

        entryName=Entry(customerFrame,textvariable=self.cname_var,font=("constantia", 10, "bold"), fg="black",bg="white",relief=SOLID,justify=CENTER)
        entryName.place(x=520,y=10,width=120)

        # Date
        self.date_var=StringVar()
        lblDate=Label(self.root,text="Date",font=("constantia", 11, "bold"), fg="black",bg="white")
        lblDate.place(x=550,y=520)

        entryDate=Entry(self.root,textvariable=self.date_var,font=("verdana",8, "bold"), fg="black",bg="white",relief=SOLID,state="readonly",justify=CENTER)
        entryDate.place(x=600,y=525,width=80)

        # Qty
        self.qty_var=StringVar()
        lblQty=Label(self.root,text="Quantity",font=("constantia", 11, "bold"), fg="black",bg="white")
        lblQty.place(x=690,y=520)

        entryQty=Entry(self.root,textvariable=self.qty_var,font=("verdana",8, "bold"), fg="black",bg="white",relief=SOLID,state="readonly",justify=CENTER)
        entryQty.place(x=770,y=525,width=80)

        # Total
        self.total_var=StringVar()
        lblTotal=Label(self.root,text="Total",font=("constantia", 11, "bold"), fg="black",bg="white")
        lblTotal.place(x=870,y=520)

        entryTotal=Entry(self.root,textvariable=self.total_var,font=("verdana",8, "bold"), fg="black",bg="white",relief=SOLID,state="readonly",justify=CENTER)
        entryTotal.place(x=920,y=525,width=80)

        # Mode
        self.mode_var=StringVar()
        lblMode=Label(self.root,text="Mode of Payment",font=("constantia", 10, "bold"), fg="black",bg="white")
        lblMode.place(x=1010,y=515)

        self.entryMode=ttk.Combobox(self.root,textvariable=self.mode_var,font=("constantia", 10, "bold"),state="readonly",justify=CENTER)
        self.entryMode['values']=("Select","Cash","Online")
        self.entryMode.current(0)
        self.entryMode.config(state=DISABLED)
        self.entryMode.place(x=1140,y=515,width=150,height=20)



        # ================ Treeview for the Products and Stock Avaliability ================

        self.treeviewTitle = Label(self.root, text="Products and Stock Avaliability",
                              font=("constantia", 15, "bold"), fg="black",bg="#fef9e7")
        self.treeviewTitle.place(x=130,y=130)


        stocktreeFrame = Frame(self.root, relief=RIDGE, bd=2, bg="white")
        stocktreeFrame.place(x=10, y=210, width=525, height=300)
        self.lblTitleStock = Label(stocktreeFrame, text="TOTAL STOCK DETAILS[]", font=("verdana", 10, "bold"), bg="#000000", fg="white")
        self.lblTitleStock.pack(side=TOP, fill=X)

        scrollx = ttk.Scrollbar(stocktreeFrame, orient=HORIZONTAL)
        scrolly = ttk.Scrollbar(stocktreeFrame, orient=VERTICAL)

        self.stockTableBill = ttk.Treeview(stocktreeFrame, columns=("pid", "pname", "category","costpunit","totalunits"), xscrollcommand=scrollx.set,
                                          yscrollcommand=scrolly.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        scrollx.config(command=self.stockTableBill.xview)
        scrolly.config(command=self.stockTableBill.yview)

        self.stockTableBill.heading("pid", text="Product ID")
        self.stockTableBill.heading("pname", text="Product Name")
        self.stockTableBill.heading("category", text="Categoty")
        self.stockTableBill.heading("costpunit", text="Cost/Unit")
        self.stockTableBill.heading("totalunits", text="Total Units")

        self.stockTableBill["show"] = "headings"
        
        self.stockTableBill.column("pid", width=50)
        self.stockTableBill.column("pname", width=200)
        self.stockTableBill.column("category", width=50)
        self.stockTableBill.column("costpunit", width=50)
        self.stockTableBill.column("totalunits", width=40)


        self.stockTableBill.pack(fill=BOTH, expand=1)

        # Add a Text widget to display the bill beside the cart
        self.bill_display = Text(self.root, font=("verdana", 6), bg="#f1f1f1", wrap=WORD,relief=SOLID)
        self.bill_display.place(x=1010, y=210, width=320, height=300)


        # Search Frame
        # ====================== Search Frame =====================
        search_frame=Frame(self.root,relief=SOLID,bd=1,bg="white")
        search_frame.place(x=10,y=160,width=525,height=40)

        # Search By Product ID
        searchLabelProductID=Label(search_frame,text="Product ID",font=("verdana",10,"bold"),bg="white")
        searchLabelProductID.place(x=5,y=8)

        self.var_search_productid=StringVar()
        entrySearchByProductID=Entry(search_frame,textvariable=self.var_search_productid,font=("verdana",10),bd=1,relief=SOLID,width=10)
        entrySearchByProductID.place(x=100,y=9)
        entrySearchByProductID.bind("<Key>",self.search_stock)


        # Search By Name
        searchLabelName=Label(search_frame,text="Name",font=("verdana",10,"bold"),bg="white")
        searchLabelName.place(x=190,y=8)

        self.var_search_Name=StringVar()
        entrySearchByName=Entry(search_frame,textvariable=self.var_search_Name,font=("verdana",10),bd=1,relief=SOLID,width=10)
        entrySearchByName.place(x=250,y=9)
        entrySearchByName.bind("<Key>",self.search_stock)

        # Search By Category
        searchLabelCategory=Label(search_frame,text="Category",font=("verdana",10,"bold"),bg="white")
        searchLabelCategory.place(x=350,y=8)

        self.var_search_Category=StringVar()
        entrySearchByCategory=Entry(search_frame,textvariable=self.var_search_Category,font=("verdana",10),bd=1,relief=SOLID,width=10)
        entrySearchByCategory.place(x=430,y=9)
        entrySearchByCategory.bind("<Key>",self.search_stock)

        # Add to Cart
        addToCartButton=Button(self.root,text="Add To Cart",command=self.add_to_cart,font=("constantia",10,"bold"),bg="#17a589",relief=SOLID,bd=1,cursor="hand2")
        addToCartButton.place(x=190,y=520,width=150,height=25)

        # Delete
        deleteButton=Button(self.root,text="Delete",command=self.delete_from_cart,font=("constantia",10,"bold"),fg="white",bg="red",relief=SOLID,bd=1,cursor="hand2")
        deleteButton.place(x=550,y=550,width=140,height=25)

        # Generate
        self.billGenerateButton=Button(self.root,text="Generate Bill",command=self.generate_bill,font=("constantia",10,"bold"),fg="white",bg="#1a5276",relief=SOLID,bd=1,cursor="hand2")
        self.billGenerateButton.place(x=705,y=550,width=140,height=25)

        # Save
        self.billSaveButton=Button(self.root,text="Save Bill",command=self.save_bill,font=("constantia",10,"bold"),fg="white",bg="#1f8011",relief=SOLID,bd=1,cursor="hand2",state=DISABLED)
        self.billSaveButton.place(x=860,y=550,width=140,height=25)

        # Clear
        billClearButton=Button(customerFrame,text="Clear",command=self.clear_customer,font=("constantia",10,"bold"),fg="white",bg="#1a5276",relief=SOLID,bd=1,cursor="hand2")
        billClearButton.place(x=650,y=9,width=120,height=25)

# ===================================== Cart Section ======================================

        # ================ Treeview for the Products and Stock Avaliability ===============

        cartFrame = Frame(self.root, relief=RIDGE, bd=2, bg="white")
        cartFrame.place(x=550, y=210, width=450, height=300)

        scrollx = ttk.Scrollbar(cartFrame, orient=HORIZONTAL)
        scrolly = ttk.Scrollbar(cartFrame, orient=VERTICAL)

        self.cartBill = ttk.Treeview(cartFrame, columns=("pid", "name", "cost","quantity","total"), xscrollcommand=scrollx.set,
                                          yscrollcommand=scrolly.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        scrollx.config(command=self.cartBill.xview)
        scrolly.config(command=self.cartBill.yview)

        self.cartBill.heading("pid", text="Product ID")
        self.cartBill.heading("name", text="Name")
        self.cartBill.heading("cost", text="Cost")
        self.cartBill.heading("quantity", text="Quantity")
        self.cartBill.heading("total", text="Total")

        self.cartBill["show"] = "headings"
        
        self.cartBill.column("pid", width=50)
        self.cartBill.column("name", width=100)
        self.cartBill.column("cost", width=50)
        self.cartBill.column("quantity", width=50)
        self.cartBill.column("total", width=40)


        self.cartBill.pack(fill=BOTH, expand=1)

        self.datetime_update()
        self.show_stock()
        self.bill_ID()
# ======================================== Functionality ===========================================
    def bill_ID(self):
        a=str("BID")
        b=int(time.strftime("%I%M%S"))
        c=int(time.strftime("%d%m%Y"))
        self.d=str(a+str(b+c))
        self.billID_var.set(self.d)
        
    
    def clear_customer(self):
        self.mobile_var.set("")
        self.cname_var.set("")
        self.bill_ID()
        self.bill_display.config(state="normal")
        self.bill_display.delete(1.0, END)
        self.cartBill.delete(*self.cartBill.get_children())
        self.date_var.set("")
        self.qty_var.set("")
        self.total_var.set("")
        self.mode_var.set("Select")
        self.entryMode.config(state=DISABLED)
        self.billGenerateButton.config(state="normal")
        self.show_stock()


    def creat_db(self):
        con=sqlite3.connect(database="inventory.db")
        cur=con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS supplier(Supplier_ID text PRIMARY KEY,Supplier_Name text)")
        con.commit()

        cur.execute("CREATE TABLE IF NOT EXISTS stock(Product_ID text PRIMARY KEY,Supplier_Name text,Product_Name text,Category text,Cost integer, Total_Units integer)")
        con.commit()

    def datetime_update(self):
        date_ = time.strftime("%d-%m-%Y (%A)")
        time_ = time.strftime("%r")
        self.lbldateTime.config(text=f"Date: {str(date_)}\t\t\t\tTime: {str(time_)}")
        self.lbldateTime.after(200, self.datetime_update)

    def show_stock(self):
        con = sqlite3.connect(database=r'inventory.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM stock")
            count = cur.fetchone()[0]
            if count > 0:
                cur.execute("SELECT Product_ID, Product_Name, Category, Cost, Total_Units FROM stock")
                data = cur.fetchall()
                self.stockTableBill.delete(*self.stockTableBill.get_children())  # Clear table
                for record in data:
                    self.stockTableBill.insert("", END, values=record)
                self.lblTitleStock.config(text=f"TOTAL STOCK DETAILS[{count}]")
                con.commit()
            con.close()
        except Exception as es:
            messagebox.showerror("Error", f"Error Due To: {str(es)}", parent=self.root)

    def search_stock(self, *args):
        search_pid = self.var_search_productid.get()
        search_name = self.var_search_Name.get().lower()
        search_cat = self.var_search_Category.get().lower()

        con = sqlite3.connect(database='inventory.db')
        cur = con.cursor()
        query = "SELECT Product_ID, Product_Name, Category, Cost, Total_Units FROM stock WHERE 1=1"
        params = []

        if search_pid:
            query += " AND Product_ID LIKE ?"
            params.append(f"%{search_pid}%")
        if search_name:
            query += " AND LOWER(Product_Name) LIKE ?"
            params.append(f"%{search_name}%")
        if search_cat:
            query += " AND LOWER(Category) LIKE ?"
            params.append(f"%{search_cat}%")

        cur.execute(query, params)
        data = cur.fetchall()
        self.stockTableBill.delete(*self.stockTableBill.get_children())  # Clear table

        for record in data:
            self.stockTableBill.insert("", END, values=record)
        con.close()
        

    def add_to_cart(self):
        selected_item = self.stockTableBill.focus()  # Get selected row
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a product!", parent=self.root)
            return
        if self.mobile_var.get()=="":
            messagebox.showwarning("Warning", "Please Enter Customer Mobile Number", parent=self.root)
            return

        item_data = self.stockTableBill.item(selected_item)['values']
        if not item_data:
            return

        product_id, product_name, category, cost, total_units = item_data

        if total_units <= 0:
            messagebox.showerror("Error", "Stock is empty!", parent=self.root)
            return

        # Check if product already exists in cart
        cart_items = self.cartBill.get_children()
        for item in cart_items:
            cart_values = self.cartBill.item(item)['values']
            if cart_values and cart_values[0] == product_id:  # Product already exists
                messagebox.showwarning("Already in Cart", f"'{product_name}' is already in the cart!", parent=self.root)
                return  # Stop execution

        # If product is not in cart, add it
        quantity = 1
        total_price = cost * quantity
        cart_item = self.cartBill.insert("", END, values=(product_id, product_name, cost, quantity, total_price))

        # Reduce stock and update UI
        self.update_stock_quantity(product_id, -quantity)

        # Add quantity Spinbox
        self.add_quantity_spinbox(cart_item, cost, total_units)

    def update_stock_quantity(self, product_id, quantity_change):
        """ Updates stockTableBill when product quantity changes in cart """
        for item in self.stockTableBill.get_children():
            values = self.stockTableBill.item(item)['values']
            if values[0] == product_id:  # Find the matching product ID
                new_stock = values[4] + quantity_change  # Increase stock if item is removed
                if new_stock < 0:  # Prevent negative stock
                    new_stock = 0

                # Update the Treeview UI (stock table)
                self.stockTableBill.item(item, values=(values[0], values[1], values[2], values[3], new_stock))
                break

    def add_quantity_spinbox(self, cart_item, cost, max_units):
        """ Add a Spinbox to modify quantity dynamically and update stock """
        x, y, width, height = self.cartBill.bbox(cart_item, column=3)  # Quantity column

        spinbox = Spinbox(self.cartBill, from_=1, to=min(10, max_units), width=5,
                        font=("Arial", 10), justify=CENTER,
                        command=lambda: self.update_cart_quantity(cart_item, cost, spinbox))

        # Place the Spinbox over the Quantity cell
        spinbox.place(x=x + 5, y=y + 2, width=width - 10, height=height - 2)

        # Store reference of Spinbox in the dictionary
        self.spinbox_dict[cart_item] = spinbox

        # Store reference to cart item with the Spinbox
        self.cartBill.item(cart_item, values=(self.cartBill.item(cart_item)["values"][:3] + (spinbox, cost)))

    def update_cart_total(self, cart_item, cost, spinbox):
        try:
            quantity = int(spinbox.get())
            total_price = cost * quantity
            values = self.cartBill.item(cart_item)["values"]
            self.cartBill.item(cart_item, values=(values[0], values[1], values[2], quantity, total_price))
        except Exception as e:
            print(f"Error updating quantity: {e}")

    def update_cart_quantity(self, cart_item, cost, spinbox):
        """ Updates total price and stock when quantity changes in cart """
        try:
            new_quantity = int(spinbox.get())  # Get updated quantity from Spinbox
            values = self.cartBill.item(cart_item)["values"]
            product_id = values[0]
            old_quantity = values[3]

            # Calculate quantity difference
            quantity_difference = new_quantity - old_quantity

            # Ensure stock is available before updating
            for item in self.stockTableBill.get_children():
                stock_values = self.stockTableBill.item(item)['values']
                if stock_values[0] == product_id:
                    available_stock = stock_values[4]
                    if available_stock - quantity_difference < 0:
                        messagebox.showwarning("Stock Limit", "Not enough stock available!", parent=self.root)
                        spinbox.set(old_quantity)  # Reset to old value
                        return

            # Update stock and cart total
            self.update_stock_quantity(product_id, -quantity_difference)
            new_total = cost * new_quantity
            self.cartBill.item(cart_item, values=(values[0], values[1], values[2], new_quantity, new_total))
        except Exception as e:
            print(f"Error updating quantity: {e}")


    def delete_from_cart(self):
        selected_item = self.cartBill.focus()  # Get selected row from the cart table
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a product to delete!", parent=self.root)
            return
        
        # Get the product details of the selected item
        item_data = self.cartBill.item(selected_item)['values']
        if not item_data:
            return
        
        product_id, product_name, cost, quantity, total = item_data

        # Show confirmation dialog
        confirm_delete = messagebox.askyesno("Delete Product", f"Are you sure you want to delete {product_name} from the cart?", parent=self.root)
        if confirm_delete:
            # Remove Spinbox first
            if selected_item in self.spinbox_dict:
                spinbox = self.spinbox_dict[selected_item]
                spinbox.destroy()  # Remove the Spinbox widget
                del self.spinbox_dict[selected_item]  # Remove reference from dictionary

            # Remove item from the cart (Treeview)
            self.cartBill.delete(selected_item)

            # Update the stock quantity
            self.update_stock_quantity(product_id, quantity)


    def generate_bill(self):
        # Check if customer name or mobile is provided
        if not self.mobile_var.get() and not self.cname_var.get() and not self.total_var.get():
            messagebox.showerror("Missing Information", "Customer name or mobile number is mandatory to generate the bill.", parent=self.root)
            return

        # Check if the cart is empty
        if not self.cartBill.get_children():
            messagebox.showerror("Empty Cart", "Your cart is empty. Please add products to the cart to generate the bill.", parent=self.root)
            return

        # Initialize bill header
        bill_text = f"\t\t\tINDIAN ELECTRONICS\n"
        bill_text += "=" * 75 + "\n"  # Decorative separator
        bill_text += f"Bill ID: {self.billID_var.get()}\n"
        bill_text += f"Mobile Number: {self.mobile_var.get()}\n"
        bill_text += f"Date: {time.strftime('%d-%m-%Y')}  Time: {time.strftime('%H:%M:%S')}\n"
        bill_text += "=" * 75 + "\n"
        bill_text += f"{'Product ID'.ljust(12)}{'Product Name'.ljust(30)}{'Qty'.rjust(6)}{'Price'.rjust(12)}{'Total'.rjust(12)}\n"
        bill_text += "-" * 75 + "\n"

        # Loop through cart items
        total_amount = 0
        total_quantity = 0  # Track total quantity of all items

        for item in self.cartBill.get_children():
            item_data = self.cartBill.item(item)["values"]
            product_id, product_name, price, quantity, total = item_data

            # Format numeric values properly
            bill_text += f"{str(product_id).ljust(12)}{product_name.ljust(30)}{str(quantity).rjust(6)}{float(price):12.2f}{float(total):12.2f}\n"
            
            total_amount += float(total)
            total_quantity += int(quantity)  # Sum up all item quantities

        # Final bill total with quantity
        bill_text += "-" * 75 + "\n"
        bill_text += f"{'Total Amount'.ljust(50)}{'Total Quantity:'.rjust(18)} {total_quantity}  {total_amount:12.2f}\n"
        bill_text += "=" * 75 + "\n"

        # Display bill in text widget
        self.bill_display.config(state="normal")  # Enable editing to update content
        self.bill_display.delete(1.0, END)
        self.bill_display.insert(END, bill_text)
        self.bill_display.config(state="disabled")  # Disable editing after update

        # Ensure 'bills' directory exists
        if not os.path.exists("bills"):
            os.makedirs("bills")

        # Generate a safe filename
        bill_filename = f"{self.billID_var.get()}.txt"
        file_path = os.path.join("bills", bill_filename)

        self.date_var.set(time.strftime('%d-%m-%Y'))
        self.qty_var.set(total_quantity)
        self.total_var.set(total_amount)
        self.billGenerateButton.config(state=DISABLED)
        self.billSaveButton.config(state="normal")
        self.entryMode.config(state="normal")
        self.entryMode.config(state="readonly")


        # Save bill to file
        try:
            with open(file_path, "w") as bill_file:
                bill_file.write(bill_text)
            # messagebox.showinfo("Success", f"Bill saved successfully as {bill_filename}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save the bill.\n{e}", parent=self.root)

    def save_bill(self):
        """ Saves bill details into the database and updates stock quantity """
        if self.mode_var.get() == "Select":
            messagebox.showerror("Error", "Please Select the Mode of Payment", parent=self.root)
        else:
            try:
                con = sqlite3.connect(database="inventory.db")
                cur = con.cursor()

                # Insert bill details into the 'bills' table
                cur.execute("INSERT INTO bills (BID, Mobile, Date, Quantity, Total, Mode) VALUES (?, ?, ?, ?, ?, ?)", (
                    self.billID_var.get(),
                    self.mobile_var.get(),
                    self.date_var.get(),
                    self.qty_var.get(),
                    self.total_var.get(),
                    self.mode_var.get()
                ))

                # Reduce stock quantities based on cart items
                for item in self.cartBill.get_children():
                    values = self.cartBill.item(item)["values"]
                    product_id = values[0]  # Product ID
                    quantity_purchased = values[3]  # Quantity bought

                    # Update stock in the database
                    cur.execute("UPDATE stock SET Total_Units = Total_Units - ? WHERE Product_ID = ?", 
                                (quantity_purchased, product_id))

                    # Update the stockTableBill UI
                    self.update_stock_quantity(product_id, -quantity_purchased)

                con.commit()
                messagebox.showinfo("Success", f"Bill ID {self.billID_var.get()} Added Successfully", parent=self.root)
                self.billSaveButton.config(state=DISABLED)
                self.show_stock()
                self.generate_pdf_bill()
                self.clear_customer()

            except Exception as es:
                messagebox.showerror("Error", f"Error Due To: {str(es)}", parent=self.root)

            finally:
                con.close()

    def generate_pdf_bill(self):
        """ Generates a PDF invoice with a border, structured data, company logo, and total in words. """

        # Ensure 'bills' directory exists
        os.makedirs("bills", exist_ok=True)

        # Generate a unique filename with better format
        pdf_filename = f"{self.billID_var.get()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        file_path = os.path.join("bills", pdf_filename)

        # Create the PDF document
        doc = SimpleDocTemplate(
            file_path,
            pagesize=A4,
            leftMargin=50,
            rightMargin=50,
            topMargin=50,
            bottomMargin=50
        )

        elements = []
        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        normal_style = styles["Normal"]

        # Define a function to draw a border on each page
        def onPage(canvas, doc):
            """ Draws a border around the page. """
            border_margin = 20  # Distance from the edges
            canvas.setStrokeColor(colors.black)
            canvas.setLineWidth(1)
            canvas.rect(border_margin, border_margin, A4[0] - 2 * border_margin, A4[1] - 2 * border_margin)

        # Load Company Logo
        logo_path = "images/plogo.png"  # Update as needed
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=80, height=80)  # Increased size for visibility
        else:
            logo = None  # Skip if not found

        # Invoice Header (Company Name)
        company_name = Paragraph("<b><font size=16>INDIAN ELECTRONICS</font></b>", title_style)
        invoice_text = Paragraph("<u><b><font size=14>INVOICE</font></b></u>", title_style)
        date_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        date_time_text = Paragraph(f"<b>Date & Time:</b> {date_time}", normal_style)

        # Centered Header (Company Name)
        header_table_data = [[company_name]]  # Single-column layout
        header_table = Table(header_table_data, colWidths=[500])  # Full width

        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))

        # Append Elements in Order
        elements.append(header_table)
        elements.append(Spacer(1, 10))  # Space after company name

        # Add logo below company name (if available)
        if logo:
            elements.append(logo)
            elements.append(Spacer(1, 10))

        elements.append(invoice_text)  # Invoice title
        elements.append(Spacer(1, 10))
        elements.append(date_time_text)
        elements.append(Spacer(1, 20))

        # Customer Details Section
        customer_details = [
            ["Bill ID:", self.billID_var.get() or "N/A"],
            ["Customer Name:", self.cname_var.get() or "N/A"],
            ["Mobile Number:", self.mobile_var.get() or "N/A"]
        ]
        customer_table = Table(customer_details, colWidths=[120, 300])
        customer_table.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, -1), "Helvetica-Bold"),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT')
        ]))

        elements.append(customer_table)
        elements.append(Spacer(1, 20))

        # Table Header for Product List
        table_data = [
            ["Product ID", "Product Name", "Qty", "Price", "Total"]
        ]

        # Fetch Data from Cart
        total_amount = 0
        total_quantity = 0
        for item in self.cartBill.get_children():
            values = self.cartBill.item(item)["values"]
            if len(values) >= 5:
                product_id, product_name, price, quantity, total = values
                table_data.append([product_id, product_name, quantity, f"{price:.2f}", f"{total:.2f}"])

                total_amount += float(total)
                total_quantity += int(quantity)

        # Add Summary Row
        table_data.append(["", "Total", total_quantity, "", f"{total_amount:.2f}"])

        # Create Product Table
        product_table = Table(table_data, colWidths=[80, 200, 50, 80, 80])
        product_table.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, 0), "Helvetica-Bold"),
            ('ALIGN', (2, 1), (4, -1), 'RIGHT')
        ]))

        elements.append(product_table)
        elements.append(Spacer(1, 20))

        # Convert Total Amount to Words
        total_words = num2words(total_amount, lang='en').capitalize()
        total_words_text = Paragraph(f"<b>Total in Words:</b> {total_words} only", normal_style)
        elements.append(total_words_text)

        # Generate the PDF with the border
        try:
            doc.build(elements, onFirstPage=onPage, onLaterPages=onPage)
            messagebox.showinfo("Success", f"PDF Invoice saved as {pdf_filename}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate invoice: {str(e)}", parent=self.root)






if __name__=="__main__":
    root=Tk()
    object=BillingSection(root)
    root.mainloop()
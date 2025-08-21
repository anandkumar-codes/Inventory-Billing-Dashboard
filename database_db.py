def generate_pdf(self):
        vehicle_no = self.vehicleno_var.get()
        if not vehicle_no:
            messagebox.showerror("Error", "Please enter Vehicle Number")
            return
        
        conn = sqlite3.connect('system.db')
        cursor = conn.cursor()

        # Fetch details from seller table with proper column names
        cursor.execute("""
            SELECT Vehicle_No, Date, Name, Care_Of, ID_Type, ID_Number, Mobile, Address, 
                Vehicle_Name, Model, Mfg, Fuel, Finance_Details, Price, Chassis, 
                Engine, CC, Wheel_base, Seating, Weight, Color, Registration_Date, 
                Valid_Upto, Tax, Insurance_Company, Valid_From, Valid_To 
            FROM seller WHERE Vehicle_No=?
        """, (vehicle_no,))
        seller_data = cursor.fetchone()

        # Fetch details from buyer table with proper column names
        cursor.execute("""
            SELECT Vehicle_Number, Date, Buyer_Name, Care_of, ID_Type, ID_Number, Mobile, Address 
            FROM buyer WHERE Vehicle_Number=?
        """, (vehicle_no,))
        buyer_data = cursor.fetchone()

        conn.close()

        if not seller_data and not buyer_data:
            messagebox.showerror("Error", "Vehicle number does not exist in both seller and buyer tables.")
            return
        elif not seller_data:
            messagebox.showerror("Error", "Vehicle details do not exist in Seller table.")
            return
        elif not buyer_data:
            messagebox.showerror("Error", "Vehicle details do not exist in Buyer table.")
            return

        # File path for saving PDF
        folder = "DeliveryNotes"
        if not os.path.exists(folder):
            os.makedirs(folder)
        file_path = os.path.join(folder, f"Delivery_Note_{vehicle_no}.pdf")

        # Create PDF canvas
        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4

        # Title
        c.setFont("Helvetica-Bold", 14)
        c.drawString(150, height - 50, "DELIVERY NOTE CUM INTERMEDIATION RECEIPT")

        # Date and Time
        current_date = datetime.now().strftime('%d-%m-%Y')
        current_time = datetime.now().strftime('%I:%M %p (%A)')
        c.setFont("Helvetica", 10)
        c.drawString(40, height - 80, f"Date: {current_date}")
        c.drawString(320, height - 80, f"Time: {current_time}")

        # ✅ Fetch using correct index
        registered_owner = seller_data[2]
        care_of = seller_data[3]
        address = seller_data[7]
        model = seller_data[9]
        chassis_no = seller_data[14]
        makers_name = seller_data[8]
        engine_number = seller_data[15]
        registration_date = seller_data[21]
        color = seller_data[20]
        class_of_vehicle = seller_data[8]
        type_of_body = seller_data[11]

        # Buyer Details
        buyer_name = buyer_data[2]
        buyer_care_of = buyer_data[3]
        buyer_address = buyer_data[7]
        buyer_phone = buyer_data[6]

        # Vehicle Details
        c.setFont("Helvetica", 10)
        c.drawString(40, height - 100, "I / We after satisfying myself / ourselves have taken delivery of Car / M. Cycle / Scooter")
        c.drawString(40, height - 115, f"Registered Owner: {registered_owner}")
        c.drawString(300, height - 115, f"S/o: {care_of}")
        c.drawString(40, height - 130, f"R/o: {address}")
        c.drawString(40, height - 150, f"Bearing Registration No.: {seller_data[0]}")
        # c.drawString(320, height - 150, f"Class to Vehicle: {class_of_vehicle}")
        c.drawString(40, height - 165, f"Model: {model}")
        c.drawString(320, height - 165, f"Chassis No.: {chassis_no}")
        c.drawString(40, height - 180, f"Maker’s Name: {makers_name}")
        c.drawString(320, height - 180, f"Engine Number: {engine_number}")
        c.drawString(40, height - 195, f"Date of Registration: {registration_date}")
        # c.drawString(320, height - 195, f"Type of Body: {type_of_body}")
        # c.drawString(40, height - 210, f"Colour of Vehicle: {color}")

        # RC Transfer
        c.drawString(40, height - 230, "Along with the R.C. Transfer letter/Temped Receipt")

        # Responsibility Clause
        c.setFont("Helvetica-Bold", 9)
        c.drawString(40, height - 260, "Receipt for my personal conveyance only. The said Vehicle has been duly")
        c.drawString(40, height - 275, "approved by me and found to my entire satisfaction. I am from today onwards")
        c.drawString(40, height - 290, "responsible to pay all types of Traffic Offence Police Litigation accident")
        c.drawString(40, height - 305, "and R.T.O.'s Municipal (Including Octroi wheel) and Premium Insurance")
        c.drawString(40, height - 320, "of the said vehicle.")

        # Seller and Buyer Address
        c.setFont("Helvetica-Bold", 10)
        c.drawString(40, height - 380, "(SELLER'S ADDRESS)")
        c.drawString(320, height - 380, "(PURCHASER'S ADDRESS)")
        c.setFont("Helvetica", 10)
        c.drawString(40, height - 400, f"Name: {registered_owner}")
        c.drawString(320, height - 400, f"Name: {buyer_name}")
        c.drawString(40, height - 415, f"S/o: {care_of}")
        c.drawString(320, height - 415, f"S/o: {buyer_care_of}")
        c.drawString(40, height - 430, f"Address: {address}")
        c.drawString(320, height - 430, f"Address: {buyer_address}")
        c.drawString(40, height - 445, f"Ph: {seller_data[6]}")
        c.drawString(320, height - 445, f"Ph: {buyer_phone}")

        # Note
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.black)
        c.rect(400, height - 500, 150, 40, stroke=1, fill=0)
        c.drawString(405, height - 480, "NOTE:")
        c.setFont("Helvetica", 8)
        c.drawString(405, height - 495, "Please transfer the vehicle within")
        c.drawString(405, height - 510, "10 days of purchase after which")
        c.drawString(405, height - 525, "no claims will be accepted.")

        # Signatures
        c.setFont("Helvetica", 10)
        c.drawString(40, height - 550, "Seller's Signature: ___________________")
        c.drawString(320, height - 550, "Purchaser's Signature: ___________________")

        # Save PDF
        c.save()

        messagebox.showinfo("Success", f"PDF Generated Successfully!\nSaved at: {file_path}")

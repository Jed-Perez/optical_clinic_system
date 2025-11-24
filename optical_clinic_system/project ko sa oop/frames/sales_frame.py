import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime

class SalesFrame(ctk.CTkFrame):
    def __init__(self, master, sales_manager, billing_manager, patient_manager, inventory_manager, invoice_manager, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.sales_manager = sales_manager
        self.billing_manager = billing_manager
        self.patient_manager = patient_manager
        self.inventory_manager = inventory_manager
        self.invoice_manager = invoice_manager
        self.cart = []
        self.build()

    def build(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=("white", "#1a1a1a"))
        header.pack(fill='x', padx=0, pady=0)
        ctk.CTkLabel(header, text='🛒 Sales Management', font=('Segoe UI', 26, 'bold')).pack(side='left', padx=20, pady=15)
        
        # Separator
        ctk.CTkLabel(self, text="", fg_color=("gray80", "gray30"), height=1).pack(fill='x', padx=0, pady=0)
        
        # Main container with two columns
        main_container = ctk.CTkFrame(self)
        main_container.pack(fill='both', expand=True, padx=15, pady=(15, 0))
        
        # ===== LEFT SECTION: SALES TRANSACTION =====
        left_frame = ctk.CTkFrame(main_container, fg_color=("white", "#0f0f0f"))
        left_frame.pack(side='left', fill='both', expand=False, padx=(0, 7.5), pady=0, ipadx=150)
        
        # Title
        sales_header = ctk.CTkFrame(left_frame, fg_color="transparent")
        sales_header.pack(fill='x', pady=(15, 10), padx=15)
        ctk.CTkLabel(sales_header, text='💰 Sales Transaction', font=('Segoe UI', 15, 'bold')).pack(side='left')
        
        # Customer and product input
        sales_frm = ctk.CTkFrame(left_frame, fg_color=("#f0f0f0", "#1a1a1a"))
        sales_frm.pack(padx=10, pady=10, fill='x')
        
        # Customer name
        ctk.CTkLabel(sales_frm, text='Customer Name', font=('Segoe UI', 11, 'bold')).pack(anchor='w', padx=10, pady=(8, 2))
        self.customer_name_combo = ctk.CTkComboBox(sales_frm, values=[], height=32, font=('Segoe UI', 11))
        self.customer_name_combo.pack(fill='x', padx=10, pady=(0, 8))
        self.customer_name_combo.set("Select Patient")
        self.patient_id_map = {}
        
        # Product selection
        ctk.CTkLabel(sales_frm, text='Select Product', font=('Segoe UI', 11, 'bold')).pack(anchor='w', padx=10, pady=(5, 2))
        self.sale_product_combo = ctk.CTkComboBox(sales_frm, values=[], height=32, font=('Segoe UI', 11), state='readonly', command=self.on_product_selected)
        self.sale_product_combo.pack(fill='x', padx=10, pady=(0, 8))
        self.sale_product_combo.set("Select Product")
        self.product_map = {}
        
        # Quantity and Price
        qty_price_frm = ctk.CTkFrame(sales_frm, fg_color=("transparent"))
        qty_price_frm.pack(fill='x', padx=10, pady=(5, 0))
        
        ctk.CTkLabel(qty_price_frm, text='Qty', font=('Segoe UI', 11, 'bold')).pack(side='left', pady=(0, 2))
        self.sale_qty = ctk.CTkEntry(qty_price_frm, placeholder_text='Qty', height=32, width=80, font=('Segoe UI', 11))
        self.sale_qty.pack(side='left', fill='x', expand=False, padx=(0, 10))
        
        ctk.CTkLabel(qty_price_frm, text='Price (₱)', font=('Segoe UI', 11, 'bold')).pack(side='left', pady=(0, 2))
        self.sale_price = ctk.CTkEntry(qty_price_frm, placeholder_text='Price', height=32, width=100, font=('Segoe UI', 11))
        self.sale_price.pack(side='left', fill='x', expand=True)
        
        # Buttons
        btn_frm2 = ctk.CTkFrame(sales_frm, fg_color=("transparent"))
        btn_frm2.pack(fill='x', padx=10, pady=10)
        ctk.CTkButton(btn_frm2, text='🛒 Add to Cart', command=self.add_to_cart, height=35, font=('Segoe UI', 11, 'bold'), fg_color=("#3498db", "#2471a3")).pack(fill='x', pady=4)
        ctk.CTkButton(btn_frm2, text='✅ Complete Sale', command=self.complete_sale, height=35, font=('Segoe UI', 11, 'bold'), fg_color=("#27ae60", "#1e8449")).pack(fill='x', pady=4)
        ctk.CTkButton(btn_frm2, text='🗑️ Clear Cart', command=self.clear_cart, height=35, font=('Segoe UI', 11, 'bold'), fg_color=("#e74c3c", "#c0392b")).pack(fill='x', pady=4)
        
        # Cart display
        ctk.CTkLabel(left_frame, text='🛍️ Shopping Cart', font=('Segoe UI', 12, 'bold')).pack(pady=(10, 5), padx=10)
        self.cart_txt = ctk.CTkTextbox(left_frame, font=('Consolas', 10), fg_color=("#f5f5f5", "#1a1a1a"), height=250)
        self.cart_txt.pack(fill='both', expand=True, padx=10, pady=(0, 15))
        
        # ===== RIGHT SECTION: PRODUCTS & SALES HISTORY =====
        right_frame = ctk.CTkFrame(main_container, fg_color=("white", "#0f0f0f"))
        right_frame.pack(side='right', fill='both', expand=True, padx=(7.5, 0), pady=0)
        
        # Products list
        prod_header = ctk.CTkFrame(right_frame, fg_color="transparent")
        prod_header.pack(fill='x', pady=(15, 10), padx=15)
        ctk.CTkLabel(prod_header, text='📦 Available Products', font=('Segoe UI', 15, 'bold')).pack(side='left')
        ctk.CTkButton(prod_header, text='🔄 Refresh', command=self.view_products, height=32, width=100, font=('Segoe UI', 10, 'bold')).pack(side='right', padx=5)
        
        self.products_txt = ctk.CTkTextbox(right_frame, font=('Consolas', 13), fg_color=("#f5f5f5", "#1a1a1a"), height=250)
        self.products_txt.pack(fill='both', expand=False, padx=10, pady=(0, 15))
        
        # Sales history
        history_header = ctk.CTkFrame(right_frame, fg_color=("transparent"))
        history_header.pack(fill='x', pady=(10, 10), padx=15)
        ctk.CTkLabel(history_header, text='📊 Sales History', font=('Segoe UI', 15, 'bold')).pack(side='left')
        ctk.CTkButton(history_header, text='🔄 Refresh', command=self.refresh_sales_history, height=32, width=100, font=('Segoe UI', 10, 'bold')).pack(side='right', padx=5)
        
        self.sales_history_txt = ctk.CTkTextbox(right_frame, font=('Consolas', 9), fg_color=("#f5f5f5", "#1a1a1a"))
        self.sales_history_txt.pack(fill='both', expand=True, padx=10, pady=(0, 15))
        
        self.load_patients()
        self.view_products()
        self.refresh_sales_history()

    def view_products(self):
        try:
            # Load from inventory instead of sales_products
            products = self.inventory_manager.list_items()
            self.products_txt.delete('1.0', 'end')
            if not products:
                self.products_txt.insert('end', 'No products available in inventory')
                return
            
            self.products_txt.insert('end', f'Total Products in Inventory: {len(products)}\n')
            self.products_txt.insert('end', '='*60 + '\n')
            
            # Load products into combobox
            self.product_map.clear()
            product_list = []
            
            current_category = None
            for p in products:
                category = p.get('Category', 'Other')
                if current_category != category:
                    current_category = category
                    self.products_txt.insert('end', f"\n--- {current_category} ---\n")
                
                pid = p.get('Inventory_ID', '?')
                pname = p.get('Item_Name', 'Unnamed')
                pprice = p.get('Unit_Price', 0)
                pqty = p.get('Quantity_On_Hand', 0)
                
                # Add to combobox list with ID to make it unique
                display_name = f"[{pid}] {pname} (₱{pprice})"
                product_list.append(display_name)
                self.product_map[display_name] = {'id': pid, 'name': pname, 'price': pprice, 'quantity': pqty, 'category': category}
                
                self.products_txt.insert('end', f"ID: {pid} | {pname} | ₱{pprice} | Stock: {pqty}\n")
            
            # Update combobox
            self.sale_product_combo.configure(values=product_list)
            self.products_txt.insert('end', f'\nTotal loaded into dropdown: {len(product_list)}\n')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def on_product_selected(self, choice):
        """Auto-fill price when product is selected"""
        if choice and choice != "Select Product":
            product_info = self.product_map.get(choice)
            if product_info:
                self.sale_price.delete(0, 'end')
                self.sale_price.insert(0, str(product_info['price']))
                self.sale_qty.delete(0, 'end')
                self.sale_qty.insert(0, '1')

    def load_patients(self):
        try:
            patients = self.patient_manager.list_patients()
            self.patient_id_map.clear()
            patient_names = []
            for p in patients:
                full_name = p['Name']
                self.patient_id_map[full_name] = p['Patient_ID']
                patient_names.append(full_name)
            self.customer_name_combo.configure(values=patient_names)
        except Exception as e:
            messagebox.showerror('Error', f'Failed to load patients: {str(e)}')

    def add_to_cart(self):
        try:
            selected_product = self.sale_product_combo.get()
            qty = self.sale_qty.get().strip()
            price = self.sale_price.get().strip()
            
            if not selected_product or selected_product == "Select Product":
                messagebox.showerror('Validation Error', 'Please select a product')
                return
            
            product_info = self.product_map.get(selected_product)
            if not product_info:
                messagebox.showerror('Validation Error', 'Invalid product selected')
                return
            
            prod_id = product_info['id']
            if not qty:
                messagebox.showerror('Validation Error', 'Quantity is required')
                return
            if not price:
                messagebox.showerror('Validation Error', 'Price is required')
                return
            
            try:
                qty_val = int(qty)
                price_val = float(price)
            except ValueError:
                messagebox.showerror('Validation Error', 'Quantity must be whole number and Price must be numeric')
                return
            
            # Add to cart
            self.cart.append({
                'product_id': prod_id,
                'quantity': qty_val,
                'price': price_val
            })
            
            messagebox.showinfo('Success', 'Item added to cart')
            self.sale_product_combo.set("Select Product")
            self.sale_qty.delete(0, 'end')
            self.sale_price.delete(0, 'end')
            self.update_cart_display()
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def update_cart_display(self):
        self.cart_txt.delete('1.0', 'end')
        total = 0
        for i, item in enumerate(self.cart, 1):
            subtotal = item['quantity'] * item['price']
            total += subtotal
            self.cart_txt.insert('end', f"{i}. Product ID: {item['product_id']} | Qty: {item['quantity']} | Price: ₱{item['price']} | Subtotal: ₱{subtotal}\n")
        
        self.cart_txt.insert('end', f"\n{'='*50}\n")
        self.cart_txt.insert('end', f"Total: ₱{total:.2f}\n")

    def complete_sale(self):
        try:
            customer_name = self.customer_name_combo.get()
            
            if not customer_name or customer_name == "Select Patient":
                messagebox.showerror('Validation Error', 'Please select a patient.')
                return
            if not self.cart:
                messagebox.showerror('Validation Error', 'Cart is empty')
                return
            
            patient_id = self.patient_id_map.get(customer_name)
            if not patient_id:
                messagebox.showerror('Validation Error', 'Invalid patient selected. Please refresh patient list.')
                return

            # Create sale
            sale_id = self.sales_manager.create_sale(customer_name, self.cart)
            
            # Create a corresponding invoice
            # Assuming you pass 'inv_m' (InvoiceManager) during initialization
            invoice_id = self.invoice_manager.create_invoice(sale_id, patient_id, "system") # "system" or current user
            
            invoice = self.invoice_manager.get_invoice_details(invoice_id)
            total_amount = invoice['Grand_Total']
            messagebox.showinfo('Success', f'Sale #{sale_id} completed and Invoice #{invoice["Invoice_Number"]} created for {customer_name}. Total: ₱{total_amount:.2f}')
            
            # Clear form
            self.customer_name_combo.set("Select Patient")
            self.clear_cart()
            self.update_cart_display()
            self.view_products()
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def clear_cart(self):
        self.cart = []
        self.update_cart_display()
        messagebox.showinfo('Info', 'Cart cleared')

    def refresh_sales_history(self):
        try:
            sales = self.sales_manager.get_all_sales()
            self.sales_history_txt.delete('1.0', 'end')
            
            if not sales:
                self.sales_history_txt.insert('end', 'No sales records found')
                return
            
            self.sales_history_txt.insert('end', f"{'Sale ID':<10} {'Customer':<20} {'Total (₱)':<15} {'Date':<20}\n")
            self.sales_history_txt.insert('end', f"{'-'*65}\n")
            
            for sale in sales:
                sale_id = sale.get('Sale_ID', sale.get('id', '?'))
                customer = sale.get('customer_name', 'Unknown')[:19]
                total = sale.get('total', 0)
                date = sale.get('sale_date', '')
                self.sales_history_txt.insert('end', f"{sale_id:<10} {customer:<20} ₱{total:<14.2f} {str(date):<20}\n")
        except Exception as e:
            messagebox.showerror('Error', f'Failed to load sales history: {str(e)}')

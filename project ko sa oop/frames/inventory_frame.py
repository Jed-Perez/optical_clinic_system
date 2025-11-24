import customtkinter as ctk
from tkinter import messagebox

class InventoryFrame(ctk.CTkFrame):
    def __init__(self, master, manager, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.manager = manager
        self.build()
    
    def build(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=("white", "#1a1a1a"))
        header.pack(fill='x', padx=0, pady=0)
        ctk.CTkLabel(header, text='📦 Inventory Management', font=('Segoe UI', 26, 'bold')).pack(side='left', padx=20, pady=15)
        
        # Separator
        ctk.CTkLabel(self, text="", fg_color=("gray80", "gray30"), height=1).pack(fill='x', padx=0, pady=0)
        
        # Main container
        main = ctk.CTkFrame(self)
        main.pack(fill='both', expand=True, padx=0, pady=0)
        
        # Left panel
        left = ctk.CTkFrame(main, fg_color=("white", "#0f0f0f"), width=300)
        left.pack(side='left', fill='both', expand=False, padx=0, pady=0)
        left.pack_propagate(False)
        
        form_title = ctk.CTkLabel(left, text='Add Item', font=('Segoe UI', 16, 'bold'))
        form_title.pack(pady=15, padx=20)
        
        # Create scrollable frame for form
        scroll_frame = ctk.CTkScrollableFrame(left, fg_color=("transparent"))
        scroll_frame.pack(fill='both', expand=True, padx=0, pady=0)
        
        frm = ctk.CTkFrame(scroll_frame, fg_color=("transparent"))
        frm.pack(padx=20, pady=10, fill='x')
        
        ctk.CTkLabel(frm, text='Item Name', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(10, 3))
        self.name = ctk.CTkEntry(frm, placeholder_text='Item name', height=35, font=('Segoe UI', 12))
        self.name.pack(fill='x', pady=(0, 10))
        
        ctk.CTkLabel(frm, text='Category', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(10, 3))
        self.category = ctk.CTkComboBox(frm, values=['Lenses', 'Frames', 'Glasses', 'Contact Lenses', 'Eye Care Products', 'Cleaning Solutions', 'Cases & Accessories', 'Reading Glasses', 'Sunglasses', 'Blue Light Glasses'], state='readonly', height=35, font=('Segoe UI', 12))
        self.category.set('Lenses')
        self.category.pack(fill='x', pady=(0, 10))
        
        ctk.CTkLabel(frm, text='Quantity', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(10, 3))
        self.qty = ctk.CTkEntry(frm, placeholder_text='Quantity', height=35, font=('Segoe UI', 12))
        self.qty.pack(fill='x', pady=(0, 10))
        
        ctk.CTkLabel(frm, text='Price (₱)', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(10, 3))
        self.price = ctk.CTkEntry(frm, placeholder_text='Price', height=35, font=('Segoe UI', 12))
        self.price.pack(fill='x', pady=(0, 20))
        
        btn_frm = ctk.CTkFrame(frm, fg_color=("transparent"))
        btn_frm.pack(fill='x', pady=10)
        
        ctk.CTkButton(btn_frm, text='➕ Add Item', command=self.add, height=40, font=('Segoe UI', 12, 'bold'), fg_color=("#27ae60", "#1e8449")).pack(fill='x', pady=5)
        ctk.CTkButton(btn_frm, text='👁️ View Items', command=self.view, height=40, font=('Segoe UI', 12, 'bold')).pack(fill='x', pady=5)
        ctk.CTkButton(btn_frm, text='📑 View Archive', command=self.view_archive, height=40, font=('Segoe UI', 12, 'bold'), fg_color=("#f39c12", "#d68910")).pack(fill='x', pady=5)
        
        # Right panel
        right = ctk.CTkFrame(main, fg_color=("white", "#0f0f0f"))
        right.pack(side='right', fill='both', expand=True, padx=15, pady=15)
        
        display_title = ctk.CTkLabel(right, text='Inventory List', font=('Segoe UI', 16, 'bold'))
        display_title.pack(pady=(0, 10))
        
        self.txt = ctk.CTkTextbox(right, font=('Consolas', 11), fg_color=("#f5f5f5", "#1a1a1a"))
        self.txt.pack(fill='both', expand=True, padx=0, pady=0)
    def add(self):
        try:
            name = self.name.get().strip()
            category = self.category.get()
            qty_str = self.qty.get().strip()
            price_str = self.price.get().strip()
            
            if not name:
                messagebox.showerror('Validation Error', 'Item name is required')
                return
            if not category:
                messagebox.showerror('Validation Error', 'Category is required')
                return
            if not qty_str:
                messagebox.showerror('Validation Error', 'Quantity is required')
                return
            if not price_str:
                messagebox.showerror('Validation Error', 'Price is required')
                return
            
            try:
                q = int(qty_str)
                p = float(price_str)
            except ValueError:
                messagebox.showerror('Invalid','Quantity must be a number and Price must be numeric')
                return
            
            self.manager.add_item(name, category, q, p, '')
            messagebox.showinfo('OK','Item added')
            self.name.delete(0, 'end')
            self.category.set('Lenses')
            self.qty.delete(0, 'end')
            self.price.delete(0, 'end')
            self.view()
        except Exception as e:
            messagebox.showerror('Error', str(e))
    def view(self):
        try:
            rows = self.manager.list_items()
            self.txt.delete('1.0', 'end')
            
            if not rows:
                self.txt.insert('end', 'No items in inventory')
                return
            
            # Group items by category
            categories = {}
            for item in rows:
                category = item.get('Category', 'Unknown')
                if category not in categories:
                    categories[category] = []
                categories[category].append(item)
            
            # Display header
            self.txt.insert('end', '='*70 + '\n')
            self.txt.insert('end', 'INVENTORY STOCK REPORT\n')
            self.txt.insert('end', '='*70 + '\n\n')
            
            # Display items by category
            for category in sorted(categories.keys()):
                items = categories[category]
                self.txt.insert('end', f'\n📦 {category.upper()}\n')
                self.txt.insert('end', '-'*70 + '\n')
                self.txt.insert('end', f'{"ID":<5} {"Item Name":<30} {"Stock":<10} {"Price":<10}\n')
                self.txt.insert('end', '-'*70 + '\n')
                
                for item in items:
                    item_id = str(item.get('Inventory_ID', '?'))
                    name = item.get('Item_Name', 'Unknown')[:28]
                    stock = item.get('Quantity_On_Hand', 0)
                    price = item.get('Unit_Price', 0)
                    
                    # Color code low stock
                    stock_display = f"{stock} pcs"
                    if stock < 10:
                        stock_display += " ⚠️"
                    
                    self.txt.insert('end', f'{item_id:<5} {name:<30} {stock_display:<10} ₱{price:<9.2f}\n')
                
                # Category summary
                total_items = len(items)
                total_stock = sum(item.get('Quantity_On_Hand', 0) for item in items)
                self.txt.insert('end', f'\nCategory Total: {total_items} items, {total_stock} units in stock\n')
            
            # Grand total
            self.txt.insert('end', '\n' + '='*70 + '\n')
            total_items = len(rows)
            total_stock = sum(item.get('Quantity_On_Hand', 0) for item in rows)
            total_value = sum(item.get('Quantity_On_Hand', 0) * item.get('Unit_Price', 0) for item in rows)
            self.txt.insert('end', f'GRAND TOTAL: {total_items} items | {total_stock} units | ₱{total_value:,.2f}\n')
            self.txt.insert('end', '='*70 + '\n')
            
        except Exception as e:
            self.txt.delete('1.0', 'end')
            self.txt.insert('end', f'Error loading inventory: {str(e)}')
    def view_archive(self):
        rows=self.manager.list_archived(); self.txt.delete('1.0','end')
        for r in rows: self.txt.insert('end', f"{r['Inventory_ID']} | {r['Item_Name']} | Deleted: {r['Deleted_On']}\n")

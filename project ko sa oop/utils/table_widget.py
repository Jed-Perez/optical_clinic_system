import customtkinter as ctk
from typing import List, Dict, Callable

class DataTable(ctk.CTkFrame):
    def __init__(self, master, columns: List[str], data: List[Dict], row_height=35, **kwargs):
        super().__init__(master, **kwargs)
        self.columns = columns
        self.data = data
        self.row_height = row_height
        self.on_row_click: Callable = None
        self.selected_row = None
        self.build()
    
    def build(self):
        header = ctk.CTkFrame(self, fg_color=("#3498db", "#1f6aa5"), height=40)
        header.pack(fill='x', padx=0, pady=0)
        header.pack_propagate(False)
        
        col_width = 100 // len(self.columns) if self.columns else 100
        for col in self.columns:
            ctk.CTkLabel(
                header, text=col, font=('Segoe UI', 11, 'bold'),
                text_color='white', width=col_width
            ).pack(side='left', fill='both', expand=True, padx=8, pady=8)
        
        self.scrollable = ctk.CTkScrollableFrame(self, fg_color=("white", "#0a0a0a"))
        self.scrollable.pack(fill='both', expand=True, padx=0, pady=0)
        
        self.row_frames = []
        for idx, row_data in enumerate(self.data):
            self._create_row(idx, row_data)
    
    def _create_row(self, idx: int, row_data: Dict):
        row_frame = ctk.CTkFrame(
            self.scrollable,
            fg_color=("#f0f0f0" if idx % 2 == 0 else "white", "#1a1a1a" if idx % 2 == 0 else "#0f0f0f"),
            height=self.row_height
        )
        row_frame.pack(fill='x', padx=2, pady=1)
        row_frame.pack_propagate(False)
        
        row_frame.bind('<Button-1>', lambda e: self._on_row_click(idx, row_data, row_frame))
        for child in row_frame.winfo_children():
            child.bind('<Button-1>', lambda e: self._on_row_click(idx, row_data, row_frame))
        
        col_width = 100 // len(self.columns) if self.columns else 100
        for col in self.columns:
            value = row_data.get(col, '-')
            label = ctk.CTkLabel(
                row_frame, text=str(value), font=('Segoe UI', 10),
                width=col_width
            )
            label.pack(side='left', fill='both', expand=True, padx=8, pady=8)
            label.bind('<Button-1>', lambda e: self._on_row_click(idx, row_data, row_frame))
        
        self.row_frames.append({'frame': row_frame, 'data': row_data, 'idx': idx})
    
    def _on_row_click(self, idx: int, row_data: Dict, row_frame):
        if self.selected_row:
            self.selected_row['frame'].configure(fg_color=("#f0f0f0" if self.selected_row['idx'] % 2 == 0 else "white", "#1a1a1a" if self.selected_row['idx'] % 2 == 0 else "#0f0f0f"))
        row_frame.configure(fg_color=("#3498db", "#1f6aa5"))
        self.selected_row = {'frame': row_frame, 'data': row_data, 'idx': idx}
        
        if self.on_row_click:
            self.on_row_click(row_data)
    
    def update_data(self, data: List[Dict]):
        self.data = data
        for item in self.scrollable.winfo_children():
            item.destroy()
        self.row_frames = []
        for idx, row_data in enumerate(self.data):
            self._create_row(idx, row_data)
    
    def get_selected(self) -> Dict:
        return self.selected_row['data'] if self.selected_row else None

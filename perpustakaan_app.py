import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import re

class DatabaseConnection:
    """Class untuk menangani koneksi database"""
    
    @staticmethod
    def create_connection():
        """Membuat koneksi ke database MySQL"""
        try:
            # Ganti host, database, user, dan password sesuai konfigurasi Anda
            connection = mysql.connector.connect(
                host='localhost',
                database='perpustakaan_db',
                user='root', 
                password='' 
            )
            if connection.is_connected():
                return connection
        except Error as e:
            messagebox.showerror("Error Koneksi", f"Gagal terhubung ke database:\n{str(e)}")
            return None

class LoginWindow:
    """Class untuk window login"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Sistem Perpustakaan")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        self.center_window()
        
        self.root.configure(bg='#2c3e50')
        self.current_user = None
        
        self.create_widgets()
    
    def center_window(self):
        """Menempatkan window di tengah layar"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Membuat widget untuk form login"""
        main_frame = tk.Frame(self.root, bg='#ecf0f1', padx=30, pady=30)
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        title_label = tk.Label(main_frame, text="SISTEM PERPUSTAKAAN", 
                                 font=('Arial', 16, 'bold'), bg='#ecf0f1', fg='#2c3e50')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        tk.Label(main_frame, text="Username:", font=('Arial', 10), 
                 bg='#ecf0f1', fg='#2c3e50').grid(row=1, column=0, sticky='w', pady=5)
        self.username_entry = tk.Entry(main_frame, font=('Arial', 10), width=25)
        self.username_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        tk.Label(main_frame, text="Password:", font=('Arial', 10), 
                 bg='#ecf0f1', fg='#2c3e50').grid(row=2, column=0, sticky='w', pady=5)
        self.password_entry = tk.Entry(main_frame, font=('Arial', 10), width=25, show='*')
        self.password_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        login_btn = tk.Button(main_frame, text="LOGIN", font=('Arial', 11, 'bold'),
                              bg='#27ae60', fg='white', width=20, cursor='hand2',
                              command=self.login)
        login_btn.grid(row=3, column=0, columnspan=2, pady=(20, 0))
        
        self.root.bind('<Return>', lambda e: self.login())
    
    def login(self):
        """Proses login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Peringatan", "Username dan password harus diisi!")
            return
        
        connection = DatabaseConnection.create_connection()
        if not connection:
            return
        
        try:
            cursor = connection.cursor(dictionary=True)
            # Menggunakan parameterized query untuk mencegah SQL Injection
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            
            if user:
                self.current_user = user
                messagebox.showinfo("Sukses", f"Selamat datang, {user['username']}!")
                self.root.destroy()
                self.open_dashboard()
            else:
                messagebox.showerror("Error", "Username atau password salah!")
                self.password_entry.delete(0, tk.END)
        
        except Error as e:
            messagebox.showerror("Error Database", f"Terjadi kesalahan:\n{str(e)}")
        
        finally:
            # Penutupan koneksi yang aman
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def open_dashboard(self):
        """Membuka dashboard setelah login berhasil"""
        root = tk.Tk()
        Dashboard(root, self.current_user)
        root.mainloop()

class Dashboard:
    """Class untuk dashboard utama"""
    
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("Dashboard - Sistem Perpustakaan")
        self.root.geometry("900x600")
        self.root.configure(bg='#ecf0f1')
        
        self.center_window()
        self.create_widgets()
        self.load_statistics()
    
    def center_window(self):
        """Menempatkan window di tengah layar"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Membuat widget untuk dashboard"""
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        welcome_label = tk.Label(header_frame, 
                                 text=f"Selamat Datang, {self.user['username']}!",
                                 font=('Arial', 18, 'bold'), bg='#2c3e50', fg='white')
        welcome_label.pack(pady=20)
        
        role_label = tk.Label(header_frame, 
                              text=f"Role: {self.user['role'].upper()}",
                              font=('Arial', 10), bg='#2c3e50', fg='#ecf0f1')
        role_label.pack()
        
        content_frame = tk.Frame(self.root, bg='#ecf0f1')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        stats_frame = tk.LabelFrame(content_frame, text="Statistik Perpustakaan",
                                     font=('Arial', 12, 'bold'), bg='#ecf0f1',
                                     fg='#2c3e50', padx=20, pady=20)
        stats_frame.pack(fill='x', pady=(0, 20))
        
        stats_container = tk.Frame(stats_frame, bg='#ecf0f1')
        stats_container.pack()
        
        # Jumlah Buku
        buku_frame = tk.Frame(stats_container, bg='#3498db', padx=30, pady=20)
        buku_frame.grid(row=0, column=0, padx=10)
        
        self.buku_count_label = tk.Label(buku_frame, text="0", 
                                         font=('Arial', 24, 'bold'),
                                         bg='#3498db', fg='white')
        self.buku_count_label.pack()
        tk.Label(buku_frame, text="Total Buku", font=('Arial', 10),
                 bg='#3498db', fg='white').pack()
        
        # Jumlah Anggota
        anggota_frame = tk.Frame(stats_container, bg='#e74c3c', padx=30, pady=20)
        anggota_frame.grid(row=0, column=1, padx=10)
        
        self.anggota_count_label = tk.Label(anggota_frame, text="0",
                                             font=('Arial', 24, 'bold'),
                                             bg='#e74c3c', fg='white')
        self.anggota_count_label.pack()
        tk.Label(anggota_frame, text="Total Anggota", font=('Arial', 10),
                 bg='#e74c3c', fg='white').pack()
        
        # Menu buttons frame
        menu_frame = tk.LabelFrame(content_frame, text="Menu Navigasi",
                                     font=('Arial', 12, 'bold'), bg='#ecf0f1',
                                     fg='#2c3e50', padx=20, pady=20)
        menu_frame.pack(fill='both', expand=True)
        
        button_container = tk.Frame(menu_frame, bg='#ecf0f1')
        button_container.pack(expand=True)
        
        buku_btn = tk.Button(button_container, text="📚 MANAJEMEN BUKU",
                              font=('Arial', 12, 'bold'), bg='#3498db', fg='white',
                              width=25, height=3, cursor='hand2',
                              command=self.open_buku_management)
        buku_btn.grid(row=0, column=0, padx=10, pady=10)
        
        anggota_btn = tk.Button(button_container, text="👥 MANAJEMEN ANGGOTA",
                                 font=('Arial', 12, 'bold'), bg='#e74c3c', fg='white',
                                 width=25, height=3, cursor='hand2',
                                 command=self.open_anggota_management)
        anggota_btn.grid(row=0, column=1, padx=10, pady=10)
        
        logout_btn = tk.Button(button_container, text="🚪 LOGOUT",
                                 font=('Arial', 12, 'bold'), bg='#95a5a6', fg='white',
                                 width=25, height=2, cursor='hand2',
                                 command=self.logout)
        logout_btn.grid(row=1, column=0, columnspan=2, pady=10)
    
    def load_statistics(self):
        """Memuat statistik dari database"""
        connection = DatabaseConnection.create_connection()
        if not connection:
            return
        
        try:
            cursor = connection.cursor()
            
            # Count buku
            cursor.execute("SELECT COUNT(*) FROM buku")
            buku_count = cursor.fetchone()[0]
            self.buku_count_label.config(text=str(buku_count))
            
            # Count anggota
            cursor.execute("SELECT COUNT(*) FROM anggota")
            anggota_count = cursor.fetchone()[0]
            self.anggota_count_label.config(text=str(anggota_count))
        
        except Error as e:
            messagebox.showerror("Error", f"Gagal memuat statistik:\n{str(e)}")
        
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def open_buku_management(self):
        """Membuka window manajemen buku"""
        BukuManagement(self.root, self.user)
    
    def open_anggota_management(self):
        """Membuka window manajemen anggota"""
        AnggotaManagement(self.root, self.user)
    
    def logout(self):
        """Logout dan kembali ke login"""
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin logout?"):
            self.root.destroy()
            root = tk.Tk()
            LoginWindow(root)
            root.mainloop()

class BukuManagement:
    """Class untuk manajemen buku"""
    
    def __init__(self, parent, user):
        self.window = tk.Toplevel(parent)
        self.window.title("Manajemen Buku")
        self.window.geometry("1000x700")
        self.window.configure(bg='#ecf0f1')
        self.user = user
        
        self.center_window()
        self.create_widgets()
        self.load_data()
    
    def center_window(self):
        """Menempatkan window di tengah layar"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Membuat widget untuk manajemen buku"""
        header_frame = tk.Frame(self.window, bg='#2c3e50', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="MANAJEMEN BUKU",
                 font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white').pack(pady=15)
        
        main_container = tk.Frame(self.window, bg='#ecf0f1')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        form_frame = tk.LabelFrame(main_container, text="Form Buku",
                                     font=('Arial', 11, 'bold'), bg='#ecf0f1',
                                     fg='#2c3e50', padx=15, pady=15)
        form_frame.pack(fill='x', pady=(0, 10))
        
        fields_frame = tk.Frame(form_frame, bg='#ecf0f1')
        fields_frame.pack()
        
        # Kode Buku
        tk.Label(fields_frame, text="Kode Buku:", font=('Arial', 9),
                 bg='#ecf0f1').grid(row=0, column=0, sticky='w', pady=3)
        self.kode_entry = tk.Entry(fields_frame, font=('Arial', 9), width=20)
        self.kode_entry.grid(row=0, column=1, padx=5, pady=3)
        
        # Judul
        tk.Label(fields_frame, text="Judul:", font=('Arial', 9),
                 bg='#ecf0f1').grid(row=0, column=2, sticky='w', pady=3, padx=(15, 0))
        self.judul_entry = tk.Entry(fields_frame, font=('Arial', 9), width=30)
        self.judul_entry.grid(row=0, column=3, padx=5, pady=3)
        
        # Pengarang
        tk.Label(fields_frame, text="Pengarang:", font=('Arial', 9),
                 bg='#ecf0f1').grid(row=1, column=0, sticky='w', pady=3)
        self.pengarang_entry = tk.Entry(fields_frame, font=('Arial', 9), width=20)
        self.pengarang_entry.grid(row=1, column=1, padx=5, pady=3)
        
        # Penerbit
        tk.Label(fields_frame, text="Penerbit:", font=('Arial', 9),
                 bg='#ecf0f1').grid(row=1, column=2, sticky='w', pady=3, padx=(15, 0))
        self.penerbit_entry = tk.Entry(fields_frame, font=('Arial', 9), width=30)
        self.penerbit_entry.grid(row=1, column=3, padx=5, pady=3)
        
        # Tahun Terbit
        tk.Label(fields_frame, text="Tahun Terbit:", font=('Arial', 9),
                 bg='#ecf0f1').grid(row=2, column=0, sticky='w', pady=3)
        self.tahun_entry = tk.Entry(fields_frame, font=('Arial', 9), width=20)
        self.tahun_entry.grid(row=2, column=1, padx=5, pady=3)
        
        # Stok
        tk.Label(fields_frame, text="Stok:", font=('Arial', 9),
                 bg='#ecf0f1').grid(row=2, column=2, sticky='w', pady=3, padx=(15, 0))
        self.stok_entry = tk.Entry(fields_frame, font=('Arial', 9), width=30)
        self.stok_entry.grid(row=2, column=3, padx=5, pady=3)
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg='#ecf0f1')
        btn_frame.pack(pady=(10, 0))
        
        tk.Button(btn_frame, text="Tambah", font=('Arial', 9, 'bold'),
                  bg='#27ae60', fg='white', width=12, cursor='hand2',
                  command=self.add_buku).grid(row=0, column=0, padx=3)
        
        tk.Button(btn_frame, text="Update", font=('Arial', 9, 'bold'),
                  bg='#f39c12', fg='white', width=12, cursor='hand2',
                  command=self.update_buku).grid(row=0, column=1, padx=3)
        
        tk.Button(btn_frame, text="Hapus", font=('Arial', 9, 'bold'),
                  bg='#e74c3c', fg='white', width=12, cursor='hand2',
                  command=self.delete_buku).grid(row=0, column=2, padx=3)
        
        tk.Button(btn_frame, text="Clear", font=('Arial', 9, 'bold'),
                  bg='#95a5a6', fg='white', width=12, cursor='hand2',
                  command=self.clear_form).grid(row=0, column=3, padx=3)
        
        # Search frame
        search_frame = tk.Frame(main_container, bg='#ecf0f1')
        search_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(search_frame, text="🔍 Cari Buku:", font=('Arial', 10, 'bold'),
                 bg='#ecf0f1').pack(side='left', padx=(0, 10))
        
        self.search_entry = tk.Entry(search_frame, font=('Arial', 10), width=40)
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.search_buku())
        
        tk.Button(search_frame, text="Refresh", font=('Arial', 9),
                  bg='#3498db', fg='white', cursor='hand2',
                  command=self.load_data).pack(side='left', padx=5)
        
        # Treeview frame
        tree_frame = tk.Frame(main_container, bg='#ecf0f1')
        tree_frame.pack(fill='both', expand=True)
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(tree_frame, orient='vertical')
        scroll_y.pack(side='right', fill='y')
        
        scroll_x = ttk.Scrollbar(tree_frame, orient='horizontal')
        scroll_x.pack(side='bottom', fill='x')
        
        # Treeview
        self.tree = ttk.Treeview(tree_frame, 
                                 columns=('ID', 'Kode', 'Judul', 'Pengarang', 
                                          'Penerbit', 'Tahun', 'Stok'),
                                 show='headings', height=15,
                                 yscrollcommand=scroll_y.set,
                                 xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # Define columns
        self.tree.heading('ID', text='ID')
        self.tree.heading('Kode', text='Kode Buku')
        self.tree.heading('Judul', text='Judul')
        self.tree.heading('Pengarang', text='Pengarang')
        self.tree.heading('Penerbit', text='Penerbit')
        self.tree.heading('Tahun', text='Tahun Terbit')
        self.tree.heading('Stok', text='Stok')
        
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Kode', width=100, anchor='center')
        self.tree.column('Judul', width=250)
        self.tree.column('Pengarang', width=150)
        self.tree.column('Penerbit', width=150)
        self.tree.column('Tahun', width=100, anchor='center')
        self.tree.column('Stok', width=80, anchor='center')
        
        self.tree.pack(fill='both', expand=True)
        
        # Bind select
        self.tree.bind('<ButtonRelease-1>', self.select_item)
    
    def validate_input(self):
        """Validasi input form"""
        kode = self.kode_entry.get().strip()
        judul = self.judul_entry.get().strip()
        pengarang = self.pengarang_entry.get().strip()
        penerbit = self.penerbit_entry.get().strip()
        tahun = self.tahun_entry.get().strip()
        stok = self.stok_entry.get().strip()
        
        if not all([kode, judul, pengarang, penerbit, tahun, stok]):
            messagebox.showwarning("Peringatan", "Semua field harus diisi!")
            return False
        
        try:
            tahun_int = int(tahun)
            if tahun_int < 1000 or tahun_int > 2100:
                messagebox.showwarning("Peringatan", "Tahun terbit tidak valid!")
                return False
        except ValueError:
            messagebox.showwarning("Peringatan", "Tahun terbit harus berupa angka!")
            return False
        
        try:
            stok_int = int(stok)
            if stok_int < 0:
                messagebox.showwarning("Peringatan", "Stok harus angka positif!")
                return False
        except ValueError:
            messagebox.showwarning("Peringatan", "Stok harus berupa angka!")
            return False
        
        return True
    
    def add_buku(self):
        """Menambah buku baru"""
        if not self.validate_input():
            return
        
        connection = DatabaseConnection.create_connection()
        if not connection:
            return
        
        try:
            cursor = connection.cursor()
            query = """INSERT INTO buku (kode_buku, judul, pengarang, penerbit, 
                       tahun_terbit, stok) VALUES (%s, %s, %s, %s, %s, %s)"""
            values = (
                self.kode_entry.get().strip(),
                self.judul_entry.get().strip(),
                self.pengarang_entry.get().strip(),
                self.penerbit_entry.get().strip(),
                int(self.tahun_entry.get().strip()),
                int(self.stok_entry.get().strip())
            )
            
            cursor.execute(query, values)
            connection.commit()
            
            messagebox.showinfo("Sukses", "Buku berhasil ditambahkan!")
            self.clear_form()
            self.load_data()
        
        except Error as e:
            if 'Duplicate entry' in str(e):
                messagebox.showerror("Error", "Kode buku sudah ada!")
            else:
                messagebox.showerror("Error Database", f"Gagal menambah buku:\n{str(e)}")
        
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    # **PERBAIKAN: Menambahkan fungsi update_buku yang hilang**
    def update_buku(self):
        """Mengupdate data buku yang dipilih"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih buku yang akan diupdate!")
            return
        
        if not self.validate_input():
            return
            
        item = self.tree.item(selected[0])
        buku_id = item['values'][0]

        connection = DatabaseConnection.create_connection()
        if not connection:
            return
        
        try:
            cursor = connection.cursor()
            query = """UPDATE buku SET kode_buku=%s, judul=%s, pengarang=%s, 
                       penerbit=%s, tahun_terbit=%s, stok=%s WHERE id=%s"""
            values = (
                self.kode_entry.get().strip(),
                self.judul_entry.get().strip(),
                self.pengarang_entry.get().strip(),
                self.penerbit_entry.get().strip(),
                int(self.tahun_entry.get().strip()),
                int(self.stok_entry.get().strip()),
                buku_id
            )
            
            cursor.execute(query, values)
            connection.commit()
            
            messagebox.showinfo("Sukses", f"Buku ID {buku_id} berhasil diupdate!")
            self.clear_form()
            self.load_data()
            
        except Error as e:
            if 'Duplicate entry' in str(e):
                messagebox.showerror("Error", "Kode buku sudah ada!")
            else:
                messagebox.showerror("Error Database", f"Gagal mengupdate buku:\n{str(e)}") 
        
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    
    def delete_buku(self):
        """Hapus data buku"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih buku yang akan dihapus!")
            return
        
        if not messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus buku ini?"):
            return
        
        connection = DatabaseConnection.create_connection()
        if not connection:
            return
        
        try:
            item = self.tree.item(selected[0])
            buku_id = item['values'][0]
            
            cursor = connection.cursor()
            cursor.execute("DELETE FROM buku WHERE id = %s", (buku_id,))
            connection.commit()
            
            messagebox.showinfo("Sukses", "Buku berhasil dihapus!")
            self.clear_form()
            self.load_data()
        
        except Error as e:
            messagebox.showerror("Error", f"Gagal menghapus buku:\n{str(e)}")
        
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def load_data(self):
        """Memuat data buku dari database"""
        connection = DatabaseConnection.create_connection()
        if not connection:
            return
        
        try:
            # Clear existing data
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM buku ORDER BY id DESC")
            rows = cursor.fetchall()
            
            for row in rows:
                self.tree.insert('', 'end', values=row)
        
        except Error as e:
            messagebox.showerror("Error", f"Gagal memuat data:\n{str(e)}")
        
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def search_buku(self):
        """Mencari buku berdasarkan judul atau pengarang"""
        search_term = self.search_entry.get().strip()
        
        connection = DatabaseConnection.create_connection()
        if not connection:
            return
        
        try:
            # Clear existing data
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            cursor = connection.cursor()
            query = """SELECT * FROM buku 
                       WHERE judul LIKE %s OR pengarang LIKE %s 
                       ORDER BY id DESC"""
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern))
            rows = cursor.fetchall()
            
            for row in rows:
                self.tree.insert('', 'end', values=row)
        
        except Error as e:
            messagebox.showerror("Error", f"Gagal mencari data:\n{str(e)}")
        
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def select_item(self, event):
        """Mengisi form saat item dipilih"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item['values']
            
            self.clear_form()
            self.kode_entry.insert(0, values[1])
            self.judul_entry.insert(0, values[2])
            self.pengarang_entry.insert(0, values[3])
            self.penerbit_entry.insert(0, values[4])
            self.tahun_entry.insert(0, values[5])
            self.stok_entry.insert(0, values[6])
    
    def clear_form(self):
        """Membersihkan form"""
        self.kode_entry.delete(0, tk.END)
        self.judul_entry.delete(0, tk.END)
        self.pengarang_entry.delete(0, tk.END)
        self.penerbit_entry.delete(0, tk.END)
        self.tahun_entry.delete(0, tk.END)
        self.stok_entry.delete(0, tk.END)


class AnggotaManagement:
    """Class untuk manajemen anggota"""
    
    def __init__(self, parent, user):
        self.window = tk.Toplevel(parent)
        self.window.title("Manajemen Anggota")
        self.window.geometry("1000x700")
        self.window.configure(bg='#ecf0f1')
        self.user = user
        
        self.center_window()
        self.create_widgets()
        self.load_data()
    
    def center_window(self):
        """Menempatkan window di tengah layar"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Membuat widget untuk manajemen anggota"""
        header_frame = tk.Frame(self.window, bg='#2c3e50', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="MANAJEMEN ANGGOTA",
                 font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white').pack(pady=15)
        
        main_container = tk.Frame(self.window, bg='#ecf0f1')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        form_frame = tk.LabelFrame(main_container, text="Form Anggota",
                                     font=('Arial', 11, 'bold'), bg='#ecf0f1',
                                     fg='#2c3e50', padx=15, pady=15)
        form_frame.pack(fill='x', pady=(0, 10))
        
        fields_frame = tk.Frame(form_frame, bg='#ecf0f1')
        fields_frame.pack()
        
        # Kode Anggota
        tk.Label(fields_frame, text="Kode Anggota:", font=('Arial', 9),
                 bg='#ecf0f1').grid(row=0, column=0, sticky='w', pady=3)
        self.kode_entry = tk.Entry(fields_frame, font=('Arial', 9), width=20)
        self.kode_entry.grid(row=0, column=1, padx=5, pady=3)
        
        # Nama
        tk.Label(fields_frame, text="Nama:", font=('Arial', 9),
                 bg='#ecf0f1').grid(row=0, column=2, sticky='w', pady=3, padx=(15, 0))
        self.nama_entry = tk.Entry(fields_frame, font=('Arial', 9), width=30)
        self.nama_entry.grid(row=0, column=3, padx=5, pady=3)
        
        # Alamat
        tk.Label(fields_frame, text="Alamat:", font=('Arial', 9),
                 bg='#ecf0f1').grid(row=1, column=0, sticky='w', pady=3)
        self.alamat_entry = tk.Entry(fields_frame, font=('Arial', 9), width=20)
        self.alamat_entry.grid(row=1, column=1, padx=5, pady=3)
        
        # Telepon
        tk.Label(fields_frame, text="Telepon:", font=('Arial', 9),
                 bg='#ecf0f1').grid(row=1, column=2, sticky='w', pady=3, padx=(15, 0))
        self.telepon_entry = tk.Entry(fields_frame, font=('Arial', 9), width=30)
        self.telepon_entry.grid(row=1, column=3, padx=5, pady=3)
        
        # Email
        tk.Label(fields_frame, text="Email:", font=('Arial', 9),
                 bg='#ecf0f1').grid(row=2, column=0, sticky='w', pady=3)
        self.email_entry = tk.Entry(fields_frame, font=('Arial', 9), width=52)
        self.email_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=3, sticky='w')
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg='#ecf0f1')
        btn_frame.pack(pady=(10, 0))
        
        tk.Button(btn_frame, text="Tambah", font=('Arial', 9, 'bold'),
                  bg='#27ae60', fg='white', width=12, cursor='hand2',
                  command=self.add_anggota).grid(row=0, column=0, padx=3)
        
        tk.Button(btn_frame, text="Update", font=('Arial', 9, 'bold'),
                  bg='#f39c12', fg='white', width=12, cursor='hand2',
                  command=self.update_anggota).grid(row=0, column=1, padx=3)
        
        tk.Button(btn_frame, text="Hapus", font=('Arial', 9, 'bold'),
                  bg='#e74c3c', fg='white', width=12, cursor='hand2',
                  command=self.delete_anggota).grid(row=0, column=2, padx=3)
        
        tk.Button(btn_frame, text="Clear", font=('Arial', 9, 'bold'),
                  bg='#95a5a6', fg='white', width=12, cursor='hand2',
                  command=self.clear_form).grid(row=0, column=3, padx=3)
        
        # Search frame
        search_frame = tk.Frame(main_container, bg='#ecf0f1')
        search_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(search_frame, text="🔍 Cari Anggota:", font=('Arial', 10, 'bold'),
                 bg='#ecf0f1').pack(side='left', padx=(0, 10))
        
        self.search_entry = tk.Entry(search_frame, font=('Arial', 10), width=40)
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.search_anggota())
        
        tk.Button(search_frame, text="Refresh", font=('Arial', 9),
                  bg='#3498db', fg='white', cursor='hand2',
                  command=self.load_data).pack(side='left', padx=5)
        
        # Treeview frame
        tree_frame = tk.Frame(main_container, bg='#ecf0f1')
        tree_frame.pack(fill='both', expand=True)
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(tree_frame, orient='vertical')
        scroll_y.pack(side='right', fill='y')
        
        scroll_x = ttk.Scrollbar(tree_frame, orient='horizontal')
        scroll_x.pack(side='bottom', fill='x')
        
        # Treeview
        self.tree = ttk.Treeview(tree_frame, 
                                 columns=('ID', 'Kode', 'Nama', 'Alamat', 
                                          'Telepon', 'Email'),
                                 show='headings', height=15,
                                 yscrollcommand=scroll_y.set,
                                 xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # Define columns
        self.tree.heading('ID', text='ID')
        self.tree.heading('Kode', text='Kode Anggota')
        self.tree.heading('Nama', text='Nama')
        self.tree.heading('Alamat', text='Alamat')
        self.tree.heading('Telepon', text='Telepon')
        self.tree.heading('Email', text='Email')
        
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Kode', width=120, anchor='center')
        self.tree.column('Nama', width=180)
        self.tree.column('Alamat', width=250)
        self.tree.column('Telepon', width=120, anchor='center')
        self.tree.column('Email', width=200)
        
        self.tree.pack(fill='both', expand=True)
        
        # Bind select
        self.tree.bind('<ButtonRelease-1>', self.select_item)
    
    # **PERBAIKAN/PENAMBAHAN: Fungsi validasi, CRUD, Load, dan Select**
    def validate_email(self, email):
        """Validasi format email"""
        # Pola regex untuk validasi email sederhana
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$' 
        return re.fullmatch(pattern, email)

    def validate_input(self):
        """Validasi input form anggota"""
        kode = self.kode_entry.get().strip()
        nama = self.nama_entry.get().strip()
        alamat = self.alamat_entry.get().strip()
        telepon = self.telepon_entry.get().strip()
        email = self.email_entry.get().strip()
        
        if not all([kode, nama, alamat, telepon, email]):
            messagebox.showwarning("Peringatan", "Semua field harus diisi!")
            return False
        
        # Validasi format telepon (hanya angka)
        if not telepon.isdigit() or len(telepon) < 8:
            messagebox.showwarning("Peringatan", "Nomor telepon tidak valid!")
            return False
            
        # Validasi format email
        if not self.validate_email(email):
            messagebox.showwarning("Peringatan", "Format email tidak valid!")
            return False
        
        return True
    
    def add_anggota(self):
        """Menambah anggota baru"""
        if not self.validate_input():
            return
        
        connection = DatabaseConnection.create_connection()
        if not connection:
            return
        
        try:
            cursor = connection.cursor()
            query = """INSERT INTO anggota (kode_anggota, nama, alamat, telepon, email) 
                       VALUES (%s, %s, %s, %s, %s)"""
            values = (
                self.kode_entry.get().strip(),
                self.nama_entry.get().strip(),
                self.alamat_entry.get().strip(),
                self.telepon_entry.get().strip(),
                self.email_entry.get().strip()
            )
            
            cursor.execute(query, values)
            connection.commit()
            
            messagebox.showinfo("Sukses", "Anggota berhasil ditambahkan!")
            self.clear_form()
            self.load_data()
        
        except Error as e:
            if 'Duplicate entry' in str(e):
                messagebox.showerror("Error", "Kode anggota sudah ada!")
            else:
                messagebox.showerror("Error Database", f"Gagal menambah anggota:\n{str(e)}")
        
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def update_anggota(self):
        """Mengupdate data anggota yang dipilih"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih anggota yang akan diupdate!")
            return
        
        if not self.validate_input():
            return
            
        item = self.tree.item(selected[0])
        anggota_id = item['values'][0]

        connection = DatabaseConnection.create_connection()
        if not connection:
            return
        
        try:
            cursor = connection.cursor()
            query = """UPDATE anggota SET kode_anggota=%s, nama=%s, alamat=%s, 
                       telepon=%s, email=%s WHERE id=%s"""
            values = (
                self.kode_entry.get().strip(),
                self.nama_entry.get().strip(),
                self.alamat_entry.get().strip(),
                self.telepon_entry.get().strip(),
                self.email_entry.get().strip(),
                anggota_id
            )
            
            cursor.execute(query, values)
            connection.commit()
            
            messagebox.showinfo("Sukses", f"Anggota ID {anggota_id} berhasil diupdate!")
            self.clear_form()
            self.load_data()
            
        except Error as e:
            if 'Duplicate entry' in str(e):
                messagebox.showerror("Error", "Kode anggota sudah ada!")
            else:
                messagebox.showerror("Error Database", f"Gagal mengupdate anggota:\n{str(e)}")
        
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def delete_anggota(self):
        """Hapus data anggota"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih anggota yang akan dihapus!")
            return
        
        if not messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus anggota ini?"):
            return
        
        connection = DatabaseConnection.create_connection()
        if not connection:
            return
        
        try:
            item = self.tree.item(selected[0])
            anggota_id = item['values'][0]
            
            cursor = connection.cursor()
            cursor.execute("DELETE FROM anggota WHERE id = %s", (anggota_id,))
            connection.commit()
            
            messagebox.showinfo("Sukses", "Anggota berhasil dihapus!")
            self.clear_form()
            self.load_data()
        
        except Error as e:
            messagebox.showerror("Error", f"Gagal menghapus anggota:\n{str(e)}")
        
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
    
    def load_data(self):
        """Memuat data anggota dari database"""
        connection = DatabaseConnection.create_connection()
        if not connection:
            return
        
        try:
            # Clear existing data
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM anggota ORDER BY id DESC")
            rows = cursor.fetchall()
            
            for row in rows:
                self.tree.insert('', 'end', values=row)
        
        except Error as e:
            messagebox.showerror("Error", f"Gagal memuat data anggota:\n{str(e)}")
        
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def search_anggota(self):
        """Mencari anggota berdasarkan nama atau kode"""
        search_term = self.search_entry.get().strip()
        
        connection = DatabaseConnection.create_connection()
        if not connection:
            return
        
        try:
            # Clear existing data
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            cursor = connection.cursor()
            query = """SELECT * FROM anggota 
                       WHERE nama LIKE %s OR kode_anggota LIKE %s 
                       ORDER BY id DESC"""
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern))
            rows = cursor.fetchall()
            
            for row in rows:
                self.tree.insert('', 'end', values=row)
        
        except Error as e:
            messagebox.showerror("Error", f"Gagal mencari data anggota:\n{str(e)}")
        
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def select_item(self, event):
        """Mengisi form saat item dipilih"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item['values']
            
            self.clear_form()
            self.kode_entry.insert(0, values[1])
            self.nama_entry.insert(0, values[2])
            self.alamat_entry.insert(0, values[3])
            self.telepon_entry.insert(0, values[4])
            self.email_entry.insert(0, values[5])
    
    def clear_form(self):
        """Membersihkan form"""
        self.kode_entry.delete(0, tk.END)
        self.nama_entry.delete(0, tk.END)
        self.alamat_entry.delete(0, tk.END)
        self.telepon_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
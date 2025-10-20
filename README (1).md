# Aplikasi Perpustakaan (Tkinter + MySQL)

**Isi File:**
- `database_setup.sql` — Membuat database dan tabel.
- `perpustakaan_app.py` — Aplikasi utama GUI dengan Tkinter.
- `README.md` — Petunjuk penggunaan.

## Persiapan
1. Jalankan MySQL lokal (`127.0.0.1`) dengan user `root` tanpa password.
2. Import database:
   ```bash
   mysql -u root < database_setup.sql
   ```
3. Install dependency:
   ```bash
   pip install mysql-connector-python
   ```
4. Jalankan aplikasi:
   ```bash
   python perpustakaan_app.py
   ```
5. Login:
   - Username: `admin`
   - Password: `admin123`

   ![alt text](image.png)
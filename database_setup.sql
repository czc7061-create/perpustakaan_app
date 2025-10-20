CREATE DATABASE IF NOT EXISTS perpustakaan_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE perpustakaan_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role ENUM('admin', 'petugas') DEFAULT 'petugas',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS buku (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kode_buku VARCHAR(20) UNIQUE NOT NULL,
    judul VARCHAR(200) NOT NULL,
    pengarang VARCHAR(100) NOT NULL,
    penerbit VARCHAR(100) NOT NULL,
    tahun_terbit INT NOT NULL,
    stok INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS anggota (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kode_anggota VARCHAR(20) UNIQUE NOT NULL,
    nama VARCHAR(100) NOT NULL,
    alamat TEXT NOT NULL,
    telepon VARCHAR(15) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT IGNORE INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin');
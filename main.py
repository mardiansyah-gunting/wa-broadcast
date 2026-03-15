from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import urllib.parse
import time
import os

load_dotenv()
BASE_URL = os.getenv("WA_BASE_URL")
if not BASE_URL or not BASE_URL.strip():
    print("Set WA_BASE_URL in your .env file. See .env.example.")
    exit(1)
BASE_URL = BASE_URL.rstrip("/")

# --- 1. MEMBACA FILE NOMOR ---
file_nomor = "nomor_kontak.txt"
file_pesan = "pesan.txt"
daftar_kontak = []

if not os.path.exists(file_nomor):
    # Buat file contoh jika belum ada
    with open(file_nomor, "w") as f:
        f.write("# Masukkan nomor di sini, satu nomor per baris\n")
        f.write("# Contoh: 08123456789 atau 628123456789\n")
    print(f"📝 File '{file_nomor}' telah dibuat. Silakan isi daftar nomor kontak di sana.")
    exit()

with open(file_nomor, "r") as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        
        # Bersihkan nomor
        if line.startswith("+"):
            nomor_final = line[1:]
        elif line.startswith("0"):
            nomor_final = "62" + line[1:]
        else:
            nomor_final = line
            
        daftar_kontak.append(nomor_final)

if not daftar_kontak:
    print(f"⚠️ Tidak ada nomor kontak yang ditemukan di '{file_nomor}'.")
    exit()

print(f"✅ Berhasil memuat {len(daftar_kontak)} nomor.")

# --- 2. MEMBACA FILE PESAN ---
if not os.path.exists(file_pesan):
    with open(file_pesan, "w", encoding="utf-8") as f:
        f.write("Halo! Ini adalah pesan otomatis dari WhatsApp Broadcast Tool.")
    print(f"📝 File '{file_pesan}' telah dibuat dengan pesan default.")

with open(file_pesan, "r", encoding="utf-8") as f:
    pesan_asli = f.read()

if not pesan_asli.strip():
    print(f"⚠️ Pesan di '{file_pesan}' kosong.")
    exit()

# Encode pesan agar bisa masuk ke URL
pesan_encoded = urllib.parse.quote(pesan_asli)

# --- 3. SETUP BROWSER (SELENIUM) ---
print("⚙️ Membuka Browser...")
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# Optional: simpan session agar tidak perlu scan QR setiap kali (butuh path profile)
# options.add_argument("--user-data-dir=./user_data") 

# Inisialisasi Driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 30)

# Buka WA Web
driver.get(BASE_URL)
print("Scan the QR code when prompted, then return here.")
input("Press Enter here once you are logged in and the chat list is visible...")

# --- 4. EKSEKUSI PENGIRIMAN ---
print("🚀 Memulai pengiriman satu per satu...")

for nomor in daftar_kontak:
    try:
        print(f"🔄 Memproses ke: {nomor}")

        # Buka chat spesifik
        url = f"{BASE_URL}/send?phone={nomor}&text={pesan_encoded}"
        driver.get(url)

        try:
            # Tunggu tombol send (ikon pesawat kertas) bisa diklik
            send_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]')))
            time.sleep(1)  # Jeda natural
            send_button.click()

            print(f"✅ Terkirim ke {nomor}")
            time.sleep(6)  # Jeda anti-ban

        except Exception as e:
            print(f"⚠️ Gagal mengirim ke {nomor}. Mungkin nomor tidak terdaftar atau koneksi lambat.")
            time.sleep(2)

    except Exception as e:
        print(f"❌ Error sistem pada {nomor}: {e}")

print("🏁 Selesai! Browser akan tertutup dalam 5 detik.")
time.sleep(5)
driver.quit()
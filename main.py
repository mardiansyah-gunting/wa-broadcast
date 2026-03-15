from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import urllib.parse
import time
import os

# --- 1. MEMBACA FILE NOMOR ---
nama_file = "nomor_kontak.txt"
daftar_kontak = []

if os.path.exists(nama_file):
    with open(nama_file, "r") as file:
        lines = file.readlines()
        for line in lines:
            nomor_bersih = line.strip()
            if nomor_bersih:
                # Pastikan format angka saja, buang + jika ada untuk diproses selenium nanti
                # Tapi untuk URL whatsapp, format internasional tanpa '+' lebih aman kadang,
                # namun format standar internasional (628xxx) paling aman.
                if nomor_bersih.startswith("+"):
                    nomor_final = nomor_bersih[1:]  # Buang tanda +
                elif nomor_bersih.startswith("0"):
                    nomor_final = "62" + nomor_bersih[1:]  # Ubah 08 jadi 628
                else:
                    nomor_final = nomor_bersih

                daftar_kontak.append(nomor_final)
    print(f"✅ Berhasil memuat {len(daftar_kontak)} nomor.")
else:
    print(f"❌ Error: File '{nama_file}' tidak ditemukan.")
    exit()

# --- 2. PESAN (Dikonversi agar aman di URL) ---
pesan_asli = """Halo teman-teman dan rekan semua,

Saya ingin mengabarkan bahwa HP saya hilang/kecopetan minggu lalu.

Karena sebelumnya saya menggunakan fitur WhatsApp Cloning untuk nomor lama (+62 812-5008-8282) di HP tersebut, saat ini aksesnya sudah tidak saya pegang lagi. Demi keamanan, mohon abaikan dan blokir jika ada pesan dari nomor lama tersebut.

Untuk komunikasi ke depannya, silakan hubungi saya melalui nomor ini saja. Mohon maaf atas ketidaknyamanan ini dan terima kasih!

---

Hi everyone,

I’m writing to let you know that my phone was stolen last week.

Since I was using a WhatsApp Cloning setup for my old number (+62 812-5008-8282) on that device, I no longer have secure access to it. For your safety, please ignore and block any messages coming from that old number.

Please use this current number for all future communication. Apologies for the inconvenience and thank you!

---

大家好，

想告知大家，我的手机在上周不幸遗失/被盗。

由于我之前在该手机上使用了旧号码 (+62 812-5008-8282) 的WhatsApp克隆/分身功能，为了安全起见，该旧号码已停止使用。

若收到该旧号码发来的任何信息，请直接忽略并拉黑。今后请通过这个新号码联系我。造成不便，敬请见谅。谢谢大家！"""

# Encode pesan agar bisa masuk ke URL (mengubah spasi jadi %20, enter jadi %0A, dll)
pesan_encoded = urllib.parse.quote(pesan_asli)

# --- 3. SETUP BROWSER (SELENIUM) ---
print("⚙️ Membuka Browser...")
options = webdriver.ChromeOptions()
# options.add_argument("--headless") # Jangan nyalakan ini karena kita perlu scan QR
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Inisialisasi Driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 30)

# Buka WA Web
driver.get("https://web.whatsapp.com")
print("⚠️ SILAKAN SCAN QR CODE WHATSAPP ANDA SEKARANG!")
input("👉 Tekan tombol ENTER di sini jika sudah berhasil login dan chat terbuka...")

# --- 4. EKSEKUSI PENGIRIMAN ---
print("🚀 Memulai pengiriman satu per satu...")

for nomor in daftar_kontak:
    try:
        print(f"🔄 Memproses ke: {nomor}")

        # Buka chat spesifik di tab yang SAMA
        url = f"https://web.whatsapp.com/send?phone={nomor}&text={pesan_encoded}"
        driver.get(url)

        # Tunggu sampai tombol kirim muncul (maksimal 20 detik)
        # Kita cari tombol dengan icon 'send' atau tombol enter
        try:
            # Cara 1: Tunggu tombol send (ikon pesawat kertas) bisa diklik
            send_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]')))
            time.sleep(1)  # Jeda dikit biar natural
            send_button.click()

            print(f"✅ Terkirim ke {nomor}")

            # Jeda antar pesan (PENTING: Jangan terlalu cepat atau WA akan memblokir sementara)
            time.sleep(6)

        except Exception as e:
            # Jika tombol send tidak muncul, mungkin nomor salah atau internet lemot
            print(f"⚠️ Gagal menemukan tombol kirim untuk {nomor}. Mungkin nomor tidak terdaftar WA? Error: {e}")
            time.sleep(2)

    except Exception as e:
        print(f"❌ Error sistem pada {nomor}: {e}")

print("🏁 Selesai! Browser akan tertutup dalam 5 detik.")
time.sleep(5)
driver.quit()
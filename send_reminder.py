import os
import json
import sys
import urllib.request
import urllib.error

# ==========================================
# 1. ISI TEXT REMINDER (DENGAN MENTION ALL)
# ==========================================

# Pengingat 1: SOP Operasional
MESSAGE_SOP = """ ⏰ Trand ZT/ SP:

1. Masih banyak ditemukan finding ZT Proper content Call beck Date kurang dari +4 hari.
2. Pastikan penginputan tanggal CBD itu +4 hari dan terhitung hari pertama di esok hari.
3. Pastikan CBL +3 hari untuk case EC confirm yg ada indikasi HC, WPWN.
4. Pastikan setelah tanggal sesuai perintah BAIK di klik agar tidak terinput otomatis CBD di esok hari.
5. Masih banyak ditemukan finding ZT FAKE PTP prolong lebih dari lusa.
6. Penginputan tanggal pastikan maksimal lusa ya, terhitung dari hari awal call.
7. Double check sebelum submit CWU, pastikan semua tanggal sesuai, baik itu yg berhubungan dengan PTP atau dengan CBD.
8. Selalu edukasi hubungi CS untuk case Hard Complaint, WPWN, Suspect Fraud, Recycle Number.
9. Untuk Register atau P1 terdapat case Suspect Fraud dan Recycle Number, tambahan edukasi user memiliki tagihan SPayLater atau SPinjam.
"""

# Pengingat 2: Kedisiplinan & Rutinitas
MESSAGE_ABSEN = """ ⏰ Reminder Harian Team:

- Jangan lupa absen login dan logout perhari
- Kumpulin Hp jangan lupa 
- Tinggalin row wajib izin TL row 
- Stay fokus until EOS 
- Bisa disambi spam idle bussy 
- Atribut lanyard selalu dipakai diarea kantor
"""

# Pengingat 3: Strategi Harian (Daily Strategy)
MESSAGE_STRATEGI = """ 💡 Strategi daily :

1. Register 100 K 
2. Mainkan amount LM terlebih dahulu sampai jam 10 pagi 
3. Setelah amount aman baru mulai kejar account star dari jam 10 sampai EOS 
4. LM ikut aliran data yg banyak di tangga kalian masuk 
5. Pengulan untuk tagihan kecil LM atau dibawah pickian kalian cukup 1 kali ( hanya mandatori tipsan 1 kali )
6. pengulangan LM big amount bisa 2 sampai 3 kali atau kejar konversi amountnya 
7. Wajib diambil jangan dibuang buang datanya 
8. HU atau MV di input setelah waktunya 6 detik ya 
9. untuk strategi yg siang dan jika ada perubahan strategi aku bakal send manual
"""


# ==========================================
# 2. FUNGSI UTAMA PENGIRIMAN
# ==========================================

def send_seatalk_reminder(message_content):
    webhook_url = os.environ.get("SEATALK_WEBHOOK_URL")

    if not webhook_url:
        raise RuntimeError(
            "SEATALK_WEBHOOK_URL tidak ditemukan. "
            "Pastikan sudah diset di GitHub Actions Secret."
        )

    # Ganti tag teks biasa menjadi format text dengan dukungan mention
    payload = {
        "tag": "text",
        "text": {
            "content": message_content,
            "at_all": True  # Parameter tambahan untuk memastikan mention all aktif di SeaTalk
        }
    }

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        webhook_url,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )

    print("Sending message to SeaTalk...")

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            status = response.status
            response_body = response.read().decode("utf-8")

            print(f"HTTP Status Code: {status}")
            print(f"SeaTalk Response: {response_body}")

            if 200 <= status < 300:
                print("✅ Pesan berhasil dikirim ke SeaTalk.")
            else:
                raise RuntimeError(
                    f"SeaTalk mengembalikan HTTP status {status}: {response_body}"
                )

    except urllib.error.HTTPError as error:
        response_body = error.read().decode("utf-8", errors="replace")
        print(f"❌ HTTP Error: {error.code}")
        print(f"SeaTalk Response: {response_body}")
        raise

    except urllib.error.URLError as error:
        print(f"❌ URL Error: {error.reason}")
        raise

    except Exception as error:
        print(f"❌ Execution Error: {repr(error)}")
        raise


# ==========================================
# 3. ALUR GERBANG UTAMA (CLI ARGUMENTS)
# ==========================================

if __name__ == "__main__":
    argument = sys.argv[1].lower() if len(sys.argv) > 1 else "sop"

    if argument == "absen":
        print("Mengeksekusi Reminder Ke-2 (Kedisiplinan & Absen)...")
        send_seatalk_reminder(MESSAGE_ABSEN)
    elif argument == "strategi":
        print("Mengeksekusi Reminder Ke-3 (Strategi Daily)...")
        send_seatalk_reminder(MESSAGE_STRATEGI)
    elif argument == "sop":
        print("Mengeksekusi Reminder Ke-1 (SOP Operasional)...")
        send_seatalk_reminder(MESSAGE_SOP)
    else:
        print(f"⚠️ Argumen '{argument}' tidak dikenal. Pilih 'sop', 'absen', atau 'strategi'.")
        sys.exit(1)

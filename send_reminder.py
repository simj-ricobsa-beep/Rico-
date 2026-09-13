import os
import json
import urllib.request
import urllib.error


def send_seatalk_reminder():
    webhook_url = os.environ.get("SEATALK_WEBHOOK_URL")

    if not webhook_url:
        raise RuntimeError(
            "SEATALK_WEBHOOK_URL tidak ditemukan. "
            "Pastikan sudah diset sebagai GitHub Actions Secret."
        )

    message = """⏰ Trand ZT/ SP:

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

    payload = {
        "tag": "text",
        "text": {
            "content": message
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


if __name__ == "__main__":
    send_seatalk_reminder()

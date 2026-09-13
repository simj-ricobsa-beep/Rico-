import os
import json
import urllib.request

def send_seatalk_reminder():
    webhook_url = os.environ.get("SEATALK_WEBHOOK_URL")
    if not webhook_url:
        print("Error: SEATALK_WEBHOOK_URL environment variable is missing.")
        return

    # Use a clean, universally accepted text payload structure
    payload = {
        "tag": "text",
        "text": {
            "content": "⏰ Trand ZT/ SP  :
1. Masih banyak ditemukan finding ZT Proper content Call beck Date kurang dari +4 hari
2. Pastikan penginputan tanggal CBD itu +4 hari dan terhitung hari pertama di esok hari 
3. Pastikan CBL +3 hari untuk case EC confirm yg ada indikasi HC, WPWN
4. Pastikan setelah tanggal sesuai printah BAIK di klik agar tidak terimput otomatis CBD di esok hari  
5. Masih banyak ditemukan finding ZT FAKE PTP prolong lebih dari lusa 
6. penginpuntan tanggal pastikan maksimal lusa ya terhitung dari hari awal call 
7. double cek sebelum submit CWU pastikan semua tanggal sesuai baik itu yg berhubungan dengan PTP atau dengan CBD 
8. Selalu edukasi hubungi CS untuk case Hard complain, WPWN, Suspect Froud, Recycle Number 
9. Untuk Register atau P1 terdapat case Suspect Froud dan Recycle number tambahan edukasi user memiliki tagihan Spaylater atau Spinjam 
  "
        }
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        webhook_url, 
        data=data, 
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            response_body = response.read().decode('utf-8')
            
            print(f"HTTP Status Code: {status}")
            print(f"SeaTalk Server Response: {response_body}")
            
            # Most chat APIs return JSON response error codes here
            if status == 200:
                print("Webhook connection completed successfully.")
    except Exception as e:
        print(f"An execution error occurred: {e}")

if __name__ == "__main__":
    send_seatalk_reminder()

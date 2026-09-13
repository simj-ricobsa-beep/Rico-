# 1. Kirim Strategi Harian jam 07:15 Pagi WIB (Sebelum mulai mainkan amount LM)
15 7 * * 1-5 SEATALK_WEBHOOK_URL="isi_url" /usr/bin/python3 /path/ke/send_reminder.py strategi >> /path/ke/cron_strategi.log 2>&1

# 2. Kirim Reminder Absen & Atribut kantor jam 07:45 Pagi WIB
45 7 * * 1-5 SEATALK_WEBHOOK_URL="isi_url" /usr/bin/python3 /path/ke/send_reminder.py absen >> /path/ke/cron_absen.log 2>&1

# 3. Kirim SOP Temuan ZT/SP jam 09:00 Pagi WIB
0 9 * * 1-5 SEATALK_WEBHOOK_URL="isi_url" /usr/bin/python3 /path/ke/send_reminder.py sop >> /path/ke/cron_sop.log 2>&1

# 4. Kirim ulang Reminder Absen jam 17:05 Sore WIB (Pengingat Absen Logout / EOS)
5 17 * * 1-5 SEATALK_WEBHOOK_URL="isi_url" /usr/bin/python3 /path/ke/send_reminder.py absen >> /path/ke/cron_absen.log 2>&1

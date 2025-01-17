import firebase_admin
from firebase_admin import credentials, db
from pyModbusTCP.client import ModbusClient
import time

# Firebase ayarları
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "Firebase Adress"
})

# PLC bağlantısı için ayarlar
PLC_IP = "192.168.3.250"  # PLC'nin IP adresi
PLC_PORT = 502            # Modbus TCP portu (genellikle 502)
plc_client = ModbusClient(host=PLC_IP, port=PLC_PORT)

# PLC'ye bağlan
if not plc_client.open():
    print("PLC'ye bağlanılamadı. Ayarları kontrol edin.")
    exit()

# Firebase'deki yolu referans alın
firebase_ref = db.reference("relay")

# Firebase'den komutları okuyan fonksiyon
def firebase_listener(event):
    command = event.data  # Firebase'deki yeni veri
    if command == "1":
        print("Röle Açılıyor...")
        plc_client.write_single_coil(0, True)  # Modbus adresi 0'daki coil'i aç
    elif command == "0":
        print("Röle Kapatılıyor...")
        plc_client.write_single_coil(0, False)  # Modbus adresi 0'daki coil'i kapat
    else:
        print(f"Bilinmeyen komut: {command}")

# Firebase'deki değişiklikleri dinle
firebase_ref.listen(firebase_listener)

try:
    print("Firebase dinleniyor, PLC ile iletişim sağlanıyor...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Program sonlandırıldı.")
    
finally:
    plc_client.close()

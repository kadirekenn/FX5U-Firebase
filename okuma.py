import firebase_admin
from firebase_admin import credentials, db
from pyModbusTCP.client import ModbusClient
import time

# Firebase ayarları
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "Firebase URL"
})

# PLC bağlantısı için ayarlar
PLC_IP = "192.168.3.250"  # PLC'nin IP adresi
PLC_PORT = 502            # Modbus TCP portu (genellikle 502)
plc_client = ModbusClient(host=PLC_IP, port=PLC_PORT)

# PLC'ye bağlan
while True:
    if plc_client.open():
        print("FX5U'ya başarıyla bağlanıldı!")

    # Coil 0'ı oku (M0 bitini)
        coil_status = plc_client.read_holding_registers(0, 1)  # Adres 0'dan 1 coil oku
        if coil_status:
            print(f"d0 durumu: {coil_status[0]}")

            # Firebase veritabanına veri yazma
            coil_with = f"{coil_status[0]} "
            ref = db.reference('Anlık Güç')  # Firebase'deki "relay" node'una veri yaz
            ref.set(coil_status[0] )# M0 bitinin durumunu yaz
             
            print("Veri Firebase'e başarıyla yazıldı.")
        else:
            print("Coil okuma hatası oluştu.")
        plc_client.close()
    else:
        print("FX5U'ya bağlanılamadı. IP adresi ve portu kontrol edin.")
    time.sleep(3) 
    
 # 3 saniye bekleme
    # Bağlantıyı kapat

    


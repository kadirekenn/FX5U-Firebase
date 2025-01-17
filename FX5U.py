import firebase_admin
from firebase_admin import credentials, db
from pyModbusTCP.client import ModbusClient
import time

# Firebase başlatma
cred = credentials.Certificate("fx5u.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fx5u-4dcee-default-rtdb.europe-west1.firebasedatabase.app/'
})

# Firebase referansları
relay_ref = db.reference('relay')
analog_value_ref = db.reference('analogValue')

# Modbus bağlantısı
plc_client = ModbusClient(host="192.168.3.250", port=502)

if plc_client.open():
    print("PLC'ye bağlanıldı.")
    while True:
        # Analog değer oku ve Firebase'e yaz
        analog_value = plc_client.read_holding_registers(1000, 1)
        analog_value = analog_value[0]
        print(f"d0 durumu: {analog_value}")
        analog_value_ref.set(analog_value)
     
             

        # Firebase'den relay durumunu oku ve PLC'ye yaz
        relay_status = relay_ref.get()
        if relay_status is not None:
            plc_client.write_single_coil(9, relay_status)  # Örnek: Adres 0

        time.sleep(1)
else:
    print("PLC'ye bağlanılamadı.")

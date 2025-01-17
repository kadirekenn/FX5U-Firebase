from pyModbusTCP.client import ModbusClient

# PLC'nin IP adresi ve Modbus TCP portu
PLC_IP = "192.168.3.250"  # FX5U'nun IP adresini buraya yazın
PLC_PORT = 502            # Varsayılan Modbus TCP portu

# Modbus istemci nesnesi
plc_client = ModbusClient(host=PLC_IP, port=PLC_PORT)

# PLC'ye bağlanmayı dene
if plc_client.open():
    print("FX5U'ya başarıyla bağlanıldı!")

    # Örnek: 0. adresteki bir coil'i (bit) aç
    if plc_client.write_single_coil(0, True):
        print("Röle açıldı (coil 0).")
    else:
        print("Röle açılırken hata oluştu.")

    # Bağlantıyı kapat
    plc_client.close()
else:
    print("FX5U'ya bağlanılamadı. IP adresi ve portu kontrol edin.")

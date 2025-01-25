import firebase_admin
from firebase_admin import credentials, db
from pyModbusTCP.client import ModbusClient
import time
import threading
import tkinter as tk

# Firebase başlatma
cred = credentials.Certificate("fx5u.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fx5u-4dcee-default-rtdb.europe-west1.firebasedatabase.app/'
})

# Firebase referansları
relay_ref = db.reference('relay')
analog_value_ref = db.reference('analogValue')
relay_wr_ref = db.reference('addresses')
analog_value_wr_ref = db.reference('addresses')

# Modbus bağlantısı
plc_client = ModbusClient(host="192.168.3.250", port=502)

# PLC iletişim kontrolü için değişkenler
relay_status = False
coil_address = 9  # Varsayılan coil adresi
register_address = 1000  # Varsayılan register adresi


def get_addresses_from_firebase():
    """Firebase'den coil ve register adreslerini al."""
    global coil_address, register_address
    try:
        coil_address_firebase = relay_wr_ref.child("coilAddress").get()
        register_address_firebase = analog_value_wr_ref.child("analogAddress").get()

        if coil_address_firebase is not None:
            coil_address = int(coil_address_firebase)
            coil_entry.delete(0, tk.END)
            coil_entry.insert(0, str(coil_address))

        if register_address_firebase is not None:
            register_address = int(register_address_firebase)
            register_entry.delete(0, tk.END)
            register_entry.insert(0, str(register_address))

    except Exception as e:
        print(f"Firebase'ten veri alınırken hata oluştu: {e}")


def refresh_addresses():
    """Adresleri Firebase'den alıp güncelle."""
    get_addresses_from_firebase()
    root.after(5000, refresh_addresses)


def update_values():
    """PLC'den analog değeri oku ve Firebase'e yaz."""
    global register_address, coil_address

    if plc_client.open():
        print("PLC'ye bağlanıldı.")
        while True:
            try:
                # Analog değeri oku
                analog_value = plc_client.read_holding_registers(register_address, 1)
                relay_status_firebase = relay_ref.get()
                if analog_value:
                    analog_value_ref.set(analog_value[0])
                    analog_value_label.config(text=f"Analog Değer: {analog_value[0]}")
                    print(f"d{register_address} durumu: {analog_value[0]}")
                else:
                    print(f"d{register_address} okunamadı.")

                # Röle durumunu güncelle
                if relay_status_firebase is not None:
                    relay_status_label.config(text=f"Röle Durumu: {'Açık' if relay_status_firebase else 'Kapalı'}")
                    if plc_client.write_single_coil(coil_address, relay_status_firebase):
                        print(f"Röle Durumu: {'Açık' if relay_status_firebase else 'Kapalı'}")
                else:
                    print("Röle Durumu yazılamadı!")
            except Exception as e:
                print(f"Hata: {e}")

            time.sleep(1)
    else:
        print("PLC'ye bağlanılamadı.")


def toggle_relay():
    """Röle durumunu değiştirir."""
    global relay_status
    relay_status = not relay_status
    relay_ref.set(relay_status)
    if plc_client.write_single_coil(coil_address, relay_status):
        relay_status_label.config(text=f"Röle Durumu: {'Açık' if relay_status else 'Kapalı'}")
        print(f"Röle Durumu: {'Açık' if relay_status else 'Kapalı'}")
    else:
        print("PLC'ye röle durumu yazılamadı!")


def set_addresses():
    """Coil ve register adreslerini kullanıcı girişine göre ayarlar."""
    global coil_address, register_address
    try:
        coil_address = int(coil_entry.get())
        register_address = int(register_entry.get())
        relay_wr_ref.child("coilAddress").set(coil_address)
        analog_value_wr_ref.child("analogAddress").set(register_address)
        print("Adresler başarıyla ayarlandı!")
    except ValueError:
        print("Geçersiz adres girdiniz!")


# Ana pencere oluşturma
root = tk.Tk()
root.title("PLC ve Firebase Kontrol Paneli")
root.geometry("400x500")

# Coil adresi giriş alanı
coil_label = tk.Label(root, text="Coil Adresi:", font=("Arial", 12))
coil_label.pack(pady=5, anchor="w")
coil_entry = tk.Entry(root, font=("Arial", 12))
coil_entry.insert(0, str(coil_address))
coil_entry.pack(pady=5, padx=20, fill=tk.X)

# Register adresi giriş alanı
register_label = tk.Label(root, text="Register Adresi:", font=("Arial", 12))
register_label.pack(pady=5, anchor="w")
register_entry = tk.Entry(root, font=("Arial", 12))
register_entry.insert(0, str(register_address))
register_entry.pack(pady=5, padx=20, fill=tk.X)

# Adresleri ayarla butonu
set_button = tk.Button(root, text="Adresleri Ayarla", font=("Arial", 12), bg="#61afef", fg="#ffffff", command=set_addresses)
set_button.pack(pady=10, ipadx=10, ipady=5)

# Röle aç/kapat butonu
toggle_button = tk.Button(root, text="Röle Aç/Kapat", font=("Arial", 12), bg="#61afef", fg="#ffffff", command=toggle_relay)
toggle_button.pack(pady=10, ipadx=10, ipady=5)

# Analog değer göstergesi
analog_value_label = tk.Label(root, text="Analog Değer: -", font=("Arial", 12))
analog_value_label.pack(pady=10)

# Röle durumu göstergesi
relay_status_label = tk.Label(root, text="Röle Durumu: -", font=("Arial", 12))
relay_status_label.pack(pady=10)

# Çıkış butonu
exit_button = tk.Button(root, text="Çıkış", font=("Arial", 12), bg="#e06c75", fg="#ffffff", command=root.quit)
exit_button.pack(pady=10, ipadx=10, ipady=5)

# GUI döngüsü
root.after(5000, refresh_addresses)
threading.Thread(target=update_values, daemon=True).start()

root.mainloop()

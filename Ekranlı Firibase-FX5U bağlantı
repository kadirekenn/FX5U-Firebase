import firebase_admin
from firebase_admin import credentials, db
from pyModbusTCP.client import ModbusClient
import time
import threading
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from ekranlı_deneme import update_gui  # Resim işlemleri için


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

# Arka plan resmi için yol
logo_path = "logo (1).png"

# PLC iletişim kontrolü için değişkenler
relay_status = False
coil_address = 9  # Varsayılan coil adresi
register_address = 1000  # Varsayılan register adresi


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
                    analog_label.config(text=f"d{register_address} durumu: {analog_value[0]}")
                    
                else:
                    analog_label.config(text=f"d{register_address} okunamadı.")

                # Firebase veya arayüzden alınan coil adresiyle röle durumunu ayarla
                
                if relay_status_firebase is not None:
                    if plc_client.write_single_coil(coil_address, relay_status_firebase):
                        relay_label.config(text=f"Röle Durumu: {'Açık' if relay_status_firebase else 'Kapalı'}")
                else:
                    relay_label.config(text=f"Röle Durumu yazılamadı!")
            except Exception as e:
                print(f"Hata: {e}")

            time.sleep(1)
    else:
        print("PLC'ye bağlanılamadı.")


def toggle_relay():
    """Röle durumunu değiştirir."""
    global relay_status
    relay_status = not relay_status
    relay_ref.set(relay_status)  # Firebase'e yaz
    if plc_client.write_single_coil(9, relay_status):  # PLC'ye yaz
        update_gui(relay_label, f"Röle Durumu: {'Açık' if relay_status else 'Kapalı'}")
       
    else:
        print("PLC'ye röle durumu yazılamadı!")
    
    if relay_status==1:
            print("Röle Açık")
    else: print("Röle Kapalı")



def set_addresses():
    """Coil ve register adreslerini kullanıcı girişine göre ayarlar."""
    global coil_address, register_address
    try:
        coil_address = int(coil_entry.get())
        register_address = int(register_entry.get())
        status_label.config(text="Adresler başarıyla ayarlandı!", fg="green")
    except ValueError:
        status_label.config(text="Geçersiz adres girdiniz!", fg="red")


# Ana pencere oluşturma
root = tk.Tk()
root.title("PLC ve Firebase Kontrol Paneli")
root.geometry("400x400")

# Arka plan resmi
try:
    logo_image = Image.open(logo_path)
    logo_image = logo_image.resize((400, 400))
    background_image = ImageTk.PhotoImage(logo_image)
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    print(f"Arka plan yüklenemedi: {e}")

# Analog değer etiketi
analog_label = tk.Label(root, text="d1000 durumu: Bekleniyor...", font=("Arial", 14), bg="#ffffff", fg="#000000")
analog_label.pack(pady=10, fill=tk.X, padx=20)

# Röle durumu etiketi
relay_label = tk.Label(root, text="Röle Durumu: Bekleniyor...", font=("Arial", 14), bg="#ffffff", fg="#000000")
relay_label.pack(pady=10, fill=tk.X, padx=20)

# Coil adresi giriş alanı
coil_label = tk.Label(root, text="Coil Adresi:", font=("Arial", 12), bg="#ffffff", fg="#000000")
coil_label.pack(pady=5, padx=20, anchor="w")
coil_entry = tk.Entry(root, font=("Arial", 12))
coil_entry.insert(0, str(coil_address))  # Varsayılan coil adresi
coil_entry.pack(pady=5, padx=20, fill=tk.X)

# Register adresi giriş alanı
register_label = tk.Label(root, text="Register Adresi:", font=("Arial", 12), bg="#ffffff", fg="#000000")
register_label.pack(pady=5, padx=20, anchor="w")
register_entry = tk.Entry(root, font=("Arial", 12))
register_entry.insert(0, str(register_address))  # Varsayılan register adresi
register_entry.pack(pady=5, padx=20, fill=tk.X)

# Adresleri ayarla butonu
set_button = tk.Button(root, text="Adresleri Ayarla", font=("Arial", 12), bg="#61afef", fg="#ffffff", command=set_addresses)
set_button.pack(pady=10, ipadx=10, ipady=5)

# Röle aç/kapat butonu
toggle_button = tk.Button(root, text="Röle Aç/Kapat", font=("Arial", 12), bg="#61afef", fg="#ffffff", command=toggle_relay)
toggle_button.pack(pady=10, ipadx=10, ipady=5)

# Durum mesajı etiketi
status_label = tk.Label(root, text="", font=("Arial", 12), bg="#ffffff", fg="#000000")
status_label.pack(pady=10, fill=tk.X, padx=20)

# Çıkış butonu
exit_button = tk.Button(root, text="Çıkış", font=("Arial", 12), bg="#e06c75", fg="#ffffff", command=root.quit)
exit_button.pack(pady=10, ipadx=10, ipady=5)

# PLC'den veri okuma işlemini arka planda başlat
threading.Thread(target=update_values, daemon=True).start()

# GUI döngüsü
root.mainloop()

import tkinter as tk
from tkinter import ttk
import math

# Analog gösterge için bir canvas üzerine çizim yapacağız
def update_gauge(value):
    # Önceki gösterge çizimini temizle
    canvas.delete("needle")
    
    # Göstergeyi güncelle
    angle = math.radians(135 + (value * 2.7))  # 0-100 değerini -135 ile +135 derece arasında çevir
    x = 150 + 100 * math.cos(angle)
    y = 150 - 100 * math.sin(angle)
    
    # İbreyi çiz
    canvas.create_line(150, 150, x, y, width=3, fill="red", tag="needle")
    value_label.config(text=f"Değer: {value}")

# Buton olay işleyici
def button_clicked():
    global value
    value = (value + 10) % 110  # Değeri 10 artır, 100'ü geçerse sıfırla
    update_gauge(value)

# Ana pencere
root = tk.Tk()
root.title("Basit Buton ve Analog Gösterge")

# Buton
button = ttk.Button(root, text="Değeri Artır", command=button_clicked)
button.pack(pady=10)

# Gösterge
canvas = tk.Canvas(root, width=300, height=300, bg="white")
canvas.pack()

# Gösterge çerçevesi çiz
canvas.create_oval(50, 50, 250, 250, width=2)
canvas.create_arc(50, 50, 250, 250, start=45, extent=90, style=tk.ARC, width=2)
canvas.create_text(150, 20, text="Analog Gösterge", font=("Arial", 12))

# Başlangıç değeri
value = 0
value_label = tk.Label(root, text=f"Değer: {value}", font=("Arial", 14))
value_label.pack()

# Başlangıç ibresini göster
update_gauge(value)

# Pencereyi başlat
root.mainloop()

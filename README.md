# 🛑 Akıllı Trafik Işık Kontrol Sistemi
Bu proje, bulanık mantık (fuzzy logic) kullanarak trafik ışıklarının süresini ve öncelik düzeyini belirlemeyi amaçlayan bir Python uygulamasıdır. Kullanıcıdan alınan çeşitli çevresel veriler doğrultusunda, sistem mantıklı kararlar verir. Uygulama, kullanıcı dostu bir **Tkinter GUI** üzerinden çalışır.

# 🔧 Kullanılan Teknolojiler
- Python
- Tkinter (GUI)
- scikit-fuzzy (bulanık mantık motoru)
- matplotlib (grafik çizimi)

# Özellikler

- Kullanıcıdan 5 adet girdi alır:

- Trafik Yoğunluğu (%)

- Yaya Sayısı (%)

- Hava Durumu (%)

- Günün Saati (0–24)

- Acil Durum (0 = Yok, 1 = Var)

- 2 adet çıktı üretir:

- Işık Süresi (10–120 saniye)

- Öncelik Düzeyi (%0–%100)

- 10 adet bulanık kural içerir

- Üyelik fonksiyonlarını grafik olarak görselleştirme

- Kuralları ayrı bir pencerede metin olarak gösterme

# 📁 Dosya İçeriği
1. Gerekli Kütüphanelerin İmport Edilmesi
```python

import tkinter as tk
from tkinter import messagebox, Toplevel, Text, Scrollbar, Spinbox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

```

2. Bulanık Değişkenlerin Tanımlanması
Girdi (antecedent) ve çıktı (consequent) değişkenleri oluşturulur:
```python

traffic_density = ctrl.Antecedent(np.arange(0, 101, 1), 'traffic_density')
pedestrian_count = ctrl.Antecedent(np.arange(0, 101, 1), 'pedestrian_count')
weather_condition = ctrl.Antecedent(np.arange(0, 101, 1), 'weather_condition')
time_of_day = ctrl.Antecedent(np.arange(0, 25, 1), 'time_of_day')
emergency = ctrl.Antecedent(np.arange(0, 2, 1), 'emergency')

green_light_duration = ctrl.Consequent(np.arange(10, 121, 1), 'green_light_duration')
priority_level = ctrl.Consequent(np.arange(0, 101, 1), 'priority_level')

```

3. Üyelik Fonksiyonlarının Tanımlanması
Her değişken için üyelik (membership) fonksiyonları tanımlanır:
```python

traffic_density['low'] = fuzz.trimf(traffic_density.universe, [0, 0, 50])
traffic_density['medium'] = fuzz.trimf(traffic_density.universe, [25, 50, 75])
traffic_density['high'] = fuzz.trimf(traffic_density.universe, [50, 100, 100])
# Diğer değişkenler için de benzer şekilde...

```
4. Bulanık Kuralların Tanımlanması
Sistem, sürücü durumu hakkında karar vermek için kurallara dayanır:
```python

rules = [
    ctrl.Rule(traffic_density['high'] & pedestrian_count['high'], green_light_duration['long']),
    ctrl.Rule(traffic_density['medium'] & pedestrian_count['medium'], green_light_duration['medium']),
    ctrl.Rule(traffic_density['low'] & pedestrian_count['low'], green_light_duration['short']),
    # Diğer kurallar...
]

```

5. Kontrol Sistemi Tanımlanması
```python

system = ctrl.ControlSystem(rules)

```

6. Tkinter Arayüzünün Oluşturulması
Ana pencere yapılandırılır:
```python

pencere = tk.Tk()
pencere.title("Akıllı Trafik Işık Kontrol Sistemi")
pencere.configure(bg="#5f0404")  # Açık gri
pencere.geometry("520x550")

```

7. Arayüz Elemanları (Etiketler ve Kaydırma Çubukları)
Kullanıcının veri girmesi için kaydırma çubukları oluşturulur:
```python

def create_label(text, row):
    # Etiket oluşturur
def create_spinbox(row, from_, to_, increment=1):
    # Kaydırma çubuğu oluşturur

```

Her parametre için kullanıcı giriş alanları:
```python

create_label("Trafik Yoğunluğu (%):", 1)
spin_traffic = create_spinbox(1, 0, 100)
# Diğer parametreler için aynı şekilde...

```

8. Hesaplama Fonksiyonu
Kullanıcıdan alınan girdilerle sistem çalıştırılır ve sonuç gösterilir:
```python

def hesapla():
    try:
        sim = ctrl.ControlSystemSimulation(system, clip_to_bounds=True)
        sim.input['traffic_density'] = int(spin_traffic.get())
        sim.input['pedestrian_count'] = int(spin_pedestrian.get())
        ...
        sonuc = f"Uyarı Düzeyi: %{fuzzy_sim.output['alert_level']:.2f}\n"
        sonuc += f"Mola Önerisi: {'EVET' if fuzzy_sim.output['break_suggestion'] > 0.5 else 'HAYIR'}"
        messagebox.showinfo("Sonuç", sonuc)

```

9. Grafik Gösterimi
Üyelik fonksiyonlarını matplotlib ile gösterir:
```python

def grafik_goster():
    grafik_pencere = Toplevel(pencere)
    grafik_pencere.title("Üyelik Fonksiyonları")
    fig, axs = plt.subplots(3, 3, figsize=(14, 10))
    axs = axs.flatten()
    # Üyelik fonksiyonları çizdirilir

```

10. Kuralların Gösterimi
Kural listesini ayrı bir pencerede metin kutusunda gösterir:
```python

def kurallar_goster():
    pencere_kurallar = Toplevel(pencere)
    pencere_kurallar.title("Kural Listesi")
    metin = Text(pencere_kurallar, wrap='word', width=80, height=20)
    metin.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = Scrollbar(pencere_kurallar, command=metin.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    metin.config(yscrollcommand=scrollbar.set)

```

11. Butonların Oluşturulması
Arayüzün altına işlem butonları yerleştirilir:
```python

def create_button(text, command, row):
    tk.Button(pencere, text=text, command=command, bg="#444", fg="white",
              activebackground="#666", font=("Helvetica", 11), width=30).grid(
              row=row, column=0, columnspan=2, pady=10, padx=20)

```

12. Arayüzün Başlatılması
```python

pencere.mainloop()

```


# 📝 Notlar
Eğer gerekli kütüphaneler yüklü değilse aşağıdaki komutla yüklenebilir:
```python

pip install numpy matplotlib scikit-fuzzy scipy networkx

```
- Arayüz sade tutulmuştur ve sezgiseldir.

# 🚀 Projeyi Çalıştırma
Aşağıdaki adımları takip ederek projeyi bilgisayarınıza indirip çalıştırabilirsiniz:
- Projeyi GitHub'dan klonla
```python

git clone https://github.com/Safvan078/trafik-kontrol-sistemi.git

```
- Proje klasörüne geç
```python

cd trafik-kontrol-sistemi

```

- Programı çalıştır
```python

python main.py

```

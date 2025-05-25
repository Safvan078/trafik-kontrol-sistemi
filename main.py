import tkinter as tk
from tkinter import messagebox, Toplevel, Text, Scrollbar, Spinbox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Fuzzy değişkenler
traffic_density = ctrl.Antecedent(np.arange(0, 101, 1), 'traffic_density')
pedestrian_count = ctrl.Antecedent(np.arange(0, 101, 1), 'pedestrian_count')
weather_condition = ctrl.Antecedent(np.arange(0, 101, 1), 'weather_condition')
time_of_day = ctrl.Antecedent(np.arange(0, 25, 1), 'time_of_day')
emergency = ctrl.Antecedent(np.arange(0, 2, 1), 'emergency')

green_light_duration = ctrl.Consequent(np.arange(10, 121, 1), 'green_light_duration')
priority_level = ctrl.Consequent(np.arange(0, 101, 1), 'priority_level')

# Üyelik fonksiyonları
traffic_density['low'] = fuzz.trimf(traffic_density.universe, [0, 0, 50])
traffic_density['medium'] = fuzz.trimf(traffic_density.universe, [25, 50, 75])
traffic_density['high'] = fuzz.trimf(traffic_density.universe, [50, 100, 100])

pedestrian_count['low'] = fuzz.trimf(pedestrian_count.universe, [0, 0, 50])
pedestrian_count['medium'] = fuzz.trimf(pedestrian_count.universe, [25, 50, 75])
pedestrian_count['high'] = fuzz.trimf(pedestrian_count.universe, [50, 100, 100])

weather_condition['bad'] = fuzz.trimf(weather_condition.universe, [0, 0, 50])
weather_condition['moderate'] = fuzz.trimf(weather_condition.universe, [25, 50, 75])
weather_condition['good'] = fuzz.trimf(weather_condition.universe, [50, 100, 100])

time_of_day['morning'] = fuzz.trimf(time_of_day.universe, [0, 0, 12])
time_of_day['noon'] = fuzz.trimf(time_of_day.universe, [8, 12, 16])
time_of_day['evening'] = fuzz.trimf(time_of_day.universe, [12, 24, 24])

emergency['no'] = fuzz.trimf(emergency.universe, [0, 0, 1])
emergency['yes'] = fuzz.trimf(emergency.universe, [0, 1, 1])

green_light_duration['short'] = fuzz.trimf(green_light_duration.universe, [10, 10, 60])
green_light_duration['medium'] = fuzz.trimf(green_light_duration.universe, [40, 65, 90])
green_light_duration['long'] = fuzz.trimf(green_light_duration.universe, [70, 120, 120])

priority_level['low'] = fuzz.trimf(priority_level.universe, [0, 0, 50])
priority_level['medium'] = fuzz.trimf(priority_level.universe, [25, 50, 75])
priority_level['high'] = fuzz.trimf(priority_level.universe, [50, 100, 100])

# Kurallar
rules = [
    ctrl.Rule(traffic_density['high'] & pedestrian_count['high'], green_light_duration['long']),
    ctrl.Rule(traffic_density['medium'] & pedestrian_count['medium'], green_light_duration['medium']),
    ctrl.Rule(traffic_density['low'] & pedestrian_count['low'], green_light_duration['short']),
    ctrl.Rule(emergency['yes'], priority_level['high']),
    ctrl.Rule(emergency['no'] & traffic_density['low'], priority_level['low']),
    ctrl.Rule(weather_condition['bad'] & time_of_day['morning'], green_light_duration['long']),
    ctrl.Rule(weather_condition['good'] & traffic_density['low'], green_light_duration['short']),
    ctrl.Rule(time_of_day['noon'], priority_level['medium']),
    ctrl.Rule(pedestrian_count['high'], priority_level['high']),
    ctrl.Rule(traffic_density['high'], priority_level['high']),
]

system = ctrl.ControlSystem(rules)

# GUI
pencere = tk.Tk()
pencere.title("Akıllı Trafik Işık Kontrol Sistemi")
pencere.configure(bg="#5f0404")  # Açık gri
pencere.geometry("520x550")

baslik = tk.Label(pencere, text="Akıllı Trafik Işık Kontrol Sistemi",
                  font=("Helvetica", 16, "bold"), bg="#ffef5b", fg="#222")
baslik.grid(row=0, column=0, columnspan=2, pady=(20, 10))

def create_label(text, row):
    tk.Label(pencere, text=text, bg="#ffef5b", fg="#222",
             font=("Helvetica", 11)).grid(row=row, column=0, padx=10, pady=10, sticky="e")

def create_spinbox(row, from_, to_, increment=1):
    spin = Spinbox(pencere, from_=from_, to=to_, increment=increment, width=10,
                   font=("Helvetica", 11), bg="#ffef5b", fg="#000000",
                   highlightthickness=1, relief="solid", borderwidth=1)
    spin.grid(row=row, column=1, padx=10, pady=10, sticky="w")
    return spin

create_label("Trafik Yoğunluğu (%):", 1)
spin_traffic = create_spinbox(1, 0, 100)

create_label("Yaya Sayısı (%):", 2)
spin_pedestrian = create_spinbox(2, 0, 100)

create_label("Hava Durumu (%):", 3)
spin_weather = create_spinbox(3, 0, 100)

create_label("Günün Saati (0-24):", 4)
spin_time = create_spinbox(4, 0, 24)

create_label("Acil Durum (0=Yok, 1=Var):", 5)
spin_emergency = create_spinbox(5, 0, 1)

def hesapla():
    try:
        sim = ctrl.ControlSystemSimulation(system, clip_to_bounds=True)
        sim.input['traffic_density'] = int(spin_traffic.get())
        sim.input['pedestrian_count'] = int(spin_pedestrian.get())
        sim.input['weather_condition'] = int(spin_weather.get())
        sim.input['time_of_day'] = int(spin_time.get())
        sim.input['emergency'] = int(spin_emergency.get())
        sim.compute()
        sonuc = f"Işık Süresi: {sim.output['green_light_duration']:.1f} saniye\n"
        sonuc += f"Öncelik Düzeyi: %{sim.output['priority_level']:.1f}"
        messagebox.showinfo("Sonuç", sonuc)
    except Exception as e:
        messagebox.showerror("Hata", f"Hata oluştu:\n{str(e)}")

def grafik_goster():
    grafik_pencere = Toplevel(pencere)
    grafik_pencere.title("Üyelik Fonksiyonları")
    fig, axs = plt.subplots(3, 3, figsize=(14, 10))
    axs = axs.flatten()

    variables = [
        (traffic_density, "Trafik Yoğunluğu"),
        (pedestrian_count, "Yaya Sayısı"),
        (weather_condition, "Hava Durumu"),
        (time_of_day, "Günün Saati"),
        (emergency, "Acil Durum"),
        (green_light_duration, "Işık Süresi"),
        (priority_level, "Öncelik Düzeyi")
    ]

    for i, (var, title) in enumerate(variables):
        ax = axs[i]
        for term, mf in var.terms.items():
            ax.plot(var.universe, mf.mf, label=term)
        ax.set_title(title)
        ax.set_xlabel("Değerler")
        ax.set_ylabel("Üyelik")
        ax.legend()
        ax.grid(True)

    for j in range(len(variables), len(axs)):
        fig.delaxes(axs[j])

    plt.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=grafik_pencere)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def kurallar_goster():
    pencere_kurallar = Toplevel(pencere)
    pencere_kurallar.title("Kural Listesi")
    metin = Text(pencere_kurallar, wrap='word', width=80, height=20)
    metin.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = Scrollbar(pencere_kurallar, command=metin.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    metin.config(yscrollcommand=scrollbar.set)

    for i, rule in enumerate(rules):
        metin.insert(tk.END, f"Kural {i + 1}: {rule}\n\n")

def create_button(text, command, row):
    tk.Button(pencere, text=text, command=command, bg="#444", fg="white",
              activebackground="#666", font=("Helvetica", 11), width=30).grid(
              row=row, column=0, columnspan=2, pady=10, padx=20)

create_button("Hesapla", hesapla, 6)
create_button("Grafikleri Göster", grafik_goster, 7)
create_button("Kuralları Göster", kurallar_goster, 8)

pencere.mainloop()

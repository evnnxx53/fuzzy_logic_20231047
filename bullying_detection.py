import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# --- 1. SETUP VARIABEL ---
# Resolusi ditingkatkan (step 0.1) agar grafik trapesium terlihat halus
absen = ctrl.Antecedent(np.arange(0, 4.1, 0.1), 'absen')
interaksi = ctrl.Antecedent(np.arange(0, 4.1, 0.1), 'interaksi')
prestasi = ctrl.Antecedent(np.arange(0, 4.1, 0.1), 'prestasi')
risiko = ctrl.Consequent(np.arange(0, 4.1, 0.1), 'risiko')

# --- 2. FUNGSI KEANGGOTAAN (TRAPESIUM MURNI) ---

# --- Variabel ABSEN ---
# Rendah (1): Datar dari 0 sampai 1.2
absen['rendah'] = fuzz.trapmf(absen.universe, [0, 0, 1.2, 1.8])
# Sedang (2): Datar dari 1.8 sampai 2.2
absen['sedang'] = fuzz.trapmf(absen.universe, [1.2, 1.8, 2.2, 2.8])
# Tinggi (3): Datar dari 2.8 sampai 4
absen['tinggi'] = fuzz.trapmf(absen.universe, [2.2, 2.8, 4, 4])

# --- Variabel INTERAKSI ---
interaksi['aktif']  = fuzz.trapmf(interaksi.universe, [0, 0, 1.2, 1.8])
interaksi['normal'] = fuzz.trapmf(interaksi.universe, [1.2, 1.8, 2.2, 2.8])
interaksi['pasif']  = fuzz.trapmf(interaksi.universe, [2.2, 2.8, 4, 4])

# --- Variabel PRESTASI ---
prestasi['tinggi'] = fuzz.trapmf(prestasi.universe, [0, 0, 1.2, 1.8])
prestasi['sedang'] = fuzz.trapmf(prestasi.universe, [1.2, 1.8, 2.2, 2.8])
prestasi['rendah'] = fuzz.trapmf(prestasi.universe, [2.2, 2.8, 4, 4])

# --- Output RISIKO ---
risiko['rendah'] = fuzz.trapmf(risiko.universe, [0, 0, 1.2, 1.8])
risiko['sedang'] = fuzz.trapmf(risiko.universe, [1.2, 1.8, 2.2, 2.8])
risiko['tinggi'] = fuzz.trapmf(risiko.universe, [2.2, 2.8, 4, 4])


rule1 = ctrl.Rule(absen['rendah'] & interaksi['aktif'] & prestasi['tinggi'], risiko['rendah'])
rule2 = ctrl.Rule(absen['rendah'] & interaksi['aktif'] & prestasi['sedang'], risiko['rendah'])
rule3 = ctrl.Rule(absen['rendah'] & interaksi['aktif'] & prestasi['rendah'], risiko['rendah']) 
rule4 = ctrl.Rule(absen['rendah'] & interaksi['normal'] & prestasi['tinggi'], risiko['rendah'])
rule5 = ctrl.Rule(absen['rendah'] & interaksi['normal'] & prestasi['sedang'], risiko['rendah'])
rule6 = ctrl.Rule(absen['rendah'] & interaksi['pasif'] & prestasi['tinggi'], risiko['rendah']) 
rule7 = ctrl.Rule(absen['sedang'] & interaksi['aktif'] & prestasi['tinggi'], risiko['rendah'])
rule8 = ctrl.Rule(absen['sedang'] & interaksi['aktif'] & prestasi['sedang'], risiko['rendah'])
rule9 = ctrl.Rule(absen['sedang'] & interaksi['normal'] & prestasi['tinggi'], risiko['rendah'])


rule10 = ctrl.Rule(absen['rendah'] & interaksi['normal'] & prestasi['rendah'], risiko['sedang'])
rule11 = ctrl.Rule(absen['rendah'] & interaksi['pasif'] & prestasi['sedang'], risiko['sedang'])
rule12 = ctrl.Rule(absen['sedang'] & interaksi['aktif'] & prestasi['rendah'], risiko['sedang'])
rule13 = ctrl.Rule(absen['sedang'] & interaksi['normal'] & prestasi['sedang'], risiko['sedang']) 
rule14 = ctrl.Rule(absen['sedang'] & interaksi['pasif'] & prestasi['tinggi'], risiko['sedang'])
rule15 = ctrl.Rule(absen['tinggi'] & interaksi['aktif'] & prestasi['tinggi'], risiko['sedang']) 
rule16 = ctrl.Rule(absen['tinggi'] & interaksi['aktif'] & prestasi['sedang'], risiko['sedang'])
rule17 = ctrl.Rule(absen['tinggi'] & interaksi['normal'] & prestasi['tinggi'], risiko['sedang'])
rule18 = ctrl.Rule(absen['tinggi'] & interaksi['pasif'] & prestasi['tinggi'], risiko['sedang'])


rule19 = ctrl.Rule(absen['rendah'] & interaksi['pasif'] & prestasi['rendah'], risiko['tinggi'])
rule20 = ctrl.Rule(absen['sedang'] & interaksi['normal'] & prestasi['rendah'], risiko['tinggi'])
rule21 = ctrl.Rule(absen['sedang'] & interaksi['pasif'] & prestasi['sedang'], risiko['tinggi'])
rule22 = ctrl.Rule(absen['sedang'] & interaksi['pasif'] & prestasi['rendah'], risiko['tinggi'])
rule23 = ctrl.Rule(absen['tinggi'] & interaksi['aktif'] & prestasi['rendah'], risiko['tinggi'])
rule24 = ctrl.Rule(absen['tinggi'] & interaksi['normal'] & prestasi['sedang'], risiko['tinggi'])
rule25 = ctrl.Rule(absen['tinggi'] & interaksi['normal'] & prestasi['rendah'], risiko['tinggi'])
rule26 = ctrl.Rule(absen['tinggi'] & interaksi['pasif'] & prestasi['sedang'], risiko['tinggi'])
rule27 = ctrl.Rule(absen['tinggi'] & interaksi['pasif'] & prestasi['rendah'], risiko['tinggi']) 

# --- Control System ---
bullying_ctrl = ctrl.ControlSystem([
    rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9,
    rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18,
    rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27
])

diagnosa_bullying = ctrl.ControlSystemSimulation(bullying_ctrl)

def evaluasi_risiko(val_absen, val_interaksi, val_prestasi):
    diagnosa_bullying.input['absen'] = val_absen
    diagnosa_bullying.input['interaksi'] = val_interaksi
    diagnosa_bullying.input['prestasi'] = val_prestasi
    
    try:
        diagnosa_bullying.compute()
        return diagnosa_bullying.output['risiko']
    except:
        return 0

if __name__ == "__main__":
    print("=== Diagnosa Risiko Bullying (Fuzzy Logic - Trapezium) ===")
    try:
        print("\nSkala Input: 1 (Baik/Rendah), 2 (Sedang), 3 (Buruk/Tinggi)")
        i_absen = float(input("Absen (1-3): "))
        i_interaksi = float(input("Interaksi (1-3): "))
        i_prestasi = float(input("Prestasi (1-3): "))

        hasil = evaluasi_risiko(i_absen, i_interaksi, i_prestasi)
        hasil_bulat = int(round(hasil))
        
        print(f"\nSkor Risiko: {hasil_bulat}")
        
        if hasil_bulat == 1:
            print("Kategori: RISIKO RENDAH")
        elif hasil_bulat == 2:
            print("Kategori: RISIKO SEDANG")
        else:
            print("Kategori: RISIKO TINGGI")
        
        # Plotting
        absen.view()
        plt.title('Absen Sekolah (Trapmf)')
        interaksi.view()
        plt.title('Interaksi Sosial (Trapmf)')
        prestasi.view()
        plt.title('Prestasi Akademik (Trapmf)')
        risiko.view(sim=diagnosa_bullying)
        plt.title(f'Output Risiko (Skor: {hasil_bulat})')
        plt.show()
        
    except Exception as e:
        print(f"Error: {e}")
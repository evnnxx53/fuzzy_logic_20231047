import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


# 1. ABSEN (0 - 20 Kali)
absen = ctrl.Antecedent(np.arange(0, 21, 1), 'absen')
absen['rendah'] = fuzz.trapmf(absen.universe, [0, 0, 4, 5])   
absen['sedang'] = fuzz.trapmf(absen.universe, [4, 5, 12, 13]) 
absen['tinggi'] = fuzz.trapmf(absen.universe, [12, 13, 20, 20])

# 2. INTERAKSI (Skala 1 - 3)
interaksi = ctrl.Antecedent(np.arange(0, 4.1, 0.1), 'interaksi')
interaksi['aktif'] = fuzz.trapmf(interaksi.universe, [0, 0, 1.2, 1.8])
interaksi['normal'] = fuzz.trapmf(interaksi.universe, [1.2, 1.8, 2.2, 2.8])
interaksi['pasif'] = fuzz.trapmf(interaksi.universe, [2.2, 2.8, 4, 4])

# 3. PRESTASI (Nilai 0 - 100)
prestasi = ctrl.Antecedent(np.arange(0, 101, 1), 'prestasi')
prestasi['rendah'] = fuzz.trapmf(prestasi.universe, [0, 0, 50, 51]) 
prestasi['sedang'] = fuzz.trapmf(prestasi.universe, [50, 51, 75, 76])
prestasi['tinggi'] = fuzz.trapmf(prestasi.universe, [75, 76, 100, 100])

# === OUTPUT RISIKO ===
risiko = ctrl.Consequent(np.arange(0, 4.1, 0.1), 'risiko')
risiko['rendah'] = fuzz.trapmf(risiko.universe, [0, 0, 1.2, 1.8])
risiko['sedang'] = fuzz.trapmf(risiko.universe, [1.2, 1.8, 2.2, 2.8])
risiko['tinggi'] = fuzz.trapmf(risiko.universe, [2.2, 2.8, 4, 4])

# === RULES ===
rule1 = ctrl.Rule(absen['rendah'] & interaksi['aktif'] & prestasi['tinggi'], risiko['rendah'])
rule2 = ctrl.Rule(absen['rendah'] & interaksi['aktif'] & prestasi['sedang'], risiko['rendah'])
rule3 = ctrl.Rule(absen['rendah'] & interaksi['aktif'] & prestasi['rendah'], risiko['sedang'])
rule4 = ctrl.Rule(absen['rendah'] & interaksi['normal'] & prestasi['tinggi'], risiko['rendah'])
rule5 = ctrl.Rule(absen['rendah'] & interaksi['normal'] & prestasi['sedang'], risiko['rendah'])
rule6 = ctrl.Rule(absen['rendah'] & interaksi['normal'] & prestasi['rendah'], risiko['sedang'])
rule7 = ctrl.Rule(absen['rendah'] & interaksi['pasif'] & prestasi['tinggi'], risiko['sedang'])
rule8 = ctrl.Rule(absen['rendah'] & interaksi['pasif'] & prestasi['sedang'], risiko['sedang'])
rule9 = ctrl.Rule(absen['rendah'] & interaksi['pasif'] & prestasi['rendah'], risiko['tinggi'])
rule10 = ctrl.Rule(absen['sedang'] & interaksi['aktif'] & prestasi['tinggi'], risiko['rendah'])
rule11 = ctrl.Rule(absen['sedang'] & interaksi['aktif'] & prestasi['sedang'], risiko['sedang'])
rule12 = ctrl.Rule(absen['sedang'] & interaksi['aktif'] & prestasi['rendah'], risiko['sedang'])
rule13 = ctrl.Rule(absen['sedang'] & interaksi['normal'] & prestasi['tinggi'], risiko['sedang'])
rule14 = ctrl.Rule(absen['sedang'] & interaksi['normal'] & prestasi['sedang'], risiko['sedang'])
rule15 = ctrl.Rule(absen['sedang'] & interaksi['normal'] & prestasi['rendah'], risiko['tinggi'])
rule16 = ctrl.Rule(absen['sedang'] & interaksi['pasif'] & prestasi['tinggi'], risiko['sedang'])
rule17 = ctrl.Rule(absen['sedang'] & interaksi['pasif'] & prestasi['sedang'], risiko['tinggi'])
rule18 = ctrl.Rule(absen['sedang'] & interaksi['pasif'] & prestasi['rendah'], risiko['tinggi'])
rule19 = ctrl.Rule(absen['tinggi'] & interaksi['aktif'] & prestasi['tinggi'], risiko['sedang'])
rule20 = ctrl.Rule(absen['tinggi'] & interaksi['aktif'] & prestasi['sedang'], risiko['sedang'])
rule21 = ctrl.Rule(absen['tinggi'] & interaksi['aktif'] & prestasi['rendah'], risiko['tinggi'])
rule22 = ctrl.Rule(absen['tinggi'] & interaksi['normal'] & prestasi['tinggi'], risiko['sedang'])
rule23 = ctrl.Rule(absen['tinggi'] & interaksi['normal'] & prestasi['sedang'], risiko['tinggi'])
rule24 = ctrl.Rule(absen['tinggi'] & interaksi['normal'] & prestasi['rendah'], risiko['tinggi'])
rule25 = ctrl.Rule(absen['tinggi'] & interaksi['pasif'] & prestasi['tinggi'], risiko['tinggi'])
rule26 = ctrl.Rule(absen['tinggi'] & interaksi['pasif'] & prestasi['sedang'], risiko['tinggi'])
rule27 = ctrl.Rule(absen['tinggi'] & interaksi['pasif'] & prestasi['rendah'], risiko['tinggi'])

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
    diagnosa_bullying.compute()
    return diagnosa_bullying.output['risiko']

# === FUNGSI BARU: MENDAPATKAN DETAIL PROSES ===
def get_fuzzy_details(val_absen, val_interaksi, val_prestasi):
    # 1. Hitung derajat keanggotaan (Membership Degree) untuk setiap variabel
    # Ini untuk menentukan input user itu masuk kategori mana (Fuzzifikasi)
    
    # Absen
    mu_absen = {
        'Rendah': fuzz.interp_membership(absen.universe, absen['rendah'].mf, val_absen),
        'Sedang': fuzz.interp_membership(absen.universe, absen['sedang'].mf, val_absen),
        'Tinggi': fuzz.interp_membership(absen.universe, absen['tinggi'].mf, val_absen)
    }
    cat_absen = max(mu_absen, key=mu_absen.get) # Ambil kategori dengan nilai tertinggi

    # Interaksi
    mu_interaksi = {
        'Aktif': fuzz.interp_membership(interaksi.universe, interaksi['aktif'].mf, val_interaksi),
        'Normal': fuzz.interp_membership(interaksi.universe, interaksi['normal'].mf, val_interaksi),
        'Pasif': fuzz.interp_membership(interaksi.universe, interaksi['pasif'].mf, val_interaksi)
    }
    cat_interaksi = max(mu_interaksi, key=mu_interaksi.get)

    # Prestasi
    mu_prestasi = {
        'Rendah': fuzz.interp_membership(prestasi.universe, prestasi['rendah'].mf, val_prestasi),
        'Sedang': fuzz.interp_membership(prestasi.universe, prestasi['sedang'].mf, val_prestasi),
        'Tinggi': fuzz.interp_membership(prestasi.universe, prestasi['tinggi'].mf, val_prestasi)
    }
    cat_prestasi = max(mu_prestasi, key=mu_prestasi.get)

    # 2. Susun Kalimat Rule yang Aktif
    # Logika sederhana: Gabungkan kategori dominan dari ketiga input
    rule_text = f"JIKA Absen <b>{cat_absen}</b> DAN Interaksi <b>{cat_interaksi}</b> DAN Prestasi <b>{cat_prestasi}</b>"

    return {
        'cat_absen': cat_absen,
        'cat_interaksi': cat_interaksi,
        'cat_prestasi': cat_prestasi,
        'rule_active': rule_text
    }
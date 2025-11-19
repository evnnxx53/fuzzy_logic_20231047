import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

waktu_respon = ctrl.Antecedent(np.arange(0, 61, 1), 'waktu_respon')

kualitas_produk = ctrl.Antecedent(np.arange(0, 11, 1), 'kualitas_produk')

kepuasan = ctrl.Consequent(np.arange(0, 101, 1), 'kepuasan')

waktu_respon['cepat'] = fuzz.trimf(waktu_respon.universe, [0, 0, 15])
waktu_respon['sedang'] = fuzz.trimf(waktu_respon.universe, [10, 25, 40])
waktu_respon['lama'] = fuzz.trimf(waktu_respon.universe, [30, 60, 60])

kualitas_produk['rendah'] = fuzz.trimf(kualitas_produk.universe, [0, 0, 5])
kualitas_produk['sedang'] = fuzz.trimf(kualitas_produk.universe, [3, 5, 8])
kualitas_produk['tinggi'] = fuzz.trimf(kualitas_produk.universe, [7, 10, 10])

kepuasan['rendah'] = fuzz.trimf(kepuasan.universe, [0, 0, 40])
kepuasan['sedang'] = fuzz.trimf(kepuasan.universe, [30, 50, 75])
kepuasan['tinggi'] = fuzz.trimf(kepuasan.universe, [60, 100, 100])

rule1 = ctrl.Rule(waktu_respon['cepat'] & kualitas_produk['tinggi'], kepuasan['tinggi'])
rule2 = ctrl.Rule(waktu_respon['cepat'] & kualitas_produk['sedang'], kepuasan['sedang'])
rule3 = ctrl.Rule(waktu_respon['cepat'] & kualitas_produk['rendah'], kepuasan['sedang'])

rule4 = ctrl.Rule(waktu_respon['sedang'] & kualitas_produk['tinggi'], kepuasan['sedang'])
rule5 = ctrl.Rule(waktu_respon['sedang'] & kualitas_produk['sedang'], kepuasan['sedang'])
rule6 = ctrl.Rule(waktu_respon['sedang'] & kualitas_produk['rendah'], kepuasan['rendah'])

rule7 = ctrl.Rule(waktu_respon['lama'] & kualitas_produk['tinggi'], kepuasan['sedang'])
rule8 = ctrl.Rule(waktu_respon['lama'] & kualitas_produk['sedang'], kepuasan['rendah'])
rule9 = ctrl.Rule(waktu_respon['lama'] & kualitas_produk['rendah'], kepuasan['rendah'])


kepuasan_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
kepuasan_simulasi = ctrl.ControlSystemSimulation(kepuasan_ctrl)

def evaluasi_kepuasan(waktu, kualitas):
    kepuasan_simulasi.input['waktu_respon'] = waktu
    kepuasan_simulasi.input['kualitas_produk'] = kualitas
    kepuasan_simulasi.compute()
    return kepuasan_simulasi.output['kepuasan']

if __name__ == "__main__":
    waktu_input = float(input("Masukkan waktu respon layanan (menit): "))
    kualitas_input = float(input("Masukkan kualitas produk (0-10): "))

    hasil = evaluasi_kepuasan(waktu_input, kualitas_input)
    print(f"Tingkat Kepuasan Pelanggan: {hasil:.2f}%")

    waktu_respon.view()
    kualitas_produk.view()
    kepuasan.view()
    plt.show()
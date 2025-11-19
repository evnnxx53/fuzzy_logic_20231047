import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

latensi = ctrl.Antecedent(np.arange(0, 301, 1), 'latensi')
kecepatan = ctrl.Antecedent(np.arange(0, 101, 1), 'kecepatan')
kualitas_jaringan = ctrl.Consequent(np.arange(0, 101, 1), 'kualitas_jaringan')

latensi['bagus'] = fuzz.trimf(latensi.universe, [0, 0, 50])
latensi['sedang'] = fuzz.trimf(latensi.universe, [30, 100, 170])
latensi['buruk'] = fuzz.trimf(latensi.universe, [150, 300, 300])

kecepatan['lambat'] = fuzz.trimf(kecepatan.universe, [0, 0, 20])
kecepatan['sedang'] = fuzz.trimf(kecepatan.universe, [10, 40, 70])
kecepatan['cepat'] = fuzz.trimf(kecepatan.universe, [60, 100, 100])

kualitas_jaringan['buruk'] = fuzz.trimf(kualitas_jaringan.universe, [0, 0, 50])
kualitas_jaringan['cukup'] = fuzz.trimf(kualitas_jaringan.universe, [40, 60, 80])
kualitas_jaringan['bagus'] = fuzz.trimf(kualitas_jaringan.universe, [70, 100, 100])

rule1 = ctrl.Rule(latensi['bagus'] & kecepatan['cepat'], kualitas_jaringan['bagus'])
rule2 = ctrl.Rule(latensi['bagus'] & kecepatan['sedang'], kualitas_jaringan['cukup'])
rule3 = ctrl.Rule(latensi['bagus'] & kecepatan['lambat'], kualitas_jaringan['cukup'])
rule4 = ctrl.Rule(latensi['sedang'] & kecepatan['cepat'], kualitas_jaringan['cukup'])
rule5 = ctrl.Rule(latensi['sedang'] & kecepatan['sedang'], kualitas_jaringan['cukup'])
rule6 = ctrl.Rule(latensi['sedang'] & kecepatan['lambat'], kualitas_jaringan['buruk'])
rule7 = ctrl.Rule(latensi['buruk'] & kecepatan['cepat'], kualitas_jaringan['cukup'])
rule8 = ctrl.Rule(latensi['buruk'] & kecepatan['sedang'], kualitas_jaringan['buruk'])
rule9 = ctrl.Rule(latensi['buruk'] & kecepatan['lambat'], kualitas_jaringan['buruk'])

jaringan_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
diagnosa_jaringan = ctrl.ControlSystemSimulation(jaringan_ctrl)

def evaluasi_jaringan(nilai_latensi, nilai_kecepatan):
    diagnosa_jaringan.input['latensi'] = nilai_latensi
    diagnosa_jaringan.input['kecepatan'] = nilai_kecepatan
    diagnosa_jaringan.compute()
    return diagnosa_jaringan.output['kualitas_jaringan']

if __name__ == "__main__":
    print("=== Diagnosa Kualitas Jaringan (Fuzzy Logic) ===")
    try:
        input_latensi = float(input("Masukkan Latensi (Ping) dalam ms (0-300): "))
        input_kecepatan = float(input("Masukkan Kecepatan Download dalam Mbps (0-100): "))

        skor_hasil = evaluasi_jaringan(input_latensi, input_kecepatan)
        
        print(f"\nSkor Kualitas Jaringan: {skor_hasil:.2f} / 100")
        
        if skor_hasil >= 70:
            print("Hasil: Jaringan SANGAT BAIK")
            print("Saran: Koneksi optimal. Tidak perlu tindakan perbaikan.")
        elif skor_hasil >= 45:
            print("Hasil: Jaringan CUKUP BAIK")
            print("Saran: Coba kurangi perangkat yang terhubung atau restart router.")
        else:
            print("Hasil: Jaringan BURUK")
            print("Saran: Dekatkan perangkat ke router atau hubungi ISP.")

        latensi.view()
        plt.vlines(input_latensi, 0, 1, colors='k', linewidth=3, label='Input User')
        plt.title(f'Latensi (Input: {input_latensi} ms)')
        plt.legend()

        kecepatan.view()
        plt.vlines(input_kecepatan, 0, 1, colors='k', linewidth=3, label='Input User')
        plt.title(f'Kecepatan (Input: {input_kecepatan} Mbps)')
        plt.legend()

        kualitas_jaringan.view(sim=diagnosa_jaringan)
        plt.title(f'Kualitas Jaringan (Output: {skor_hasil:.2f})')

        plt.show()
        
    except ValueError:
        print("Error: Masukkan angka yang valid.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

latensi = ctrl.Antecedent(np.arange(0, 301, 1), 'latensi')
kecepatan = ctrl.Antecedent(np.arange(0, 101, 1), 'kecepatan')
kualitas_jaringan = ctrl.Consequent(np.arange(0, 101, 1), 'kualitas_jaringan')

latensi['bagus'] = fuzz.gbellmf(latensi.universe, 25, 2.5, 0)
latensi['sedang'] = fuzz.gbellmf(latensi.universe, 35, 2.5, 100)
latensi['buruk'] = fuzz.gbellmf(latensi.universe, 75, 2.5, 300)

kecepatan['lambat'] = fuzz.gbellmf(kecepatan.universe, 10, 2.5, 0)
kecepatan['sedang'] = fuzz.gbellmf(kecepatan.universe, 15, 2.5, 40)
kecepatan['cepat'] = fuzz.gbellmf(kecepatan.universe, 20, 2.5, 100)

kualitas_jaringan['bagus'] = fuzz.gbellmf(kualitas_jaringan.universe, 15, 2.5, 100)
kualitas_jaringan['cukup'] = fuzz.gbellmf(kualitas_jaringan.universe, 10, 2.5, 60)
kualitas_jaringan['buruk'] = fuzz.gbellmf(kualitas_jaringan.universe, 25, 2.5, 0)

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
    print("=== Diagnosa Kualitas Jaringan (Fuzzy Logic - GBELLMF) ===")
    try:
        input_latensi = float(input("Masukkan Latensi (Ping) dalam ms (0-300): "))
        input_kecepatan = float(input("Masukkan Kecepatan Download dalam Mbps (0-100): "))

        skor_hasil = evaluasi_jaringan(input_latensi, input_kecepatan)
        
        print(f"\nSkor Kualitas Jaringan: {skor_hasil:.2f} / 100")
        
        if skor_hasil >= 70:
            print("Hasil: Jaringan SANGAT BAIK")
        elif skor_hasil >= 45:
            print("Hasil: Jaringan CUKUP BAIK")
        else:
            print("Hasil: Jaringan BURUK")

        latensi.view()
        plt.title(f'Latensi (Gbellmf)')
        
        kecepatan.view()
        plt.title(f'Kecepatan (Gbellmf)')
        
        kualitas_jaringan.view(sim=diagnosa_jaringan)
        plt.title(f'Output Kualitas (Gbellmf)')

        plt.show()
        
    except ValueError:
        print("Error: Masukkan angka yang valid.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
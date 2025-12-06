from flask import Flask, render_template, request
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from bullying_detection import (
    evaluasi_risiko, 
    absen, 
    interaksi, 
    prestasi,
    risiko, 
    diagnosa_bullying
)

app = Flask(__name__)

def get_plot_url(variable, input_val=None, is_output=False, simulation=None):
    # Bersihkan figure sebelumnya sepenuhnya
    plt.close('all')
    
    # SETUP UKURAN FIGURE LEBIH LEBAR (8x4.5 inch)
    # Ini membuat jarak horizontal angka 1-2-3 lebih lega
    fig = plt.figure(figsize=(8, 4.5))
    
    bg_color = '#2c3440'
    text_color = '#ffffff'
    accent_color = '#ffffff'
    
    # Warna Dasar
    col_good = '#2ecc71'  # Hijau (Baik/Aman)
    col_mid  = '#ff8000'  # Orange (Sedang/Waspada)
    col_bad  = '#ea3b2e'  # Merah (Buruk/Bahaya)

    # Mapping warna
    color_mapping = {
        'aktif': col_good,
        'normal': col_mid,
        'pasif': col_bad,
        'sedang': col_mid
    }

    fig.set_facecolor(bg_color)
    
    if is_output:
        # Visualisasi Output (Risiko)
        variable.view(sim=simulation)
        
        # Logika Judul & Warna
        skor_int = int(round(input_val))
        if skor_int > 3: skor_int = 3
        if skor_int < 1: skor_int = 1
        
        plt.title(f"Output: Risiko Bullying (Skor: {skor_int})", color=text_color, fontsize=12, pad=10)
        
        if skor_int == 1:
            fill_color = col_good 
        elif skor_int == 3:
            fill_color = col_bad
        else:
            fill_color = col_mid
            
        ax = plt.gca()
        
        # Warnai area arsiran
        for collection in ax.collections:
            collection.set_facecolor(fill_color)
            collection.set_alpha(0.6)
            
        # Garis Hasil (Putih)
        for line in ax.get_lines():
            if line.get_color() == 'k': 
                line.set_color(accent_color)
                line.set_label('Hasil')
                line.set_xdata([skor_int, skor_int]) # Paksa di angka bulat
                
    else:
        # Visualisasi Input
        variable.view()
        if input_val is not None:
            plt.vlines(input_val, 0, 1, colors=accent_color, linewidth=3, label='Input User')
            plt.title(f"{variable.label.capitalize()} (Input: {int(input_val)})", color=text_color, fontsize=12, pad=10)

    ax = plt.gca()
    ax.set_ylabel('') 
    
    # === PENGATURAN TAMPILAN AGAR TIDAK MEPET ===
    # 1. Hanya tampilkan angka 1, 2, 3
    ax.set_xticks([1, 2, 3])
    
    # 2. Margin Horizontal (0.5 - 3.5) agar tidak mentok pinggir kiri/kanan
    ax.set_xlim(0.5, 3.5)
    
    # 3. Margin Vertikal agar puncak tidak mentok atas
    ax.set_ylim(0, 1.1)
    
    # === PEWARNAAN GARIS ===
    for line in ax.get_lines():
        label = line.get_label()
        if label in color_mapping:
            line.set_color(color_mapping[label])
            
        if label == 'rendah':
            if variable.label == 'prestasi': line.set_color(col_bad)
            else: line.set_color(col_good)
                
        if label == 'tinggi':
            if variable.label == 'prestasi': line.set_color(col_good)
            else: line.set_color(col_bad)

    # Legend
    legend_loc = 'upper right'
    if not is_output and input_val is not None and input_val > 2:
        legend_loc = 'upper left'
        
    legend = plt.legend(loc=legend_loc)
    legend.get_frame().set_facecolor(bg_color)
    legend.get_frame().set_edgecolor(text_color)
    for text in legend.get_texts():
        text.set_color(text_color)

    # Styling Axis
    ax.set_facecolor(bg_color)
    ax.tick_params(axis='x', colors=text_color)
    ax.tick_params(axis='y', colors=text_color)
    ax.xaxis.label.set_color(text_color)
    ax.yaxis.label.set_color(text_color)
    
    for spine in ax.spines.values():
        spine.set_color(text_color)

    # Simpan Gambar
    img = io.BytesIO()
    # bbox_inches='tight' membuang margin berlebih, tapi pad_inches memberi napas sedikit
    plt.savefig(img, format='png', bbox_inches='tight', pad_inches=0.1, facecolor=bg_color)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url

@app.route('/', methods=['GET', 'POST'])
def index():
    result_data = None
    
    if request.method == 'POST':
        try:
            val_absen = float(request.form['absen'])
            val_interaksi = float(request.form['interaksi'])
            val_prestasi = float(request.form['prestasi'])
            
            skor_hasil = evaluasi_risiko(val_absen, val_interaksi, val_prestasi)
            skor_bulat = int(round(skor_hasil))
            
            if skor_bulat < 1: skor_bulat = 1
            if skor_bulat > 3: skor_bulat = 3
            
            if skor_bulat == 1:
                kategori = "RISIKO RENDAH"
                warna = "success"
                saran = [
                    "Tidak ada indikasi bullying yang serius.",
                    "Siswa dalam kondisi baik dan adaptif.",
                    "Pertahankan lingkungan belajar yang positif."
                ]
            elif skor_bulat == 2:
                kategori = "RISIKO SEDANG"
                warna = "warning"
                saran = [
                    "Ada gejala awal yang perlu dipantau.",
                    "Lakukan konseling ringan atau wawancara.",
                    "Perhatikan perubahan perilaku di kelas."
                ]
            else: 
                kategori = "RISIKO TINGGI"
                warna = "danger"
                saran = [
                    "Indikasi kuat siswa mengalami bullying.",
                    "Segera lakukan intervensi dan panggil orang tua.",
                    "Butuh pendampingan psikologis segera."
                ]

            plot_absen = get_plot_url(absen, val_absen)
            plot_interaksi = get_plot_url(interaksi, val_interaksi)
            plot_prestasi = get_plot_url(prestasi, val_prestasi)
            plot_output = get_plot_url(risiko, skor_hasil, is_output=True, simulation=diagnosa_bullying)

            result_data = {
                'skor': str(skor_bulat),
                'kategori': kategori,
                'warna': warna,
                'saran': saran,
                'plot_1': plot_absen,
                'plot_2': plot_interaksi,
                'plot_3': plot_prestasi,
                'plot_output': plot_output
            }

        except ValueError:
            result_data = {'error': "Mohon masukkan angka yang valid!"}

    return render_template('index.html', result=result_data)

if __name__ == '__main__':
    app.run(debug=True)
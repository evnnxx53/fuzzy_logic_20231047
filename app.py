from flask import Flask, render_template, request
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from network_quality import (
    evaluasi_jaringan, 
    latensi, 
    kecepatan, 
    kualitas_jaringan, 
    diagnosa_jaringan
)

app = Flask(__name__)

def get_plot_url(variable, input_val=None, is_output=False, simulation=None):
    plt.clf()
    
    bg_color = '#2c3440'
    text_color = '#ffffff'
    accent_color = '#ffffff'

    fig = plt.gcf()
    fig.set_facecolor(bg_color)
    
    if is_output:
        variable.view(sim=simulation)
        plt.title(f"Output: Kualitas Jaringan (Skor: {input_val:.2f})", color=text_color)
        
        ax = plt.gca()
        for line in ax.get_lines():
            if line.get_color() == 'k': 
                line.set_color(accent_color)
    else:
        variable.view()
        if input_val is not None:
            plt.vlines(input_val, 0, 1, colors=accent_color, linewidth=3, label='Input User')
            plt.title(f"{variable.label} (Input: {input_val})", color=text_color)
            
            legend = plt.legend()
            legend.get_frame().set_facecolor(bg_color)
            legend.get_frame().set_edgecolor(text_color)
            for text in legend.get_texts():
                text.set_color(text_color)

    ax = plt.gca()
    ax.set_facecolor(bg_color)
    ax.tick_params(axis='x', colors=text_color)
    ax.tick_params(axis='y', colors=text_color)
    ax.xaxis.label.set_color(text_color)
    ax.yaxis.label.set_color(text_color)
    
    for spine in ax.spines.values():
        spine.set_color(text_color)

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', facecolor=bg_color)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return plot_url

@app.route('/', methods=['GET', 'POST'])
def index():
    result_data = None
    
    if request.method == 'POST':
        try:
            input_latensi = float(request.form['latensi'])
            input_kecepatan = float(request.form['kecepatan'])
            
            skor_hasil = evaluasi_jaringan(input_latensi, input_kecepatan)
            
            if skor_hasil >= 70:
                kategori = "SANGAT BAIK"
                warna = "success"
                saran = [
                    "Koneksi optimal.", 
                    "Cocok untuk streaming 4K dan gaming kompetitif.",
                    "Tidak perlu tindakan perbaikan."
                ]
            elif skor_hasil >= 45:
                kategori = "CUKUP BAIK"
                warna = "warning"
                saran = [
                    "Cukup stabil untuk browsing dan streaming HD.",
                    "Mungkin agak lag untuk gaming berat.",
                    "Coba restart router jika terasa lambat."
                ]
            else:
                kategori = "BURUK"
                warna = "danger"
                saran = [
                    "Koneksi tidak stabil.",
                    "Sulit untuk aktivitas berat.",
                    "Periksa kabel atau hubungi ISP Anda."
                ]

            plot_latensi = get_plot_url(latensi, input_latensi)
            plot_kecepatan = get_plot_url(kecepatan, input_kecepatan)
            plot_output = get_plot_url(kualitas_jaringan, skor_hasil, is_output=True, simulation=diagnosa_jaringan)

            result_data = {
                'skor': f"{skor_hasil:.2f}",
                'kategori': kategori,
                'warna': warna,
                'saran': saran,
                'plot_latensi': plot_latensi,
                'plot_kecepatan': plot_kecepatan,
                'plot_output': plot_output
            }

        except ValueError:
            result_data = {'error': "Mohon masukkan angka yang valid!"}

    return render_template('index.html', result=result_data)

if __name__ == '__main__':
    app.run(debug=True)
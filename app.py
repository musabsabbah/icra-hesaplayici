from flask import Flask, render_template, request, jsonify
from datetime import datetime
from core.calculator import IcraEngine
from core.rates import YASAL_FAIZ_ORANLARI, AVANS_FAIZ_ORANLARI

app = Flask(__name__, template_folder='templates')

FAIZ_ORANLARI_MAP = {
    "yasal": YASAL_FAIZ_ORANLARI,
    "avans": AVANS_FAIZ_ORANLARI,
}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/hesapla', methods=['POST'])
def hesapla():
    data = request.get_json()

    asil_alacak = float(data.get('asil_alacak', 0))
    baslangic_tarihi = datetime.strptime(data.get('baslangic_tarihi'), "%Y-%m-%d").date()
    bitis_tarihi = datetime.strptime(data.get('bitis_tarihi'), "%Y-%m-%d").date()

    faiz_turu = data.get('faiz_turu', 'yasal')
    faiz_tipi = data.get('faiz_tipi', 'degisken')
    sabit_faiz_orani = float(data.get('sabit_faiz_orani', 0))

    tahsil_harci_safhasi = data.get('tahsil_harci_safhasi', 'hicbiri')
    basvurma_harci_ekle = bool(data.get('basvurma_harci_ekle', False))
    pesin_harc_ekle = bool(data.get('pesin_harc_ekle', False))
    vekalet_ucreti_ekle = bool(data.get('vekalet_ucreti_ekle', False))
    tebligat_masrafi_ekle = bool(data.get('tebligat_masrafi_ekle', False))
    tebligat_masrafi_tutari = float(data.get('tebligat_masrafi_tutari', 0))
    kismi_odemeler = float(data.get('kismi_odemeler', 0))

    engine = IcraEngine(asil_alacak, baslangic_tarihi, bitis_tarihi)

    # Kademeli faiz için doğru oran listesini seç (akdi/mevduat için hazır liste yok)
    oran_listesi = FAIZ_ORANLARI_MAP.get(faiz_turu)

    faiz_sonuc = engine.faiz_hesabla(
        faiz_turu=faiz_turu,
        faiz_tipi=faiz_tipi,
        sabit_oran=sabit_faiz_orani,
        oran_listesi=oran_listesi
    )

    harc_sonuc = engine.harclari_hesabla(
        basvurma_harci_ekle=basvurma_harci_ekle,
        pesin_harc_ekle=pesin_harc_ekle,
        tahsil_harci_safhasi=tahsil_harci_safhasi
    )

    vekalet_ucreti = 0.0
    if vekalet_ucreti_ekle:
        vekalet_ucreti = engine.vekalet_ucreti_hesabla()['toplam_vekalet_ucreti']

    tebligat_masrafi = tebligat_masrafi_tutari if tebligat_masrafi_ekle else 0.0

    harclar_toplami = round(harc_sonuc['toplam_harc'] + vekalet_ucreti + tebligat_masrafi, 2)
    genel_toplam = round(asil_alacak + faiz_sonuc['toplam_faiz'] + harclar_toplami - kismi_odemeler, 2)

    return jsonify({
        "asil_alacak": asil_alacak,
        "odenecek_faiz": faiz_sonuc['toplam_faiz'],
        "harclar_toplami": harclar_toplami,
        "genel_toplam": genel_toplam,
        "harc_detaylari": {
            "basvurma_harci": harc_sonuc['basvurma_harci'],
            "pesin_harc": harc_sonuc['pesin_harc'],
            "tahsil_harci": harc_sonuc['tahsil_harci'],
            "tebligat_masrafi": tebligat_masrafi,
            "vekalet_ucreti": vekalet_ucreti
        },
        "faiz_dokumu": faiz_sonuc['faiz_dokumu']
    })

if __name__ == '__main__':
    app.run()

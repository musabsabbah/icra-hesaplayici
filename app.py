from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import date
from core.calculator import IcraEngine
from core.rates import YASAL_FAIZ_ORANLARI, AVANS_FAIZ_ORANLARI

app = FastAPI(title="Gelişmiş İcra Takip Servisi")
templates = Jinja2Templates(directory="templates")

class HesaplamaIstegi(BaseModel):
    asil_alacak: float
    baslangic_tarihi: date
    bitis_tarihi: date
    faiz_turu: str
    faiz_tipi: str
    sabit_faiz_orani: float = 0.0
    tahsil_harci_safhasi: str = "hicbiri"
    basvurma_harci_ekle: bool = False
    pesin_harc_ekle: bool = False
    tebligat_masrafi_ekle: bool = False
    tebligat_masrafi_tutari: float = 0.0
    vekalet_ucreti_ekle: bool = False
    kismi_odemeler: float = 0.0

@app.get("/", response_class=HTMLResponse)
def ana_sayfa(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})

@app.post("/hesapla")
def hesapla(istek: HesaplamaIstegi):
    engine = IcraEngine(istek.asil_alacak, istek.baslangic_tarihi, istek.bitis_tarihi)
    
    # 1. Faiz Oranlarını Belirleme
    oran_listesi = None
    if istek.faiz_tipi == "degisken":
        if istek.faiz_turu == "yasal":
            oran_listesi = YASAL_FAIZ_ORANLARI
        elif istek.faiz_turu in ["avans", "mevduat"]:
            oran_listesi = AVANS_FAIZ_ORANLARI
            
    faiz_sonuc = engine.faiz_hesabla(
        faiz_turu=istek.faiz_turu,
        faiz_tipi=istek.faiz_tipi,
        sabit_oran=istek.sabit_faiz_orani,
        oran_listesi=oran_listesi
    )
    
    # 2. Harç Hesapları (Yalnızca seçilenler hesaplanır)
    harclar = engine.harclari_hesabla(
        basvurma_harci_ekle=istek.basvurma_harci_ekle,
        pesin_harc_ekle=istek.pesin_harc_ekle,
        tahsil_harci_safhasi=istek.tahsil_harci_safhasi
    )
    
    # 3. AAÜT Vekalet Ücreti (Yalnızca seçildiyse eklenir)
    vekalet_sonuc = engine.vekalet_ucreti_hesabla() if istek.vekalet_ucreti_ekle else {"toplam_vekalet_ucreti": 0.0}
    
    # 4. Tebligat / Masraflar
    tebligat_tutari = istek.tebligat_masrafi_tutari if istek.tebligat_masrafi_ekle else 0.0
    
    # 5. Toplam Harçlar Kalemi
    toplam_harçlar_kalemi = round(harclar["toplam_harc"] + tebligat_tutari + vekalet_sonuc["toplam_vekalet_ucreti"], 2)

    # 6. Toplam Borç Hesabı
    brut_toplam = round(istek.asil_alacak + faiz_sonuc["toplam_faiz"] + toplam_harçlar_kalemi, 2)
    net_bakiye = max(0.0, round(brut_toplam - istek.kismi_odemeler, 2))

    return {
        "asil_alacak": istek.asil_alacak,
        "odenecek_faiz": faiz_sonuc["toplam_faiz"],
        "harclar_toplami": toplam_harçlar_kalemi,
        "genel_toplam": net_bakiye,
        "faiz_dokumu": faiz_sonuc["faiz_dokumu"],
        "harc_detaylari": {
            "basvurma_harci": harclar["basvurma_harci"],
            "pesin_harc": harclar["pesin_harc"],
            "tahsil_harci": harclar["tahsil_harci"],
            "vekalet_ucreti": vekalet_sonuc["toplam_vekalet_ucreti"],
            "tebligat_masrafi": tebligat_tutari
        }
    }

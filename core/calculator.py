# core/calculator.py
from datetime import date
from typing import List, Dict
from core.rates import GUNCEL_MAKTU_HARCLAR, AAUT_DILIMLERI

class IcraEngine:
    def __init__(self, asil_alacak: float, baslangic_tarihi: date, bitis_tarihi: date):
        self.asil_alacak = asil_alacak
        self.baslangic_tarihi = baslangic_tarihi
        self.bitis_tarihi = bitis_tarihi

    def faiz_hesabla(self, faiz_turu: str, faiz_tipi: str, sabit_oran: float = 0.0, oran_listesi: List[Dict] = None) -> Dict:
        """
        Faiz türü ve tipine göre (Kademeli vs Sabit) faiz hesabı yapar.
        """
        toplam_faiz = 0.0
        detaylar = []
        toplam_gun = (self.bitis_tarihi - self.baslangic_tarihi).days

        if toplam_gun <= 0:
            return {"toplam_faiz": 0.0, "faiz_dokumu": []}

        # 1. Sabit Oranlı Faiz Hesabı (Akdi Faiz veya Özel Sabit Faizler)
        if faiz_tipi == "sabit":
            toplam_faiz = (self.asil_alacak * sabit_oran * toplam_gun) / 36500
            detaylar.append({
                "baslangic": self.baslangic_tarihi.strftime("%Y-%m-%d"),
                "bitis": self.bitis_tarihi.strftime("%Y-%m-%d"),
                "gun": toplam_gun,
                "oran": sabit_oran,
                "tutar": round(toplam_faiz, 2)
            })
        
        # 2. Değişken (Kademeli) Faiz Hesabı
        else:
            if oran_listesi:
                for dilim in oran_listesi:
                    bas = max(self.baslangic_tarihi, dilim["baslangic"])
                    bit = min(self.bitis_tarihi, dilim["bitis"])

                    if bas < bit:
                        gun_sayisi = (bit - bas).days
                        faiz_tutari = (self.asil_alacak * dilim["oran"] * gun_sayisi) / 36500
                        toplam_faiz += faiz_tutari
                        
                        detaylar.append({
                            "baslangic": bas.strftime("%Y-%m-%d"),
                            "bitis": bit.strftime("%Y-%m-%d"),
                            "gun": gun_sayisi,
                            "oran": dilim["oran"],
                            "tutar": round(faiz_tutari, 2)
                        })

        return {
            "toplam_faiz": round(toplam_faiz, 2),
            "faiz_dokumu": detaylar
        }

    def harclari_hesabla(self, basvurma_harci_ekle: bool, pesin_harc_ekle: bool, tahsil_harci_safhasi: str) -> Dict:
        """Harç kalemlerini hesaplar."""
        pesin_harc = round(self.asil_alacak * 0.005, 2) if pesin_harc_ekle else 0.0
        basvurma_harci = GUNCEL_MAKTU_HARCLAR["basvurma_harci"] if basvurma_harci_ekle else 0.0

        tahsil_oranlari = {
            "hicbiri": 0.0,
            "haciz_oncesi": 4.55,
            "haciz_sonrasi": 9.10,
            "satis_sonrasi": 11.38
        }
        tahsil_orani = tahsil_oranlari.get(tahsil_harci_safhasi, 0.0)
        tahsil_harci = round((self.asil_alacak * tahsil_orani) / 100, 2)

        toplam_harc = round(pesin_harc + basvurma_harci + tahsil_harci, 2)

        return {
            "pesin_harc": pesin_harc,
            "basvurma_harci": basvurma_harci,
            "tahsil_harci_orani": tahsil_orani,
            "tahsil_harci": tahsil_harci,
            "toplam_harc": toplam_harc
        }

    def vekalet_ucreti_hesabla(self) -> Dict:
        """AAÜT İcra Vekalet Ücreti (KDV'siz Sabit Tarife)."""
        kalan_alacak = self.asil_alacak
        toplam_ucret = 0.0

        for dilim in AAUT_DILIMLERI:
            if kalan_alacak <= 0:
                break
            islenen_tutar = min(kalan_alacak, dilim["limit"])
            ucret = (islenen_tutar * dilim["oran"]) / 100
            toplam_ucret += ucret
            kalan_alacak -= islenen_tutar

        return {"toplam_vekalet_ucreti": round(toplam_ucret, 2)}
# core/rates.py
from datetime import date

# Yasal Faiz Geçmişi (3095 s. Kanun)
YASAL_FAIZ_ORANLARI = [
    {"baslangic": date(2024, 6, 1), "bitis": date(2099, 12, 31), "oran": 24.0},
    {"baslangic": date(2006, 1, 1), "bitis": date(2024, 5, 31), "oran": 9.0},
]

# Ticari (Avans) Faiz Geçmişi (TCMB)
AVANS_FAIZ_ORANLARI = [
    {"baslangic": date(2024, 4, 1), "bitis": date(2099, 12, 31), "oran": 52.5},
    {"baslangic": date(2023, 12, 23), "bitis": date(2024, 3, 31), "oran": 48.0},
]

# Güncel Maktu Harçlar (Her yıl Harçlar Kanunu Genel Tebliği ile güncellenir)
GUNCEL_MAKTU_HARCLAR = {
    "basvurma_harci": 427.60,      # İcra Takip Başvurma Harcı
    "vekalet_harci": 60.50,         # İcra Vekalet Harcı
    "baro_pulu": 96.00              # Vekaletname Baro Pulu
}

# AAÜT (Avukatlık Asgari Ücret Tarifesi) Kademeli Dilimleri (İcra Takipleri İçin)
# Her dilim: (Limit, Oran %)
AAUT_DILIMLERI = [
    {"limit": 400000.0, "oran": 16.0},      # İlk 400.000 TL için %16
    {"limit": 400000.0, "oran": 15.0},      # Sonraki 400.000 TL için %15
    {"limit": 800000.0, "oran": 14.0},      # Sonraki 800.000 TL için %14
    {"limit": 1200000.0, "oran": 11.0},     # Sonraki 1.200.000 TL için %11
    {"limit": 1600000.0, "oran": 8.0},      # Sonraki 1.600.000 TL için %8
    {"limit": 2000000.0, "oran": 5.0},      # Sonraki 2.000.000 TL için %5
    {"limit": 2000000.0, "oran": 3.0},      # Sonraki 2.000.000 TL için %3
    {"limit": float("inf"), "oran": 1.0}    # Üzeri için %1
]
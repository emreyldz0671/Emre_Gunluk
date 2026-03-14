#!/usr/bin/env python3
"""
WaveTrend DİP AL Sinyal Tarayıcı — BIST 600
--------------------------------------------
Kurulum: pip install yfinance pandas requests
Çalıştırma: python wavetrend_bist_scanner.py
"""

import yfinance as yf
import pandas as pd
import requests
import time
from datetime import datetime

# ============================================================
#  ✏️  BURAYA KENDİ BİLGİLERİNİ GİR
# ============================================================
import os
TELEGRAM_TOKEN   = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# ============================================================
#  ⚙️  İNDİKATÖR AYARLARI (Pine Script ile aynı)
# ============================================================
N1             = 10       # Channel Length
N2             = 21       # Average Length
TRIGGER_LEVEL  = -45.0    # Başarısız Sinyal Sınırı
TARGET_CROSS   = 3        # Kaçıncı AL sinyali özel olsun

# ============================================================
#  📋  BIST HİSSELERİ (yfinance için .IS eki)
# ============================================================
BIST_SEMBOLLER = [
    "ACSEL.IS","ADEL.IS","ADESE.IS","AEFES.IS","AFYON.IS","AGESA.IS",
    "AGHOL.IS","AGYO.IS","AKBNK.IS","AKCNS.IS","AKENR.IS","AKFGY.IS",
    "AKFYE.IS","AKGRT.IS","AKMGY.IS","AKSA.IS","AKSEN.IS","AKSGY.IS",
    "AKSUE.IS","AKTIF.IS","ALARK.IS","ALBRK.IS","ALFAS.IS","ALGYO.IS",
    "ALKA.IS","ALKIM.IS","ALKLC.IS","ALMAD.IS","ALTINS.IS","ALYAG.IS",
    "ANACM.IS","ANELE.IS","ANEL.IS","ANHYT.IS","ANSGR.IS","ARASE.IS",
    "ARCLK.IS","ARDYZ.IS","ARENA.IS","ARSAN.IS","ASCEL.IS","ASELS.IS",
    "ASGYO.IS","ASTOR.IS","ASUZU.IS","ATAGY.IS","ATAKP.IS","ATATP.IS",
    "ATEKS.IS","ATLAS.IS","ATSYH.IS","AVGYO.IS","AVHOL.IS","AVOD.IS",
    "AVPGY.IS","AVTUR.IS","AYCES.IS","AYDEM.IS","AYEN.IS","AYES.IS",
    "AYGAZ.IS","AZTEK.IS","BAGFS.IS","BAKAB.IS","BANVT.IS","BARMA.IS",
    "BASCM.IS","BASGZ.IS","BAYRK.IS","BEGYO.IS","BERA.IS","BIENY.IS",
    "BIMAS.IS","BIOEN.IS","BIZIM.IS","BJKAS.IS","BKFIN.IS","BLCYT.IS",
    "BNTAS.IS","BOSSA.IS","BREZN.IS","BRISA.IS","BRKO.IS","BRMEN.IS",
    "BRKVY.IS","BRSAN.IS","BRYAT.IS","BSOKE.IS","BTCIM.IS","BUCIM.IS",
    "BURCE.IS","BURVA.IS","BVSAN.IS","BYDNR.IS","CANTE.IS","CASA.IS",
    "CCOLA.IS","CELHA.IS","CEMAS.IS","CEMTS.IS","CEOEM.IS","CIMSA.IS",
    "CLEBI.IS","CMBTN.IS","CMENT.IS","CONSE.IS","COSMO.IS","CRDFA.IS",
    "CRFSA.IS","CUSAN.IS","CVKMD.IS","CWENE.IS","DAGHL.IS","DAGI.IS",
    "DAPGM.IS","DARDL.IS","DENGE.IS","DERHL.IS","DESA.IS","DESPC.IS",
    "DEVA.IS","DGATE.IS","DGGYO.IS","DGRLS.IS","DITAS.IS","DMSAS.IS",
    "DNISI.IS","DOAS.IS","DOBUR.IS","DOCO.IS","DOGUB.IS","DOHOL.IS",
    "DOKTA.IS","DURDO.IS","DYOBY.IS","DZGYO.IS","ECILC.IS","ECZYT.IS",
    "EDATA.IS","EDIP.IS","EGEEN.IS","EGEPO.IS","EGGUB.IS","EGPRO.IS",
    "EGSER.IS","EKGYO.IS","EKIZ.IS","EKSUN.IS","ELITE.IS","EMKEL.IS",
    "EMNIS.IS","ENERY.IS","ENGYO.IS","ENKAI.IS","ENSRI.IS","ENTRA.IS",
    "EPLAS.IS","ERBOS.IS","ERCB.IS","EREGL.IS","ERSU.IS","ESCAR.IS",
    "ESCOM.IS","ESEN.IS","ETILR.IS","ETYAT.IS","EUHOL.IS","EUPWR.IS",
    "EUREN.IS","EUYO.IS","EYGYO.IS","FENER.IS","FLAP.IS","FMIZP.IS",
    "FONET.IS","FORMT.IS","FORTE.IS","FRIGO.IS","FROTO.IS","FZLGY.IS",
    "GARAN.IS","GARFA.IS","GEDIK.IS","GEDZA.IS","GENIL.IS","GENTS.IS",
    "GEREL.IS","GESAN.IS","GIPTA.IS","GLBMD.IS","GLCVY.IS","GLRYH.IS",
    "GLYHO.IS","GMTAS.IS","GOZDE.IS","GRSEL.IS","GRTRK.IS","GSDDE.IS",
    "GSDHO.IS","GSRAY.IS","GUBRF.IS","GWIND.IS","GZNMI.IS","HALKB.IS",
    "HATEK.IS","HDFGS.IS","HEDEF.IS","HEKTS.IS","HLGYO.IS","HKTM.IS",
    "HLSYN.IS","HOROZ.IS","HRKET.IS","HTTBT.IS","HUBVC.IS","HUNER.IS",
    "HURGZ.IS","ICBCT.IS","IEYHO.IS","IGDAS.IS","IHLGM.IS","IHEVA.IS",
    "IHGZT.IS","IHLAS.IS","IHLGM.IS","IHYAY.IS","IMASM.IS","INDES.IS",
    "INFO.IS","INGRM.IS","INTEM.IS","INVEO.IS","INVES.IS","IPEKE.IS",
    "ISATR.IS","ISBIR.IS","ISCTR.IS","ISFIN.IS","ISGSY.IS","ISGYO.IS",
    "ISMEN.IS","ISSEN.IS","ISYAT.IS","IZENR.IS","IZFAS.IS","IZINV.IS",
    "IZMDC.IS","JANTS.IS","KAPLM.IS","KAREL.IS","KARSN.IS","KARTN.IS",
    "KATMR.IS","KAYSE.IS","KBORU.IS","KCAER.IS","KCHOL.IS","KENT.IS",
    "KERVN.IS","KERVT.IS","KFEIN.IS","KGYO.IS","KLGYO.IS","KLKIM.IS",
    "KLMSN.IS","KLNMA.IS","KLRHO.IS","KLSER.IS","KMPUR.IS","KNFRT.IS",
    "KONKA.IS","KONTR.IS","KONYA.IS","KOPOL.IS","KORDS.IS","KOTON.IS",
    "KOZAA.IS","KOZAL.IS","KRDMA.IS","KRDMB.IS","KRDMD.IS","KRGYO.IS",
    "KRONT.IS","KRPLS.IS","KRSTL.IS","KRTEK.IS","KTLEV.IS","KTSKR.IS",
    "KUTPO.IS","KUYAS.IS","KZGYO.IS","LIDER.IS","LIDFA.IS","LILAK.IS",
    "LINK.IS","LKMNH.IS","LMKDC.IS","LOGO.IS","LRSHO.IS","LUKSK.IS",
    "MAALT.IS","MAGEN.IS","MAKIM.IS","MAKTK.IS","MANAGEMENT.IS","MANAS.IS",
    "MARBL.IS","MARKA.IS","MARTI.IS","MATUR.IS","MEDTR.IS","MEGAP.IS",
    "MEPET.IS","MERCN.IS","MERIT.IS","MERKO.IS","METRO.IS","METUR.IS",
    "MGROS.IS","MIATK.IS","MIPAZ.IS","MMCAS.IS","MNDRS.IS","MNDTR.IS",
    "MNVRL.IS","MOBTL.IS","MPARK.IS","MRGYO.IS","MRSHL.IS","MSGYO.IS",
    "MTRKS.IS","MTRYO.IS","MZHLD.IS","NATEN.IS","NETAS.IS","NIBAS.IS",
    "NTGAZ.IS","NTHOL.IS","NUGYO.IS","NUHCM.IS","OBAMS.IS","OBASE.IS",
    "ODAS.IS","OFSYM.IS","ONCSM.IS","ORCAY.IS","ORGE.IS","ORION.IS",
    "ORKGT.IS","OTKAR.IS","OTTO.IS","OYAKC.IS","OYAYO.IS","OYLUM.IS",
    "OZATD.IS","OZKGY.IS","OZRDN.IS","OZSUB.IS","PAGYO.IS","PAMEL.IS",
    "PAPIL.IS","PARSN.IS","PASEU.IS","PCILT.IS","PEKGY.IS","PENGD.IS",
    "PENTA.IS","PETKM.IS","PETUN.IS","PGSUS.IS","PINSU.IS","PKART.IS",
    "PKENT.IS","PLTUR.IS","PNLSN.IS","POLHO.IS","POLTK.IS","PRDGS.IS",
    "PRKAB.IS","PRKME.IS","PRZMA.IS","PSDTC.IS","PTOFS.IS","QNBFB.IS",
    "QNBFL.IS","RALYH.IS","RAYSG.IS","REEDR.IS","RGYAS.IS","RHOLT.IS",
    "RNPOL.IS","RODRG.IS","ROYAL.IS","RTALB.IS","RUBNS.IS","RYSAS.IS",
    "SAFKR.IS","SAMAT.IS","SANEL.IS","SANFM.IS","SANKO.IS","SARKY.IS",
    "SASA.IS","SAYAS.IS","SDTTR.IS","SEGMN.IS","SEGYO.IS","SEKFK.IS",
    "SEKUR.IS","SELEC.IS","SELGD.IS","SELVA.IS","SEYKM.IS","SILVR.IS",
    "SISE.IS","SKBNK.IS","SKTAS.IS","SKYLP.IS","SMART.IS","SMRTG.IS",
    "SNGYO.IS","SNKRN.IS","SNPAM.IS","SODSN.IS","SOKM.IS","SONME.IS",
    "SRVGY.IS","SSTEK.IS","SUMAS.IS","SUNTK.IS","SUWEN.IS","TABGD.IS",
    "TARKM.IS","TATEN.IS","TATGD.IS","TAVHL.IS","TBORG.IS","TCELL.IS",
    "TDGYO.IS","TEKTU.IS","TERA.IS","TEZOL.IS","THYAO.IS","TKFEN.IS",
    "TKNSA.IS","TLMAN.IS","TMPOL.IS","TMSN.IS","TNZTP.IS","TOASO.IS",
    "TRCAS.IS","TRGYO.IS","TRILC.IS","TSKB.IS","TSPOR.IS","TTKOM.IS",
    "TTRAK.IS","TUCLK.IS","TUDDF.IS","TURGZ.IS","TURSG.IS","TUPRS.IS",
    "UFUK.IS","ULKER.IS","ULUUN.IS","UMPAS.IS","UNLU.IS","USAK.IS",
    "USDTR.IS","UTPYA.IS","UZERB.IS","VAKBN.IS","VAKFN.IS","VAKKO.IS",
    "VANGD.IS","VAROL.IS","VESBE.IS","VESTL.IS","VKFYO.IS","VKGYO.IS",
    "VKING.IS","YAPRK.IS","YATAS.IS","YBTAS.IS","YEOTK.IS","YESIL.IS",
    "YGYO.IS","YKSLN.IS","YUNSA.IS","ZEDUR.IS","ZOREN.IS","ZRGYO.IS",
]

# ============================================================
#  📊  WAVETREND HESAPLAMA
# ============================================================
def hesapla_wavetrend(df, n1=N1, n2=N2):
    ap = (df['High'] + df['Low'] + df['Close']) / 3
    esa = ap.ewm(span=n1, adjust=False).mean()
    d = (ap - esa).abs().ewm(span=n1, adjust=False).mean()
    ci = (ap - esa) / (0.015 * d)
    tci = ci.ewm(span=n2, adjust=False).mean()
    wt1 = tci
    wt2 = wt1.rolling(4).mean()
    return wt1, wt2

# ============================================================
#  🔍  SİNYAL KONTROL
# ============================================================
def sinyal_var_mi(wt1, wt2, trigger=TRIGGER_LEVEL, target=TARGET_CROSS):
    cross_count = 0
    n = len(wt1)

    for i in range(1, n):
        # Sayaç sıfırlama: trigger seviyesinin üstüne çıktıysa
        if wt1.iloc[i] > trigger:
            cross_count = 0

        # Yukarı kesişim (bullCross) ve trigger altında
        bull_cross = (wt1.iloc[i-1] < wt2.iloc[i-1]) and (wt1.iloc[i] > wt2.iloc[i])
        if bull_cross and wt1.iloc[i] < trigger:
            cross_count += 1

        # Özel sinyal: hedef sayıya ulaştı
        if bull_cross and (wt1.iloc[i] < trigger) and (cross_count == target):
            # Son bara denk geliyorsa sinyal var
            if i == n - 1:
                return True, wt1.iloc[-1], wt2.iloc[-1]
            cross_count = 0  # Sinyalden sonra sıfırla

    return False, wt1.iloc[-1], wt2.iloc[-1]

# ============================================================
#  📱  TELEGRAM MESAJ GÖNDER
# ============================================================
def telegram_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    veri = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mesaj,
        "parse_mode": "HTML"
    }
    try:
        r = requests.post(url, data=veri, timeout=10)
        return r.status_code == 200
    except Exception as e:
        print(f"Telegram hatası: {e}")
        return False

# ============================================================
#  🚀  ANA TARAMA FONKSİYONU
# ============================================================
def tara():
    simdi = datetime.now().strftime("%d.%m.%Y %H:%M")
    print(f"\n{'='*50}")
    print(f"WaveTrend BIST Tarama Başladı — {simdi}")
    print(f"{'='*50}")

    sinyal_verenler = []
    hata_verenler = []

    for i, sembol in enumerate(BIST_SEMBOLLER):
        try:
            # Günlük veri çek (son 120 gün yeterli)
            df = yf.download(sembol, period="120d", interval="1d",
                             progress=False, auto_adjust=True)

            if df is None or len(df) < 50:
                continue

            wt1, wt2 = hesapla_wavetrend(df)
            sinyal, wt1_son, wt2_son = sinyal_var_mi(wt1, wt2)

            if sinyal:
                sinyal_verenler.append({
                    "sembol": sembol.replace(".IS", ""),
                    "wt1": round(float(wt1_son), 2),
                    "wt2": round(float(wt2_son), 2),
                    "kapanis": round(float(df['Close'].iloc[-1]), 2)
                })
                print(f"  ✅ SİNYAL: {sembol}")
            else:
                print(f"  — {sembol} ({i+1}/{len(BIST_SEMBOLLER)})", end="\r")

            # API'yi yormamak için küçük bekleme
            time.sleep(0.3)

        except Exception as e:
            hata_verenler.append(sembol)
            continue

    # Sonuçları Telegram'a gönder
    if sinyal_verenler:
        mesaj = f"🟢 <b>WaveTrend DİP AL Sinyalleri</b>\n"
        mesaj += f"📅 {simdi}\n"
        mesaj += f"{'─'*25}\n\n"

        for s in sinyal_verenler:
            mesaj += (f"📌 <b>{s['sembol']}</b>\n"
                      f"   Kapanış: {s['kapanis']} ₺\n"
                      f"   WT1: {s['wt1']} | WT2: {s['wt2']}\n\n")

        mesaj += f"\nToplam {len(sinyal_verenler)} hisse sinyal verdi."
        telegram_gonder(mesaj)
        print(f"\n✅ {len(sinyal_verenler)} hisse Telegram'a gönderildi!")
    else:
        # Sinyal yoksa da bilgi ver
        mesaj = f"ℹ️ <b>WaveTrend Tarama Tamamlandı</b>\n📅 {simdi}\n\nBugün sinyal veren hisse bulunamadı."
        telegram_gonder(mesaj)
        print("\nℹ️ Sinyal veren hisse yok.")

    print(f"\nTarama tamamlandı. Toplam: {len(BIST_SEMBOLLER)} hisse")

# ============================================================
#  ▶️  ÇALIŞTIR
# ============================================================
if __name__ == "__main__":
    tara()

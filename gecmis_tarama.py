#!/usr/bin/env python3
"""
WaveTrend GEÇMİŞ Sinyal Tarayıcı — Son 5 Gün
"""

import os
import yfinance as yf
import pandas as pd
import requests
import time
from datetime import datetime, timedelta

TELEGRAM_TOKEN   = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

N1             = 10
N2             = 21
TRIGGER_LEVEL  = -45.0
TARGET_CROSS   = 3
GECMIS_GUN     = 5  # Kaç günü geriye tarayalım

BIST_SEMBOLLER = [
    "QNBTR.IS","ASELS.IS","DSTKF.IS","GARAN.IS","ENKAI.IS","TUPRS.IS","KCHOL.IS","BIMAS.IS",
    "THYAO.IS","FROTO.IS","AKBNK.IS","ISCTR.IS","ISBTR.IS","VAKBN.IS","HALKB.IS","YKBNK.IS",
    "KLRHO.IS","TCELL.IS","HEDEF.IS","TTKOM.IS","TERA.IS","SAHOL.IS","CCOLA.IS","EREGL.IS",
    "ASTOR.IS","GUBRF.IS","TRALT.IS","KENT.IS","TOASO.IS","MAGEN.IS","ENJSA.IS","TURSG.IS",
    "SISE.IS","ISDMR.IS","KTLEV.IS","OYAKC.IS","SASA.IS","MGROS.IS","TAVHL.IS","KLNMA.IS",
    "AEFES.IS","QNBFK.IS","ZRGYO.IS","DOCO.IS","AKSEN.IS","PGSUS.IS","TRGYO.IS","ECILC.IS",
    "MPARK.IS","PASEU.IS","ENERY.IS","INVES.IS","ARCLK.IS","ODINE.IS","BRSAN.IS","DMLKT.IS",
    "EKGYO.IS","LIDER.IS","UFUK.IS","AGHOL.IS","ISMEN.IS","LYDHO.IS","TABGD.IS","PEKGY.IS",
    "RYGYO.IS","BRYAT.IS","AHGAZ.IS","AYGAZ.IS","TRMET.IS","ANSGR.IS","DOHOL.IS","BSOKE.IS",
    "RGYAS.IS","GLRMK.IS","SELEC.IS","ANHYT.IS","PETKM.IS","TBORG.IS","NUHCM.IS","RALYH.IS",
    "CIMSA.IS","TTRAK.IS","OTKAR.IS","CVKMD.IS","CLEBI.IS","YGGYO.IS","IEYHO.IS","AKSA.IS",
    "GENIL.IS","ULKER.IS","AGESA.IS","AKCNS.IS","DOAS.IS","ALARK.IS","EFOR.IS","DAPGM.IS",
    "BASGZ.IS","BTCIM.IS","TSKB.IS","TEHOL.IS","GRSEL.IS","KRDMA.IS","KRDMD.IS","KRDMB.IS",
    "RYSAS.IS","RAYSG.IS","MAVI.IS","SOKM.IS","GRTHO.IS","LYDYE.IS","CWENE.IS","TKFEN.IS",
    "ECZYT.IS","ALKLC.IS","SARKY.IS","PAHOL.IS","CMENT.IS","GLYHO.IS","ADGYO.IS","TRENJ.IS",
    "BRISA.IS","SKBNK.IS","KUYAS.IS","VERUS.IS","GUNDG.IS","AKFYE.IS","HEKTS.IS","TRHOL.IS",
    "ARASE.IS","AKFIS.IS","IZENR.IS","CEMZY.IS","MOGAN.IS","EUPWR.IS","KLYPV.IS","KCAER.IS",
    "BMSTL.IS","OBAMS.IS","NTHOL.IS","HLGYO.IS","GESAN.IS","AKSGY.IS","ALBRK.IS","NETCD.IS",
    "ISGYO.IS","ARMGD.IS","KONYA.IS","OZKGY.IS","ENTRA.IS","MIATK.IS","OYYAT.IS","POLTK.IS",
    "AVPGY.IS","KLKIM.IS","ENSRI.IS","FENER.IS","BINBN.IS","LILAK.IS","EGEEN.IS","SUNTK.IS",
    "LMKDC.IS","YEOTK.IS","BFREN.IS","AYDEM.IS","MEGMT.IS","AYCES.IS","ASUZU.IS","FZLGY.IS",
    "ISKPL.IS","ECOGR.IS","OZATD.IS","CRFSA.IS","BALSU.IS","BANVT.IS","EGPRO.IS","TCKRC.IS",
    "MRSHL.IS","CANTE.IS","GSRAY.IS","SNGYO.IS","ALTNY.IS","POLHO.IS","ULUSE.IS","ZOREN.IS",
    "PSGYO.IS","KAYSE.IS","AHSGY.IS","DOFRB.IS","ALFAS.IS","IHAAS.IS","ESCAR.IS","TATEN.IS",
    "GWIND.IS","ZERGY.IS","ISFIN.IS","KLSER.IS","ARDYZ.IS","SMRTG.IS","KZBGY.IS","SDTTR.IS",
    "LOGO.IS","KSTUR.IS","AKGRT.IS","BARMA.IS","ICBCT.IS","TMSN.IS","KOTON.IS","PATEK.IS",
    "YYLGD.IS","DEVA.IS","JANTS.IS","AKFGY.IS","VESBE.IS","HTTBT.IS","EGGUB.IS","KONTR.IS",
    "BERA.IS","KORDS.IS","BULGS.IS","SONME.IS","A1CAP.IS","TRCAS.IS","MEYSU.IS","VAKFA.IS",
    "BINHO.IS","KBORU.IS","VAKKO.IS","MOPAS.IS","GEREL.IS","TUKAS.IS","ISGSY.IS","GARFA.IS",
    "MOBTL.IS","SRVGY.IS","ALGYO.IS","EBEBK.IS","EUREN.IS","IZMDC.IS","DGGYO.IS","VKGYO.IS",
    "BESLR.IS","SURGY.IS","VESTL.IS","VAKFN.IS","SEGMN.IS","BASCM.IS","PRKAB.IS","BUCIM.IS",
    "INGRM.IS","KARSN.IS","OFSYM.IS","TNZTP.IS","GLCVY.IS","PAGYO.IS","GMTAS.IS","IZFAS.IS",
    "GEDIK.IS","BIOEN.IS","VSNMD.IS","ATATR.IS","TUREX.IS","SNPAM.IS","GIPTA.IS","BIENY.IS",
    "NTGAZ.IS","ADEL.IS","ODAS.IS","ALKA.IS","QUAGR.IS","MAALT.IS","AKMGY.IS","GOZDE.IS",
    "KLGYO.IS","BOSSA.IS","HATSN.IS","ALCAR.IS","BLUME.IS","BIGTK.IS","CATES.IS","TEZOL.IS",
    "KGYO.IS","KOPOL.IS","AYEN.IS","DITAS.IS","TARKM.IS","TMPOL.IS","KAPLM.IS","CRDFA.IS",
    "KMPUR.IS","HRKET.IS","ATAKP.IS","INVEO.IS","BOBET.IS","ASGYO.IS","KAREL.IS","DOKTA.IS",
    "TSPOR.IS","GOKNR.IS","AKHAN.IS","AKENR.IS","ESEN.IS","ARSAN.IS","SMRVA.IS","PARSN.IS",
    "EGEPO.IS","BAHKM.IS","AGROT.IS","YIGIT.IS","KONKA.IS","MANAS.IS","AFYON.IS","BJKAS.IS",
    "YATAS.IS","GENTS.IS","EKOS.IS","INDES.IS","FORTE.IS","KRVGD.IS","YBTAS.IS","ENDAE.IS",
    "KATMR.IS","MNDTR.IS","PLTUR.IS","GOLTS.IS","CGCAM.IS","SOKE.IS","ULUUN.IS","NATEN.IS",
    "BORSK.IS","EDATA.IS","DMRGD.IS","REEDR.IS","DESA.IS","KOCMT.IS","ONCSM.IS","BURVA.IS",
    "EGEGY.IS","UCAYM.IS","MEKAG.IS","MERIT.IS","ORGE.IS","BRKVY.IS","CEMTS.IS","KARTN.IS",
    "ADESE.IS","HOROZ.IS","PENTA.IS","SAFKR.IS","BIGEN.IS","LINK.IS","INTEM.IS","SUWEN.IS",
    "AYES.IS","ALKIM.IS","KIMMR.IS","ALCTL.IS","OZYSR.IS","ALVES.IS","BAGFS.IS","DARDL.IS",
    "TKNSA.IS","SEGYO.IS","TATGD.IS","GSDHO.IS","ORMA.IS","ARFYE.IS","TSGYO.IS","KZGYO.IS",
    "FMIZP.IS","AZTEK.IS","ERCB.IS","FONET.IS","GZNMI.IS","MHRGY.IS","YAPRK.IS","KUVVA.IS",
    "YUNSA.IS","BVSAN.IS","KLSYN.IS","DUNYH.IS","ESCOM.IS","USAK.IS","BLCYT.IS","DYOBY.IS",
    "MNDRS.IS","NETAS.IS","HURGZ.IS","PKENT.IS","GOODY.IS","ANELE.IS","ELITE.IS","CELHA.IS",
    "BIGCH.IS","PNLSN.IS","KUTPO.IS","ATATP.IS","GATEG.IS","CEMAS.IS","ONRYT.IS","HDFGS.IS",
    "BRLSM.IS","MEDTR.IS","KRONT.IS","PETUN.IS","KTSKR.IS","ERBOS.IS","MRGYO.IS","LKMNH.IS",
    "LIDFA.IS","SERNT.IS","PNSUT.IS","TURGG.IS","SAYAS.IS","BEGYO.IS","INFO.IS","BURCE.IS",
    "IMASM.IS","DCTTR.IS","MERCN.IS","MACKO.IS","MSGYO.IS","PAPIL.IS","EKSUN.IS","PINSU.IS",
    "HUNER.IS","RUZYE.IS","ISSEN.IS","OSMEN.IS","FORMT.IS","BYDNR.IS","SANKO.IS","CMBTN.IS",
    "PCILT.IS","METRO.IS","NUGYO.IS","DZGYO.IS","IHLAS.IS","KNFRT.IS","DERHL.IS","BEYAZ.IS",
    "YYAPI.IS","EMKEL.IS","KRGYO.IS","BAKAB.IS","GLRYH.IS","TEKTU.IS","PRKME.IS","LUKSK.IS",
    "RUBNS.IS","OZSUB.IS","NIBAS.IS","ARENA.IS","SKYLP.IS","FRIGO.IS","MARBL.IS","VBTYZ.IS",
    "MAKTK.IS","TRILC.IS","DOGUB.IS","LRSHO.IS","CONSE.IS","PAMEL.IS","SANFM.IS","TGSAS.IS",
    "ARTMS.IS","ATEKS.IS","OTTO.IS","UNLU.IS","KLMSN.IS","OZRDN.IS","DNISI.IS","DURKN.IS",
    "SELVA.IS","EDIP.IS","DAGI.IS","MARTI.IS","SNICA.IS","AGYO.IS","ANGEN.IS","EYGYO.IS",
    "INTEK.IS","BIZIM.IS","ULUFA.IS","EUHOL.IS","DGATE.IS","MTRKS.IS","EGSER.IS","IHLGM.IS",
    "VERTU.IS","BORLS.IS","MEPET.IS","OZGYO.IS","DOFER.IS","ISBIR.IS","DERIM.IS","RTALB.IS",
    "AKSUE.IS","BRKO.IS","TLMAN.IS","MAKIM.IS","SKYMD.IS","BMSCH.IS","VRGYO.IS","VANGD.IS",
    "DURDO.IS","MERKO.IS","KRSTL.IS","KERVN.IS","CUSAN.IS","DMSAS.IS","KFEIN.IS","OSTIM.IS",
    "PKART.IS","A1YEN.IS","ARZUM.IS","SKTAS.IS","YKSLN.IS","GSDDE.IS","SUMAS.IS","OBASE.IS",
    "PENGD.IS","TUCLK.IS","BNTAS.IS","DENGE.IS","KRPLS.IS","GLBMD.IS","GEDZA.IS","ZEDUR.IS",
    "HUBVC.IS","AVGYO.IS","DGNMO.IS","ISYAT.IS","AVHOL.IS","COSMO.IS","PRDGS.IS","TDGYO.IS",
    "BALAT.IS","MMCAS.IS","PRZMA.IS","EPLAS.IS","SODSN.IS","VKING.IS","HKTM.IS","YAYLA.IS",
    "IHGZT.IS","FADE.IS","RNPOL.IS","YESIL.IS","AVOD.IS","OYAYO.IS","BAYRK.IS","ACSEL.IS",
    "SMART.IS","SEKUR.IS","FLAP.IS","IZINV.IS","SEKFK.IS","ICUGS.IS","KRTEK.IS","SILVR.IS",
    "EKIZ.IS","ETILR.IS","PSDTC.IS","SEYKM.IS","EMNIS.IS","CEOEM.IS","HATEK.IS","VKFYO.IS",
    "YONGA.IS","DESPC.IS","AVTUR.IS","ULAS.IS","BRKSN.IS","ORCAY.IS","ERSU.IS","MEGAP.IS",
    "IHYAY.IS","IHEVA.IS","BRMEN.IS","OYLUM.IS","MZHLD.IS","SANEL.IS","AKYHO.IS","SAMAT.IS",
    "ATAGY.IS","RODRG.IS","IDGYO.IS","ATLAS.IS","GRNYO.IS","MARKA.IS","CASA.IS","ETYAT.IS",
    "MTRYO.IS","ATSYH.IS","EUKYO.IS","EUYO.IS","DIRIT.IS","ALTIN.IS","MARMR.IS","EMPAE.IS",
    "BESTE.IS","LXGYO.IS","ZGYO.IS","MCARD.IS","SVGYO.IS","GENKM.IS","FRMPL.IS",
]

def hesapla_wavetrend(df, n1=N1, n2=N2):
    ap = (df['High'] + df['Low'] + df['Close']) / 3
    esa = ap.ewm(span=n1, adjust=False).mean()
    d = (ap - esa).abs().ewm(span=n1, adjust=False).mean()
    ci = (ap - esa) / (0.015 * d)
    tci = ci.ewm(span=n2, adjust=False).mean()
    wt1 = tci
    wt2 = wt1.rolling(4).mean()
    return wt1, wt2

def sinyal_var_mi(wt1, wt2, trigger=TRIGGER_LEVEL, target=TARGET_CROSS):
    cross_count = 0
    n = len(wt1)
    for i in range(1, n):
        # Pine gibi ÖNCE sıfırla
        if wt1.iloc[i] > trigger:
            cross_count = 0
        bull_cross = (wt1.iloc[i-1] < wt2.iloc[i-1]) and (wt1.iloc[i] > wt2.iloc[i])
        # SONRA say
        if bull_cross and wt1.iloc[i] < trigger:
            cross_count += 1
        # Sinyal kontrolü
        if bull_cross and wt1.iloc[i] < trigger and cross_count == target:
            if i == n - 1:
                return True, wt1.iloc[-1], wt2.iloc[-1]
            cross_count = 0
    return False, wt1.iloc[-1], wt2.iloc[-1]

def telegram_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    veri = {"chat_id": TELEGRAM_CHAT_ID, "text": mesaj, "parse_mode": "HTML"}
    try:
        r = requests.post(url, data=veri, timeout=10)
        print(f"Telegram: {r.status_code}")
        return r.status_code == 200
    except Exception as e:
        print(f"Telegram hatası: {e}")
        return False

def gecmis_tara():
    simdi = datetime.now().strftime("%d.%m.%Y %H:%M")
    print(f"\n{'='*50}")
    print(f"GEÇMİŞ Tarama Başladı — Son {GECMIS_GUN} Gün")
    print(f"TOKEN: {'VAR ✅' if TELEGRAM_TOKEN else 'YOK ❌'}")
    print(f"{'='*50}")

    # Günlük sonuçlar dict'i
    gunluk_sinyaller = {}

    for i, sembol in enumerate(BIST_SEMBOLLER):
        try:
            df = yf.download(sembol, period="2y", interval="1d",
                             progress=False, auto_adjust=True)
            if df is None or len(df) < 50:
                continue

            wt1, wt2 = hesapla_wavetrend(df)
            n = len(wt1)

            # Son GECMIS_GUN günü kontrol et
            for gun_geri in range(GECMIS_GUN, 0, -1):
                hedef_idx = n - gun_geri
                if hedef_idx < 1:
                    continue

                tarih = df.index[hedef_idx]
                # Hafta sonu atla
                if tarih.weekday() >= 5:
                    continue

                tarih_str = tarih.strftime("%d.%m.%Y")

                if sinyal_var_mi_gun(wt1, wt2, hedef_idx):
                    if tarih_str not in gunluk_sinyaller:
                        gunluk_sinyaller[tarih_str] = []
                    gunluk_sinyaller[tarih_str].append({
                        "sembol": sembol.replace(".IS", ""),
                        "kapanis": round(float(df['Close'].iloc[hedef_idx]), 2)
                    })
                    print(f"  ✅ {tarih_str} — {sembol}")

            print(f"  — {sembol} ({i+1}/{len(BIST_SEMBOLLER)})", end="\r")
            time.sleep(0.3)

        except Exception as e:
            continue

    # Sonuçları Telegram'a gönder
    if gunluk_sinyaller:
        for tarih, hisseler in sorted(gunluk_sinyaller.items()):
            mesaj = f"📅 <b>{tarih} — Geçmiş Sinyaller</b>\n{'─'*25}\n\n"
            for h in hisseler:
                mesaj += f"📌 <b>{h['sembol']}</b> — {h['kapanis']} ₺\n"
            mesaj += f"\nToplam {len(hisseler)} hisse"
            telegram_gonder(mesaj)
            time.sleep(1)
    else:
        mesaj = f"ℹ️ Son {GECMIS_GUN} günde sinyal veren hisse bulunamadı."
        telegram_gonder(mesaj)

    print(f"\nTarama tamamlandı!")

if __name__ == "__main__":
    gecmis_tara()

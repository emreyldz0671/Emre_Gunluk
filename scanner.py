#!/usr/bin/env python3
"""
WaveTrend DİP AL Sinyal Tarayıcı — TradingView Verisi
"""

import os
import requests
import time
from datetime import datetime
import pandas as pd
from tvdatafeed import TvDatafeed, Interval

TELEGRAM_TOKEN   = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
TV_USERNAME      = os.environ.get("TV_USERNAME", "")
TV_PASSWORD      = os.environ.get("TV_PASSWORD", "")

N1             = 10
N2             = 21
TRIGGER_LEVEL  = -45.0
TARGET_CROSS   = 3

BIST_SEMBOLLER = [
    "QNBTR","ASELS","DSTKF","GARAN","ENKAI","TUPRS","KCHOL","BIMAS",
    "THYAO","FROTO","AKBNK","ISCTR","ISBTR","VAKBN","HALKB","YKBNK",
    "KLRHO","TCELL","HEDEF","TTKOM","TERA","SAHOL","CCOLA","EREGL",
    "ASTOR","GUBRF","TRALT","KENT","TOASO","MAGEN","ENJSA","TURSG",
    "SISE","ISDMR","KTLEV","OYAKC","SASA","MGROS","TAVHL","KLNMA",
    "AEFES","QNBFK","ZRGYO","DOCO","AKSEN","PGSUS","TRGYO","ECILC",
    "MPARK","PASEU","ENERY","INVES","ARCLK","ODINE","BRSAN","DMLKT",
    "EKGYO","LIDER","UFUK","AGHOL","ISMEN","LYDHO","TABGD","PEKGY",
    "RYGYO","BRYAT","AHGAZ","AYGAZ","TRMET","ANSGR","DOHOL","BSOKE",
    "RGYAS","GLRMK","SELEC","ANHYT","PETKM","TBORG","NUHCM","RALYH",
    "CIMSA","TTRAK","OTKAR","CVKMD","CLEBI","YGGYO","IEYHO","AKSA",
    "GENIL","ULKER","AGESA","AKCNS","DOAS","ALARK","EFOR","DAPGM",
    "BASGZ","BTCIM","TSKB","TEHOL","GRSEL","KRDMA","KRDMD","KRDMB",
    "RYSAS","RAYSG","MAVI","SOKM","GRTHO","LYDYE","CWENE","TKFEN",
    "ECZYT","ALKLC","SARKY","PAHOL","CMENT","GLYHO","ADGYO","TRENJ",
    "BRISA","SKBNK","KUYAS","VERUS","GUNDG","AKFYE","HEKTS","TRHOL",
    "ARASE","AKFIS","IZENR","CEMZY","MOGAN","EUPWR","KLYPV","KCAER",
    "BMSTL","OBAMS","NTHOL","HLGYO","GESAN","AKSGY","ALBRK","NETCD",
    "ISGYO","ARMGD","KONYA","OZKGY","ENTRA","MIATK","OYYAT","POLTK",
    "AVPGY","KLKIM","ENSRI","FENER","BINBN","LILAK","EGEEN","SUNTK",
    "LMKDC","YEOTK","BFREN","AYDEM","MEGMT","AYCES","ASUZU","FZLGY",
    "ISKPL","ECOGR","OZATD","CRFSA","BALSU","BANVT","EGPRO","TCKRC",
    "MRSHL","CANTE","GSRAY","SNGYO","ALTNY","POLHO","ULUSE","ZOREN",
    "PSGYO","KAYSE","AHSGY","DOFRB","ALFAS","IHAAS","ESCAR","TATEN",
    "GWIND","ZERGY","ISFIN","KLSER","ARDYZ","SMRTG","KZBGY","SDTTR",
    "LOGO","KSTUR","AKGRT","BARMA","ICBCT","TMSN","KOTON","PATEK",
    "YYLGD","DEVA","JANTS","AKFGY","VESBE","HTTBT","EGGUB","KONTR",
    "BERA","KORDS","BULGS","SONME","A1CAP","TRCAS","MEYSU","VAKFA",
    "BINHO","KBORU","VAKKO","MOPAS","GEREL","TUKAS","ISGSY","GARFA",
    "MOBTL","SRVGY","ALGYO","EBEBK","EUREN","IZMDC","DGGYO","VKGYO",
    "BESLR","SURGY","VESTL","VAKFN","SEGMN","BASCM","PRKAB","BUCIM",
    "INGRM","KARSN","OFSYM","TNZTP","GLCVY","PAGYO","GMTAS","IZFAS",
    "GEDIK","BIOEN","VSNMD","ATATR","TUREX","SNPAM","GIPTA","BIENY",
    "NTGAZ","ADEL","ODAS","ALKA","QUAGR","MAALT","AKMGY","GOZDE",
    "KLGYO","BOSSA","HATSN","ALCAR","BLUME","BIGTK","CATES","TEZOL",
    "KGYO","KOPOL","AYEN","DITAS","TARKM","TMPOL","KAPLM","CRDFA",
    "KMPUR","HRKET","ATAKP","INVEO","BOBET","ASGYO","KAREL","DOKTA",
    "TSPOR","GOKNR","AKHAN","AKENR","ESEN","ARSAN","SMRVA","PARSN",
    "EGEPO","BAHKM","AGROT","YIGIT","KONKA","MANAS","AFYON","BJKAS",
    "YATAS","GENTS","EKOS","INDES","FORTE","KRVGD","YBTAS","ENDAE",
    "KATMR","MNDTR","PLTUR","GOLTS","CGCAM","SOKE","ULUUN","NATEN",
    "BORSK","EDATA","DMRGD","REEDR","DESA","KOCMT","ONCSM","BURVA",
    "EGEGY","UCAYM","MEKAG","MERIT","ORGE","BRKVY","CEMTS","KARTN",
    "ADESE","HOROZ","PENTA","SAFKR","BIGEN","LINK","INTEM","SUWEN",
    "AYES","ALKIM","KIMMR","ALCTL","OZYSR","ALVES","BAGFS","DARDL",
    "TKNSA","SEGYO","TATGD","GSDHO","ORMA","ARFYE","TSGYO","KZGYO",
    "FMIZP","AZTEK","ERCB","FONET","GZNMI","MHRGY","YAPRK","KUVVA",
    "YUNSA","BVSAN","KLSYN","DUNYH","ESCOM","USAK","BLCYT","DYOBY",
    "MNDRS","NETAS","HURGZ","PKENT","GOODY","ANELE","ELITE","CELHA",
    "BIGCH","PNLSN","KUTPO","ATATP","GATEG","CEMAS","ONRYT","HDFGS",
    "BRLSM","MEDTR","KRONT","PETUN","KTSKR","ERBOS","MRGYO","LKMNH",
    "LIDFA","SERNT","PNSUT","TURGG","SAYAS","BEGYO","INFO","BURCE",
    "IMASM","DCTTR","MERCN","MACKO","MSGYO","PAPIL","EKSUN","PINSU",
    "HUNER","RUZYE","ISSEN","OSMEN","FORMT","BYDNR","SANKO","CMBTN",
    "PCILT","METRO","NUGYO","DZGYO","IHLAS","KNFRT","DERHL","BEYAZ",
    "YYAPI","EMKEL","KRGYO","BAKAB","GLRYH","TEKTU","PRKME","LUKSK",
    "RUBNS","OZSUB","NIBAS","ARENA","SKYLP","FRIGO","MARBL","VBTYZ",
    "MAKTK","TRILC","DOGUB","LRSHO","CONSE","PAMEL","SANFM","TGSAS",
    "ARTMS","ATEKS","OTTO","UNLU","KLMSN","OZRDN","DNISI","DURKN",
    "SELVA","EDIP","DAGI","MARTI","SNICA","AGYO","ANGEN","EYGYO",
    "INTEK","BIZIM","ULUFA","EUHOL","DGATE","MTRKS","EGSER","IHLGM",
    "VERTU","BORLS","MEPET","OZGYO","DOFER","ISBIR","DERIM","RTALB",
    "AKSUE","BRKO","TLMAN","MAKIM","SKYMD","BMSCH","VRGYO","VANGD",
    "DURDO","MERKO","KRSTL","KERVN","CUSAN","DMSAS","KFEIN","OSTIM",
    "PKART","A1YEN","ARZUM","SKTAS","YKSLN","GSDDE","SUMAS","OBASE",
    "PENGD","TUCLK","BNTAS","DENGE","KRPLS","GLBMD","GEDZA","ZEDUR",
    "HUBVC","AVGYO","DGNMO","ISYAT","AVHOL","COSMO","PRDGS","TDGYO",
    "BALAT","MMCAS","PRZMA","EPLAS","SODSN","VKING","HKTM","YAYLA",
    "IHGZT","FADE","RNPOL","YESIL","AVOD","OYAYO","BAYRK","ACSEL",
    "SMART","SEKUR","FLAP","IZINV","SEKFK","ICUGS","KRTEK","SILVR",
    "EKIZ","ETILR","PSDTC","SEYKM","EMNIS","CEOEM","HATEK","VKFYO",
    "YONGA","DESPC","AVTUR","ULAS","BRKSN","ORCAY","ERSU","MEGAP",
    "IHYAY","IHEVA","BRMEN","OYLUM","MZHLD","SANEL","AKYHO","SAMAT",
    "ATAGY","RODRG","IDGYO","ATLAS","GRNYO","MARKA","CASA","ETYAT",
    "MTRYO","ATSYH","EUKYO","EUYO","DIRIT","ALTIN","MARMR","EMPAE",
    "BESTE","LXGYO","ZGYO","MCARD","SVGYO","GENKM","FRMPL",
]

def hesapla_wavetrend(df):
    ap = (df['high'] + df['low'] + df['close']) / 3
    esa = ap.ewm(span=N1, adjust=False).mean()
    d = (ap - esa).abs().ewm(span=N1, adjust=False).mean()
    ci = (ap - esa) / (0.015 * d)
    tci = ci.ewm(span=N2, adjust=False).mean()
    wt1 = tci
    wt2 = wt1.rolling(4).mean()
    return wt1, wt2

def sinyal_var_mi(wt1, wt2):
    cross_count = 0
    n = len(wt1)
    for i in range(1, n):
        # Pine Script ile aynı sıra
        if wt1.iloc[i] > TRIGGER_LEVEL:
            cross_count = 0
        bull_cross = (wt1.iloc[i-1] < wt2.iloc[i-1]) and (wt1.iloc[i] > wt2.iloc[i])
        if bull_cross and wt1.iloc[i] < TRIGGER_LEVEL:
            cross_count += 1
        if bull_cross and wt1.iloc[i] < TRIGGER_LEVEL and cross_count == TARGET_CROSS:
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

def tara():
    simdi = datetime.now().strftime("%d.%m.%Y %H:%M")
    print(f"\n{'='*50}")
    print(f"WaveTrend BIST Tarama — {simdi}")
    print(f"TOKEN: {'VAR ✅' if TELEGRAM_TOKEN else 'YOK ❌'}")
    print(f"TV: {'VAR ✅' if TV_USERNAME else 'YOK ❌'}")
    print(f"{'='*50}")

    # TradingView bağlantısı
    try:
        tv = TvDatafeed(TV_USERNAME, TV_PASSWORD)
        print("TradingView bağlantısı kuruldu ✅")
    except Exception as e:
        print(f"TradingView bağlantı hatası: {e}")
        telegram_gonder(f"❌ TradingView bağlantı hatası: {e}")
        return

    sinyal_verenler = []

    for i, sembol in enumerate(BIST_SEMBOLLER):
        try:
            df = tv.get_hist(sembol, exchange='BIST',
                           interval=Interval.in_daily, n_bars=500)
            if df is None or len(df) < 50:
                continue

            wt1, wt2 = hesapla_wavetrend(df)
            sinyal, wt1_son, wt2_son = sinyal_var_mi(wt1, wt2)

            if sinyal:
                sinyal_verenler.append({
                    "sembol": sembol,
                    "wt1": round(float(wt1_son), 2),
                    "wt2": round(float(wt2_son), 2),
                    "kapanis": round(float(df['close'].iloc[-1]), 2)
                })
                print(f"  ✅ SİNYAL: {sembol}")
            else:
                print(f"  — {sembol} ({i+1}/{len(BIST_SEMBOLLER)})", end="\r")

            time.sleep(0.1)

        except Exception as e:
            print(f"  ⚠️ {sembol}: {e}")
            continue

    if sinyal_verenler:
        mesaj = f"🟢 <b>WaveTrend DİP AL Sinyalleri</b>\n📅 {simdi}\n{'─'*25}\n\n"
        for s in sinyal_verenler:
            mesaj += (f"📌 <b>{s['sembol']}</b>\n"
                      f"   Kapanış: {s['kapanis']} ₺\n"
                      f"   WT1: {s['wt1']} | WT2: {s['wt2']}\n\n")
        mesaj += f"Toplam {len(sinyal_verenler)} hisse sinyal verdi."
    else:
        mesaj = f"ℹ️ <b>WaveTrend Tarama Tamamlandı</b>\n📅 {simdi}\n\nBugün sinyal veren hisse bulunamadı."

    telegram_gonder(mesaj)
    print(f"\nTarama tamamlandı. Toplam: {len(BIST_SEMBOLLER)} hisse")

if __name__ == "__main__":
    tara()

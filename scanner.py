#!/usr/bin/env python3
"""
WaveTrend DİP AL Sinyal Tarayıcı — TradingView Verisi (Gömülü)
"""

import os
import datetime
import enum
import json
import logging
import random
import re
import string
import time
import requests
import pandas as pd
from websocket import create_connection

TELEGRAM_TOKEN   = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
TV_USERNAME      = os.environ.get("TV_USERNAME", "")
TV_PASSWORD      = os.environ.get("TV_PASSWORD", "")

N1             = 10
N2             = 21
TRIGGER_LEVEL  = -45.0
TARGET_CROSS   = 3

# ============================================================
#  TvDatafeed — Gömülü
# ============================================================
class Interval(enum.Enum):
    in_daily  = "1D"
    in_weekly = "1W"

class TvDatafeed:
    __sign_in_url   = 'https://www.tradingview.com/accounts/signin/'
    __ws_headers    = json.dumps({"Origin": "https://data.tradingview.com"})
    __signin_headers = {'Referer': 'https://www.tradingview.com'}
    __ws_timeout    = 10

    def __init__(self, username=None, password=None):
        self.token = self.__auth(username, password)
        if self.token is None:
            self.token = "unauthorized_user_token"
        self.ws = None
        self.session = "qs_" + ''.join(random.choices(string.ascii_lowercase, k=12))
        self.chart_session = "cs_" + ''.join(random.choices(string.ascii_lowercase, k=12))

    def __auth(self, username, password):
        if not username or not password:
            return None
        try:
            r = requests.post(self.__sign_in_url,
                              data={"username": username, "password": password, "remember": "on"},
                              headers=self.__signin_headers, timeout=10)
            return r.json()['user']['auth_token']
        except:
            return None

    def __create_connection(self):
        self.ws = create_connection(
            "wss://data.tradingview.com/socket.io/websocket",
            headers=self.__ws_headers, timeout=self.__ws_timeout)

    @staticmethod
    def __prepend_header(st):
        return "~m~" + str(len(st)) + "~m~" + st

    @staticmethod
    def __construct_message(func, param_list):
        return json.dumps({"m": func, "p": param_list}, separators=(",", ":"))

    def __create_message(self, func, paramList):
        return self.__prepend_header(self.__construct_message(func, paramList))

    def __send_message(self, func, args):
        self.ws.send(self.__create_message(func, args))

    @staticmethod
    def __create_df(raw_data, symbol):
        try:
            out = re.search('"s":\[(.+?)\}\]', raw_data).group(1)
            x = out.split(',{"')
            data = []
            for xi in x:
                xi = re.split("\[|:|,|\]", xi)
                ts = datetime.datetime.fromtimestamp(float(xi[4]))
                row = [ts]
                for i in range(5, 10):
                    try:
                        row.append(float(xi[i]))
                    except:
                        row.append(0.0)
                data.append(row)
            df = pd.DataFrame(data, columns=["datetime","open","high","low","close","volume"])
            df = df.set_index("datetime")
            return df
        except:
            return None

    def get_hist(self, symbol, exchange="NSE", interval=Interval.in_daily, n_bars=500):
        if ":" not in symbol:
            symbol = f"{exchange}:{symbol}"
        try:
            self.__create_connection()
            self.__send_message("set_auth_token", [self.token])
            self.__send_message("chart_create_session", [self.chart_session, ""])
            self.__send_message("quote_create_session", [self.session])
            self.__send_message("resolve_symbol", [
                self.chart_session, "symbol_1",
                '={"symbol":"' + symbol + '","adjustment":"splits","session":"regular"}'
            ])
            self.__send_message("create_series",
                [self.chart_session, "s1", "s1", "symbol_1", interval.value, n_bars])
            self.__send_message("switch_timezone", [self.chart_session, "exchange"])

            raw_data = ""
            while True:
                try:
                    result = self.ws.recv()
                    raw_data += result + "\n"
                except:
                    break
                if "series_completed" in result:
                    break
            self.ws.close()
            return self.__create_df(raw_data, symbol)
        except Exception as e:
            return None

# ============================================================
#  BIST HİSSELERİ
# ============================================================
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

# ============================================================
#  WAVETREND
# ============================================================
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

# ============================================================
#  TELEGRAM
# ============================================================
def telegram_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        r = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": mesaj, "parse_mode": "HTML"}, timeout=10)
        print(f"Telegram: {r.status_code}")
        return r.status_code == 200
    except Exception as e:
        print(f"Telegram hatası: {e}")
        return False

# ============================================================
#  ANA TARAMA
# ============================================================
def tara():
    simdi = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    print(f"\n{'='*50}")
    print(f"WaveTrend BIST Tarama — {simdi}")
    print(f"TOKEN: {'VAR ✅' if TELEGRAM_TOKEN else 'YOK ❌'}")
    print(f"TV: {'VAR ✅' if TV_USERNAME else 'YOK ❌'}")
    print(f"{'='*50}")

    try:
        tv = TvDatafeed(TV_USERNAME, TV_PASSWORD)
        print("TradingView bağlantısı ✅")
    except Exception as e:
        print(f"TV bağlantı hatası: {e}")
        telegram_gonder(f"❌ TradingView bağlantı hatası: {e}")
        return

    sinyal_verenler = []

    for i, sembol in enumerate(BIST_SEMBOLLER):
        try:
            df = tv.get_hist(sembol, exchange='BIST', interval=Interval.in_daily, n_bars=500)
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
            mesaj += f"📌 <b>{s['sembol']}</b> — {s['kapanis']} ₺\n   WT1: {s['wt1']} | WT2: {s['wt2']}\n\n"
        mesaj += f"Toplam {len(sinyal_verenler)} hisse sinyal verdi."
    else:
        mesaj = f"ℹ️ <b>WaveTrend Tarama Tamamlandı</b>\n📅 {simdi}\n\nBugün sinyal veren hisse bulunamadı."

    telegram_gonder(mesaj)
    print(f"\nTarama tamamlandı. Toplam: {len(BIST_SEMBOLLER)} hisse")

if __name__ == "__main__":
    tara()

"""Generate the bronze seed CSVs for the mock banking dbt project.

Six retail personas bank with us and transact with each other and with the merchants and
companies below, from 1 Aug to 29 Sep 2026 (Asia/Jakarta time). The random seed is fixed,
so re-running produces identical files:

    python3 scripts/generate_bronze_seeds.py
"""

import csv
import random
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

WIB = timezone(timedelta(hours=7))
START, END = date(2026, 8, 1), date(2026, 9, 29)
SEED_DIR = Path(__file__).resolve().parents[1] / "dbt" / "banking" / "seeds"

rng = random.Random(20260930)

# --- Customers ----------------------------------------------------------------------------
# Rizky and Siti are married, Maya is their daughter and Dewi is Siti's mother.
# Andi is Maya's friend from campus, and Budi runs the warung where they all eat.
PERSONAS = {
    # key: (cif, full_name, segment, merchant_category, date_of_birth, gender, city, occupation,
    #       kyc_risk_level, onboarded_at, updated_at)
    "andi": ("CIF10000001", "Andi Pratama", "MASS_AFFLUENT", "", "1999-03-14", "M", "Jakarta Selatan",
             "Software Engineer", "LOW", "2021-06-02 10:15:22", "2026-08-12 14:22:05"),
    "siti": ("CIF10000002", "Siti Rahayu", "MASS", "", "1981-11-02", "F", "Bekasi",
             "Homemaker", "LOW", "2019-02-11 09:03:41", "2019-02-11 09:03:41"),
    "budi": ("CIF10000003", "Budi Santoso", "SME", "FOOD_BEVERAGE", "1979-07-21", "M", "Depok",
             "Warung Owner", "MEDIUM", "2020-09-30 13:47:10", "2026-09-10 10:31:58"),
    "maya": ("CIF10000004", "Maya Putri Hidayat", "YOUTH", "", "2005-09-14", "F", "Depok",
             "University Student", "LOW", "2023-08-20 16:20:03", "2026-08-03 19:45:12"),
    "rizky": ("CIF10000005", "Rizky Hidayat", "PRIORITY", "", "1977-05-09", "M", "Bekasi",
              "Sales Director", "LOW", "2018-04-16 11:02:37", "2026-08-20 15:10:44"),
    "dewi": ("CIF10000006", "Dewi Lestari", "SENIOR", "", "1957-12-25", "F", "Bogor",
             "Retired Teacher", "LOW", "2016-01-05 08:41:29", "2016-01-05 08:41:29"),
}

MERCHANTS = {
    # key: (name, merchant_category)
    "indomaret": ("Indomaret", "MINIMARKET"),
    "alfamart": ("Alfamart", "MINIMARKET"),
    "tokopedia": ("Tokopedia", "ECOMMERCE"),
    "shopee": ("Shopee", "ECOMMERCE"),
    "loket": ("Loket.com", "ENTERTAINMENT"),
    "cgv": ("CGV Cinemas", "ENTERTAINMENT"),
    "spotify": ("Spotify", "DIGITAL_SUBSCRIPTION"),
    "netflix": ("Netflix", "DIGITAL_SUBSCRIPTION"),
    "claude": ("Claude Pro", "AI_SUBSCRIPTION"),
    "chatgpt": ("ChatGPT Plus", "AI_SUBSCRIPTION"),
    "traveloka": ("Traveloka", "TRAVEL"),
    "agoda": ("Agoda", "TRAVEL"),
    "kopken": ("Kopi Kenangan", "FOOD_BEVERAGE"),
    "gofood": ("GoFood", "FOOD_BEVERAGE"),
    "sate": ("Sate Khas Senayan", "RESTAURANT"),
    "sushitei": ("Sushi Tei", "RESTAURANT"),
    "sederhana": ("RM Sederhana", "RESTAURANT"),
    "pln": ("PLN Token Listrik", "UTILITIES"),
    "kimiafarma": ("Kimia Farma", "HEALTH"),
    "school": ("SD Tunas Bangsa", "EDUCATION"),
    "supplier": ("CV Sumber Pangan Jaya", "WHOLESALE"),
}

CORPORATES = {
    "employer_andi": "PT Nusantara Teknologi Digital",
    "employer_rizky": "PT Maju Distribusi Indonesia",
    "pension_fund": "Dana Pensiun Guru Nusantara",
    "qris_settlement": "PT Settlement QRIS Nusantara",
}

# --- Accounts -----------------------------------------------------------------------------
PERSONAL_ACCOUNTS = [
    # (account_number, owner, account_type, account_name, status, opened_at, updated_at)
    ("1001000011", "andi", "MAIN", "Tabungan Utama", "ACTIVE", "2021-06-02 10:18:40", "2021-06-02 10:18:40"),
    ("1001000012", "andi", "POCKET_SAVINGS", "Dana Darurat", "ACTIVE", "2022-01-10 20:11:05", "2022-01-10 20:11:05"),
    ("1001000013", "andi", "POCKET_SPENDING", "Konser & Hiburan", "ACTIVE", "2025-11-03 21:40:18", "2025-11-03 21:40:18"),
    ("1001000014", "andi", "POCKET_SAVINGS", "Mudik Lebaran", "CLOSED", "2025-04-15 19:05:51", "2026-08-05 12:36:09"),
    ("1001000021", "siti", "MAIN", "Tabungan Utama", "ACTIVE", "2019-02-11 09:07:12", "2019-02-11 09:07:12"),
    ("1001000022", "siti", "POCKET_SPENDING", "Belanja Bulanan", "ACTIVE", "2023-03-01 08:30:44", "2023-03-01 08:30:44"),
    ("1001000023", "siti", "POCKET_SAVINGS", "Biaya Sekolah Anak", "ACTIVE", "2024-06-17 21:02:19", "2024-06-17 21:02:19"),
    ("1001000031", "budi", "MAIN", "Tabungan Pribadi", "ACTIVE", "2020-09-30 13:50:02", "2020-09-30 13:50:02"),
    ("1001000032", "budi", "BUSINESS", "Usaha Warung Makan Budi", "ACTIVE", "2020-10-05 10:12:37", "2026-09-10 10:35:21"),
    ("1001000033", "budi", "POCKET_SAVINGS", "Modal Usaha", "ACTIVE", "2022-07-01 07:45:10", "2022-07-01 07:45:10"),
    ("1001000041", "maya", "MAIN", "Tabungan Utama", "ACTIVE", "2023-08-20 16:24:51", "2023-08-20 16:24:51"),
    ("1001000042", "maya", "POCKET_SPENDING", "Jajan Kampus", "ACTIVE", "2024-02-05 12:01:33", "2024-02-05 12:01:33"),
    ("1001000043", "maya", "POCKET_SAVINGS", "Nabung Konser", "ACTIVE", "2026-07-20 22:14:06", "2026-07-20 22:14:06"),
    ("1001000051", "rizky", "MAIN", "Tabungan Utama", "ACTIVE", "2018-04-16 11:05:59", "2018-04-16 11:05:59"),
    ("1001000052", "rizky", "POCKET_SAVINGS", "Liburan Keluarga", "ACTIVE", "2021-12-28 19:33:47", "2021-12-28 19:33:47"),
    ("1001000053", "rizky", "POCKET_SAVINGS", "Dana Pendidikan Anak", "ACTIVE", "2019-01-02 09:18:25", "2019-01-02 09:18:25"),
    ("1001000061", "dewi", "MAIN", "Tabungan Utama", "ACTIVE", "2016-01-05 08:45:03", "2016-01-05 08:45:03"),
    ("1001000062", "dewi", "POCKET_SAVINGS", "Tabungan Hari Tua", "ACTIVE", "2020-03-09 10:27:50", "2020-03-09 10:27:50"),
]

# Merchants and companies get a CIF and a settlement account too, so every transaction has
# a source and a beneficiary on both sides.
COUNTERPARTIES = {}  # key -> (cif, account_number, name, customer_type, merchant_category, onboarded_at)
for i, (key, (name, category)) in enumerate(MERCHANTS.items(), start=1):
    onboarded = f"{2015 + i % 6}-{1 + i % 12:02d}-{1 + i % 27:02d} 10:00:00"
    COUNTERPARTIES[key] = (f"CIF9{i:07d}", f"900100{i:04d}", name, "MERCHANT", category, onboarded)
for i, (key, name) in enumerate(CORPORATES.items(), start=len(MERCHANTS) + 1):
    onboarded = f"{2014 + i % 5}-{1 + i % 12:02d}-{1 + i % 27:02d} 10:00:00"
    COUNTERPARTIES[key] = (f"CIF9{i:07d}", f"900100{i:04d}", name, "CORPORATE", "", onboarded)

ACCOUNT_CIF = {acc: PERSONAS[owner][0] for acc, owner, *_ in PERSONAL_ACCOUNTS}
ACCOUNT_CIF.update({acc: cif for cif, acc, *_ in COUNTERPARTIES.values()})
M = {key: cp[1] for key, cp in COUNTERPARTIES.items()}  # counterparty key -> account number

# Persona accounts by nickname
ANDI, ANDI_DARURAT, ANDI_HIBURAN, ANDI_MUDIK = "1001000011", "1001000012", "1001000013", "1001000014"
SITI, SITI_BELANJA, SITI_SEKOLAH = "1001000021", "1001000022", "1001000023"
BUDI, BUDI_USAHA, BUDI_MODAL = "1001000031", "1001000032", "1001000033"
MAYA, MAYA_JAJAN, MAYA_KONSER = "1001000041", "1001000042", "1001000043"
RIZKY, RIZKY_LIBURAN, RIZKY_PENDIDIKAN = "1001000051", "1001000052", "1001000053"
DEWI, DEWI_HARI_TUA = "1001000061", "1001000062"

# --- Transactions -------------------------------------------------------------------------
transactions = []


def add(ts, source, beneficiary, amount, channel, txn_type, description, status="SUCCESS"):
    transactions.append((ts, source, beneficiary, amount, channel, txn_type, description, status))


def at(day, hh, mm, ss=None):
    return datetime(day.year, day.month, day.day, hh, mm, rng.randint(0, 59) if ss is None else ss, tzinfo=WIB)


def between(day, start_hour, end_hour):
    """Random time between two hours of `day`. end_hour > 24 spills past midnight."""
    seconds = rng.randint(int(start_hour * 3600), int(end_hour * 3600))
    return datetime(day.year, day.month, day.day, tzinfo=WIB) + timedelta(seconds=seconds)


def rupiah(low, high, step=500):
    return rng.randrange(low, high + 1, step)


def chance(p):
    return rng.random() < p


def payday(year, month):
    """Salaries land on the 25th, or the Friday before when it falls on a weekend."""
    d = date(year, month, 25)
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d


def minimarket(day, source, start_hour, end_hour, low, high, store=None):
    store = store or rng.choice(["indomaret", "alfamart"])
    branch = rng.choice(["Kemang Raya", "Margonda", "Harapan Indah", "Juanda", "Sudirman", "Pajajaran"])
    add(between(day, start_hour, end_hour), source, M[store], rupiah(low, high, 100), "QRIS", "PAYMENT",
        f"{MERCHANTS[store][0]} {branch}")


def online_order(day, when, source, shop, low, high, description):
    ts = when if isinstance(when, datetime) else between(day, *when)
    amount = rupiah(low, high, 100)
    if chance(0.04):  # declined first try, retried a couple of minutes later
        add(ts, source, M[shop], amount, "VIRTUAL_ACCOUNT", "PAYMENT", description, status="FAILED")
        ts += timedelta(minutes=rng.randint(1, 4), seconds=rng.randint(0, 59))
    add(ts, source, M[shop], amount, "VIRTUAL_ACCOUNT", "PAYMENT", description)


FLASH_SALE_DAYS = {date(2026, 8, 8), date(2026, 9, 9)}  # 8.8 and 9.9 twin-date sales
CONCERT_TICKET_WAR = date(2026, 8, 15)
CONCERT_DAY = date(2026, 9, 19)
MAYA_BIRTHDAY = date(2026, 9, 14)
BANDUNG_HOLIDAY = {date(2026, 8, 15), date(2026, 8, 16), date(2026, 8, 17)}
# Rizky's business trips: (first day, nights, city, booking day)
TRIPS = [
    (date(2026, 8, 11), 2, "Surabaya", date(2026, 8, 4)),
    (date(2026, 8, 26), 2, "Medan", date(2026, 8, 19)),
    (date(2026, 9, 15), 3, "Denpasar", date(2026, 9, 7)),
]
TRAVEL_DAYS = {first + timedelta(days=n) for first, nights, _, _ in TRIPS for n in range(nights + 1)}

day = START
while day <= END:
    weekday, weekend = day.weekday(), day.weekday() >= 5
    first_of_month = day.day == 1
    is_payday = day == payday(day.year, day.month)

    # ---- Andi: software engineer, lives on coffee, GoFood and online shopping ----
    if is_payday:
        add(at(day, 7, rng.randint(2, 20)), M["employer_andi"], ANDI, 25_000_000, "PAYROLL", "PAYROLL",
            "Gaji bulanan - PT Nusantara Teknologi Digital")
        add(at(day, 8, rng.randint(5, 40)), ANDI, ANDI_DARURAT, 5_000_000, "MOBILE_APP", "OWN_ACCOUNT_TRANSFER",
            "Nabung Dana Darurat")
        add(at(day, 8, rng.randint(41, 59)), ANDI, ANDI_HIBURAN, 1_500_000, "MOBILE_APP", "OWN_ACCOUNT_TRANSFER",
            "Isi kantong Konser & Hiburan")
    if day == date(2026, 8, 5):
        add(at(day, 12, 35, 41), ANDI_MUDIK, ANDI, 2_350_000, "MOBILE_APP", "OWN_ACCOUNT_TRANSFER",
            "Tutup kantong Mudik Lebaran")
    if day.day == 3:
        add(at(day, 3, rng.randint(5, 25)), ANDI, M["claude"], 330_000, "AUTO_DEBIT", "PAYMENT",
            "Claude Pro - monthly subscription")
    if day.day == 12:
        add(at(day, 2, rng.randint(30, 50)), ANDI, M["spotify"], 54_990, "AUTO_DEBIT", "PAYMENT",
            "Spotify Premium Individual")
    if not weekend and chance(0.6):
        add(between(day, 7.5, 9.5), ANDI, M["kopken"], rng.choice([28_000, 32_000, 38_000, 43_000]), "QRIS",
            "PAYMENT", "Kopi Kenangan - Kopi Kenangan Mantan")
    if not weekend and chance(0.55):
        add(between(day, 11.5, 13.25), ANDI, M["gofood"], rupiah(35_000, 95_000), "MOBILE_APP", "PAYMENT",
            "GoFood - makan siang")
    elif not weekend and chance(0.3):
        add(between(day, 12, 13.5), ANDI, BUDI_USAHA, rupiah(25_000, 45_000), "QRIS", "PAYMENT",
            "QRIS Warung Makan Budi")
    if chance(0.3):
        minimarket(day, ANDI, 19, 22.5, 15_000, 120_000)
    if day in FLASH_SALE_DAYS:
        online_order(day, (0, 0.2), ANDI, "tokopedia", 450_000, 1_800_000, f"Tokopedia - Flash Sale {day.month}.{day.month}")
    elif chance(0.12):
        online_order(day, (20, 24.5), ANDI, rng.choice(["tokopedia", "shopee"]), 150_000, 1_800_000,
                     "Belanja online - gadget & aksesoris")
    if day == date(2026, 8, 14):
        add(at(day, 22, 41), ANDI, ANDI_HIBURAN, 2_000_000, "MOBILE_APP", "OWN_ACCOUNT_TRANSFER",
            "Top up kantong konser - war tiket besok!")
    if day == CONCERT_TICKET_WAR:
        add(at(day, 10, 0, 7), ANDI_HIBURAN, M["loket"], 3_250_000, "VIRTUAL_ACCOUNT", "PAYMENT",
            "Loket.com - Tiket Konser CAT 1")
    if weekend and chance(0.3):
        add(between(day, 19, 21), ANDI_HIBURAN, M["cgv"], rng.choice([50_000, 100_000, 120_000]), "QRIS",
            "PAYMENT", "CGV Cinemas - tiket bioskop")
    if (weekend and chance(0.35)) or day == CONCERT_DAY:
        bill = rupiah(250_000, 750_000, 1_000)
        dinner = at(day, 18, rng.randint(0, 20)) if day == CONCERT_DAY else between(day, 18.5, 20.5)
        restaurant = "sushitei" if day == CONCERT_DAY else rng.choice(["sushitei", "sate"])
        add(dinner, ANDI, M[restaurant], bill, "DEBIT_CARD", "PAYMENT", f"{MERCHANTS[restaurant][0]} - dinner")
        if day == CONCERT_DAY or chance(0.4):  # Maya pays back her half
            add(dinner + timedelta(minutes=rng.randint(30, 90)), MAYA, ANDI, bill // 2, "MOBILE_APP",
                "P2P_TRANSFER", "Patungan makan")

    # ---- Siti: runs the household from her Belanja Bulanan pocket ----
    if day == payday(day.year, day.month) + timedelta(days=1):
        add(at(day, 9, rng.randint(0, 30)), RIZKY, SITI, 12_000_000, "MOBILE_APP", "P2P_TRANSFER", "Uang bulanan")
        add(at(day, 9, rng.randint(31, 59)), SITI, SITI_BELANJA, 4_000_000, "MOBILE_APP", "OWN_ACCOUNT_TRANSFER",
            "Isi Belanja Bulanan")
        add(at(day, 10, rng.randint(0, 20)), SITI, SITI_SEKOLAH, 1_250_000, "MOBILE_APP", "OWN_ACCOUNT_TRANSFER",
            "Tabungan SPP")
    if first_of_month:
        add(at(day, 7, rng.randint(30, 50)), SITI, MAYA, 2_500_000, "MOBILE_APP", "P2P_TRANSFER",
            "Uang saku bulanan Maya")
    if day.day == 10:
        add(between(day, 8, 10), SITI_SEKOLAH, M["school"], 1_250_000, "VIRTUAL_ACCOUNT", "BILL_PAYMENT",
            "SPP SD Tunas Bangsa")
    if day.day == 5:
        add(between(day, 20, 21.5), SITI, M["pln"], rng.choice([202_500, 302_500, 502_500]), "MOBILE_APP",
            "BILL_PAYMENT", "Token listrik PLN")
    if day.day == 28:
        add(at(day, 16, rng.randint(0, 59)), SITI, DEWI, 1_000_000, "MOBILE_APP", "P2P_TRANSFER", "Kiriman untuk Ibu")
    if chance(0.65):
        morning = chance(0.5)
        minimarket(day, SITI_BELANJA, 7 if morning else 16, 9.5 if morning else 19.5, 25_000, 350_000)
    if day == date(2026, 8, 16):
        minimarket(day, SITI_BELANJA, 9, 11, 250_000, 320_000, store="alfamart")  # prizes for lomba 17-an
    if day in FLASH_SALE_DAYS:
        for _ in range(2):
            online_order(day, (0, 0.25), SITI, "shopee", 60_000, 400_000, f"Shopee - {day.month}.{day.month} Sale")
    elif chance(0.2):
        online_order(day, (21, 24), SITI, "shopee", 45_000, 400_000, "Shopee - kebutuhan rumah")
    if not weekend and chance(0.12):
        add(between(day, 11, 13), SITI, BUDI_USAHA, rupiah(45_000, 120_000), "QRIS", "PAYMENT",
            "QRIS Warung Makan Budi - lauk")
    if chance(0.04):
        add(between(day, 10, 17), SITI, M["kimiafarma"], rupiah(40_000, 180_000, 100), "DEBIT_CARD", "PAYMENT",
            "Kimia Farma - obat")

    # ---- Budi: warung owner, busy business account ----
    if weekday < 6:  # warung open Monday to Saturday
        add(between(day, 23.5, 23.9), M["qris_settlement"], BUDI_USAHA,
            rupiah(1_400_000, 3_000_000) if weekday == 5 else rupiah(900_000, 2_200_000),
            "QRIS_SETTLEMENT", "MERCHANT_SETTLEMENT", "Settlement QRIS harian")
    if weekday in (0, 3):
        add(between(day, 6, 7.5), BUDI_USAHA, M["supplier"], rupiah(1_500_000, 4_200_000, 1_000), "MOBILE_APP",
            "PAYMENT", "Belanja bahan baku")
    if weekday == 5:
        add(between(day, 21, 22), BUDI_USAHA, BUDI, rupiah(2_000_000, 3_500_000, 50_000), "MOBILE_APP",
            "OWN_ACCOUNT_TRANSFER", "Tarik keuntungan mingguan")
    if day.day == 2:
        add(at(day, 20, rng.randint(0, 59)), BUDI_USAHA, BUDI_MODAL, 3_000_000, "MOBILE_APP",
            "OWN_ACCOUNT_TRANSFER", "Sisihkan modal usaha")
    if day.day == 6:
        add(between(day, 19, 21), BUDI, M["pln"], rng.choice([302_500, 502_500]), "MOBILE_APP", "BILL_PAYMENT",
            "Token listrik PLN - warung")
    if chance(0.2):
        minimarket(day, BUDI, 20, 22, 20_000, 150_000)

    # ---- Maya: university student, small but frequent spending ----
    if first_of_month:
        add(at(day, 8, rng.randint(0, 30)), MAYA, MAYA_JAJAN, 1_200_000, "MOBILE_APP", "OWN_ACCOUNT_TRANSFER",
            "Isi Jajan Kampus")
        add(at(day, 8, rng.randint(31, 59)), MAYA, MAYA_KONSER, 500_000, "MOBILE_APP", "OWN_ACCOUNT_TRANSFER",
            "Nabung konser")
    if day == date(2026, 8, 14):
        add(at(day, 21, rng.randint(0, 59)), MAYA, MAYA_KONSER, 750_000, "MOBILE_APP", "OWN_ACCOUNT_TRANSFER",
            "Tambah tabungan konser")
    if day == CONCERT_TICKET_WAR:
        add(at(day, 10, 0, 4), MAYA_KONSER, M["loket"], 1_750_000, "VIRTUAL_ACCOUNT", "PAYMENT",
            "Loket.com - Tiket Konser CAT 3", status="FAILED")
        add(at(day, 10, 2, 41), MAYA_KONSER, M["loket"], 1_750_000, "VIRTUAL_ACCOUNT", "PAYMENT",
            "Loket.com - Tiket Konser CAT 3")
    if not weekend and chance(0.55):
        add(between(day, 11.5, 13.5), MAYA_JAJAN, BUDI_USAHA, rupiah(18_000, 35_000), "QRIS", "PAYMENT",
            "QRIS Warung Makan Budi")
    if chance(0.35):
        minimarket(day, MAYA_JAJAN, 15, 21, 12_000, 65_000, store="alfamart")
    if chance(0.3):
        add(between(day, 14, 17), MAYA_JAJAN, M["kopken"], rng.choice([22_000, 27_000, 33_000, 38_000]), "QRIS",
            "PAYMENT", "Kopi Kenangan - es kopi susu")
    if chance(0.2):
        add(between(day, 21, 24.5), MAYA_JAJAN, M["gofood"], rupiah(25_000, 70_000), "MOBILE_APP", "PAYMENT",
            "GoFood - makan malam")
    if day.day == 14:
        add(at(day, 1, rng.randint(40, 59)), MAYA, M["spotify"], 34_990, "AUTO_DEBIT", "PAYMENT",
            "Spotify Premium Student")
    if day == date(2026, 9, 2):
        add(at(day, 22, 13), MAYA, M["claude"], 330_000, "DEBIT_CARD", "PAYMENT",
            "Claude Pro - first month (skripsi)")
    if day in FLASH_SALE_DAYS:
        online_order(day, (0, 0.2), MAYA, "shopee", 50_000, 250_000, f"Shopee - {day.month}.{day.month} Sale")
    elif chance(0.12):
        online_order(day, (19, 23.5), MAYA, "shopee", 35_000, 250_000, "Shopee - fashion")
    if day == MAYA_BIRTHDAY:
        add(at(day, 0, 0, 38), ANDI, MAYA, 150_000, "MOBILE_APP", "P2P_TRANSFER", "HBD Maya! Traktir kopi ya")
        add(at(day, 7, 12), RIZKY, MAYA, 1_000_000, "MOBILE_APP", "P2P_TRANSFER", "Selamat ulang tahun, Nak")
        add(at(day, 8, 5), DEWI, MAYA, 500_000, "MOBILE_APP", "P2P_TRANSFER", "Selamat ulang tahun cucuku")

    # ---- Rizky: sales director, travels for work and pays for family dinners ----
    if is_payday:
        add(at(day, 7, rng.randint(0, 15)), M["employer_rizky"], RIZKY, 65_000_000, "PAYROLL", "PAYROLL",
            "Gaji bulanan - PT Maju Distribusi Indonesia")
        add(at(day, 8, rng.randint(0, 30)), RIZKY, RIZKY_LIBURAN, 10_000_000, "MOBILE_APP", "OWN_ACCOUNT_TRANSFER",
            "Nabung liburan keluarga")
        add(at(day, 8, rng.randint(31, 59)), RIZKY, RIZKY_PENDIDIKAN, 5_000_000, "MOBILE_APP",
            "OWN_ACCOUNT_TRANSFER", "Dana pendidikan anak")
    if day.day == 7:
        add(at(day, 4, rng.randint(0, 30)), RIZKY, M["chatgpt"], 330_000, "AUTO_DEBIT", "PAYMENT",
            "ChatGPT Plus - monthly subscription")
    if day.day == 18:
        add(at(day, 3, rng.randint(0, 30)), RIZKY, M["netflix"], 186_000, "AUTO_DEBIT", "PAYMENT",
            "Netflix Premium")
    if day.day == 28:
        add(at(day, 16, rng.randint(0, 59)), RIZKY, DEWI, 2_000_000, "MOBILE_APP", "P2P_TRANSFER",
            "Untuk Ibu - bulanan")
    for first, nights, city, booked in TRIPS:
        if day == booked:
            ts = between(day, 10, 16)
            add(ts, RIZKY, M["traveloka"], rupiah(1_800_000, 3_900_000, 1_000), "VIRTUAL_ACCOUNT", "PAYMENT",
                f"Traveloka - tiket pesawat PP {city}")
            add(ts + timedelta(minutes=rng.randint(5, 20)), RIZKY, M[rng.choice(["traveloka", "agoda"])],
                nights * rupiah(1_100_000, 2_800_000, 10_000), "VIRTUAL_ACCOUNT", "PAYMENT",
                f"Hotel {city} - {nights} malam")
    if day in TRAVEL_DAYS:
        add(between(day, 19, 21.5), RIZKY, M[rng.choice(["sate", "sushitei"])], rupiah(750_000, 2_500_000, 1_000),
            "DEBIT_CARD", "PAYMENT", "Makan malam dengan klien")
    if day == date(2026, 8, 3):
        add(at(day, 20, rng.randint(0, 59)), RIZKY_LIBURAN, M["agoda"], 3_600_000, "VIRTUAL_ACCOUNT", "PAYMENT",
            "Agoda - hotel Bandung 2 malam (libur 17 Agustus)")
    if day in BANDUNG_HOLIDAY:
        add(between(day, 12, 14), RIZKY_LIBURAN, M["sederhana"], rupiah(450_000, 1_200_000, 1_000), "DEBIT_CARD",
            "PAYMENT", "Makan siang keluarga di Bandung")
    elif weekday == 6 and day not in TRAVEL_DAYS and chance(0.6):
        add(between(day, 18, 20.5), RIZKY, M[rng.choice(["sederhana", "sushitei", "sate"])],
            rupiah(450_000, 1_600_000, 1_000), "DEBIT_CARD", "PAYMENT", "Makan malam keluarga")
    if chance(0.05):
        add(between(day, 9, 20), RIZKY, M["kimiafarma"], rupiah(60_000, 250_000, 100), "DEBIT_CARD", "PAYMENT",
            "Kimia Farma - vitamin")

    # ---- Dewi: retired teacher, early riser, pension on the 1st ----
    if first_of_month:
        add(at(day, 6, rng.randint(0, 15)), M["pension_fund"], DEWI, 4_200_000, "PAYROLL", "PAYROLL",
            "Pembayaran pensiun bulanan")
        add(at(day, 9, rng.randint(0, 59)), DEWI, DEWI_HARI_TUA, 1_000_000, "MOBILE_APP", "OWN_ACCOUNT_TRANSFER",
            "Tabungan hari tua")
    if weekday == 1:
        add(between(day, 9, 11), DEWI, M["kimiafarma"], rupiah(85_000, 320_000, 100), "DEBIT_CARD", "PAYMENT",
            "Kimia Farma - obat rutin")
    if chance(0.3):
        minimarket(day, DEWI, 6.5, 10, 20_000, 150_000, store="indomaret")
    if day.day == 4:
        add(between(day, 8, 10), DEWI, M["pln"], rng.choice([102_500, 202_500]), "MOBILE_APP", "BILL_PAYMENT",
            "Token listrik PLN")
    if weekday == 6 and chance(0.15):
        add(between(day, 11.5, 13.5), DEWI, M["sederhana"], rupiah(300_000, 650_000, 1_000), "DEBIT_CARD",
            "PAYMENT", "Makan siang dengan cucu")

    day += timedelta(days=1)

# Transactions after midnight belong to the next business date; the extract only runs to END.
transactions = [t for t in transactions if t[0].date() <= END]
transactions.sort(key=lambda t: t[0])

# --- Write CSVs ---------------------------------------------------------------------------
SEED_DIR.mkdir(parents=True, exist_ok=True)


def write(name, header, rows):
    with open(SEED_DIR / f"{name}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"{name}: {len(rows)} rows")


def wib(ts):
    return f"{ts}+07:00"


write(
    "bronze_customer",
    ["cif", "full_name", "customer_type", "segment", "merchant_category", "date_of_birth", "gender", "city",
     "occupation", "kyc_risk_level", "onboarded_at", "updated_at"],
    [(cif, name, "INDIVIDUAL", segment, category, dob, gender, city, occupation, kyc, wib(onboarded), wib(updated))
     for cif, name, segment, category, dob, gender, city, occupation, kyc, onboarded, updated in PERSONAS.values()]
    + [(cif, name, ctype, ctype, category, "", "", "Jakarta", "", "LOW", wib(onboarded), wib(onboarded))
       for cif, _, name, ctype, category, onboarded in COUNTERPARTIES.values()],
)

write(
    "bronze_account",
    ["account_number", "cif", "account_type", "account_name", "currency", "status", "opened_at", "updated_at"],
    [(acc, PERSONAS[owner][0], acc_type, name, "IDR", status, wib(opened), wib(updated))
     for acc, owner, acc_type, name, status, opened, updated in PERSONAL_ACCOUNTS]
    + [(acc, cif, "MERCHANT_SETTLEMENT" if ctype == "MERCHANT" else "CORPORATE_OPERATING", f"{name} - Operasional",
        "IDR", "ACTIVE", wib(onboarded), wib(onboarded))
       for cif, acc, name, ctype, _, onboarded in COUNTERPARTIES.values()],
)

sequence_per_day = {}
rows = []
for ts, source, beneficiary, amount, channel, txn_type, description, status in transactions:
    sequence_per_day[ts.date()] = sequence_per_day.get(ts.date(), 0) + 1
    rows.append((
        f"TRX{ts:%Y%m%d}{sequence_per_day[ts.date()]:05d}",
        ts.isoformat(sep=" "),
        ACCOUNT_CIF[source], source, ACCOUNT_CIF[beneficiary], beneficiary,
        amount, "IDR", channel, txn_type, description, status,
    ))
write(
    "bronze_transaction",
    ["transaction_id", "transaction_ts", "source_cif", "source_account", "beneficiary_cif", "beneficiary_account",
     "amount", "currency", "channel", "transaction_type", "description", "status"],
    rows,
)

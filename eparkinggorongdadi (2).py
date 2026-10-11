# -*- coding: utf-8 -*-
"""
E-Parking Restaurant

Program sederhana untuk mencatat mobil/motor yang masuk dan keluar parkiran,
lalu menghitung biaya parkirnya.
"""

import re

HARGA_PER_JAM = 2000
GARIS = "============================"

# Daftar kendaraan yang sedang parkir.
# Bentuknya: { "B1234XYZ": {"waktu_masuk": "18.20", "menit_masuk": 1100, "slot": "A5"} }
parkir = {}


# ---------- Alat bantu kecil ----------

def baca_waktu(pertanyaan):
    """Minta waktu "jam.menit" (contoh 18.20) sampai benar.
    Hasilnya: (teks waktu, total menit sejak jam 00.00)."""
    while True:
        teks = input(pertanyaan).strip()
        try:
            jam, menit = map(int, teks.split("."))
        except ValueError:
            print("Format waktu salah, gunakan titik. Contoh: 18.20")
            continue

        if 0 <= jam <= 23 and 0 <= menit <= 59:
            return teks, jam * 60 + menit
        print("Waktu tidak valid, silahkan isi kembali")


def plat_formatnya_benar(plat):
    """Contoh plat yang benar: B1234XYZ, D1234AB, AB1234C."""
    return re.fullmatch(r"[A-Z]{1,2}[0-9]{4}[A-Z]{1,3}", plat) is not None


def slot_formatnya_benar(slot):
    """Slot yang benar: A1 sampai A99."""
    return re.fullmatch(r"A[0-9]{1,2}", slot) is not None and int(slot[1:]) >= 1


def daftar_slot_terisi():
    return [data["slot"] for data in parkir.values()]


# ---------- Kendaraan masuk ----------

def tanya_plat():
    while True:
        plat = input(" Masukkan Plat nomer anda: ").upper().strip()
        print("Slot yang terisi: ", daftar_slot_terisi())

        if plat in parkir:
            print("[error] : plat nomor tersebut sudah terdaftar. silahkan masukkan plat nomor anda dengan benar")
        elif not plat_formatnya_benar(plat):
            print("[error]: format plat nomor salah")
        else:
            return plat


def tanya_slot():
    while True:
        slot = input(" pilih slot parkir yang tersedia (A1 - A99): ").upper().strip()

        if slot in daftar_slot_terisi():
            print("\n Pemilihan slot gagal", slot, "Sudah terisi\n")
            print("=========== Silahkan isi kembali ===========\n")
        elif not slot_formatnya_benar(slot):
            print("pemilihan Slot tidak Valid")
            print("=========== Silahkan isi kembali ===========\n")
        else:
            print("\n==========\nPemilihan slot berhasil, silahkan masuk\n==========\n")
            return slot


def kendaraan_masuk():
    waktu_masuk, menit_masuk = baca_waktu(" masukkan waktu, (jam.menit) contoh: 18.20: ")
    plat = tanya_plat()
    slot = tanya_slot()

    parkir[plat] = {
        "waktu_masuk": waktu_masuk,
        "menit_masuk": menit_masuk,
        "slot": slot,
    }


# ---------- Kendaraan keluar ----------

def hitung_lama_parkir(menit_masuk, menit_keluar):
    """Hitung lama parkir dalam menit (minimal 1 menit).
    Kalau waktu keluar lebih kecil dari waktu masuk, berarti parkir sampai besok."""
    if menit_masuk > menit_keluar:
        menit_keluar += 24 * 60
    return max(menit_keluar - menit_masuk, 1)


def cetak_struk(plat, data, waktu_keluar, lama_jam, total_harga):
    print("------------ struk parkir ------------")
    print("Plat nomor           :", plat)
    print("waktu masuk          :", data["waktu_masuk"])
    print("waktu keluar         :", waktu_keluar)
    print("total jam masuk      :", lama_jam)
    print("harga parkir per jam :", HARGA_PER_JAM)
    print("Slot parkir          :", data["slot"])
    print("\ntotal harga        :", total_harga)
    print("--------------------------------------")
    print("  Terimakasih atas kunjungan anda \n")


def kendaraan_keluar():
    if not parkir:
        print("\n[Error]: tidak ada kendaraan masuk yang tercatat, silahkan pilih kembali")
        return

    plat = input("masukkan plat nomor (tanpa spasi): ").upper().strip()
    if plat not in parkir:
        print("\n[Error] : Kendaraan dengan plat tersebut tidak ditemukan di parkiran\n")
        return

    waktu_keluar, menit_keluar = baca_waktu(" masukkan waktu ketika keluar, (jam.menit) contoh: 18.20: ")

    data = parkir[plat]
    lama_menit = hitung_lama_parkir(data["menit_masuk"], menit_keluar)
    lama_jam = lama_menit / 60
    total_harga = int(HARGA_PER_JAM * lama_jam)

    cetak_struk(plat, data, waktu_keluar, lama_jam, total_harga)
    del parkir[plat]  # slot otomatis kosong lagi


# ---------- Menu utama ----------

def tampilkan_menu():
    print(GARIS)
    print(" e-parking Restaurant")
    print(GARIS)
    print("apakah kendaraan masuk atau keluar")
    print(" 1 - kendaraan masuk")
    print(" 2 - kendaraan keluar")
    print(" 3 - Exit program")
    print(GARIS)


def main():
    while True:
        tampilkan_menu()
        pilihan = input(" pilih 1, 2 atau 3 : ").strip()

        if pilihan == "1":
            kendaraan_masuk()
        elif pilihan == "2":
            kendaraan_keluar()
        elif pilihan == "3":
            print("terimakasih telah menggunakan program kami")
            break
        else:
            print("\033[31m Error: input tidak ada dalam menu\033[0m")


main()

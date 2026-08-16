#!/usr/bin/env python3

import os
import subprocess
import sys


HOME = os.path.expanduser("~")
SCRIPT = os.path.join(HOME, "termux-theme.py")


def run(cmd):
    try:
        subprocess.run(cmd, shell=True, check=False)
    except KeyboardInterrupt:
        print("\nDibatalkan.")


def main():
    print("\033[1;36m╭──────────────────────────────╮")
    print("│       TERMUX THEME           │")
    print("╰──────────────────────────────╯\033[0m")
    print()
    print("1. Jalankan tema")
    print("2. Keluar")
    print()

    try:
        pilihan = input("Pilih [1-2]: ").strip()
    except KeyboardInterrupt:
        print()
        return

    if pilihan == "1":
        print("\nMenjalankan tema...\n")

        # ==================================================
        # MASUKKAN KODE TEMA KAMU DI SINI
        # ==================================================

        print("\033[1;32mTema aktif.\033[0m")

    elif pilihan == "2":
        print("Keluar.")
        return

    else:
        print("\033[1;31mPilihan tidak valid.\033[0m")


if __name__ == "__main__":
    main()

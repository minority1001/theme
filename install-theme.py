#!/usr/bin/env python3

import os
import sys
import shutil
import tarfile
import urllib.request
import subprocess
from pathlib import Path

H = Path.home()
T = H / ".termux"
B = H / "bin"
FC = H / ".config/fish/conf.d"
FD = H / ".termux-themes/fonts"
BK = H / ".termux-backup"
SCRIPT = H / "termux-theme.py"
PROMPT = FC / "90-elmy0711.fish"

RAW = "https://raw.githubusercontent.com/minority1001/theme/main/install-theme.py"
FONT = "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/{}.tar.xz"

THEMES = {
"1":("Tokyo Night","JetBrainsMono","#1a1b26","#a9b1d6",
["#15161e","#f7768e","#73daca","#e0af68","#7aa2f7","#bb9af7","#7dcfff","#787c99",
"#414868","#f7768e","#73daca","#e0af68","#7aa2f7","#bb9af7","#7dcfff","#a9b1d6"]),

"2":("Dracula","FiraCode","#282a36","#f8f8f2",
["#21222c","#ff5555","#50fa7b","#f1fa8c","#bd93f9","#ff79c6","#8be9fd","#f8f8f2",
"#6272a4","#ff6e6e","#69ff94","#ffffa5","#d6acff","#ff92df","#a4ffff","#ffffff"]),

"3":("Nord","Hack","#2e3440","#d8dee9",
["#3b4252","#bf616a","#a3be8c","#ebcb8b","#81a1c1","#b48ead","#88c0d0","#e5e9f0",
"#4c566a","#bf616a","#a3be8c","#ebcb8b","#81a1c1","#b48ead","#8fbcbb","#eceff4"]),

"4":("Gruvbox","CascadiaCode","#282828","#ebdbb2",
["#282828","#cc241d","#98971a","#d79921","#458588","#b16286","#689d6a","#a89984",
"#928374","#fb4934","#b8bb26","#fabd2f","#83a598","#d3869b","#8ec07c","#ebdbb2"]),

"5":("Catppuccin","Iosevka","#1e1e2e","#cdd6f4",
["#45475a","#f38ba8","#a6e3a1","#f9e2af","#89b4fa","#f5c2e7","#94e2d5","#bac2de",
"#585b70","#f38ba8","#a6e3a1","#f9e2af","#89b4fa","#f5c2e7","#94e2d5","#a6adc8"]),

"6":("One Dark","Meslo","#282c34","#abb2bf",
["#282c34","#e06c75","#98c379","#e5c07b","#61afef","#c678dd","#56b6c2","#abb2bf",
"#5c6370","#e06c75","#98c379","#e5c07b","#61afef","#c678dd","#56b6c2","#ffffff"]),

"7":("Cyberpunk","VictorMono","#090014","#00ffff",
["#120024","#ff0055","#00ff9c","#ffe600","#00aaff","#ff00ff","#00ffff","#d8d8d8",
"#3b0057","#ff3366","#33ffbb","#ffff33","#33bbff","#ff33ff","#33ffff","#ffffff"]),

"8":("Solarized","RobotoMono","#002b36","#839496",
["#073642","#dc322f","#859900","#b58900","#268bd2","#d33682","#2aa198","#eee8d5",
"#002b36","#cb4b16","#586e75","#657b83","#839496","#6c71c4","#93a1a1","#fdf6e3"]),

"9":("Everforest","UbuntuMono","#2d353b","#d3c6aa",
["#343f44","#e67e80","#a7c080","#dbbc7f","#7fbbb3","#d699b6","#83c092","#d3c6aa",
"#475258","#e67e80","#a7c080","#dbbc7f","#7fbbb3","#d699b6","#83c092","#e9e8d2"]),

"10":("Monokai","Mononoki","#272822","#f8f8f2",
["#272822","#f92672","#a6e22e","#f4bf75","#66d9ef","#ae81ff","#a1efe4","#f8f8f2",
"#75715e","#f92672","#a6e22e","#f4bf75","#66d9ef","#ae81ff","#a1efe4","#f9f8f5"])
}


def setup():
    for p in (T,B,FC,FD):
        p.mkdir(parents=True,exist_ok=True)


def backup():
    BK.mkdir(parents=True,exist_ok=True)
    for n in ("colors.properties","font.ttf","termux.properties"):
        a,b=T/n,BK/n
        if a.exists() and not b.exists():
            shutil.copy2(a,b)


def write_colors(c):
    keys=[
        "color0","color1","color2","color3",
        "color4","color5","color6","color7",
        "color8","color9","color10","color11",
        "color12","color13","color14","color15"
    ]
    s=f"foreground={c[3]}\nbackground={c[2]}\ncursor={c[3]}\n"
    s+="".join(f"{k}={v}\n" for k,v in zip(keys,c[4]))
    (T/"colors.properties").write_text(s)


def write_fish(c):
    c1=c[4][1]
    c2=c[4][2]
    c3=c[4][3]
    c5=c[4][5]
    c6=c[4][6]

    s=f'''set -g fish_greeting ""
fish_add_path $HOME/bin

function tema
    python3 $HOME/termux-theme.py
end

function ll
    ls -lah $argv
end

function fish_prompt
    set_color {c6}
    echo -n (date "+%a %b %d %H:%M:%S")
    echo ""

    set_color {c5}
    echo -n "╭─"

    set_color {c1}
    echo -n "💖"

    set_color {c5}
    echo -n "ELMY0711"

    set_color {c1}
    echo -n "💜"

    set_color {c5}
    echo -n "─["

    set_color {c3}
    echo -n (prompt_pwd)

    set_color {c5}
    echo -n "]"
    echo ""

    set_color {c5}
    echo -n "╰──╼"

    set_color {c2}
    echo -n "╼ "

    set_color normal
end

function fish_right_prompt
end
'''
    PROMPT.write_text(s)


def write_keyboard():
    s='''extra-keys=[["bash ","python3 ","nano ","go run ","UP","END","PGUP","node "],[{macro:"python3 ~/termux-theme.py\\\\n",display:"tema"},"CTRL","BKSP","LEFT","DOWN","RIGHT","git clone ","curl -i "],["ls ","cd ","clear ","ENTER","ping ","git pull ","rm -rf ",{macro:"CTRL d",display:"exit"}]]'''
    (T/"termux.properties").write_text(s)


def write_command():
    p=B/"tema"
    p.write_text(
        '#!/data/data/com.termux/files/usr/bin/bash\n'
        'exec python3 "$HOME/termux-theme.py" "$@"\n'
    )
    p.chmod(0o755)


def install_fish():
    if shutil.which("fish"):
        return
    if shutil.which("pkg"):
        subprocess.run(
            ["pkg","install","fish","-y"],
            check=False
        )


def install_font(name):
    d=FD/name
    d.mkdir(parents=True,exist_ok=True)

    f=next(d.rglob("*.ttf"),None)

    if not f:
        a=d/f"{name}.tar.xz"
        try:
            urllib.request.urlretrieve(
                FONT.format(name),a
            )
            with tarfile.open(a,"r:xz") as z:
                z.extractall(d)
            a.unlink(missing_ok=True)
        except Exception as e:
            print(f"[!] Font {name}: gagal")
            return

        f=next(d.rglob("*.ttf"),None)

    if f:
        shutil.copy2(f,T/"font.ttf")


def reload():
    if shutil.which("termux-reload-settings"):
        subprocess.run(
            ["termux-reload-settings"],
            check=False
        )


def apply(n):
    c=THEMES[n]

    print()
    print(f"Tema : {c[0]}")
    print(f"Font : {c[1]}")

    backup()
    write_colors(c)
    write_fish(c)
    write_keyboard()
    write_command()
    install_font(c[1])
    reload()

    print("\n✓ Tema diterapkan")
    print("✓ config.fish aman")
    print("✓ Jalankan: exec fish")


def restore():
    if not BK.exists():
        print("Backup tidak ditemukan.")
        return

    for n in ("colors.properties","font.ttf","termux.properties"):
        a,b=BK/n,T/n
        if a.exists():
            shutil.copy2(a,b)

    reload()
    print("✓ Backup dipulihkan")


def menu():
    while True:
        os.system("clear")

        print("╭── ELMY0711 THEME ──╮")

        for n,c in THEMES.items():
            print(f"│ {n:>2}. {c[0]:<16}│")

        print("│ K. keyboard        │")
        print("│ R. restore         │")
        print("│ X. hapus prompt    │")
        print("│ Q. keluar          │")
        print("╰────────────────────╯")

        x=input("Pilih: ").strip().lower()

        if x in THEMES:
            apply(x)
            input("\nENTER...")

        elif x=="k":
            write_keyboard()
            reload()
            print("✓ Keyboard diperbarui")
            input("\nENTER...")

        elif x=="r":
            restore()
            input("\nENTER...")

        elif x=="x":
            if PROMPT.exists():
                PROMPT.unlink()
            print("✓ Prompt dihapus")
            input("\nENTER...")

        elif x=="q":
            break


def install():
    setup()
    backup()
    install_fish()

    try:
        if Path(__file__).exists() and Path(__file__).name != "termux-theme.py":
            shutil.copy2(__file__,SCRIPT)
        else:
            urllib.request.urlretrieve(RAW,SCRIPT)
    except Exception:
        try:
            urllib.request.urlretrieve(RAW,SCRIPT)
        except Exception:
            pass

    c=THEMES["1"]
    write_colors(c)
    write_fish(c)
    write_keyboard()
    write_command()
    install_font(c[1])
    reload()

    print()
    print("╭────────────────────────╮")
    print("│ ELMY0711 INSTALL OK    │")
    print("├────────────────────────┤")
    print("│ tema  : menu tema      │")
    print("│ exit  : Ctrl+D         │")
    print("│ fish  : aktif          │")
    print("│ config.fish : aman     │")
    print("╰────────────────────────╯")
    print()
    print("Jalankan: exec fish")


def main():
    setup()

    if len(sys.argv)>1:
        if sys.argv[1] in ("-i","--install"):
            install()
            return

    if not sys.stdin.isatty():
        install()
    else:
        menu()


main()

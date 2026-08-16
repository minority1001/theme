#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess
import urllib.request
import tarfile
from pathlib import Path

HOME = Path.home()
PREFIX = Path(os.environ.get(
    "PREFIX",
    "/data/data/com.termux/files/usr"
))

TERMUX = HOME / ".termux"
BIN = HOME / "bin"
FISH = HOME / ".config/fish"
CONFIG = FISH / "config.fish"
PROMPT = FISH / "ELMY0711-prompt.fish"

BACKUP = HOME / ".termux-backup"
FONT_DIR = HOME / ".termux-themes/fonts"
MAIN = HOME / "termux-theme.py"

PYTHON = PREFIX / "bin/python3"
BASH = PREFIX / "bin/bash"

RAW = (
    "https://raw.githubusercontent.com/"
    "minority1001/theme/main/install-theme.py"
)

FONT_URL = (
    "https://github.com/ryanoasis/nerd-fonts/"
    "releases/latest/download/{}.tar.xz"
)

THEMES = {
    "1": (
        "Tokyo Night",
        "Iosevka",
        "regular",
        "#1a1b26",
        "#a9b1d6",
        [
            "#15161e","#f7768e","#73daca","#e0af68",
            "#7aa2f7","#bb9af7","#7dcfff","#a9b1d6",
            "#414868","#f7768e","#73daca","#e0af68",
            "#7aa2f7","#bb9af7","#7dcfff","#c0caf5"
        ]
    ),

    "2": (
        "Dracula",
        "VictorMono",
        "italic",
        "#282a36",
        "#f8f8f2",
        [
            "#21222c","#ff5555","#50fa7b","#f1fa8c",
            "#bd93f9","#ff79c6","#8be9fd","#f8f8f2",
            "#6272a4","#ff6e6e","#69ff94","#ffffa5",
            "#d6acff","#ff92df","#a4ffff","#ffffff"
        ]
    ),

    "3": (
        "Nord",
        "Hack",
        "regular",
        "#2e3440",
        "#d8dee9",
        [
            "#3b4252","#bf616a","#a3be8c","#ebcb8b",
            "#81a1c1","#b48ead","#88c0d0","#e5e9f0",
            "#4c566a","#bf616a","#a3be8c","#ebcb8b",
            "#81a1c1","#b48ead","#8fbcbb","#eceff4"
        ]
    ),

    "4": (
        "Gruvbox",
        "CascadiaCode",
        "regular",
        "#282828",
        "#ebdbb2",
        [
            "#282828","#cc241d","#98971a","#d79921",
            "#458588","#b16286","#689d6a","#a89984",
            "#928374","#fb4934","#b8bb26","#fabd2f",
            "#83a598","#d3869b","#8ec07c","#ebdbb2"
        ]
    ),

    "5": (
        "Catppuccin",
        "Iosevka",
        "regular",
        "#1e1e2e",
        "#cdd6f4",
        [
            "#45475a","#f38ba8","#a6e3a1","#f9e2af",
            "#89b4fa","#f5c2e7","#94e2d5","#bac2de",
            "#585b70","#f38ba8","#a6e3a1","#f9e2af",
            "#89b4fa","#f5c2e7","#94e2d5","#cdd6f4"
        ]
    ),

    "6": (
        "One Dark",
        "Meslo",
        "regular",
        "#282c34",
        "#abb2bf",
        [
            "#282c34","#e06c75","#98c379","#e5c07b",
            "#61afef","#c678dd","#56b6c2","#abb2bf",
            "#5c6370","#e06c75","#98c379","#e5c07b",
            "#61afef","#c678dd","#56b6c2","#ffffff"
        ]
    ),

    "7": (
        "Cyberpunk",
        "JetBrainsMono",
        "regular",
        "#090014",
        "#00ffff",
        [
            "#120024","#ff0055","#00ff9c","#ffe600",
            "#00aaff","#ff00ff","#00ffff","#d8d8d8",
            "#3b0057","#ff3366","#33ffbb","#ffff33",
            "#33bbff","#ff33ff","#33ffff","#ffffff"
        ]
    ),

    "8": (
        "Solarized",
        "RobotoMono",
        "regular",
        "#002b36",
        "#839496",
        [
            "#073642","#dc322f","#859900","#b58900",
            "#268bd2","#d33682","#2aa198","#eee8d5",
            "#002b36","#cb4b16","#586e75","#657b83",
            "#839496","#6c71c4","#93a1a1","#fdf6e3"
        ]
    ),

    "9": (
        "Everforest",
        "UbuntuMono",
        "regular",
        "#2d353b",
        "#d3c6aa",
        [
            "#343f44","#e67e80","#a7c080","#dbbc7f",
            "#7fbbb3","#d699b6","#83c092","#d3c6aa",
            "#475258","#e67e80","#a7c080","#dbbc7f",
            "#7fbbb3","#d699b6","#83c092","#e9e8d2"
        ]
    ),

    "10": (
        "Monokai",
        "Mononoki",
        "regular",
        "#272822",
        "#f8f8f2",
        [
            "#272822","#f92672","#a6e22e","#f4bf75",
            "#66d9ef","#ae81ff","#a1efe4","#f8f8f2",
            "#75715e","#f92672","#a6e22e","#f4bf75",
            "#66d9ef","#ae81ff","#a1efe4","#f9f8f5"
        ]
    )
}


def setup():
    for p in (TERMUX, BIN, FISH, FONT_DIR):
        p.mkdir(parents=True, exist_ok=True)


def backup():
    BACKUP.mkdir(parents=True, exist_ok=True)

    files = [
        CONFIG,
        TERMUX / "colors.properties",
        TERMUX / "font.ttf",
        TERMUX / "termux.properties"
    ]

    for src in files:
        if src.exists():
            dst = BACKUP / src.name
            if not dst.exists():
                shutil.copy2(src, dst)


def write_colors(theme):
    _, _, _, bg, fg, palette = theme

    names = [
        f"color{i}" for i in range(16)
    ]

    text = (
        f"background={bg}\n"
        f"foreground={fg}\n"
        f"cursor={fg}\n"
    )

    for name, value in zip(names, palette):
        text += f"{name}={value}\n"

    (TERMUX / "colors.properties").write_text(text)


def write_prompt(theme):
    p = theme[5]

    c1 = p[1]
    c2 = p[2]
    c3 = p[3]
    c5 = p[5]
    c6 = p[6]

    text = f'''function fish_prompt
    set_color {c6}
    echo -n (date "+%d %b %H:%M")
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
    echo -n "╰─"

    set_color {c2}
    echo -n "> "

    set_color normal
end

function fish_right_prompt
end
'''

    PROMPT.write_text(text)


def hook_prompt():
    CONFIG.touch()

    hook = (
        "source ~/.config/fish/"
        "ELMY0711-prompt.fish"
    )

    text = CONFIG.read_text()

    if hook not in text:
        if text and not text.endswith("\n"):
            text += "\n"

        text += (
            "\n# ELMY0711 PROMPT\n"
            f"{hook}\n"
        )

        CONFIG.write_text(text)


def write_keyboard():
    text = (
        'extra-keys=['
        '["bash ","python3 ","nano ","go run ",'
        '"UP","END","PGUP","node "],'
        '["tema ","CTRL","BKSP","LEFT","DOWN",'
        '"RIGHT","git clone ","curl -i "],'
        '["ls ","cd ","clear ","ENTER","ping ",'
        '"git pull ","rm -rf ",'
        '{macro:"CTRL d",display:"exit"}]'
        ']'
    )

    (TERMUX / "termux.properties").write_text(text)


def write_tema():
    file = BIN / "tema"

    text = (
        f"#!{BASH}\n"
        f'exec "{PYTHON}" '
        '"$HOME/termux-theme.py" "$@"\n'
    )

    file.write_text(text)
    file.chmod(0o755)


def install_font(name, style):
    folder = FONT_DIR / name
    folder.mkdir(parents=True, exist_ok=True)

    wanted = {
        "italic": (
            f"{name}-Italic.ttf",
            f"{name}_Italic.ttf",
            f"{name}Italic.ttf"
        ),
        "regular": (
            f"{name}-Regular.ttf",
            f"{name}_Regular.ttf",
            f"{name}.ttf"
        )
    }

    font = None

    for filename in wanted[style]:
        found = list(folder.rglob(filename))
        if found:
            font = found[0]
            break

    if font is None:
        archive = folder / f"{name}.tar.xz"

        try:
            urllib.request.urlretrieve(
                FONT_URL.format(name),
                archive
            )

            with tarfile.open(
                archive,
                "r:xz"
            ) as tar:
                tar.extractall(folder)

            archive.unlink(missing_ok=True)

        except Exception as e:
            print("! Font gagal:", e)
            return

        for filename in wanted[style]:
            found = list(folder.rglob(filename))
            if found:
                font = found[0]
                break

    if font:
        shutil.copy2(
            font,
            TERMUX / "font.ttf"
        )

        print(
            f"✓ Font {name} {style}"
        )
    else:
        print(
            f"! {name} {style} tidak ditemukan"
        )


def install_fish():
    if shutil.which("fish"):
        return

    pkg = shutil.which("pkg")

    if pkg:
        subprocess.run(
            [pkg, "install", "fish", "-y"],
            check=False
        )


def reload_termux():
    cmd = shutil.which(
        "termux-reload-settings"
    )

    if cmd:
        subprocess.run(
            [cmd],
            check=False
        )


def apply_theme(number):
    theme = THEMES[number]

    name = theme[0]
    font = theme[1]
    style = theme[2]

    print()
    print("Tema :", name)
    print("Font :", font)
    print("Style:", style)

    backup()
    write_colors(theme)
    write_prompt(theme)
    hook_prompt()
    write_keyboard()
    write_tema()
    install_font(font, style)
    reload_termux()

    print()
    print("✓ Tema aktif")
    print("✓ Prompt aktif")
    print("✓ Keyboard aktif")
    print("✓ config.fish aman")


def restore():
    if not BACKUP.exists():
        print("Backup tidak ditemukan.")
        return

    for name in (
        "config.fish",
        "colors.properties",
        "font.ttf",
        "termux.properties"
    ):
        src = BACKUP / name
        dst = (
            CONFIG if name == "config.fish"
            else TERMUX / name
        )

        if src.exists():
            shutil.copy2(src, dst)

    reload_termux()
    print("✓ Backup dipulihkan")


def create_main():
    try:
        urllib.request.urlretrieve(
            RAW,
            MAIN
        )

        MAIN.chmod(0o755)

        print(
            "✓ ~/termux-theme.py dibuat"
        )

    except Exception as e:
        print(
            "! Gagal membuat "
            "~/termux-theme.py"
        )
        print(e)


def install():
    setup()
    backup()
    install_fish()
    create_main()

    apply_theme("1")

    print()
    print(
        "╭────────────────────╮"
    )
    print(
        "│ ELMY0711 THEME OK  │"
    )
    print(
        "├────────────────────┤"
    )
    print(
        "│ 10 tema            │"
    )
    print(
        "│ 10 font            │"
    )
    print(
        "│ Tema 1 Iosevka     │"
    )
    print(
        "│ Tema 2 Italic      │"
    )
    print(
        "│ Fish               │"
    )
    print(
        "│ Keyboard           │"
    )
    print(
        "│ Backup             │"
    )
    print(
        "╰────────────────────╯"
    )

    print()
    print("Jalankan:")
    print("  exec fish")
    print()
    print("Tekan: tema + ENTER")


def menu():
    while True:
        os.system("clear")

        print("╭── ELMY0711 THEME ──╮")

        for key, theme in THEMES.items():
            print(
                f"│ {key:>2}. "
                f"{theme[0]:<15} │"
            )

        print("│ K. keyboard         │")
        print("│ R. restore          │")
        print("│ Q. keluar           │")
        print("╰─────────────────────╯")

        choice = input(
            "Pilih: "
        ).strip().lower()

        if choice in THEMES:
            apply_theme(choice)
            input("\nENTER...")

        elif choice == "k":
            write_keyboard()
            reload_termux()
            print("✓ Keyboard aktif")
            input("\nENTER...")

        elif choice == "r":
            restore()
            input("\nENTER...")

        elif choice == "q":
            break


def main():
    setup()

    if (
        "--install" in sys.argv
        or "-i" in sys.argv
        or not sys.stdin.isatty()
    ):
        install()
    else:
        menu()


if __name__ == "__main__":
    main()

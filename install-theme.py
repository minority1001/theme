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
PROMPT = FISH / "ELMY0711-prompt.fish"
CONFIG = FISH / "config.fish"

FONT_DIR = HOME / ".termux-themes/fonts"
BACKUP = HOME / ".termux-backup"
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
        "Tokyo Night", "JetBrainsMono",
        "#1a1b26", "#a9b1d6",
        [
            "#15161e", "#f7768e", "#73daca",
            "#e0af68", "#7aa2f7", "#bb9af7",
            "#7dcfff", "#a9b1d6", "#414868",
            "#f7768e", "#73daca", "#e0af68",
            "#7aa2f7", "#bb9af7", "#7dcfff",
            "#c0caf5"
        ]
    ),

    "2": (
        "Dracula", "FiraCode",
        "#282a36", "#f8f8f2",
        [
            "#21222c", "#ff5555", "#50fa7b",
            "#f1fa8c", "#bd93f9", "#ff79c6",
            "#8be9fd", "#f8f8f2", "#6272a4",
            "#ff6e6e", "#69ff94", "#ffffa5",
            "#d6acff", "#ff92df", "#a4ffff",
            "#ffffff"
        ]
    ),

    "3": (
        "Nord", "Hack",
        "#2e3440", "#d8dee9",
        [
            "#3b4252", "#bf616a", "#a3be8c",
            "#ebcb8b", "#81a1c1", "#b48ead",
            "#88c0d0", "#e5e9f0", "#4c566a",
            "#bf616a", "#a3be8c", "#ebcb8b",
            "#81a1c1", "#b48ead", "#8fbcbb",
            "#eceff4"
        ]
    ),

    "4": (
        "Gruvbox", "CascadiaCode",
        "#282828", "#ebdbb2",
        [
            "#282828", "#cc241d", "#98971a",
            "#d79921", "#458588", "#b16286",
            "#689d6a", "#a89984", "#928374",
            "#fb4934", "#b8bb26", "#fabd2f",
            "#83a598", "#d3869b", "#8ec07c",
            "#ebdbb2"
        ]
    ),

    "5": (
        "Catppuccin", "Iosevka",
        "#1e1e2e", "#cdd6f4",
        [
            "#45475a", "#f38ba8", "#a6e3a1",
            "#f9e2af", "#89b4fa", "#f5c2e7",
            "#94e2d5", "#bac2de", "#585b70",
            "#f38ba8", "#a6e3a1", "#f9e2af",
            "#89b4fa", "#f5c2e7", "#94e2d5",
            "#cdd6f4"
        ]
    ),

    "6": (
        "One Dark", "Meslo",
        "#282c34", "#abb2bf",
        [
            "#282c34", "#e06c75", "#98c379",
            "#e5c07b", "#61afef", "#c678dd",
            "#56b6c2", "#abb2bf", "#5c6370",
            "#e06c75", "#98c379", "#e5c07b",
            "#61afef", "#c678dd", "#56b6c2",
            "#ffffff"
        ]
    ),

    "7": (
        "Cyberpunk", "VictorMono",
        "#090014", "#00ffff",
        [
            "#120024", "#ff0055", "#00ff9c",
            "#ffe600", "#00aaff", "#ff00ff",
            "#00ffff", "#d8d8d8", "#3b0057",
            "#ff3366", "#33ffbb", "#ffff33",
            "#33bbff", "#ff33ff", "#33ffff",
            "#ffffff"
        ]
    ),

    "8": (
        "Solarized", "RobotoMono",
        "#002b36", "#839496",
        [
            "#073642", "#dc322f", "#859900",
            "#b58900", "#268bd2", "#d33682",
            "#2aa198", "#eee8d5", "#002b36",
            "#cb4b16", "#586e75", "#657b83",
            "#839496", "#6c71c4", "#93a1a1",
            "#fdf6e3"
        ]
    ),

    "9": (
        "Everforest", "UbuntuMono",
        "#2d353b", "#d3c6aa",
        [
            "#343f44", "#e67e80", "#a7c080",
            "#dbbc7f", "#7fbbb3", "#d699b6",
            "#83c092", "#d3c6aa", "#475258",
            "#e67e80", "#a7c080", "#dbbc7f",
            "#7fbbb3", "#d699b6", "#83c092",
            "#e9e8d2"
        ]
    ),

    "10": (
        "Monokai", "Mononoki",
        "#272822", "#f8f8f2",
        [
            "#272822", "#f92672", "#a6e22e",
            "#f4bf75", "#66d9ef", "#ae81ff",
            "#a1efe4", "#f8f8f2", "#75715e",
            "#f92672", "#a6e22e", "#f4bf75",
            "#66d9ef", "#ae81ff", "#a1efe4",
            "#f9f8f5"
        ]
    )
}


def setup():
    for path in (
        TERMUX,
        BIN,
        FISH,
        FONT_DIR
    ):
        path.mkdir(
            parents=True,
            exist_ok=True
        )


def backup():
    BACKUP.mkdir(
        parents=True,
        exist_ok=True
    )

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
    _, _, bg, fg, palette = theme

    names = [
        "color0", "color1", "color2", "color3",
        "color4", "color5", "color6", "color7",
        "color8", "color9", "color10", "color11",
        "color12", "color13", "color14", "color15"
    ]

    text = (
        f"background={bg}\n"
        f"foreground={fg}\n"
        f"cursor={fg}\n"
    )

    for name, color in zip(
        names,
        palette
    ):
        text += f"{name}={color}\n"

    (
        TERMUX / "colors.properties"
    ).write_text(text)


def write_prompt(theme):
    p = theme[4]

    c1 = p[1]
    c2 = p[2]
    c3 = p[3]
    c5 = p[5]
    c6 = p[6]

    text = f'''function fish_prompt
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
    if not CONFIG.exists():
        CONFIG.write_text("")

    text = CONFIG.read_text()

    hook = (
        "source "
        "~/.config/fish/"
        "ELMY0711-prompt.fish"
    )

    if hook not in text:
        if text and not text.endswith("\n"):
            text += "\n"

        text += (
            "\n"
            "# ELMY0711 PROMPT\n"
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

    (
        TERMUX /
        "termux.properties"
    ).write_text(text)


def write_tema():
    command = BIN / "tema"

    text = (
        f"#!{BASH}\n"
        f'exec "{PYTHON}" '
        '"$HOME/termux-theme.py" "$@"\n'
    )

    command.write_text(text)
    command.chmod(0o755)


def install_font(name):
    folder = FONT_DIR / name

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    font = next(
        folder.rglob("*.ttf"),
        None
    )

    if font is None:
        archive = (
            folder /
            f"{name}.tar.xz"
        )

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

            archive.unlink(
                missing_ok=True
            )

            font = next(
                folder.rglob("*.ttf"),
                None
            )

        except Exception:
            print(
                f"! Font {name} gagal"
            )
            return

    if font:
        shutil.copy2(
            font,
            TERMUX / "font.ttf"
        )


def install_fish():
    if shutil.which("fish"):
        return

    if shutil.which("pkg"):
        subprocess.run(
            ["pkg", "install", "fish", "-y"],
            check=False
        )


def reload_termux():
    command = shutil.which(
        "termux-reload-settings"
    )

    if command:
        subprocess.run(
            [command],
            check=False
        )


def apply_theme(number):
    theme = THEMES[number]

    print()
    print(
        "Tema :",
        theme[0]
    )

    print(
        "Font :",
        theme[1]
    )

    backup()
    write_colors(theme)
    write_prompt(theme)
    hook_prompt()
    write_keyboard()
    write_tema()
    install_font(theme[1])
    reload_termux()

    print()
    print("✓ Tema aktif")
    print("✓ Font aktif")
    print("✓ Fish aktif")
    print("✓ Prompt aktif")
    print("✓ Keyboard aktif")
    print("✓ config.fish aman")


def restore():
    if not BACKUP.exists():
        print(
            "Backup tidak ditemukan."
        )
        return

    src = BACKUP / "config.fish"

    if src.exists():
        shutil.copy2(
            src,
            CONFIG
        )

    for name in (
        "colors.properties",
        "font.ttf",
        "termux.properties"
    ):
        src = BACKUP / name
        dst = TERMUX / name

        if src.exists():
            shutil.copy2(
                src,
                dst
            )

    reload_termux()

    print(
        "✓ Backup dipulihkan"
    )


def remove_prompt():
    if PROMPT.exists():
        PROMPT.unlink()

    text = CONFIG.read_text(
        errors="ignore"
    )

    marker = "# ELMY0711 PROMPT"

    if marker in text:
        lines = text.splitlines()
        result = []
        skip = False

        for line in lines:
            if line.strip() == marker:
                skip = True
                continue

            if skip and line.strip().startswith(
                "source ~/.config/fish/"
            ):
                continue

            skip = False
            result.append(line)

        CONFIG.write_text(
            "\n".join(result).rstrip() + "\n"
        )

    print(
        "✓ Prompt ELMY0711 dihapus"
    )


def menu():
    while True:
        os.system("clear")

        print(
            "╭── ELMY0711 THEME ──╮"
        )

        for number, theme in THEMES.items():
            print(
                f"│ {number:>2}. "
                f"{theme[0]:<16}│"
            )

        print(
            "│ K. keyboard        │"
        )
        print(
            "│ R. restore         │"
        )
        print(
            "│ X. prompt off      │"
        )
        print(
            "│ Q. keluar          │"
        )
        print(
            "╰────────────────────╯"
        )

        choice = input(
            "Pilih: "
        ).strip().lower()

        if choice in THEMES:
            apply_theme(choice)
            input("\nENTER...")

        elif choice == "k":
            write_keyboard()
            reload_termux()

            print(
                "✓ Keyboard diperbarui"
            )

            input("\nENTER...")

        elif choice == "r":
            restore()
            input("\nENTER...")

        elif choice == "x":
            remove_prompt()
            input("\nENTER...")

        elif choice == "q":
            break


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

    except Exception as error:
        print(
            "! Gagal membuat "
            "~/termux-theme.py"
        )
        print(error)


def install():
    setup()
    backup()
    install_fish()
    create_main()

    theme = THEMES["1"]

    write_colors(theme)
    write_prompt(theme)
    hook_prompt()
    write_keyboard()
    write_tema()
    install_font(theme[1])
    reload_termux()

    print()
    print(
        "╭──────────────────────╮"
    )
    print(
        "│ ELMY0711 THEME OK    │"
    )
    print(
        "├──────────────────────┤"
    )
    print(
        "│ 10 tema              │"
    )
    print(
        "│ 10 font              │"
    )
    print(
        "│ Fish                 │"
    )
    print(
        "│ Keyboard             │"
    )
    print(
        "│ Backup               │"
    )
    print(
        "│ config.fish aman     │"
    )
    print(
        "╰──────────────────────╯"
    )

    print()
    print(
        "Jalankan:"
    )
    print(
        "  exec fish"
    )

    print()
    print(
        "Lalu tekan:"
    )
    print(
        "  tema + ENTER"
    )


def main():
    setup()

    if (
        "-i" in sys.argv
        or "--install" in sys.argv
    ):
        install()
        return

    if not sys.stdin.isatty():
        install()
        return

    menu()


if __name__ == "__main__":
    main()

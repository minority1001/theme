#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess
import urllib.request
import tarfile
from pathlib import Path


HOME = Path.home()

TERMUX_DIR = HOME / ".termux"

THEME_DIR = HOME / ".termux-themes"

FONT_CACHE = THEME_DIR / "fonts"

BIN_DIR = HOME / "bin"

THEME_SCRIPT = HOME / "termux-theme.py"

BACKUP_DIR = HOME / ".termux-backup"

FISH_CONFIG_DIR = (
    HOME /
    ".config" /
    "fish"
)

FISH_CONF_D_DIR = (
    FISH_CONFIG_DIR /
    "conf.d"
)

ELMY_FISH_FILE = (
    FISH_CONF_D_DIR /
    "90-elmy0711.fish"
)

INSTALLER_URL = (
    "https://raw.githubusercontent.com/"
    "minority1001/theme/main/install-theme.py"
)

NERD_FONT_URL = (
    "https://github.com/ryanoasis/nerd-fonts/"
    "releases/latest/download/{}.tar.xz"
)


THEMES = {

    "1": {
        "name": "Tokyo Night",
        "font": "JetBrainsMono",

        "colors": {
            "foreground": "#a9b1d6",
            "background": "#1a1b26",
            "cursor": "#c0caf5",

            "color0": "#15161e",
            "color1": "#f7768e",
            "color2": "#73daca",
            "color3": "#e0af68",
            "color4": "#7aa2f7",
            "color5": "#bb9af7",
            "color6": "#7dcfff",
            "color7": "#787c99",

            "color8": "#414868",
            "color9": "#f7768e",
            "color10": "#73daca",
            "color11": "#e0af68",
            "color12": "#7aa2f7",
            "color13": "#bb9af7",
            "color14": "#7dcfff",
            "color15": "#a9b1d6",
        }
    },

    "2": {
        "name": "Dracula",
        "font": "FiraCode",

        "colors": {
            "foreground": "#f8f8f2",
            "background": "#282a36",
            "cursor": "#f8f8f0",

            "color0": "#21222c",
            "color1": "#ff5555",
            "color2": "#50fa7b",
            "color3": "#f1fa8c",
            "color4": "#bd93f9",
            "color5": "#ff79c6",
            "color6": "#8be9fd",
            "color7": "#f8f8f2",

            "color8": "#6272a4",
            "color9": "#ff6e6e",
            "color10": "#69ff94",
            "color11": "#ffffa5",
            "color12": "#d6acff",
            "color13": "#ff92df",
            "color14": "#a4ffff",
            "color15": "#ffffff",
        }
    },

    "3": {
        "name": "Nord",
        "font": "Hack",

        "colors": {
            "foreground": "#d8dee9",
            "background": "#2e3440",
            "cursor": "#d8dee9",

            "color0": "#3b4252",
            "color1": "#bf616a",
            "color2": "#a3be8c",
            "color3": "#ebcb8b",
            "color4": "#81a1c1",
            "color5": "#b48ead",
            "color6": "#88c0d0",
            "color7": "#e5e9f0",

            "color8": "#4c566a",
            "color9": "#bf616a",
            "color10": "#a3be8c",
            "color11": "#ebcb8b",
            "color12": "#81a1c1",
            "color13": "#b48ead",
            "color14": "#8fbcbb",
            "color15": "#eceff4",
        }
    },

    "4": {
        "name": "Gruvbox",
        "font": "CascadiaCode",

        "colors": {
            "foreground": "#ebdbb2",
            "background": "#282828",
            "cursor": "#ebdbb2",

            "color0": "#282828",
            "color1": "#cc241d",
            "color2": "#98971a",
            "color3": "#d79921",
            "color4": "#458588",
            "color5": "#b16286",
            "color6": "#689d6a",
            "color7": "#a89984",

            "color8": "#928374",
            "color9": "#fb4934",
            "color10": "#b8bb26",
            "color11": "#fabd2f",
            "color12": "#83a598",
            "color13": "#d3869b",
            "color14": "#8ec07c",
            "color15": "#ebdbb2",
        }
    },

    "5": {
        "name": "Catppuccin",
        "font": "Iosevka",

        "colors": {
            "foreground": "#cdd6f4",
            "background": "#1e1e2e",
            "cursor": "#f5e0e0",

            "color0": "#45475a",
            "color1": "#f38ba8",
            "color2": "#a6e3a1",
            "color3": "#f9e2af",
            "color4": "#89b4fa",
            "color5": "#f5c2e7",
            "color6": "#94e2d5",
            "color7": "#bac2de",

            "color8": "#585b70",
            "color9": "#f38ba8",
            "color10": "#a6e3a1",
            "color11": "#f9e2af",
            "color12": "#89b4fa",
            "color13": "#f5c2e7",
            "color14": "#94e2d5",
            "color15": "#a6adc8",
        }
    },

    "6": {
        "name": "One Dark",
        "font": "Meslo",

        "colors": {
            "foreground": "#abb2bf",
            "background": "#282c34",
            "cursor": "#528bff",

            "color0": "#282c34",
            "color1": "#e06c75",
            "color2": "#98c379",
            "color3": "#e5c07b",
            "color4": "#61afef",
            "color5": "#c678dd",
            "color6": "#56b6c2",
            "color7": "#abb2bf",

            "color8": "#5c6370",
            "color9": "#e06c75",
            "color10": "#98c379",
            "color11": "#e5c07b",
            "color12": "#61afef",
            "color13": "#c678dd",
            "color14": "#56b6c2",
            "color15": "#ffffff",
        }
    },

    "7": {
        "name": "Cyberpunk",
        "font": "VictorMono",

        "colors": {
            "foreground": "#00ffff",
            "background": "#090014",
            "cursor": "#ff00ff",

            "color0": "#120024",
            "color1": "#ff0055",
            "color2": "#00ff9c",
            "color3": "#ffe600",
            "color4": "#00aaff",
            "color5": "#ff00ff",
            "color6": "#00ffff",
            "color7": "#d8d8d8",

            "color8": "#3b0057",
            "color9": "#ff3366",
            "color10": "#33ffbb",
            "color11": "#ffff33",
            "color12": "#33bbff",
            "color13": "#ff33ff",
            "color14": "#33ffff",
            "color15": "#ffffff",
        }
    },

    "8": {
        "name": "Solarized",
        "font": "RobotoMono",

        "colors": {
            "foreground": "#839496",
            "background": "#002b36",
            "cursor": "#93a1a1",

            "color0": "#073642",
            "color1": "#dc322f",
            "color2": "#859900",
            "color3": "#b58900",
            "color4": "#268bd2",
            "color5": "#d33682",
            "color6": "#2aa198",
            "color7": "#eee8d5",

            "color8": "#002b36",
            "color9": "#cb4b16",
            "color10": "#586e75",
            "color11": "#657b83",
            "color12": "#839496",
            "color13": "#6c71c4",
            "color14": "#93a1a1",
            "color15": "#fdf6e3",
        }
    },

    "9": {
        "name": "Everforest",
        "font": "UbuntuMono",

        "colors": {
            "foreground": "#d3c6aa",
            "background": "#2d353b",
            "cursor": "#d3c6aa",

            "color0": "#343f44",
            "color1": "#e67e80",
            "color2": "#a7c080",
            "color3": "#dbbc7f",
            "color4": "#7fbbb3",
            "color5": "#d699b6",
            "color6": "#83c092",
            "color7": "#d3c6aa",

            "color8": "#475258",
            "color9": "#e67e80",
            "color10": "#a7c080",
            "color11": "#dbbc7f",
            "color12": "#7fbbb3",
            "color13": "#d699b6",
            "color14": "#83c092",
            "color15": "#e9e8d2",
        }
    },

    "10": {
        "name": "Monokai",
        "font": "Mononoki",

        "colors": {
            "foreground": "#f8f8f2",
            "background": "#272822",
            "cursor": "#f8f8f0",

            "color0": "#272822",
            "color1": "#f92672",
            "color2": "#a6e22e",
            "color3": "#f4bf75",
            "color4": "#66d9ef",
            "color5": "#ae81ff",
            "color6": "#a1efe4",
            "color7": "#f8f8f2",

            "color8": "#75715e",
            "color9": "#f92672",
            "color10": "#a6e22e",
            "color11": "#f4bf75",
            "color12": "#66d9ef",
            "color13": "#ae81ff",
            "color14": "#a1efe4",
            "color15": "#f9f8f5",
        }
    },
}

def clear():
    os.system("clear")


def pause():
    input("\nTekan ENTER untuk kembali...")


def command_exists(command):
    return shutil.which(command) is not None


def run(command, check=False):
    try:
        return subprocess.run(
            command,
            check=check
        )
    except Exception as e:
        print(f"[!] Error: {e}")
        return None


def ensure_directories():

    TERMUX_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    THEME_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    FONT_CACHE.mkdir(
        parents=True,
        exist_ok=True
    )

    BIN_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    FISH_CONF_D_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

def backup_file(source):

    if not source.exists():
        return

    BACKUP_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    destination = (
        BACKUP_DIR /
        source.name
    )

    if not destination.exists():

        try:
            shutil.copy2(
                source,
                destination
            )
        except Exception:
            pass


def backup_config():

    ensure_directories()

    backup_file(
        TERMUX_DIR /
        "colors.properties"
    )

    backup_file(
        TERMUX_DIR /
        "font.ttf"
    )

    backup_file(
        TERMUX_DIR /
        "termux.properties"
    )


def install_theme_manager():

    ensure_directories()

    try:

        source = Path(__file__)

        if (
            source.exists()
            and source.is_file()
            and source.resolve()
            != THEME_SCRIPT.resolve()
        ):

            shutil.copy2(
                source,
                THEME_SCRIPT
            )

            print(
                "[+] ~/termux-theme.py dibuat."
            )

            return True

    except Exception:
        pass

    print(
        "[+] Mengambil Theme Manager dari GitHub..."
    )

    try:

        urllib.request.urlretrieve(
            INSTALLER_URL,
            THEME_SCRIPT
        )

        print(
            "[+] ~/termux-theme.py dibuat."
        )

        return True

    except Exception as e:

        print(
            "[!] Gagal membuat ~/termux-theme.py"
        )

        print(
            f"    {e}"
        )

        return False


def create_theme_command():

    ensure_directories()

    command_file = (
        BIN_DIR /
        "tema"
    )

    content = '''#!/data/data/com.termux/files/usr/bin/bash

exec python3 "$HOME/termux-theme.py" "$@"
'''

    try:

        command_file.write_text(
            content,
            encoding="utf-8"
        )

        command_file.chmod(
            0o755
        )

        print(
            "[+] ~/bin/tema dibuat."
        )

    except Exception as e:

        print(
            f"[!] Gagal membuat command tema: {e}"
        )


def configure_fish(colors):

    """
    IMPORTANT:

    ~/.config/fish/config.fish TIDAK PERNAH DITIMPA.

    Theme Pack menggunakan:

        ~/.config/fish/conf.d/90-elmy0711.fish
    """

    FISH_CONF_D_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    c1 = colors.get(
        "color1",
        "#ff5555"
    )

    c2 = colors.get(
        "color2",
        "#50fa7b"
    )

    c3 = colors.get(
        "color3",
        "#f1fa8c"
    )

    c4 = colors.get(
        "color4",
        "#bd93f9"
    )

    c5 = colors.get(
        "color5",
        "#ff79c6"
    )

    c6 = colors.get(
        "color6",
        "#8be9fd"
    )

    content = f'''# ============================================================
# ELMY0711 TERMUX THEME PACK
#
# AUTO GENERATED
#
# DO NOT EDIT ~/.config/fish/config.fish
#
# Theme Pack menggunakan conf.d agar konfigurasi pengguna
# tetap aman.
# ============================================================

# ============================================================
# PATH
# ============================================================

if type -q fish_add_path

    fish_add_path "$HOME/bin"

else

    if not contains "$HOME/bin" $PATH
        set -gx PATH "$HOME/bin" $PATH
    end

end


# ============================================================
# FISH GREETING
# ============================================================

set -g fish_greeting ""


# ============================================================
# COMMAND TEMA
# ============================================================

function tema
    command python3 "$HOME/termux-theme.py" $argv
end


# ============================================================
# ALIAS
# ============================================================

function ll
    command ls -lah $argv
end

function la
    command ls -A $argv
end

function c
    command clear
end


# ============================================================
# ELMY0711 PROMPT
# ============================================================

function __elmy0711_prompt --on-event fish_prompt

    # Hapus fungsi prompt sebelumnya dari Theme Pack.
    functions -e fish_prompt

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

        echo -n "╰──"

        set_color {c2}

        echo -n "╼ "

        set_color normal

    end


    functions -e fish_right_prompt

    function fish_right_prompt
    end

end


# END PROMPT CUSTOM ELMY0711
'''

    try:

        ELMY_FISH_FILE.write_text(
            content,
            encoding="utf-8"
        )

        print(
            "[+] Fish configuration dibuat:"
        )

        print(
            f"    {ELMY_FISH_FILE}"
        )

        print(
            "[+] ~/.config/fish/config.fish TIDAK DIUBAH."
        )

        return True

    except Exception as e:

        print(
            f"[!] Gagal membuat Fish config: {e}"
        )

        return False


def install_fish():

    if command_exists("fish"):

        print(
            "[+] Fish sudah terpasang."
        )

        return True

    if not command_exists("pkg"):

        print(
            "[!] pkg tidak ditemukan."
        )

        return False

    print(
        "[+] Memasang Fish..."
    )

    run(
        ["pkg", "update", "-y"],
        check=False
    )

    run(
        ["pkg", "install", "fish", "-y"],
        check=False
    )

    if command_exists("fish"):

        print(
            "[+] Fish berhasil dipasang."
        )

        return True

    print(
        "[!] Fish gagal dipasang."
    )

    return False



def set_fish_default():

    fish = shutil.which(
        "fish"
    )

    if not fish:
        return

    print()
    print(
        f"Fish: {fish}"
    )

    answer = input(
        "Jadikan Fish default shell? [y/N]: "
    ).strip().lower()

    if answer != "y":
        return

    if command_exists("chsh"):

        run(
            ["chsh", "-s", fish],
            check=False
        )

        print(
            "[+] Fish diset sebagai default shell."
        )

    else:

        print(
            "[!] chsh tidak tersedia."
        )


def write_colors(colors):

    file = (
        TERMUX_DIR /
        "colors.properties"
    )

    try:

        with file.open(
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                "# Generated by ELMY0711 Theme Pack\n\n"
            )

            for key, value in colors.items():

                f.write(
                    f"{key}={value}\n"
                )

        print(
            "[+] colors.properties diterapkan."
        )

    except Exception as e:

        print(
            f"[!] Gagal menulis colors.properties: {e}"
        )



def write_keyboard():

    file = (
        TERMUX_DIR /
        "termux.properties"
    )

    config = '''# ============================================================
# ELMY0711 CUSTOM TERMUX KEYBOARD
# ============================================================

extra-keys = [["bash ","python3 ","nano ","go run ","UP","END","PGUP","node "],["tema ","CTRL","BKSP","LEFT","DOWN","RIGHT","git clone ","curl -i "],["ls","cd ","clear ","ENTER","ping ","git pull","rm -rf ","exit "]]

volume-keys = true
'''

    try:

        file.write_text(
            config,
            encoding="utf-8"
        )

        print(
            "[+] Custom keyboard diterapkan."
        )

    except Exception as e:

        print(
            f"[!] Gagal membuat keyboard: {e}"
        )



def configure_bash_path():

    line = (
        'export PATH="$HOME/bin:$PATH"'
    )

    for name in [
        ".bashrc",
        ".profile"
    ]:

        file = HOME / name

        try:

            if file.exists():

                text = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

            else:

                text = ""

            if line not in text:

                with file.open(
                    "a",
                    encoding="utf-8"
                ) as f:

                    f.write(
                        "\n# ELMY0711 Theme Pack\n"
                    )

                    f.write(
                        line +
                        "\n"
                    )

        except Exception:
            pass



def find_font(directory):

    fonts = list(
        directory.glob("*.ttf")
    )

    if not fonts:
        return None

    mono = [
        font
        for font in fonts
        if "Mono" in font.name
        or "mono" in font.name
    ]

    if mono:
        return mono[0]

    return fonts[0]


def download_font(font_name):

    cache_dir = (
        FONT_CACHE /
        font_name
    )

    cache_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    cached = find_font(
        cache_dir
    )

    if cached:
        return cached

    archive = (
        cache_dir /
        f"{font_name}.tar.xz"
    )

    url = NERD_FONT_URL.format(
        font_name
    )

    print(
        f"[+] Download font: {font_name}"
    )

    try:

        urllib.request.urlretrieve(
            url,
            archive
        )

    except Exception as e:

        print(
            f"[!] Download gagal: {e}"
        )

        return None

    try:

        with tarfile.open(
            archive,
            "r:xz"
        ) as tar:

            for member in tar.getmembers():

                path = Path(
                    member.name
                )

                if path.is_absolute():
                    continue

                if ".." in path.parts:
                    continue

                tar.extract(
                    member,
                    path=cache_dir
                )

    except Exception as e:

        print(
            f"[!] Extract font gagal: {e}"
        )

        archive.unlink(
            missing_ok=True
        )

        return None

    archive.unlink(
        missing_ok=True
    )

    return find_font(
        cache_dir
    )


def install_font(font_name):

    font = download_font(
        font_name
    )

    if not font:
        return False

    destination = (
        TERMUX_DIR /
        "font.ttf"
    )

    try:

        shutil.copy2(
            font,
            destination
        )

        print(
            f"[+] Font aktif: {font.name}"
        )

        return True

    except Exception as e:

        print(
            f"[!] Gagal memasang font: {e}"
        )

        return False


def reload_termux():

    if command_exists(
        "termux-reload-settings"
    ):

        run(
            ["termux-reload-settings"],
            check=False
        )

        print(
            "[+] Termux settings direload."
        )


def apply_theme(number):

    if number not in THEMES:

        print(
            "[!] Tema tidak ditemukan."
        )

        return

    theme = THEMES[number]

    clear()

    print(
        "╔══════════════════════════════════════╗"
    )

    print(
        "║           APPLYING THEME             ║"
    )

    print(
        "╠══════════════════════════════════════╣"
    )

    print(
        f"║ Tema : {theme['name']:<26}║"
    )

    print(
        f"║ Font : {theme['font']:<26}║"
    )

    print(
        "╚══════════════════════════════════════╝"
    )

    backup_config()

    
    write_colors(
        theme["colors"]
    )

    
    configure_fish(
        theme["colors"]
    )

    
    install_font(
        theme["font"]
    )

    
    write_keyboard()

    
    create_theme_command()

    
    configure_bash_path()

    
    reload_termux()

    print()
    print(
        "[+] Tema berhasil diterapkan."
    )

    print()
    print(
        "Untuk memuat prompt Fish:"
    )

    print(
        "    exec fish"
    )



def restore_backup():

    if not BACKUP_DIR.exists():

        print(
            "[!] Backup tidak ditemukan."
        )

        return

    restored = 0

    for name in [
        "colors.properties",
        "font.ttf",
        "termux.properties"
    ]:

        source = (
            BACKUP_DIR /
            name
        )

        destination = (
            TERMUX_DIR /
            name
        )

        if source.exists():

            try:

                shutil.copy2(
                    source,
                    destination
                )

                restored += 1

            except Exception:
                pass

    print(
        f"[+] {restored} konfigurasi dikembalikan."
    )

    reload_termux()



def remove_elmy_fish():

    if ELMY_FISH_FILE.exists():

        try:

            ELMY_FISH_FILE.unlink()

            print(
                "[+] ELMY0711 Fish config dihapus."
            )

        except Exception as e:

            print(
                f"[!] Gagal menghapus: {e}"
            )

    else:

        print(
            "[+] ELMY0711 Fish config tidak ditemukan."
        )



def theme_menu():

    while True:

        clear()

        print(
            "╔══════════════════════════════════════╗"
        )

        print(
            "║        TERMUX THEME SETTINGS         ║"
        )

        print(
            "╠══════════════════════════════════════╣"
        )

        for number, theme in THEMES.items():

            print(
                f"║ {number:>2}. "
                f"{theme['name']:<17}"
                f"{theme['font']:<12}║"
            )

        print(
            "╠══════════════════════════════════════╣"
        )

        print(
            "║ K. Refresh keyboard                  ║"
        )

        print(
            "║ R. Restore Termux                    ║"
        )

        print(
            "║ X. Hapus prompt ELMY0711             ║"
        )

        print(
            "║ B. Kembali                           ║"
        )

        print(
            "╚══════════════════════════════════════╝"
        )

        choice = input(
            "\nPilih: "
        ).strip().lower()

        if choice in THEMES:

            apply_theme(
                choice
            )

            pause()

        elif choice == "k":

            write_keyboard()

            reload_termux()

            pause()

        elif choice == "r":

            restore_backup()

            pause()

        elif choice == "x":

            remove_elmy_fish()

            print(
                "Jalankan: exec fish"
            )

            pause()

        elif choice == "b":

            break

        else:

            print(
                "[!] Pilihan tidak valid."
            )

            pause()




def install_all():

    clear()

    print(
        "╔══════════════════════════════════════╗"
    )

    print(
        "║       ELMY0711 TERMUX THEME PACK     ║"
    )

    print(
        "╚══════════════════════════════════════╝"
    )

    ensure_directories()

    backup_config()

    print(
        "\n[1/6] Theme Manager"
    )

    install_theme_manager()

    print(
        "\n[2/6] Fish"
    )

    install_fish()

    print(
        "\n[3/6] Fish Prompt"
    )

    configure_fish(
        THEMES["1"]["colors"]
    )

    print(
        "\n[4/6] Custom Keyboard"
    )

    write_keyboard()

    print(
        "\n[5/6] Command tema"
    )

    create_theme_command()

    configure_bash_path()

    print(
        "\n[6/6] Selesai"
    )

    print()
    print(
        "╔══════════════════════════════════════╗"
    )

    print(
        "║             SELESAI                  ║"
    )

    print(
        "╠══════════════════════════════════════╣"
    )

    print(
        "║ Command : tema                       ║"
    )

    print(
        "║                                      ║"
    )

    print(
        "║ config.fish pengguna AMAN            ║"
    )

    print(
        "╚══════════════════════════════════════╝"
    )

    print()

    set_fish_default()


# ============================================================
# MAIN MENU
# ============================================================

def main_menu():

    while True:

        clear()

        print(
            "╔══════════════════════════════════════╗"
        )

        print(
            "║       TERMUX CUSTOM THEME PACK       ║"
        )

        print(
            "║              ELMY0711                ║"
        )

        print(
            "╠══════════════════════════════════════╣"
        )

        print(
            "║ 1. Install semua                     ║"
        )

        print(
            "║ 2. Pengaturan tema                   ║"
        )

        print(
            "║ 3. Custom keyboard                   ║"
        )

        print(
            "║ 4. Install Fish                      ║"
        )

        print(
            "║ 5. Restore backup                    ║"
        )

        print(
            "║ Q. Keluar                            ║"
        )

        print(
            "╚══════════════════════════════════════╝"
        )

        choice = input(
            "\nPilih: "
        ).strip().lower()

        if choice == "1":

            install_all()

            pause()

        elif choice == "2":

            theme_menu()

        elif choice == "3":

            write_keyboard()

            reload_termux()

            pause()

        elif choice == "4":

            install_fish()

            configure_fish(
                THEMES["1"]["colors"]
            )

            print(
                "\nJalankan 'exec fish' untuk memuat prompt."
            )

            pause()

        elif choice == "5":

            restore_backup()

            pause()

        elif choice == "q":

            print(
                "\nBye."
            )

            break

        else:

            print(
                "[!] Pilihan tidak valid."
            )

            pause()


# ============================================================
# ENTRY
# ============================================================

def main():

    ensure_directories()

    main_menu()


if __name__ == "__main__":

    main()

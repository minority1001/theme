#!/usr/bin/env python3
import os,sys,shutil,subprocess,urllib.request,tarfile
from pathlib import Path

H=Path.home()
P=Path(os.getenv("PREFIX","/data/com.termux/files/usr"))
T=H/".termux"; F=H/".config/fish"; B=H/"bin"
BK=H/".termux-backup"; FD=H/".termux-themes/fonts"
CFG=F/"config.fish"; PR=F/"ELMY0711-prompt.fish"
PY=P/"bin/python3"; SH=P/"bin/bash"

NF="https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/"

THEMES={
"1":("Tokyo Night","FiraCode","regular","#1a1b26","#a9b1d6",["#15161e","#f7768e","#73daca","#e0af68","#7aa2f7","#bb9af7","#7dcfff","#a9b1d6","#414868","#f7768e","#73daca","#e0af68","#7aa2f7","#bb9af7","#7dcfff","#c0caf5"]),
"2":("Dracula","JetBrainsMono","italic","#282a36","#f8f8f2",["#21222c","#ff5555","#50fa7b","#f1fa8c","#bd93f9","#ff79c6","#8be9fd","#f8f8f2","#6272a4","#ff6e6e","#69ff94","#ffffa5","#d6acff","#ff92df","#a4ffff","#ffffff"]),
"3":("Nord","Hack","regular","#2e3440","#d8dee9",["#3b4252","#bf616a","#a3be8c","#ebcb8b","#81a1c1","#b48ead","#88c0d0","#e5e9f0","#4c566a","#bf616a","#a3be8c","#ebcb8b","#81a1c1","#b48ead","#8fbcbb","#eceff4"]),
"4":("Gruvbox","CascadiaCode","regular","#282828","#ebdbb2",["#282828","#cc241d","#98971a","#d79921","#458588","#b16286","#689d6a","#a89984","#928374","#fb4934","#b8bb26","#fabd2f","#83a598","#d3869b","#8ec07c","#ebdbb2"]),
"5":("Catppuccin","FiraCode","regular","#1e1e2e","#cdd6f4",["#45475a","#f38ba8","#a6e3a1","#f9e2af","#89b4fa","#f5c2e7","#94e2d5","#bac2de","#585b70","#f38ba8","#a6e3a1","#f9e2af","#89b4fa","#f5c2e7","#94e2d5","#cdd6f4"]),
"6":("One Dark","Meslo","regular","#282c34","#abb2bf",["#282c34","#e06c75","#98c379","#e5c07b","#61afef","#c678dd","#56b6c2","#abb2bf","#5c6370","#e06c75","#98c379","#e5c07b","#61afef","#c678dd","#56b6c2","#ffffff"]),
"7":("Cyberpunk","JetBrainsMono","regular","#090014","#00ffff",["#120024","#ff0055","#00ff9c","#ffe600","#00aaff","#ff00ff","#00ffff","#d8d8","#3b0057","#ff3366","#33ffbb","#ffff33","#33bbff","#ff33ff","#33ffff","#ffffff"]),
"8":("Solarized","RobotoMono","regular","#002b36","#839496",["#073642","#dc322f","#859900","#b58900","#268bd2","#d33682","#2aa198","#eee8d5","#002b36","#cb4b16","#586e75","#657b83","#839496","#6c71c4","#93a1a1","#fdf6e3"]),
"9":("Everforest","UbuntuMono","regular","#2d353b","#d3c6aa",["#343f44","#e67e80","#a7c080","#dbbc7f","#7fbbb3","#d699b6","#83c092","#d3c6aa","#475258","#e67e80","#a7c080","#dbbc7f","#7fbbb3","#d699b6","#83c092","#e9e8d2"]),
"10":("Monokai","Mononoki","regular","#272822","#f8f8f2",["#272822","#f92672","#a6e22e","#f4bf75","#66d9ef","#ae81ff","#a1efe4","#f8f8f2","#75715e","#f92672","#a6e22e","#f4bf75","#66d9ef","#ae81ff","#a1efe4","#f9f8f5"])
}

def setup():
    for x in (T,F,BK,FD): x.mkdir(parents=True,exist_ok=True)

def backup():
    BK.mkdir(exist_ok=True)
    for x in (CFG,T/"colors.properties",T/"font.ttf",T/"termux.properties"):
        if x.exists() and not (BK/x.name).exists():
            shutil.copy2(x,BK/x.name)

def colors(t):
    _,_,bg,fg,p=t # FIX: skip 3
    s=f"background={bg}\nforeground={fg}\ncursor={fg}\n"
    s+="".join(f"color{i}={c}\n" for i,c in enumerate(p))
    (T/"colors.properties").write_text(s)

def prompt(t):
    _,_,_,_,_,p=t # FIX: skip 3 juga
    c1,c2,c3,c5,c6=p[1],p[2],p[3],p[5],p[6]
    s=f'''function fish_prompt
    set_color {c6}
    echo -n (date "+%b %d %H:%M")
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
    PR.write_text(s)

def hook():
    CFG.touch()
    h="source ~/.config/fish/ELMY0711-prompt.fish"
    s=CFG.read_text()
    if h not in s:
        if s and not s.endswith("\n"): s+="\n"
        CFG.write_text(s+"\n# ELMY0711\n"+h+"\n")

def keyboard():
    s='''extra-keys=[["bash ","python3 ","nano ","go run ","UP","END","PGUP","node "],["tema ","CTRL","BKSP","LEFT","DOWN","RIGHT","git clone ","curl -i "],["ls ","cd ","clear ","ENTER","ping ","git pull ","rm -rf ",{macro:"CTRL d",display:"exit"}]]'''
    (T/"termux.properties").write_text(s)

def tema_cmd():
    x=B/"tema"
    x.write_text(f'#!{SH}\nexec "{PY}" "$HOME/theme/termux-theme.py" "$@"\n')
    x.chmod(0o755)

def download_font(name, style):
    d = FD / name
    d.mkdir(parents=True, exist_ok=True)
    url = f"{NF}{name}.tar.xz"
    archive = d / f"{name}.tar.xz"
    if (T / "font.ttf").exists(): (T / "font.ttf").unlink()
    print(f"Downloading {name}...")
    subprocess.run(["curl","-L",url,"-o",str(archive)], check=False)
    try:
        with tarfile.open(archive, "r:xz") as tar: tar.extractall(d)
    except: pass
    target_style = "italic" if style == "italic" else "regular"
    for f in d.rglob("*.ttf"):
        n = f.name.lower()
        if name.lower() in n and "mono" in n and target_style in n:
            shutil.copy2(f, T / "font.ttf")
            print("✓ Font:", f.name); return
    for f in d.rglob("*.ttf"):
        if name.lower() in f.name.lower() and "mono" in f.name.lower():
            shutil.copy2(f, T / "font.ttf")
            print("✓ Font:", f.name); return
    print("! Font gagal")

def reload():
    x=shutil.which("termux-reload-settings")
    if x: subprocess.run([x],check=False)

def apply(n):
    t=THEMES[n]
    print(f"\nTema : {t[0]}\nFont : {t[1]}\nStyle: {t[2]}")
    backup(); colors(t); prompt(t); hook()
    keyboard(); tema_cmd(); download_font(t[1],t[2]); reload()
    print("\n✓ Tema aktif\n✓ Prompt aktif\n✓ Keyboard aktif\n✓ config.fish aman")

def restore():
    for n in ("config.fish","colors.properties","font.ttf","termux.properties"):
        a=BK/n; b=CFG if n=="config.fish" else T/n
        if a.exists(): shutil.copy2(a,b)
    reload(); print("✓ Backup dipulihkan")

def menu():
    while True:
        os.system("clear")
        print("╭── ELMY0711 THEME v3 FIX ──╮")
        for n,t in THEMES.items():
            print(f"│ {n:>2}. {t[0]:<12} {t[1]:<12} │")
        print("│ R. restore │")
        print("│ Q. keluar │")
        print("╰───────────────────────────╯")
        x=input("Pilih: ").strip().lower()
        if x in THEMES:
            apply(x); input("\nENTER...")
        elif x=="r":
            restore(); input("\nENTER...")
        elif x=="q": break

def main():
    setup()
    menu()

if __name__=="__main__":
    main()

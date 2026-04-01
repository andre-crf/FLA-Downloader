import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os

try:
    import yt_dlp
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    import yt_dlp


BG        = "#0f0f0f"
CARD      = "#1a1a1a"
ACCENT    = "#ff0000"
ACCENT2   = "#ff4444"
TEXT      = "#ffffff"
SUBTEXT   = "#aaaaaa"
BORDER    = "#2a2a2a"
SUCCESS   = "#00c853"
FONT_BIG  = ("Helvetica", 20, "bold")
FONT_MED  = ("Helvetica", 11)
FONT_SM   = ("Helvetica", 9)


class YoutubeDownloader(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FLADOWNLOADER")
        self.geometry("620x560")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.pasta_destino = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        self.qualidade     = tk.StringVar(value="1080p")
        self.formato       = tk.StringVar(value="MP4")
        self.progresso     = tk.DoubleVar(value=0)
        self.status_txt    = tk.StringVar(value="Aguardando...")
        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self, bg=ACCENT, height=5)
        header.pack(fill="x")

        title_frame = tk.Frame(self, bg=BG, pady=20)
        title_frame.pack(fill="x", padx=30)

        tk.Label(title_frame, text="FLA", font=("Helvetica", 22, "bold"),
                 fg=ACCENT, bg=BG).pack(side="left")
        tk.Label(title_frame, text=" Downloader", font=("Helvetica", 22, "bold"),
                 fg=TEXT, bg=BG).pack(side="left")
        tk.Label(title_frame, text="v1.0", font=FONT_SM,
                 fg=SUBTEXT, bg=BG).pack(side="left", padx=(8, 0), pady=(6, 0))

        card = tk.Frame(self, bg=CARD, bd=0, highlightthickness=1,
                        highlightbackground=BORDER)
        card.pack(fill="x", padx=30, pady=(0, 15))

        self._section(card, "URL do vídeo ou playlist")
        self.url_entry = self._entry(card)
        self.url_entry.pack(fill="x", padx=20, pady=(0, 15))

        row = tk.Frame(card, bg=CARD)
        row.pack(fill="x", padx=20, pady=(0, 15))

        left = tk.Frame(row, bg=CARD)
        left.pack(side="left", expand=True, fill="x", padx=(0, 8))
        self._section(left, "Qualidade")
        self._dropdown(left, self.qualidade,
                       ["2160p (4K)", "1080p", "720p", "480p", "360p", "Melhor disponível"])

        right = tk.Frame(row, bg=CARD)
        right.pack(side="left", expand=True, fill="x")
        self._section(right, "Formato")
        self._dropdown(right, self.formato, ["MP4", "MP3 (só áudio)", "WEBM", "MKV"])

        # ── Pasta destino ──
        self._section(card, "Pasta de destino")
        pasta_row = tk.Frame(card, bg=CARD)
        pasta_row.pack(fill="x", padx=20, pady=(0, 20))

        pasta_entry = tk.Entry(pasta_row, textvariable=self.pasta_destino,
                               bg="#252525", fg=TEXT, insertbackground=TEXT,
                               relief="flat", font=FONT_MED, bd=0)
        pasta_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))
        self._style_entry(pasta_entry)

        btn_pasta = tk.Button(pasta_row, text="📁", font=("Helvetica", 14),
                              bg=BORDER, fg=TEXT, relief="flat", cursor="hand2",
                              command=self._escolher_pasta, padx=10)
        btn_pasta.pack(side="left", ipady=4)

        prog_frame = tk.Frame(self, bg=BG)
        prog_frame.pack(fill="x", padx=30, pady=(0, 5))

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Red.Horizontal.TProgressbar",
                        troughcolor=BORDER, background=ACCENT,
                        darkcolor=ACCENT, lightcolor=ACCENT2,
                        bordercolor=BG, thickness=8)

        self.bar = ttk.Progressbar(prog_frame, variable=self.progresso,
                                   maximum=100, style="Red.Horizontal.TProgressbar")
        self.bar.pack(fill="x")

        status_row = tk.Frame(self, bg=BG)
        status_row.pack(fill="x", padx=30, pady=(4, 0))
        tk.Label(status_row, textvariable=self.status_txt,
                 font=FONT_SM, fg=SUBTEXT, bg=BG).pack(side="left")
        self.pct_label = tk.Label(status_row, text="0%",
                                  font=FONT_SM, fg=ACCENT, bg=BG)
        self.pct_label.pack(side="right")

        self.btn_baixar = tk.Button(
            self, text="⬇  BAIXAR", font=("Helvetica", 13, "bold"),
            bg=ACCENT, fg=TEXT, relief="flat", cursor="hand2",
            activebackground=ACCENT2, activeforeground=TEXT,
            command=self._iniciar_download, pady=12
        )
        self.btn_baixar.pack(fill="x", padx=30, pady=15)

        tk.Label(self, text="Feito com yt-dlp  •  uso pessoal",
                 font=FONT_SM, fg=BORDER, bg=BG).pack(pady=(0, 10))

    def _section(self, parent, texto):
        tk.Label(parent, text=texto.upper(), font=("Helvetica", 8, "bold"),
                 fg=SUBTEXT, bg=parent["bg"], anchor="w").pack(
                     fill="x", padx=20 if parent == self else 0, pady=(12, 4))

    def _entry(self, parent):
        e = tk.Entry(parent, bg="#252525", fg=TEXT, insertbackground=TEXT,
                     relief="flat", font=FONT_MED, bd=0)
        e.configure(highlightthickness=1, highlightbackground=BORDER,
                    highlightcolor=ACCENT)
        e.pack_configure(ipady=8)
        return e

    def _style_entry(self, e):
        e.configure(highlightthickness=1, highlightbackground=BORDER,
                    highlightcolor=ACCENT, relief="flat")

    def _dropdown(self, parent, var, opcoes):
        style = ttk.Style()
        style.configure("Dark.TCombobox",
                        fieldbackground="#252525", background=BORDER,
                        foreground=TEXT, arrowcolor=ACCENT,
                        selectbackground=ACCENT, selectforeground=TEXT)
        cb = ttk.Combobox(parent, textvariable=var, values=opcoes,
                          state="readonly", style="Dark.TCombobox", font=FONT_MED)
        cb.pack(fill="x", ipady=5)

    def _escolher_pasta(self):
        pasta = filedialog.askdirectory(initialdir=self.pasta_destino.get())
        if pasta:
            self.pasta_destino.set(pasta)

    def _iniciar_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Atenção", "Cole uma URL válida!")
            return
        self.btn_baixar.config(state="disabled", text="Baixando...")
        self.progresso.set(0)
        self.pct_label.config(text="0%")
        self.status_txt.set("Iniciando download...")
        threading.Thread(target=self._download, args=(url,), daemon=True).start()

    def _download(self, url):
        fmt = self.formato.get()
        qual = self.qualidade.get().replace("p", "").split()[0]

        if fmt == "MP3 (só áudio)":
            opcoes = {
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
                "outtmpl": os.path.join(self.pasta_destino.get(), "%(title)s.%(ext)s"),
                "progress_hooks": [self._hook],
            }
        else:
            ext = fmt.lower()
            if qual.isdigit():
                fmt_str = f"bestvideo[height<={qual}]+bestaudio/best[height<={qual}]"
            else:
                fmt_str = "bestvideo+bestaudio/best"

            opcoes = {
                "format": fmt_str,
                "merge_output_format": ext,
                "outtmpl": os.path.join(self.pasta_destino.get(), "%(title)s.%(ext)s"),
                "progress_hooks": [self._hook],
            }

        try:
            with yt_dlp.YoutubeDL(opcoes) as ydl:
                ydl.download([url])
            self._finalizar(sucesso=True)
        except Exception as e:
            self._finalizar(sucesso=False, erro=str(e))

    def _hook(self, d):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
            baixado = d.get("downloaded_bytes", 0)
            nome = d.get("filename", "")
            nome = os.path.basename(nome)[:50]
            velocidade = d.get("_speed_str", "")
            eta = d.get("_eta_str", "")

            if total:
                pct = (baixado / total) * 100
                self.progresso.set(pct)
                self.pct_label.config(text=f"{pct:.0f}%")

            self.status_txt.set(f"{nome}  {velocidade}  ETA {eta}")

        elif d["status"] == "finished":
            self.progresso.set(99)
            self.status_txt.set("Processando arquivo...")

    def _finalizar(self, sucesso, erro=""):
        self.btn_baixar.config(state="normal", text="⬇  BAIXAR")
        if sucesso:
            self.progresso.set(100)
            self.pct_label.config(text="100%", fg=SUCCESS)
            self.status_txt.set("✓ Download concluído!")
            messagebox.showinfo("Pronto!", f"Arquivo salvo em:\n{self.pasta_destino.get()}")
        else:
            self.progresso.set(0)
            self.pct_label.config(text="Erro", fg=ACCENT)
            self.status_txt.set("Erro no download.")
            messagebox.showerror("Erro", f"Falha no download:\n{erro}")


if __name__ == "__main__":
    app = YoutubeDownloader()
    app.mainloop()

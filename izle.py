#!/usr/bin/env python3
"""Fedora'da reklamsız YouTube izleme.

Videoyu tarayıcı yerine yt-dlp + mpv ile oynatır; YouTube'un reklam
sistemi hiç yüklenmediği için reklam gösterilmez.

Kurulum (Fedora):
    sudo dnf install mpv yt-dlp

Kullanım:
    ./izle.py <youtube-linki> [<link> ...]
    ./izle.py            # link sorar
"""
import shutil
import subprocess
import sys


def eksik_bagimliliklar():
    return [p for p in ("mpv", "yt-dlp") if shutil.which(p) is None]


def gecerli_link(link):
    return link.startswith(("http://", "https://"))


def main(argv):
    eksik = eksik_bagimliliklar()
    if eksik:
        print("Eksik paket(ler): " + ", ".join(eksik), file=sys.stderr)
        print("Kurmak için: sudo dnf install " + " ".join(eksik), file=sys.stderr)
        return 1

    linkler = argv[1:]
    if not linkler:
        try:
            linkler = [input("YouTube linki: ").strip()]
        except (EOFError, KeyboardInterrupt):
            return 1

    linkler = [l for l in linkler if gecerli_link(l)]
    if not linkler:
        print("Geçerli bir http(s) linki girin.", file=sys.stderr)
        return 1

    komut = [
        "mpv",
        "--ytdl=yes",
        "--ytdl-format=bestvideo[height<=1080]+bestaudio/best",
        "--",
    ] + linkler
    return subprocess.call(komut)


if __name__ == "__main__":
    sys.exit(main(sys.argv))

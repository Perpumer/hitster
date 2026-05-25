"""
Generador de cartas PDF para Hitster Personal
==============================================
Genera un PDF listo para imprimir con:
  - FRENTE: QR code de la canción
  - DORSO: año, título y artista (se revela después de adivinar)

Las cartas se imprimen en hoja A4, 3 columnas x 4 filas = 12 cartas por hoja.
Tamaño de carta: 6.3cm x 8.8cm (similar a Hitster original).

Uso:
    python generate_cards.py

Instalación de dependencias:
    pip install reportlab pillow
"""

import json
import os
from pathlib import Path

# Tamaño de carta en puntos (1cm = 28.35 pt)
CARD_W = 6.3 * 28.35   # ~179 pt
CARD_H = 8.8 * 28.35   # ~249 pt
MARGIN = 1.0 * 28.35   # ~28 pt
COLS = 3
ROWS = 4

# Colores
COLOR_BG_FRONT = (0.06, 0.06, 0.12)    # Azul muy oscuro
COLOR_BG_BACK  = (0.49, 0.23, 0.93)    # Violeta
COLOR_WHITE    = (1, 1, 1)
COLOR_LIGHT    = (1, 1, 1, 0.7)


def draw_front(c, x, y, song_id: str, qr_path: str):
    """Dibuja el frente de la carta (QR code)"""
    from reportlab.lib.units import cm

    # Fondo oscuro
    c.setFillColorRGB(*COLOR_BG_FRONT)
    c.roundRect(x, y, CARD_W, CARD_H, 8, fill=1, stroke=0)

    # Borde sutil
    c.setStrokeColorRGB(1, 1, 1, 0.1)
    c.setLineWidth(0.5)
    c.roundRect(x, y, CARD_W, CARD_H, 8, fill=0, stroke=1)

    # Título "HITSTER" arriba
    c.setFillColorRGB(1, 1, 1, 0.3)
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(x + CARD_W / 2, y + CARD_H - 18, "🎵 HITSTER PERSONAL")

    # QR code centrado
    if os.path.exists(qr_path):
        qr_size = CARD_W - 30
        qr_x = x + (CARD_W - qr_size) / 2
        qr_y = y + (CARD_H - qr_size) / 2 - 5
        c.drawImage(qr_path, qr_x, qr_y, width=qr_size, height=qr_size,
                    preserveAspectRatio=True, mask='auto')
    else:
        # Placeholder si no existe el QR
        c.setFillColorRGB(0.2, 0.2, 0.3)
        c.roundRect(x + 15, y + 30, CARD_W - 30, CARD_H - 60, 4, fill=1, stroke=0)
        c.setFillColorRGB(1, 1, 1, 0.4)
        c.setFont("Helvetica", 8)
        c.drawCentredString(x + CARD_W / 2, y + CARD_H / 2, "QR no generado aún")

    # Número de carta abajo
    c.setFillColorRGB(1, 1, 1, 0.25)
    c.setFont("Helvetica", 7)
    c.drawCentredString(x + CARD_W / 2, y + 10, f"#{song_id}")


def draw_back(c, x, y, song: dict):
    """Dibuja el dorso de la carta (año + info)"""
    # Fondo violeta
    c.setFillColorRGB(*COLOR_BG_BACK)
    c.roundRect(x, y, CARD_W, CARD_H, 8, fill=1, stroke=0)

    # Patrón de puntos decorativo
    c.setFillColorRGB(1, 1, 1, 0.05)
    dot_size = 3
    dot_gap = 14
    for col in range(0, int(CARD_W / dot_gap) + 1):
        for row in range(0, int(CARD_H / dot_gap) + 1):
            c.circle(x + col * dot_gap, y + row * dot_gap, dot_size / 2, fill=1, stroke=0)

    # Label "AÑO" pequeño
    c.setFillColorRGB(1, 1, 1, 0.5)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(x + CARD_W / 2, y + CARD_H - 30, "AÑO")

    # Año grande
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 44)
    c.drawCentredString(x + CARD_W / 2, y + CARD_H / 2 + 10, str(song.get("year", "????"))  )

    # Línea separadora
    c.setStrokeColorRGB(1, 1, 1, 0.2)
    c.setLineWidth(0.5)
    c.line(x + 20, y + CARD_H / 2 - 10, x + CARD_W - 20, y + CARD_H / 2 - 10)

    # Título de la canción
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 10)
    title = song.get("title", "–")
    # Truncar si es muy largo
    if len(title) > 22:
        title = title[:21] + "…"
    c.drawCentredString(x + CARD_W / 2, y + CARD_H / 2 - 30, title)

    # Artista
    c.setFillColorRGB(1, 1, 1, 0.65)
    c.setFont("Helvetica", 9)
    artist = song.get("artist", "–")
    if len(artist) > 26:
        artist = artist[:25] + "…"
    c.drawCentredString(x + CARD_W / 2, y + CARD_H / 2 - 48, artist)

    # Número de carta
    c.setFillColorRGB(1, 1, 1, 0.25)
    c.setFont("Helvetica", 7)
    c.drawCentredString(x + CARD_W / 2, y + 10, f"#{song.get('id', '?')}")


def generate_pdf():
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
    except ImportError:
        print("❌ Instalá las dependencias primero:")
        print("   pip install reportlab pillow")
        return

    with open("songs.json", "r", encoding="utf-8") as f:
        songs = json.load(f)

    page_w, page_h = A4  # 595 x 842 pt

    # Calcular márgenes para centrar la grilla
    grid_w = COLS * CARD_W + (COLS - 1) * 6
    grid_h = ROWS * CARD_H + (ROWS - 1) * 6
    margin_x = (page_w - grid_w) / 2
    margin_y = (page_h - grid_h) / 2

    # ---- FRENTES ----
    c = canvas.Canvas("cartas_frente.pdf", pagesize=A4)
    cards_per_page = COLS * ROWS

    for page_idx in range(0, len(songs), cards_per_page):
        page_songs = songs[page_idx: page_idx + cards_per_page]

        for i, song in enumerate(page_songs):
            col = i % COLS
            row = i // COLS
            x = margin_x + col * (CARD_W + 6)
            # Empezamos desde arriba
            y = page_h - margin_y - (row + 1) * CARD_H - row * 6

            qr_path = f"qrcodes/{song['id']}.png"
            draw_front(c, x, y, song["id"], qr_path)

        c.showPage()

    c.save()
    print("✅ Frentes generados: cartas_frente.pdf")

    # ---- DORSOS ----
    c = canvas.Canvas("cartas_dorso.pdf", pagesize=A4)

    for page_idx in range(0, len(songs), cards_per_page):
        page_songs = songs[page_idx: page_idx + cards_per_page]

        for i, song in enumerate(page_songs):
            col = i % COLS
            row = i // COLS
            # Espejo horizontal para que al imprimir dorso coincida con frente
            mirrored_col = COLS - 1 - col
            x = margin_x + mirrored_col * (CARD_W + 6)
            y = page_h - margin_y - (row + 1) * CARD_H - row * 6

            draw_back(c, x, y, song)

        c.showPage()

    c.save()
    print("✅ Dorsos generados: cartas_dorso.pdf")
    print("\n🎉 Listo! Imprimí primero cartas_frente.pdf, luego volvé a poner el papel")
    print("   y pasá a imprimir cartas_dorso.pdf (modo dúplex manual).")
    print(f"   Total: {len(songs)} cartas en {(len(songs) + cards_per_page - 1) // cards_per_page} página(s)")


if __name__ == "__main__":
    generate_pdf()

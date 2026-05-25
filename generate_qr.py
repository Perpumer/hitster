"""
Generador de QR codes para Hitster Personal
============================================
Lee songs.json y genera un QR code por canción en la carpeta qrcodes/

Uso:
    python generate_qr.py --url https://TU_USUARIO.github.io/hitster

Instalación de dependencias:
    pip install qrcode[pil] pillow
"""

import json
import os
import argparse

def generate_qrs(base_url: str):
    # Leer canciones
    with open("songs.json", "r", encoding="utf-8") as f:
        songs = json.load(f)

    os.makedirs("qrcodes", exist_ok=True)

    try:
        import qrcode
        from PIL import Image
    except ImportError:
        print("❌ Instalá las dependencias primero:")
        print("   pip install qrcode[pil] pillow")
        return

    base_url = base_url.rstrip("/")

    for song in songs:
        song_id = song["id"]
        url = f"{base_url}/?song={song_id}"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        output_path = f"qrcodes/{song_id}.png"
        img.save(output_path)
        print(f"✅ QR generado: {output_path}  →  {url}")

    print(f"\n🎉 {len(songs)} QR codes generados en la carpeta qrcodes/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generador de QR codes para Hitster Personal")
    parser.add_argument(
        "--url",
        required=True,
        help="URL base de tu GitHub Pages. Ej: https://tu_usuario.github.io/hitster"
    )
    args = parser.parse_args()
    generate_qrs(args.url)

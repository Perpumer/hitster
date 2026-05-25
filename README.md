# 🎵 Hitster Personal

Tu propia versión del juego Hitster con canciones personalizadas.

---

## Estructura del proyecto

```
hitster/
├── index.html          ← Reproductor web (va a GitHub Pages)
├── songs.json          ← Base de datos de canciones
├── songs/              ← Acá van los archivos MP3
│   ├── 001.mp3
│   └── ...
├── qrcodes/            ← QR codes generados (se crean automáticamente)
├── generate_qr.py      ← Script para generar QR codes
└── generate_cards.py   ← Script para generar el PDF imprimible
```

---

## Paso 1 — Crear el repositorio en GitHub

1. Entrá a [github.com](https://github.com) y hacé clic en **New repository**
2. Nombre: `hitster` (importante: en minúsculas, sin espacios)
3. Visibilidad: **Public** (necesario para GitHub Pages gratuito)
4. Hacé clic en **Create repository**

---

## Paso 2 — Subir los archivos

Podés hacerlo de dos formas:

**Opción A — Desde la web de GitHub (más fácil):**
1. En tu repositorio, hacé clic en **Add file → Upload files**
2. Subí `index.html` y `songs.json`
3. Creá la carpeta `songs/` subiendo un MP3 (GitHub crea la carpeta automáticamente)
4. Repetí para cada MP3

**Opción B — Con Git (más rápido si tenés muchas canciones):**
```bash
git init
git remote add origin https://github.com/TU_USUARIO/hitster.git
git add .
git commit -m "Primer commit - Hitster Personal"
git push -u origin main
```

---

## Paso 3 — Activar GitHub Pages

1. En tu repositorio, hacé clic en **Settings**
2. En el menú lateral, hacé clic en **Pages**
3. En "Branch", seleccioná **main** y hacé clic en **Save**
4. Esperá 1-2 minutos y tu sitio estará en:
   ```
   https://TU_USUARIO.github.io/hitster/
   ```

---

## Paso 4 — Editar songs.json con tus canciones

Abrí `songs.json` y completá tus canciones. El formato es:

```json
[
  {
    "id": "001",
    "title": "Nombre de la Canción",
    "artist": "Nombre del Artista",
    "year": 1995,
    "file": "songs/001.mp3"
  }
]
```

**Reglas:**
- El `id` debe coincidir con el nombre del archivo MP3 (ej: `"001"` → `songs/001.mp3`)
- Nombrá los MP3 con números con ceros al principio: `001.mp3`, `002.mp3`, etc.
- El `year` es el año en que se lanzó la canción (es lo que se revela en el dorso de la carta)

---

## Paso 5 — Generar los QR codes

Instalá las dependencias:
```bash
pip install qrcode[pil] pillow
```

Ejecutá el script (reemplazá `TU_USUARIO` con tu usuario de GitHub):
```bash
python generate_qr.py --url https://TU_USUARIO.github.io/hitster
```

Los QR codes se guardan en la carpeta `qrcodes/` como `001.png`, `002.png`, etc.

---

## Paso 6 — Generar las cartas PDF para imprimir

Instalá las dependencias:
```bash
pip install reportlab pillow
```

Ejecutá el script:
```bash
python generate_cards.py
```

Se generan dos archivos:
- `cartas_frente.pdf` — con los QR codes (frente de cada carta)
- `cartas_dorso.pdf` — con el año y nombre (dorso de cada carta)

**Para imprimir a doble cara manual:**
1. Imprimí `cartas_frente.pdf`
2. Volvé a cargar el papel en la impresora con la cara impresa hacia arriba/abajo (depende de tu impresora)
3. Imprimí `cartas_dorso.pdf`
4. Cortá las cartas con tijera o guillotina

---

## Cómo se juega

Las reglas son iguales al Hitster original:

1. Cada jugador empieza con una carta en su línea de tiempo
2. En tu turno, tomás una carta, escaneás el QR y escuchás la canción
3. Tenés que ubicarla **en el orden cronológico correcto** entre las cartas que ya tenés
4. Si acertás el año relativo, te quedás con la carta y seguís construyendo tu línea de tiempo
5. Gana quien llegue primero a **10 cartas** en su línea de tiempo

---

## Agregar más canciones

1. Agregá el MP3 a la carpeta `songs/` con el número siguiente
2. Agregá la entrada en `songs.json`
3. Volvé a correr `generate_qr.py`
4. Volvé a correr `generate_cards.py`
5. Subí el MP3 nuevo y el `songs.json` actualizado a GitHub

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/CustomTkinter-0078D7?style=for-the-badge&logo=python&logoColor=white" alt="CustomTkinter">
  <img src="https://img.shields.io/badge/YT--DLP-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YT-DLP">
</div>

# 🎥 Sebs YT Downloader

¡Un descargador de videos y listas de reproducción de YouTube con una interfaz gráfica moderna, elegante y _bien mela_! Construido en Python para hacer la vida mucho más fácil a la hora de descargar tu música o videos favoritos.

---

## ✨ Características

- 🎵 **Descargas en MP3 y MP4**: Extrae puro audio o baja el video completo con la mejor calidad disponible.
- 📺 **Soporte robusto para Playlists**: Pega el link de una lista de reproducción y descárgala completica. Cuenta con sistema de reintentos y reporte detallado si un video falla.
- 🎨 **Interfaz Moderna**: Diseño oscuro con acentos en verde (Dark Mode) chulísimo gracias a `CustomTkinter`.
- ⚡ **Rendimiento Óptimo**: Utiliza `yt-dlp` bajo el capó (mucho más rápido y confiable que pytube) y hace uso de `FFmpeg` para conversiones precisas sin pérdida de calidad.
- 📁 **Selección de Ruta**: Elige exactamente en qué carpeta guardar los archivos.

## 🛠️ Requisitos e Instalación

1. Clona este repositorio o descarga los archivos.
2. Asegúrate de tener Python instalado en tu compu (preferiblemente 3.8 o superior).
3. Instala las dependencias necesarias. Puedes hacerlo abriendo tu terminal y ejecutando:

```bash
pip install customtkinter yt-dlp imageio-ffmpeg
```

_(Nota: `imageio-ffmpeg` se encarga de descargar y proveer el ejecutable de FFmpeg automáticamente para este proyecto, así que no tienes que preocuparte por configurarlo a mano)._

## 🚀 Uso

Es tan simple como correr el archivo principal:

```bash
python main.py
```

1. **Pega el enlace** (link del video o playlist) en la barra principal.
2. Presiona en **Obtener info** para ver los detalles del video/canal.
3. Elige el **formato** (MP4 o MP3) y la **calidad** de video deseada si descargas en MP4.
4. Elige tu **carpeta de destino** pinchando en "Elegir carpeta destino".
5. ¡Presiona **Descargar**!

## 📦 Ejecutable (.exe)

El proyecto ya está configurado para generar un ejecutable usando PyInstaller (`SebsYTDownloader.spec`). Para compilarlo tú mismo y no depender de Python:

**1. Instala los requerimientos**
```bash
pip install -r requirements.txt
```

**2. Obtén la ruta de FFmpeg**
Antes de compilar necesitas saber dónde está el FFmpeg que instaló `imageio-ffmpeg` en tu PC. Corre esto:

```bash
python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"
```

**3. Compila el ejecutable**
Reemplaza `<RUTA_FFMPEG>` con la ruta que obtuviste arriba y ejecuta:

```bash
python -m PyInstaller --onefile --windowed --name "SebsYTDownloader" --add-binary "<RUTA_FFMPEG>;imageio_ffmpeg/binaries" main.py
```

*(Opcional: Si ya tienes todo configurado o quieres usar el archivo .spec existente)*
```bash
pyinstaller SebsYTDownloader.spec
```

El `.exe` quedará en la carpeta `dist`.

## 📂 Archivos del Proyecto

- `main.py`: Punto de entrada de la aplicación.
- `ui.py`: Contiene toda la lógica de la interfaz gráfica y notificaciones del usuario.
- `downloader.py`: Es el corazón de la descarga. Maneja toda la lógica de `yt-dlp`, los reintentos automáticos y el post-procesado con `FFmpeg`.
- `test.py`: Pruebas de código u operaciones desde consola (script de testing).

---

<p align="center">
  Hecho con 🩵 por <b>Sebs</b>
</p>

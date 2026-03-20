<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/CustomTkinter-0078D7?style=for-the-badge&logo=python&logoColor=white" alt="CustomTkinter">
  <img src="https://img.shields.io/badge/YT--DLP-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YT-DLP">
</div>

# 🎥 Sebs YT Downloader

¡Un descargador de videos y listas de reproducción de YouTube con una interfaz gráfica moderna, elegante y *bien mela*! Construido en Python para hacer la vida mucho más fácil a la hora de descargar tu música o videos favoritos.

---

## ✨ Características

- 🎵 **Descargas en MP3 y MP4**: Extrae puro audio o baja el video completo con la mejor calidad.
- 📺 **Soporte para Playlists**: Pega el link de una lista de reproducción y descárgala completica, sin enredarse.
- 🎨 **Interfaz Moderna**: Diseño oscuro (Dark Mode) chulísimo gracias a `CustomTkinter`.
- ⚡ **Rendimiento Óptimo**: Utiliza `yt-dlp` bajo el capó (mucho más rápido y confiable que pytube) y hace uso de `FFmpeg` para conversiones precisas.
- 📁 **Selección de Ruta**: Elige exactamente en qué carpeta guardar los archivos.

## 🛠️ Requisitos e Instalación

1. Clona este repositorio o descarga los archivos.
2. Asegúrate de tener Python instalado en tu compu (preferiblemente 3.8 o superior).
3. Instala las dependencias necesarias. Puedes hacerlo abriendo tu terminal y ejecutando:

```bash
pip install customtkinter yt-dlp imageio-ffmpeg
```

*(Nota: `imageio-ffmpeg` se encarga de descargar y proveer el ejecutable de FFmpeg automáticamente para este proyecto, así que no tienes que preocuparte por configurarlo a mano).*

## 🚀 Uso

Es tan simple como correr el archivo de la interfaz:

```bash
python ui.py
```

1. **Pega el enlace** (link del video o playlist) en la barra principal.
2. Presiona en **Obtener info** para ver los detalles del video/canal.
3. Elige el **formato** (MP4 o MP3).
4. Elige tu **carpeta de destino** pinchando en "Elegir carpeta destino".
5. ¡Descarga! (*(Asegúrate de haber habilitado el botón de descargar si lo tienes comentado en el código 😉)*)

## 📂 Archivos del Proyecto

- `ui.py`: Contiene toda la lógica de la interfaz gráfica moderna. 
- `downloader.py`: Es el corazón de la descarga, maneja toda la lógica potente de `yt-dlp` y el post-procesado con `FFmpeg`.
- `test.py`: Pruebas de código que muestran cómo interactuar con `downloader.py` desde la consola.

---

<p align="center">
  Hecho con 🩵 por <b>Sebs</b>
</p>

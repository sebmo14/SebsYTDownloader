import yt_dlp
import imageio_ffmpeg


class Downloader:
    def __init__(self):
        self.downloading = False
        self.folder = ""
        self.callback_progress = None

    def format_duration(self, seconds):
        if not seconds:
            return "Desconocida"

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"

    def progress_hook(self, d):
        if d["status"] == "downloading":
            downloaded = d.get("downloaded_bytes", 0)
            total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)

            if total > 0:
                percent = downloaded / total
                if self.callback_progress:
                    self.callback_progress(percent, f"Descargando: {percent:.0%}")
                print(f"Progreso: {percent:.0%}")

        elif d["status"] == "finished":
            if self.callback_progress:
                self.callback_progress(1, "Descarga finalizada")
            print("Descarga finalizada en la carpeta: ", self.folder)

    def download(self, url, folder, fmt, callback_progress=None):
        self.downloading = True
        self.folder = folder
        self.callback_progress = callback_progress
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

        opciones = {
            "outtmpl": f"{folder}/%(title)s.%(ext)s",
            "progress_hooks": [self.progress_hook],
            "ffmpeg_location": ffmpeg_path,
        }

        if fmt == "mp3":
            opciones["format"] = "bestaudio/best"
            opciones["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ]
        else:
            opciones["format"] = fmt
            opciones["merge_output_format"] = "mp4"
            opciones["postprocessor_args"] = {"merger": ["-c:v", "copy", "-c:a", "aac"]}
        try:
            with yt_dlp.YoutubeDL(opciones) as ydl:
                ydl.download([url])
        except Exception as e:
            print("Error", e)
        finally:
            self.downloading = False

    def get_info_formats(self, url):
        options = {
            "quiet": True,
            "skip_download": True,
        }
        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=False)
            result = {
                "title": info.get("title", "Sin título"),
                "duration": self.format_duration(info.get("duration", 0)),
                "thumbnail": info.get("thumbnail", ""),
                "channel": info.get("channel", "Desconocido"),
                "is_playlist": info.get("_type") == "playlist",
                "playlist_count": info.get("playlist_count", 0),
            }

            formats = info.get("formats", [])

            alturas = set()
            for f in formats:
                height = f.get("height")
                has_video = f.get("vcodec") != "none"
                if has_video and height:
                    alturas.add(height)

            formats = []
            for height in sorted(alturas, reverse=True):
                formats.append(
                    {
                        "label": f"{height}p",
                        "format_id": f"bestvideo[height<={height}]+bestaudio/best[height<={height}]",
                        "height": height,
                    }
                )

            formats.insert(
                0,
                {
                    "label": "Mejor calidad",
                    "format_id": "bestvideo+bestaudio/best",
                    "height": 9999,
                },
            )

            result["formats"] = formats
            return result

        except Exception as e:
            print("Error al obtener información", e)
            return None

    def download_playlist(
        self, url, folder, fmt, start=1, end=None, callback_progress=None
    ):
        self.downloading = True
        self.folder = folder
        self.failed = []
        self.callback_progress = callback_progress

        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

        def error_hook(d):
            if d["status"] == "error":
                titulo = d.get("info_dict", {}).get(
                    "title", d.get("filename", "Video desconocido")
                )
                if titulo not in self.failed:
                    self.failed.append(titulo)
                    print(f" Falló: {titulo}")

        opciones = {
            "outtmpl": f"{folder}/%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s",
            "progress_hooks": [self.progress_hook, error_hook],
            "ffmpeg_location": ffmpeg_path,
            "ignoreerrors": True,
            "retries": 5,
            "fragment_retries": 10,
            "sleep_interval": 2,
            "continuedl": True,
            "quiet": True,
            "no_warnings": True,
        }

        if end:
            opciones["playliststart"] = start
            opciones["playlistend"] = end
        else:
            opciones["playliststart"] = start

        if fmt == "mp3":
            opciones["format"] = "bestaudio/best"
            opciones["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ]
        else:
            opciones["format"] = fmt
            opciones["merge_output_format"] = "mp4"
            opciones["postprocessor_args"] = {"merger": ["-c:v", "copy", "-c:a", "aac"]}

        try:
            with yt_dlp.YoutubeDL(opciones) as ydl:
                ydl.download([url])
        except Exception as e:
            print("Error:", e)
        finally:
            self.downloading = False

        if self.failed:
            print(f"\n {len(self.failed)} video(s) fallaron:")
            for f in self.failed:
                print(f"  - {f}")
        else:
            print("\n Todos los videos se descargaron correctamente")

import customtkinter as ctk
from downloader import Downloader

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("YT Downloader BY sebs")
        self.geometry("700x800")
        self.resizable(True, True)
        self.callback_progress = None
        self.is_playlist = False
        self.playlist_count = 0

        self.downloader = Downloader()

        self.folder_path = ctk.StringVar(value=".")
        self.fmt = ctk.StringVar(value="mp4")
        self.formats_list = []

        self.build_url_section()
        self.build_info_section()
        self.build_options_section()
        self.build_download_section()

    def build_url_section(self):
        frame = ctk.CTkFrame(self)
        frame.pack(fill="x", padx=20, pady=(20, 10))

        tittle = ctk.CTkLabel(
            frame,
            text="YT Downloader BY sebs",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        tittle.pack(pady=(10, 5))

        darkmode_switch = ctk.CTkSwitch(
            self,
            text="Light mode",
            command=self.toggle_darkmode,
        )
        darkmode_switch.place(relx=0.95, rely=0.02, anchor="ne")

        self.url_entry = ctk.CTkEntry(
            frame,
            placeholder_text="Ponga el link del video o playlist aca, mi so",
            width=500,
            height=40,
        )
        self.url_entry.pack(pady=(5, 10))

        self.btn_info = ctk.CTkButton(
            frame,
            text="Obtener info",
            command=self.get_info_action,
            width=200,
        )
        self.btn_info.pack(pady=(0, 10))

    def get_info_action(self):
        url = self.url_entry.get()
        if not url:
            return

        self.btn_info.configure(state="disabled", text="Obteniendo info...")

        import threading

        hilo = threading.Thread(target=self._run_get_info, args=(url,))
        hilo.daemon = True
        hilo.start()

    def _run_get_info(self, url):
        result = self.downloader.get_info_formats(url)
        self.after(0, self._on_info_finished, result)

    def _on_info_finished(self, result):
        self.btn_info.configure(state="normal", text="Obtener info")

        if not result:
            return

        self.label_title.configure(text=f"Título: {result['title']}")
        self.label_channel.configure(text=f"Canal: {result['channel']}")
        self.label_duration.configure(text=f"Duración: {result['duration']}")
        self.label_status.configure(text="Informacion obtenida correctamente")

        # detectar playlist
        self.is_playlist = result["is_playlist"]
        self.playlist_count = result["playlist_count"]

        if self.is_playlist:
            self.label_playlist_info.configure(
                text=f"Playlist: {self.playlist_count} videos"
            )
            self.entry_end.delete(0, "end")
            self.entry_end.insert(0, str(self.playlist_count))
            self.frame_playlist.grid()
        else:
            self.frame_playlist.grid_remove()

        formats = result.get("formats")
        self.formats_list = formats
        labels = [f["label"] for f in self.formats_list]
        self.quality_menu.configure(values=labels)
        if labels:
            self.quality_menu.set(labels[0])

    def build_info_section(self):
        self.frame_info = ctk.CTkFrame(self)
        self.frame_info.pack(fill="x", padx=20, pady=(20, 10))

        self.thumbnail_label = ctk.CTkLabel(self.frame_info, text="")
        self.thumbnail_label.grid(row=0, column=0, rowspan=3, padx=10, pady=10)

        self.label_title = ctk.CTkLabel(
            self.frame_info,
            text="Título: —",
            font=ctk.CTkFont(size=13, weight="bold"),
            wraplength=380,
            anchor="w",
        )
        self.label_title.grid(row=0, column=1, sticky="w", padx=10, pady=(10, 2))

        self.label_channel = ctk.CTkLabel(
            self.frame_info,
            text="Canal: —",
            anchor="w",
        )
        self.label_channel.grid(row=1, column=1, sticky="w", padx=10)

        self.label_duration = ctk.CTkLabel(
            self.frame_info,
            text="Duración: —",
            anchor="w",
        )
        self.label_duration.grid(row=2, column=1, sticky="w", padx=10, pady=(2, 10))

    def build_options_section(self):
        frame = ctk.CTkFrame(self)
        frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            frame, text="Opciones de descarga", font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(10, 5))

        inner = ctk.CTkFrame(frame, fg_color="transparent")
        inner.pack(fill="x", padx=10, pady=10)

        # --- formato ---
        ctk.CTkLabel(inner, text="Formato:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )

        self.btn_mp4 = ctk.CTkButton(
            inner, text="MP4", width=80, command=lambda: self.set_formato("mp4")
        )
        self.btn_mp4.grid(row=0, column=1, padx=5, pady=10)

        self.btn_mp3 = ctk.CTkButton(
            inner, text="MP3", width=80, command=lambda: self.set_formato("mp3")
        )
        self.btn_mp3.grid(row=0, column=2, padx=5, pady=10)

        # --- calidad ---
        ctk.CTkLabel(inner, text="Calidad:").grid(
            row=1, column=0, padx=10, pady=10, sticky="w"
        )

        self.quality_menu = ctk.CTkOptionMenu(
            inner, values=["Mejor calidad"], width=200
        )
        self.quality_menu.grid(
            row=1, column=1, columnspan=2, padx=5, pady=10, sticky="w"
        )

        # --- carpeta ---
        ctk.CTkLabel(inner, text="Carpeta:").grid(
            row=2, column=0, padx=10, pady=10, sticky="w"
        )

        self.folder_entry = ctk.CTkEntry(
            inner, textvariable=self.folder_path, width=300
        )
        self.folder_entry.grid(
            row=2, column=1, columnspan=2, padx=5, pady=10, sticky="w"
        )

        self.btn_folder = ctk.CTkButton(
            inner,
            text="Elegir carpeta destino",
            width=80,
            command=self.choose_folder,
        )
        self.btn_folder.grid(row=2, column=3, padx=5, pady=10)

        # --- opciones playlist ---
        self.frame_playlist = ctk.CTkFrame(inner, fg_color="transparent")
        self.frame_playlist.grid(
            row=3, column=0, columnspan=4, sticky="w", padx=10, pady=5
        )

        self.label_playlist_info = ctk.CTkLabel(
            self.frame_playlist, text="", anchor="w"
        )
        self.label_playlist_info.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(self.frame_playlist, text="Desde:").pack(side="left", padx=(0, 5))
        self.entry_start = ctk.CTkEntry(self.frame_playlist, width=50)
        self.entry_start.insert(0, "1")
        self.entry_start.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(self.frame_playlist, text="Hasta:").pack(side="left", padx=(0, 5))
        self.entry_end = ctk.CTkEntry(self.frame_playlist, width=50)
        self.entry_end.pack(side="left")

        # ocultar por defecto
        self.frame_playlist.grid_remove()

    def set_formato(self, fmt):
        self.fmt.set(fmt)
        if fmt == "mp4":
            self.btn_mp4.configure(fg_color="#1f6aa5")
            self.btn_mp3.configure(fg_color="gray30")
            self.quality_menu.configure(state="normal")  # 👈 mostrar
        else:
            self.btn_mp3.configure(fg_color="#1f6aa5")
            self.btn_mp4.configure(fg_color="gray30")
            self.quality_menu.configure(state="disabled")

    def choose_folder(self):
        from tkinter import filedialog

        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def build_download_section(self):
        frame = ctk.CTkFrame(self)
        frame.pack(fill="x", padx=20, pady=(0, 20))

        # boton descargar
        self.btn_download = ctk.CTkButton(
            frame,
            text="⬇ Descargar",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            command=self.on_download,
        )
        self.btn_download.pack(fill="x", padx=20, pady=(15, 10))

        # barra de progreso
        self.progress_bar = ctk.CTkProgressBar(frame, width=500)
        self.progress_bar.pack(padx=20, pady=(0, 5))
        self.progress_bar.set(0)

        # label de estado
        self.label_status = ctk.CTkLabel(frame, text="Esperando...")
        self.label_status.pack(pady=(0, 15))

    def on_download(self):
        url = self.url_entry.get()
        folder = self.folder_path.get()
        fmt = self.fmt.get()

        if not url:
            self.label_status.configure(text="Ingresa una URL!")
            return
        if not folder:
            self.label_status.configure(text="Elige una carpeta!")
            return

        if fmt == "mp3":
            format_id = "mp3"
        else:
            calidad_label = self.quality_menu.get()
            format_id = "bestvideo+bestaudio/best"
            for f in self.formats_list:
                if f.get("label") == calidad_label:
                    format_id = f["format_id"]
                    break

        self.btn_download.configure(state="disabled", text="Descargando...")
        self.label_status.configure(text="Iniciando descarga...")
        self.progress_bar.set(0)

        import threading

        if self.is_playlist:
            start = int(self.entry_start.get() or 1)
            end_val = self.entry_end.get()
            end = int(end_val) if end_val else None
            hilo = threading.Thread(
                target=self._run_download_playlist,
                args=(url, folder, format_id, start, end),
            )
        else:
            hilo = threading.Thread(
                target=self._run_download, args=(url, folder, format_id)
            )

        hilo.daemon = True
        hilo.start()

    def _run_download(self, url, folder, format_id):
        def actualizar_ui(porcentaje, status):
            self.progress_bar.set(porcentaje)
            self.label_status.configure(text=status)

        def callback(porcentaje, status):
            self.after(0, actualizar_ui, porcentaje, status)

        self.downloader.download(url, folder, format_id, callback_progress=callback)

        # al terminar, volver a habilitar el botón desde el hilo principal
        self.after(0, self._on_download_finished)

    def _run_download_playlist(self, url, folder, format_id, start, end):
        def actualizar_ui(porcentaje, status):
            self.progress_bar.set(porcentaje)
            self.label_status.configure(text=status)

        def callback(porcentaje, status):
            self.after(0, actualizar_ui, porcentaje, status)

        self.downloader.download_playlist(
            url, folder, format_id, start=start, end=end, callback_progress=callback
        )
        self.after(0, self._on_download_finished)

    def _on_download_finished(self):
        self.btn_download.configure(state="normal", text="⬇ Descargar")
        self.label_status.configure(text="Descarga completada")
        self.progress_bar.set(1)

        if hasattr(self.downloader, "failed") and self.downloader.failed:
            self.show_failed_download(self.downloader.failed)

    def show_failed_download(self, failed):
        if not failed:
            return
        ventana = ctk.CTkToplevel(self)

        ventana.title("Videos que fallaron")
        ventana.geometry("500x400")
        ventana.grab_set()  # bloquea la ventana principal hasta cerrar esta

        ctk.CTkLabel(
            ventana,
            text=f" {len(failed)} video(s) no se pudieron descargar:",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(pady=(20, 10), padx=20)

        # caja de texto con scroll para listar los fallos
        textbox = ctk.CTkTextbox(ventana, width=460, height=280)
        textbox.pack(padx=20, pady=(0, 10))

        for f in failed:
            textbox.insert("end", f"FALLO: {f}\n")

        textbox.configure(state="disabled")  # solo lectura

        ctk.CTkButton(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)

    def toggle_darkmode(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")


if __name__ == "__main__":
    app = App()
    app.mainloop()

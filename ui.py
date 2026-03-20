import customtkinter as ctk
from downloader import Downloader

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("YT Downloader BY sebs")
        self.geometry("700x800")
        self.resizable(False, False)

        self.downloader = Downloader()

        self.folder_path = ctk.StringVar(value=".")
        self.fmt = ctk.StringVar(value="mp4")
        self.formats_list = []

        self.build_url_section()
        self.build_info_section()
        self.build_options_section()
        # self.build_download_section()

    def build_url_section(self):
        frame = ctk.CTkFrame(self)
        frame.pack(fill="x", padx=20, pady=(20, 10))

        tittle = ctk.CTkLabel(
            frame,
            text="YT Downloader BY sebs",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        tittle.pack(pady=(10, 5))

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

        info = self.downloader.get_info(url)
        if not info:
            return

        self.label_title.configure(text=f"Título: {info['title']}")
        self.label_channel.configure(text=f"Canal: {info['channel']}")
        self.label_duration.configure(text=f"Duración: {info['duration']}")

        formats = self.downloader.get_formats(url)
        self.formats_list = [f["label"] for f in formats]
        self.quality_menu.configure(values=self.formats_list)

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

    def set_formato(self, fmt):
        self.fmt.set(fmt)
        if fmt == "mp4":
            self.btn_mp4.configure(fg_color="#1f6aa5")
            self.btn_mp3.configure(fg_color="gray30")
        else:
            self.btn_mp3.configure(fg_color="#1f6aa5")
            self.btn_mp4.configure(fg_color="gray30")

    def choose_folder(self):
        from tkinter import filedialog

        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)


if __name__ == "__main__":
    app = App()
    app.mainloop()

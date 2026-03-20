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

        # self.build_url_section()
        # self.build_info_section()
        # self.build_options_section()
        # self.build_download_section()


if __name__ == "__main__":
    app = App()
    app.mainloop()

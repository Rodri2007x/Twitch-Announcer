import customtkinter as ctk
import threading
import requests
import time
from tkinter import messagebox
import os
import sys
import winshell
from os.path import join, expanduser

CHANNELS_FILE = "channels.txt"
STARTUP_FOLDER = winshell.startup()
SHORTCUT_NAME = "TwitchAnnouncer.lnk"

class TwitchAnnouncerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Twitch Announcer")
        self.geometry("500x480")
        ctk.set_appearance_mode("dark")

        self.channels = self.load_channels()
        self.live_status = {channel: False for channel in self.channels}
        self.channel_frames = {}
        self.check_interval = ctk.IntVar(value=60)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Input Frame ---
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.channel_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Nombre del canal")
        self.channel_entry.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="ew")

        self.add_button = ctk.CTkButton(self.input_frame, text="Añadir", command=self.add_channel)
        self.add_button.grid(row=0, column=1, padx=(5, 0), pady=5)

        # --- Channel List Frame ---
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Canales Seguidos")
        self.scrollable_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # --- Status & Settings Frame ---
        self.status_frame = ctk.CTkFrame(self)
        self.status_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.status_frame.grid_columnconfigure(1, weight=1)

        self.interval_label = ctk.CTkLabel(self.status_frame, text=f"Intervalo: {self.check_interval.get()}s")
        self.interval_label.grid(row=0, column=0, padx=10)

        self.interval_slider = ctk.CTkSlider(self.status_frame, from_=30, to=300, number_of_steps=27, variable=self.check_interval, command=self.update_interval_label)
        self.interval_slider.grid(row=0, column=1, sticky="ew", padx=5)

        self.countdown_label = ctk.CTkLabel(self.status_frame, text="Iniciando...")
        self.countdown_label.grid(row=0, column=2, padx=10)

        self.startup_var = ctk.BooleanVar(value=self.is_startup_shortcut_present())
        self.startup_check = ctk.CTkCheckBox(self.status_frame, text="Iniciar con Windows", variable=self.startup_var, command=self.toggle_startup)
        self.startup_check.grid(row=1, column=0, columnspan=3, pady=10, padx=10, sticky="w")

        self.update_channel_display()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.monitoring_thread = threading.Thread(target=self.monitor_channels, daemon=True)
        self.monitoring_thread.start()

    def update_interval_label(self, value):
        self.interval_label.configure(text=f"Intervalo: {int(value)}s")

    def load_channels(self):
        if not os.path.exists(CHANNELS_FILE):
            return ["sayko_o6"]
        with open(CHANNELS_FILE, "r") as f:
            return [line.strip() for line in f if line.strip()]

    def save_channels(self):
        with open(CHANNELS_FILE, "w") as f:
            for channel in self.channels:
                f.write(f"{channel}\n")

    def add_channel(self):
        channel_name = self.channel_entry.get().strip().lower()
        if channel_name and channel_name not in self.channels:
            self.channels.append(channel_name)
            self.live_status[channel_name] = False
            self.channel_entry.delete(0, "end")
            self.update_channel_display()
            self.save_channels()

    def remove_channel(self, channel_name):
        if channel_name in self.channels:
            self.channels.remove(channel_name)
            self.live_status.pop(channel_name, None)
            if channel_name in self.channel_frames:
                self.channel_frames[channel_name].destroy()
                self.channel_frames.pop(channel_name, None)
            self.save_channels()

    def update_channel_display(self):
        for frame in self.channel_frames.values():
            frame.destroy()
        self.channel_frames.clear()

        for channel in self.channels:
            frame = ctk.CTkFrame(self.scrollable_frame)
            frame.pack(fill="x", padx=5, pady=5)
            frame.grid_columnconfigure(0, weight=1)

            status = self.live_status.get(channel, False)
            status_text = "  Online" if status else "  Offline"
            status_color = "#2ECC71" if status else "#E74C3C"

            label = ctk.CTkLabel(frame, text=f"{channel.capitalize()}{status_text}", anchor="w")
            label.grid(row=0, column=0, sticky="ew", padx=5)

            status_indicator = ctk.CTkLabel(frame, text="", fg_color=status_color, width=10, height=10)
            status_indicator.grid(row=0, column=1, padx=5)

            remove_button = ctk.CTkButton(frame, text="Eliminar", width=70, command=lambda c=channel: self.remove_channel(c))
            remove_button.grid(row=0, column=2, padx=5)
            
            self.channel_frames[channel] = frame

    def is_live(self, channel_name):
        url = f"https://www.twitch.tv/{channel_name}"
        try:
            response = requests.get(url, headers={"Cache-Control": "no-cache"}, timeout=10)
            response.raise_for_status()
            return '"isLiveBroadcast":true' in response.text
        except requests.exceptions.RequestException:
            return False

    def monitor_channels(self):
        while True:
            self.after(0, self.update_countdown_label, "Comprobando...")
            needs_update = False
            for channel in list(self.channels):
                status = self.is_live(channel)
                if status and not self.live_status.get(channel, False):
                    self.show_popup(channel)
                    self.live_status[channel] = True
                    needs_update = True
                elif not status and self.live_status.get(channel, False):
                    self.live_status[channel] = False
                    needs_update = True
            
            if needs_update:
                self.after(0, self.update_channel_display)

            for i in range(self.check_interval.get(), 0, -1):
                self.after(0, self.update_countdown_label, f"Próx. en {i}s")
                time.sleep(1)

    def update_countdown_label(self, text):
        self.countdown_label.configure(text=text)

    def show_popup(self, channel_name):
        messagebox.showinfo("¡Directo en Twitch!", f"¡{channel_name.upper()} ha iniciado un directo!")

    def is_startup_shortcut_present(self):
        return os.path.exists(os.path.join(STARTUP_FOLDER, SHORTCUT_NAME))

    def toggle_startup(self):
        shortcut_path = os.path.join(STARTUP_FOLDER, SHORTCUT_NAME)
        is_checked = self.startup_var.get()

        if not getattr(sys, 'frozen', False):
            messagebox.showwarning("Aviso", "Esta función solo crea un acceso directo funcional cuando se ejecuta desde el archivo .exe final.")
            # For development, we can point to the python executable
            target_path = sys.executable
            working_directory = os.path.dirname(os.path.abspath(__file__))
            icon_path = target_path
        else:
            target_path = sys.executable
            working_directory = os.path.dirname(target_path)
            icon_path = target_path

        if is_checked:
            if not self.is_startup_shortcut_present():
                with winshell.shortcut(shortcut_path) as shortcut:
                    shortcut.path = target_path
                    shortcut.working_directory = working_directory
                    shortcut.icon_location = (icon_path, 0)
        else:
            if self.is_startup_shortcut_present():
                os.remove(shortcut_path)

    def on_closing(self):
        self.save_channels()
        self.destroy()

if __name__ == "__main__":
    app = TwitchAnnouncerApp()
    app.mainloop()

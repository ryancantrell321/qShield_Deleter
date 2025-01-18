import os
import shutil
import sys
import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk
from colorama import Fore, Style, init
from datetime import datetime

# Initialize colorama for colored output
init(autoreset=True)

def configure_icon(master, icon_path):
    ico = getattr(sys, '_MEIPASS', '.') + f"/{icon_path}"
    image = Image.open(ico)
    icon = ImageTk.PhotoImage(image)
    master.tk.call('wm', 'iconphoto', master._w, icon)

class FolderCleanupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("qShield qBittorrent Cleanup Tool")
        self.root.geometry("500x400")
        configure_icon(self.root, "bin.ico")
        self.root.config(bg="#f2f2f2")

        # Header label
        self.header_label = tk.Label(self.root, text="qBittorrent Cleanup Tool", font=("Arial", 16, "bold"), bg="darkgreen", fg="white", pady=20)
        self.header_label.pack(fill="x")

        # Info Text
        self.info_text = tk.Label(self.root, text="This tool will help you delete the contents of qBittorrent folders.", font=("Arial", 12), bg="#f2f2f2", fg="#333")
        self.info_text.pack(pady=10)

        # Path Labels
        self.localappdata_label = tk.Label(self.root, text="Path: %localappdata%\\qBittorrent", font=("Arial", 10), bg="#f2f2f2", fg="#555")
        self.localappdata_label.pack(pady=5)
        self.appdata_label = tk.Label(self.root, text="Path: %appdata%\\qBittorrent", font=("Arial", 10), bg="#f2f2f2", fg="#555")
        self.appdata_label.pack(pady=5)

        # Action Buttons
        self.cleanup_button = tk.Button(self.root, text="Start Cleanup", font=("Arial", 12, "bold"), bg="#ff5722", fg="white", command=self.start_cleanup)
        self.cleanup_button.pack(pady=30, padx=50, fill="x")

        # Status Label
        self.status_label = tk.Label(self.root, text="Waiting for action...", font=("Arial", 10), bg="#f2f2f2", fg="#777")
        self.status_label.pack(pady=5)

        # Footer Label with dynamic year and company name
        current_year = datetime.now().year
        self.footer_label = tk.Label(self.root, text=f"{current_year} Pandora Dynamics", font=("Arial", 10, "italic"), bg="darkgreen", fg="white", pady=10)
        self.footer_label.pack(side="bottom", fill="x")

    def delete_folder_contents(self, folder_path):
        try:
            if os.path.exists(folder_path):
                self.status_label.config(text=f"Found folder: {folder_path}", fg="blue")

                confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete all contents of:\n{folder_path}?")

                if confirm:
                    for item in os.listdir(folder_path):
                        item_path = os.path.join(folder_path, item)
                        try:
                            if os.path.isfile(item_path) or os.path.islink(item_path):
                                os.unlink(item_path)
                            elif os.path.isdir(item_path):
                                shutil.rmtree(item_path)
                            print(f"{Fore.GREEN}Deleted: {item_path}")
                        except Exception as e:
                            print(f"{Fore.RED}Failed to delete {item_path}: {e}")
                    self.status_label.config(text=f"All contents of '{folder_path}' have been deleted.", fg="green")
                else:
                    self.status_label.config(text=f"Skipped deleting contents of '{folder_path}'.", fg="red")
            else:
                self.status_label.config(text=f"Folder does not exist: {folder_path}", fg="red")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def start_cleanup(self):
        # Paths to the folders
        localappdata_qbittorrent = os.path.expandvars(r'%localappdata%\qBittorrent')
        appdata_qbittorrent = os.path.expandvars(r'%appdata%\qBittorrent')

        # Start cleanup process
        self.status_label.config(text="Cleaning up folders...", fg="orange")
        self.cleanup_button.config(state="disabled")

        self.delete_folder_contents(localappdata_qbittorrent)
        self.delete_folder_contents(appdata_qbittorrent)

        # Reset button and status after operation
        self.cleanup_button.config(state="normal")
        self.status_label.config(text="Cleanup complete!", fg="blue")


# Run the Tkinter Application
if __name__ == "__main__":
    root = tk.Tk()
    app = FolderCleanupApp(root)
    root.mainloop()

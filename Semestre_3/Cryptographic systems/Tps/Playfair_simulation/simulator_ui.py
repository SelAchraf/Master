import tkinter as tk
from tkinter import font, messagebox, scrolledtext
from playfair_cipher import crypt

# --- Main Application Class ---
class PlayfairApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Playfair Cipher Simulator")
        self.geometry("1000x600")
        self.configure(bg="#2E2E2E")
        self.resizable(False, False)

        # --- FONT & COLOR CONFIGURATION ---
        self.font_label = font.Font(family="Segoe UI", size=12)
        self.font_entry = font.Font(family="Consolas", size=12)
        self.font_button = font.Font(family="Segoe UI", size=12, weight="bold")
        self.font_matrix_header = font.Font(family="Segoe UI", size=14, weight="bold")
        self.font_matrix = font.Font(family="Consolas", size=16, weight="bold")
        
        self.color_bg = "#2E2E2E"
        self.color_fg = "#E0E0E0"
        self.color_frame = "#3C3C3C"
        self.color_entry_bg = "#505050"
        self.color_button_bg = "#007ACC"
        self.color_button_fg = "#FFFFFF"
        self.color_button_active = "#005F9E"
        self.color_accent = "#007ACC"

        # --- UI WIDGETS ---
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self, bg=self.color_bg, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- LEFT PANEL: CONTROLS ---
        controls_frame = tk.Frame(main_frame, bg=self.color_frame, padx=20, pady=20)
        controls_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Title
        tk.Label(controls_frame, text="Cipher Controls", font=self.font_matrix_header, bg=self.color_frame, fg=self.color_fg).pack(pady=(0, 20))
        
        # Keyword
        tk.Label(controls_frame, text="Keyword", font=self.font_label, bg=self.color_frame, fg=self.color_fg).pack(anchor="w")
        self.key_entry = tk.Entry(controls_frame, font=self.font_entry, bg=self.color_entry_bg, fg=self.color_fg, insertbackground=self.color_fg, relief=tk.FLAT, width=40)
        self.key_entry.pack(pady=(5, 15), ipady=5)

        # Plaintext
        tk.Label(controls_frame, text="Plaintext", font=self.font_label, bg=self.color_frame, fg=self.color_fg).pack(anchor="w")
        self.plaintext_entry = scrolledtext.ScrolledText(controls_frame, font=self.font_entry, bg=self.color_entry_bg, fg=self.color_fg, insertbackground=self.color_fg, relief=tk.FLAT, height=6, width=40, wrap=tk.WORD)
        self.plaintext_entry.pack(pady=(5, 15))

        # Ciphertext
        tk.Label(controls_frame, text="Ciphertext", font=self.font_label, bg=self.color_frame, fg=self.color_fg).pack(anchor="w")
        self.ciphertext_entry = scrolledtext.ScrolledText(controls_frame, font=self.font_entry, bg=self.color_entry_bg, fg=self.color_fg, insertbackground=self.color_fg, relief=tk.FLAT, height=6, width=40, wrap=tk.WORD)
        self.ciphertext_entry.pack(pady=(5, 20))

        # Action Buttons
        button_frame = tk.Frame(controls_frame, bg=self.color_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.encrypt_button = tk.Button(button_frame, text="Encrypt", font=self.font_button, bg=self.color_button_bg, fg=self.color_button_fg, activebackground=self.color_button_active, activeforeground=self.color_button_fg, relief=tk.FLAT, command=self.perform_encrypt, width=12)
        self.encrypt_button.pack(side=tk.LEFT, expand=True, padx=5, ipady=8)
        
        self.decrypt_button = tk.Button(button_frame, text="Decrypt", font=self.font_button, bg=self.color_button_bg, fg=self.color_button_fg, activebackground=self.color_button_active, activeforeground=self.color_button_fg, relief=tk.FLAT, command=self.perform_decrypt, width=12)
        self.decrypt_button.pack(side=tk.LEFT, expand=True, padx=5, ipady=8)

        self.clear_button = tk.Button(controls_frame, text="Clear All", font=self.font_button, bg="#707070", fg=self.color_button_fg, activebackground="#505050", activeforeground=self.color_button_fg, relief=tk.FLAT, command=self.clear_fields)
        self.clear_button.pack(fill=tk.X, pady=(10, 0), ipady=8)

        # --- RIGHT PANEL: KEY MATRIX ---
        matrix_frame = tk.Frame(main_frame, bg=self.color_frame, padx=20, pady=20)
        matrix_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        tk.Label(matrix_frame, text="5x5 Key Matrix", font=self.font_matrix_header, bg=self.color_frame, fg=self.color_fg).pack(pady=(0, 20))
        
        self.matrix_canvas = tk.Canvas(matrix_frame, width=300, height=300, bg=self.color_entry_bg, highlightthickness=0)
        self.matrix_canvas.pack(pady=20)
        self.draw_matrix_grid() # Draw initial empty grid

    def draw_matrix_grid(self, matrix_data=None):
        self.matrix_canvas.delete("all")
        cell_size = 300 / 5
        for i in range(5):
            for j in range(5):
                x1, y1 = j * cell_size, i * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                self.matrix_canvas.create_rectangle(x1, y1, x2, y2, outline=self.color_frame, width=2)
                if matrix_data:
                    char = matrix_data[i][j]
                    self.matrix_canvas.create_text(x1 + cell_size / 2, y1 + cell_size / 2, text=char, font=self.font_matrix, fill=self.color_accent)

    def perform_encrypt(self):
        key = self.key_entry.get()
        plaintext = self.plaintext_entry.get("1.0", tk.END).strip()
        self.ciphertext_entry.delete("1.0", tk.END)
        try:
            encrypted_text, matrix = crypt(plaintext, key, mode='encrypt')
            self.ciphertext_entry.insert(tk.END, encrypted_text)
            self.draw_matrix_grid(matrix)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def perform_decrypt(self):
        key = self.key_entry.get()
        ciphertext = self.ciphertext_entry.get("1.0", tk.END).strip()
        self.plaintext_entry.delete("1.0", tk.END)
        try:
            decrypted_text, matrix = crypt(ciphertext, key, mode='decrypt')
            self.plaintext_entry.insert(tk.END, decrypted_text)
            self.draw_matrix_grid(matrix)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def clear_fields(self):
        self.key_entry.delete(0, tk.END)
        self.plaintext_entry.delete("1.0", tk.END)
        self.ciphertext_entry.delete("1.0", tk.END)
        self.draw_matrix_grid() # Reset to empty grid

# --- Main execution block ---
if __name__ == "__main__":
    app = PlayfairApp()
    app.mainloop()
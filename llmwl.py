import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import subprocess
import threading
import requests

# === Static Config ===
class Config:
    USE_API = False
    API_URL = "http://localhost:11434/api/generate"
    MODEL = "llama3"
    MASKS = ["{word}123", "123{word}", "{word}@2025", "{word}!", "!{word}", "{word}#1", "{word}_pass", "pass_{word}"]
    KAONASHI_DIR = "Kaonashi"  # Folder to clone Kaonashi resources

# === Kaonashi Downloader ===
def download_kaonashi(log_func):
    try:
        base = Path(Config.KAONASHI_DIR)
        if base.exists():
            log_func("Updating existing Kaonashi repository...")
            subprocess.run(["git", "-C", str(base), "pull"], check=True)
            log_func(" Kaonashi updated ✔")
        else:
            log_func("Cloning Kaonashi repository...")
            subprocess.run(["git", "clone",
                            "https://github.com/kaonashi-passwords/Kaonashi",
                            Config.KAONASHI_DIR], check=True)
            log_func(" Kaonashi cloned ✔")
    except Exception as e:
        log_func(f"  Kaonashi clone/update failed: {e}")

# === LLM Backends ===
def generate_with_api(prompt: str, model: str, api_url: str) -> str:
    resp = requests.post(api_url, json={"model": model, "prompt": prompt, "stream": False})
    resp.raise_for_status()
    return resp.json().get("response", "").strip()

def generate_with_local(prompt: str, model: str) -> str:
    res = subprocess.run(["ollama", "run", model, prompt], capture_output=True, text=True, check=True)
    return res.stdout.strip()

# === GUI App ===
class WordlistApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Wordlist Generator with Kaonashi Support")
        self.geometry("750x650")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Prompt:").pack(anchor='w', padx=10)
        self.prompt_entry = tk.Text(self, height=3)
        self.prompt_entry.pack(fill='x', padx=10)

        tk.Label(self, text="Optional Data (comma-separated):").pack(anchor='w', padx=10, pady=(10, 0))
        self.data_var = tk.StringVar()
        tk.Entry(self, textvariable=self.data_var).pack(fill='x', padx=10)

        tk.Label(self, text="Optional Base Wordlist (.txt):").pack(anchor='w', padx=10, pady=(10, 0))
        self.wordlist_path = tk.StringVar()
        fframe = tk.Frame(self)
        fframe.pack(fill='x', padx=10)
        tk.Entry(fframe, textvariable=self.wordlist_path).pack(side='left', expand=True, fill='x')
        tk.Button(fframe, text="Browse", command=self.browse_wordlist).pack(side='left')

        tk.Label(self, text="Static Mask Options:").pack(anchor='w', padx=10, pady=(10, 0))
        self.masks = tk.Listbox(self, selectmode='multiple', height=5)
        for mask in Config.MASKS:
            self.masks.insert(tk.END, mask)
        self.masks.pack(fill='x', padx=10)

        tk.Label(self, text="Iterations:").pack(anchor='w', padx=10, pady=(10, 0))
        self.iterations_var = tk.IntVar(value=1)
        tk.Spinbox(self, from_=1, to=100, textvariable=self.iterations_var).pack(fill='x', padx=10)

        tk.Label(self, text="Output File:").pack(anchor='w', padx=10, pady=(10, 0))
        self.output_path = tk.StringVar()
        oframe = tk.Frame(self)
        oframe.pack(fill='x', padx=10)
        tk.Entry(oframe, textvariable=self.output_path).pack(side='left', expand=True, fill='x')
        tk.Button(oframe, text="Browse", command=self.browse_output).pack(side='left')

        self.use_api_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self, text="Use API instead of local model", variable=self.use_api_var).pack(anchor='w', padx=10, pady=(10, 0))

        tk.Label(self, text="Model Name:").pack(anchor='w', padx=10, pady=(10, 0))
        self.model_var = tk.StringVar(value=Config.MODEL)
        tk.Entry(self, textvariable=self.model_var).pack(fill='x', padx=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(fill='x', pady=15, padx=10)
        tk.Button(btn_frame, text="Download Kaonashi Resources", command=lambda: threading.Thread(target=download_kaonashi, args=(self.log,), daemon=True).start()).pack(side='left', padx=(0, 10))
        tk.Button(btn_frame, text="Generate Wordlist", command=self.run_generation).pack(side='right')

        tk.Label(self, text="Log:").pack(anchor='w', padx=10)
        self.log_box = tk.Text(self, height=8, state='disabled')
        self.log_box.pack(fill='both', padx=10, pady=(0, 10), expand=True)

    def browse_wordlist(self):
        fn = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if fn: self.wordlist_path.set(fn)

    def browse_output(self):
        fn = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if fn: self.output_path.set(fn)

    def log(self, msg):
        self.log_box.configure(state='normal')
        self.log_box.insert('end', msg + "\n")
        self.log_box.configure(state='disabled')
        self.log_box.see('end')

    def run_generation(self):
        threading.Thread(target=self.generate_wordlist, daemon=True).start()

    def apply_masks(self, words, masks):
        return [mask.replace("{word}", w) for w in words for mask in masks]

    def generate_wordlist(self):
        prompt = self.prompt_entry.get("1.0", "end").strip()
        output = self.output_path.get()
        itr = self.iterations_var.get()
        use_api = self.use_api_var.get()
        model = self.model_var.get()
        data = self.data_var.get()
        base_word = self.wordlist_path.get()
        masks_sel = [self.masks.get(i) for i in self.masks.curselection()]

        if not prompt or not output:
            messagebox.showerror("Input Error", "Prompt and output file are required.")
            return

        try:
            self.log("Starting generation...")
            words = []

            if data:
                extras = [d.strip() for d in data.split(",") if d.strip()]
                prompt += f"\nInclude personal data: {', '.join(extras)}."
                self.log(f"Added structured data: {extras}")

            base_words = []
            if base_word and Path(base_word).exists():
                base_words = [w.strip() for w in Path(base_word).read_text(encoding="utf-8").splitlines() if w.strip()]
                self.log(f"Loaded {len(base_words)} words from base file.")

            for i in range(itr):
                self.log(f"Batch {i+1}/{itr}...")
                res = generate_with_api(prompt, model, Config.API_URL) if use_api else generate_with_local(prompt, model)
                gen = [line.strip() for line in res.splitlines() if line.strip()]
                words.extend(gen)

            words.extend(base_words)

            if masks_sel:
                masked = self.apply_masks(words, masks_sel)
                words.extend(masked)
                self.log(f"Applied {len(masks_sel)} mask patterns to {len(words)} words.")

            final = sorted(set(words))
            Path(output).write_text("\n".join(final), encoding="utf-8")
            self.log(f"Saved {len(final)} unique entries to {output}")
            messagebox.showinfo("Success", f"Wordlist generated with {len(final)} unique entries.")
        except Exception as e:
            self.log(f"Error: {e}")
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    WordlistApp().mainloop()

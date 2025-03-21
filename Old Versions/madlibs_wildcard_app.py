import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re
import json
from pathlib import Path

class MadLibsWildcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mad Libs Wildcard Prompt Builder")
        self.root.geometry("800x600")

        # Load config and wildcard folder
        self.config_file = Path(filedialog.askopenfilename(title="Select wildcard_categories.json"))
        self.story_folder = Path(filedialog.askdirectory(title="Select your story template folder"))
        self.wildcard_folder = Path(filedialog.askdirectory(title="Select your wildcards folder"))

        with open(self.config_file, "r") as f:
            self.wildcard_config = json.load(f)

        self.build_ui()

    def build_ui(self):
        # Story selector
        tk.Label(self.root, text="Select a Story Template:").pack(pady=5)
        self.story_var = tk.StringVar()
        self.story_dropdown = ttk.Combobox(self.root, textvariable=self.story_var, state="readonly")
        self.story_dropdown.pack(fill='x', padx=10)
        self.story_dropdown['values'] = [f.name for f in self.story_folder.glob("*.txt")]
        self.story_dropdown.bind("<<ComboboxSelected>>", self.load_story)

        # Story display and prompt config
        self.story_text = tk.Text(self.root, height=10, wrap='word')
        self.story_text.pack(padx=10, pady=10, fill='x')

        self.dropdown_frame = tk.Frame(self.root)
        self.dropdown_frame.pack(fill='both', expand=True)

        self.generate_button = tk.Button(self.root, text="Generate Wildcardified Prompt", command=self.generate_prompt)
        self.generate_button.pack(pady=10)

        self.output_text = tk.Text(self.root, height=6, wrap='word')
        self.output_text.pack(padx=10, pady=10, fill='both', expand=True)

    def load_story(self, event=None):
        story_file = self.story_folder / self.story_var.get()
        with open(story_file, "r") as f:
            story_content = f.read()
        self.story_text.delete("1.0", tk.END)
        self.story_text.insert(tk.END, story_content)

        self.setup_placeholders()

    def setup_placeholders(self):
        prompt = self.story_text.get("1.0", tk.END).strip()
        placeholders = list(set(re.findall(r"__([a-zA-Z0-9_-]+)__", prompt)))

        for widget in self.dropdown_frame.winfo_children():
            widget.destroy()

        self.dropdown_vars = {}
        for ph in placeholders:
            frame = tk.Frame(self.dropdown_frame)
            frame.pack(fill='x', padx=10, pady=5)

            tk.Label(frame, text=f"__{ph}__:", width=20, anchor='w').pack(side='left')

            matching_wildcards = [k for k, v in self.wildcard_config.items() if ph in v]
            var = tk.StringVar()
            dropdown = ttk.Combobox(frame, textvariable=var, values=sorted(matching_wildcards), state="readonly")
            dropdown.pack(side='left', fill='x', expand=True)

            self.dropdown_vars[ph] = var

    def generate_prompt(self):
        prompt = self.story_text.get("1.0", tk.END).strip()
        for ph, var in self.dropdown_vars.items():
            chosen = var.get()
            if chosen:
                prompt = prompt.replace(f"__{ph}__", f"__{chosen}__")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, prompt)

if __name__ == "__main__":
    root = tk.Tk()
    app = MadLibsWildcardApp(root)
    root.mainloop()

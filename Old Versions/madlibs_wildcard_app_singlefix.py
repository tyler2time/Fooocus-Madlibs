import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re
import json
import random
from pathlib import Path

class MadLibsWildcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mad Libs Wildcard Prompt Builder")
        self.root.geometry("800x700")

        default_config = Path("wildcard_categories_no_nested.json")
        default_story_folder = Path("story_templates")
        default_wildcard_folder = Path("cleaned_tyler_wildcards_no_nested")

        self.config_file = default_config if default_config.exists() else Path(filedialog.askopenfilename(title="Select wildcard_categories.json"))
        self.story_folder = default_story_folder if default_story_folder.exists() else Path(filedialog.askdirectory(title="Select your story template folder"))
        self.wildcard_folder = default_wildcard_folder if default_wildcard_folder.exists() else Path(filedialog.askdirectory(title="Select your wildcards folder"))

        with open(self.config_file, "r") as f:
            self.wildcard_config = json.load(f)

        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="Select a Story Template:").pack(pady=5)
        self.story_var = tk.StringVar()
        self.story_dropdown = ttk.Combobox(self.root, textvariable=self.story_var, state="readonly")
        self.story_dropdown.pack(fill='x', padx=10)
        self.story_dropdown['values'] = [f.name for f in self.story_folder.glob("*.txt")]
        self.story_dropdown.bind("<<ComboboxSelected>>", self.load_story)

        self.story_text = tk.Text(self.root, height=10, wrap='word')
        self.story_text.pack(padx=10, pady=10, fill='x')

        self.randomize_dropdown_var = tk.BooleanVar()
        self.randomize_dropdown_check = tk.Checkbutton(
            self.root, text="Auto-fill dropdowns with random wildcard files",
            variable=self.randomize_dropdown_var
        )
        self.randomize_dropdown_check.pack()

        self.randomize_values_var = tk.BooleanVar()
        self.randomize_values_check = tk.Checkbutton(
            self.root, text="Randomly choose a value from wildcard file at generation",
            variable=self.randomize_values_var
        )
        self.randomize_values_check.pack()

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

        self.setup_placeholders(story_content)

    def setup_placeholders(self, content):
        placeholders = re.findall(r"__([a-zA-Z0-9_-]+)__", content)
        seen = set()
        ordered_placeholders = []
        for ph in placeholders:
            if ph not in seen:
                seen.add(ph)
                ordered_placeholders.append(ph)

        for widget in self.dropdown_frame.winfo_children():
            widget.destroy()

        self.dropdown_vars = {}
        for ph in ordered_placeholders:
            frame = tk.Frame(self.dropdown_frame)
            frame.pack(fill='x', padx=10, pady=5)

            tk.Label(frame, text=f"__{ph}__:", width=20, anchor='w').pack(side='left')

            matching_wildcards = [k for k, v in self.wildcard_config.items() if ph in v]
            var = tk.StringVar()

            dropdown = ttk.Combobox(frame, textvariable=var, values=sorted(matching_wildcards), state="readonly")
            dropdown.pack(side='left', fill='x', expand=True)

            self.dropdown_vars[ph] = var

            if self.randomize_dropdown_var.get() and matching_wildcards:
                var.set(random.choice(matching_wildcards))
            elif len(matching_wildcards) == 1:
                var.set(matching_wildcards[0])

    def get_random_value_from_file(self, wildcard_name):
        file_path = self.wildcard_folder / f"{wildcard_name}.txt"
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
            if lines:
                return random.choice(lines)
        return f"__{wildcard_name}__"

    def generate_prompt(self):
        prompt = self.story_text.get("1.0", tk.END).strip()
        for ph, var in self.dropdown_vars.items():
            wildcard_name = var.get()
            if wildcard_name:
                if self.randomize_values_var.get():
                    value = self.get_random_value_from_file(wildcard_name)
                    prompt = prompt.replace(f"__{ph}__", value)
                else:
                    prompt = prompt.replace(f"__{ph}__", f"__{wildcard_name}__")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, prompt)

if __name__ == "__main__":
    root = tk.Tk()
    app = MadLibsWildcardApp(root)
    root.mainloop()

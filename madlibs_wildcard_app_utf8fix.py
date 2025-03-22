import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re
import os
import json
import random
from pathlib import Path

class MadLibsWildcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mad Libs Wildcard Prompt Builder (UTF-8 Fix)")
        self.root.geometry("800x700")

        self.nsfw_mode = tk.BooleanVar(value=False)  # Add NSFW mode toggle

        self.load_paths()
        self.build_ui()

    def load_paths(self):
        # Update paths based on NSFW mode
        if self.nsfw_mode.get():
            default_config = Path("wildcard_categories_nsfw.json")
            default_story_folder = Path("story_templates_nsfw")
            default_wildcard_folder = Path("NSFWWildcards")
        else:
            default_config = Path("wildcard_categories.json")
            default_story_folder = Path("story_templates_v2")
            default_wildcard_folder = Path("TylersWildcards")

        # Check if files/folders exist and prompt if they don't
        if not default_config.exists():
            config_path = filedialog.askopenfilename(title="Select wildcard_categories.json")
            self.config_file = Path(config_path) if config_path else Path("wildcard_categories.json")
        else:
            self.config_file = default_config
            
        if not default_story_folder.exists():
            story_path = filedialog.askdirectory(title="Select your story template folder")
            self.story_folder = Path(story_path) if story_path else Path("story_templates_v2")
        else:
            self.story_folder = default_story_folder
            
        if not default_wildcard_folder.exists():
            wildcard_path = filedialog.askdirectory(title="Select your wildcards folder")
            self.wildcard_folder = Path(wildcard_path) if wildcard_path else Path("TylersWildcards")
        else:
            self.wildcard_folder = default_wildcard_folder

        with open(self.config_file, "r", encoding="utf-8") as f:
            self.wildcard_config = json.load(f)

    def build_ui(self):
        # NSFW Mode Toggle
        tk.Checkbutton(
            self.root,
            text="NSFW Mode",
            variable=self.nsfw_mode,
            command=self.reload_paths  # Reload paths when toggled
        ).pack(pady=5)

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

        self.copy_button = tk.Button(self.root, text="Copy Prompt to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.pack(pady=(5, 15))

        self.output_text = tk.Text(self.root, height=6, wrap='word')
        self.output_text.pack(padx=10, pady=10, fill='both', expand=True)

    def reload_paths(self):
        self.load_paths()
        self.refresh_story_list()

    def refresh_story_list(self):
        self.story_dropdown['values'] = [f.name for f in self.story_folder.glob("*.txt")]
        self.story_var.set("")
        self.story_text.delete("1.0", tk.END)
        for widget in self.dropdown_frame.winfo_children():
            widget.destroy()
        self.output_text.delete("1.0", tk.END)

    def load_story(self, _=None):
        story_file = self.story_folder / self.story_var.get()
        with open(story_file, "r", encoding="utf-8") as f:
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

            matching_wildcards = []
            for k, v in self.wildcard_config.items():
                # Convert v to a list if it's not already
                categories = v if isinstance(v, list) else [v]
                if ph.lower() in [x.lower() for x in categories]:
                    matching_wildcards.append(k)
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
        print(f"🔍 Loading: {file_path}")
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
            print(f"📄 {len(lines)} entries found in {wildcard_name}.txt")
            if lines:
                chosen = random.choice(lines)
                print(f"🎯 Chosen value: {chosen}")
                return chosen
        else:
            print(f"⚠️ File not found: {file_path}")
        return f"__{wildcard_name}__"

    def generate_prompt(self):
        prompt = self.story_text.get("1.0", tk.END).strip()
        print("🛠 Generating prompt:")
        for ph, var in self.dropdown_vars.items():
            wildcard_name = var.get()
            if wildcard_name:
                print(f"🧩 Placeholder: __{ph}__ → Wildcard: {wildcard_name}")
                if self.randomize_values_var.get():
                    value = self.get_random_value_from_file(wildcard_name)
                    prompt = prompt.replace(f"__{ph}__", value)
                else:
                    prompt = prompt.replace(f"__{ph}__", f"__{wildcard_name}__")
        print("✅ Final Prompt:", prompt)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, prompt)
        self.copy_to_clipboard()

    def copy_to_clipboard(self):
        prompt = self.output_text.get("1.0", tk.END).strip()
        self.root.clipboard_clear()
        self.root.clipboard_append(prompt)
        self.root.update()
        messagebox.showinfo("Copied!", "Prompt copied to clipboard.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MadLibsWildcardApp(root)
    root.mainloop()

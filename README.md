# 🎭 Mad Libs Wildcard Prompt App

A GUI tool for building structured, wildcard-enhanced prompts for text-to-image generation — perfect for use with **Fooocus** and similar AI tools.

---

## ✅ Features

- 🧠 **Category-based dropdowns**  
  Each blank in the story (`__noun__`, `__location__`, etc.) maps to matching wildcard categories.

- 🔁 **Dropdown order preserved**  
  Dropdowns appear in the same order as placeholders in your story.

- 🎲 **Two randomization modes**  
  - Auto-fill dropdowns with random wildcard files  
  - Randomly select a value from the file when generating the prompt

- 📜 **Story template loader**  
  Load and choose from `.txt` story templates.

- 🧹 **Wildcard cleanup**  
  NSFW and overlapping wildcards removed. Cleaned set with updated category mapping.

- 🧠 **Smart defaults**  
  Automatically detects folders/configs and only prompts if missing.

---

## 📁 Project Structure

```
/madlibs/
├── madlibs_wildcard_app_final.py
├── wildcard_categories_cleaned.json
├── cleaned_tyler_wildcards/         ← Cleaned, non-NSFW wildcards
├── story_templates/                 ← Flexible prompt templates
├── silly_story_templates/          ← Kid-friendly stories
└── madlibs-style.json              ← Wide-angle style for Fooocus
```

---

## 🎨 Default Style: `madlibs-style.json`

A flexible wide-angle Fooocus style that works for multi-subject, storytelling scenes.

```json
{
  "name": "madlibs-style",
  "prompt": "ultra wide angle, full scene composition, cinematic lighting, detailed background, realistic shadows, coherent subjects, storytelling photography",
  "negative_prompt": "cropped, zoomed in, close-up, low detail, blurry, out of frame, missing limbs, text, watermark"
}
```

---

## 🤪 Silly Story Templates for Kids

| Filename | Summary |
|----------|---------|
| `the_pizza_planet.txt` | Astronaut finds a snack-based planet full of edible surprises |
| `the_great_slime_race.txt` | A creature race powered by bananas, slime, and giggles |
| `the_dancing_dinosaur.txt` | A dino finds magic shoes and starts a prehistoric dance party |

---

## 🧭 Future Ideas

- Break long stories into multiple prompts (for multi-image generation)
- Add per-genre styles (horror, fantasy, scifi, romance)
- Send final prompt with style directly to Fooocus
- Export to JSON or Markdown storybooks
- Web version for sharing or mobile use

---

Built for storytelling, randomness, and fun — one silly image at a time.

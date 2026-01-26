# 🐍 Python Static Site Generator

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green)

A lightweight, custom-built static site generator written in **Python**. It converts Markdown files into a fully functional HTML website using Liquid templates. This project was designed as a high-performance, developer-friendly alternative to Jekyll for GitHub Pages.

**Live Demo:** [stornov.github.io](https://stornov.github.io/)

---

## 🚀 Features

* **Custom Python Engine**: A minimal core with no Ruby or Jekyll dependencies.
* **Liquid Templating**: Full support for logic-based HTML templates via `python-liquid`.
* **Smart Content Management**:
  * **Auto-Slugs**: Automatically generates clean, SEO-friendly URLs from post titles.
  * **Categorization**: Organizes posts into custom sections (e.g., Blog, Games, Programming) via `_config.yml`.
  * **Template Switching**: Separate templates for blog posts (with dates) and static pages (like 404 or About).
* **Developer-Centric Design**:
  * **Terminal-Style Code**: High-contrast dark theme for all code blocks by default.
  * **Syntax Highlighting**: Integrated `highlight.js` for beautiful code snippets.
* **Automated CI/CD**: Seamless deployment to GitHub Pages using GitHub Actions.

## 🛠️ Tech Stack

* **python-liquid**: Templating engine for flexible HTML layouts.
* **python-frontmatter**: For parsing YAML metadata in Markdown files.
* **markdown**: For converting content with extensions like `fenced_code` and `attr_list`.
* **pyyaml**: For project configuration management.

## 📂 Project Structure

```text
.
├── main.py               # The core build script (The Engine)
├── _config.yml           # Global site & navigation settings
├── requirements.txt      # Python dependencies
├── _posts/               # Markdown content files
├── _templates/           # Liquid HTML templates
│   ├── header.html       # Shared site header
│   ├── footer.html       # Shared site footer
│   ├── index.html        # Homepage with section logic
│   ├── post.html         # Template for blog articles (with date)
│   └── page.html         # Template for static pages (no date)
├── _themes/              # CSS Stylesheets
└── .github/workflows/    # GitHub Actions automation script
```

## ⚙️ Configuration

Manage your site structure via `_config.yml` without touching any Python code:

```yaml
title: Arhip Storozhev
theme: mystyle.css

# Top Navigation Menu
menu:
  - title: Home
    url: /
  - title: GitHub
    url: https://github.com/stornov

# Homepage Sections
# id: must match the 'category' in your .md files
sections:
  - id: blog
    title: "Latest Blog Posts"
  - id: games
    title: "Game Reviews"
  - id: programming
    title: "Dev Log & Code"
```

## ✍️ Writing Content

To create a new post or page, add a `.md` file to the `_posts/` directory.

### Metadata (Frontmatter)

Each file starts with a YAML block. Here is the configuration:

```markdown
---
title: "How to use Pathlib"
date: 2026-01-26
category: programming  # Places post in the "Dev Log" section
slug: pathlib-guide    # Custom URL (optional)
published: true         # Set to false to hide from lists
template: post          # Use 'page' to hide date/location
location: "Ozersk"
---
```

### 📝 Supported Markdown Features

The generator supports advanced Markdown syntax out of the box:

* **Headings**: `# H1` to `###### H6`.
* **Lists**: Ordered (`1.`) and unordered (`*` or `-`).
* **Emphasis**: `**Bold**`, `*Italic*`, and `~~Strikethrough~~`.
* **Links & Images**: `[Text](URL)` and `![Alt](/path/to/img)`.
* **Tables**: Clean data structures with header alignment.
* **Blockquotes**: `> This is a quote` (styled with a vertical border).
* **Code Blocks**: Supports fenced blocks with syntax highlighting.

## 💻 Local Development

1. **Clone the repository:**

    ```bash
    git clone https://github.com/stornov/stornov.github.io.git
    cd stornov.github.io
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Build the site:**

    ```bash
    python main.py
    ```

4. **Preview locally:**
    Launch a local server to view the `_site` directory:

    ```bash
    python -m http.server --directory _site
    ```

    Then visit [http://localhost:8000](http://localhost:8000).

## 🤖 CI/CD Automation

This project is fully automated. When you push changes to the `main` branch:

1. **GitHub Actions** triggers the build process.
2. The script generates the static HTML in a clean environment.
3. The results are automatically deployed to the `gh-pages` branch.
4. Your site is updated live at your GitHub Pages URL.

---
*Created with ❤️ by [stornov](https://github.com/stornov) using Python.*

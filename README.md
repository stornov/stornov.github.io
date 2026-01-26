# Arhip Storozhev | Personal Website

Welcome to the source code of my personal website and blog: **[stornov.github.io](https://stornov.github.io/)**

Here I share my thoughts on programming, and life updates.

## 🔧 Powered by Luna SSG

This website is not built with Jekyll or Hugo. It runs on my own custom engine written in **Python**.

I developed **Luna SSG** to have full control over the build process, SEO, and templating. It features:

* Pure Python architecture.
* Liquid templates.
* Automated GitHub Actions deployment.
* Custom "Terminal-style" highlighting for code blocks.

👉 **[Check out the Generator Source Code](https://github.com/stornov/luna-ssg)**

## 📂 Content Overview

* **_posts/**: My articles and reviews written in Markdown.
* **_templates/**: Custom HTML layouts for this specific site design.
* **_themes/**: CSS styling (mystyle.css).

## 🚀 Running Locally

If you want to see how this specific site looks locally:

1. Clone the repo.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the engine: `python main.py`.
4. Serve: `python -m http.server --directory _site`.

---
© Arhip Storozhev.
The site content is for personal use. The site generator engine is Open Source (MIT).

import shutil
import datetime
import re
from pathlib import Path
from PIL import Image
import yaml
import frontmatter
from markdown_it import MarkdownIt
from liquid import Environment, FileSystemLoader
from liquid.extra.tags import ExtendsTag, BlockTag

BASE_DIR = Path.cwd()
DIRS = {
    "templates": BASE_DIR / "_templates",
    "posts": BASE_DIR / "_posts",
    "site": BASE_DIR / "_site",
    "themes": BASE_DIR / "_themes",
    "config": BASE_DIR / "_config.yml",
    "media": BASE_DIR / "_media"
}

def load_config():
    if not DIRS["config"].exists():
        print(f"Error: Config not found at {DIRS['config']}")
        exit(1)
        
    with open(DIRS["config"], 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def setup_environment():
    env = Environment(loader=FileSystemLoader(search_path=str(DIRS["templates"])))
    # Регистрируем теги наследования, которых нет в стандартном Liquid
    env.add_tag(ExtendsTag)
    env.add_tag(BlockTag)
    return env

def slugify(text):
    text = str(text).lower().strip()
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'[^\w-]', '', text)
    return text.strip('-')

def get_global_context(config):
    return {
        "lang": config.get("lang", "en"),
        "site_title": config.get("title"),
        "author": config.get("author"),
        "theme_file": config.get("theme"),
        "menu_items": config.get("menu", []),
        "footer_columns": config.get("footer", []),
        "current_year": datetime.datetime.now().year
    }

def process_posts(env, config, global_context):
    posts_metadata = []
    
    if DIRS["site"].exists():
        shutil.rmtree(DIRS["site"])
    DIRS["site"].mkdir()
    (DIRS["site"] / ".nojekyll").touch()

    valid_sections = [s["id"] for s in config.get("sections", [])]
    DEFAULT_SECTION = "blog"

    md = MarkdownIt()
    md.enable('table')
    md.enable('strikethrough')

    def render_image(self, tokens, idx, options, env):
        token = tokens[idx]
        
        src = token.attrs.get('src', '')
        alt = token.content
        
        if src.startswith('/media/') and any(src.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
            src = str(Path(src).with_suffix('.webp'))
            src = src.replace('\\', '/')

        return f'<img src="{src}" alt="{alt}" loading="lazy">'

    md.add_render_rule("image", render_image)

    for md_file in DIRS["posts"].glob("*.md"):
        post = frontmatter.load(md_file)  # type: ignore
        
        post_date = post.get("date")
        if not post_date:
            post_date = datetime.date.today()
        
        html_content = md.render(post.content)
        
        custom_slug = post.get("slug")
        post_title = post.get("title")

        if custom_slug:
            filename_base = custom_slug
        elif post_title:
            filename_base = slugify(post_title)
            if not filename_base:
                filename_base = md_file.stem
        else:
            filename_base = md_file.stem

        output_filename = f"{filename_base}.html"
        
        user_section = post.get("section", DEFAULT_SECTION)
        if user_section in valid_sections:
            final_section = user_section
        else:
            final_section = DEFAULT_SECTION

        post_context = global_context.copy()
        post_context.update({
            "page_title": post_title,
            "title": post_title,
            "date": post_date,
            "location": post.get("location"),
            "content": html_content,
            "is_post": True,
            "external_link": post.get("link") 
        })

        template_name = f"{post.get('template', 'post')}.html"
        template = env.get_template(template_name)
        rendered_html = template.render(**post_context)
        
        (DIRS["site"] / output_filename).write_text(rendered_html, encoding="utf-8")
        print(f"Generated: {output_filename}")

        if post.get("published", True):
            posts_metadata.append({
                "title": post_title,
                "date": post_date,
                "url": output_filename,
                "section": final_section,
                "external_link": post.get("link")
            })
            
    posts_metadata.sort(key=lambda x: x['date'], reverse=True)
    return posts_metadata

def build_index(env, config, global_context, posts):
    template = env.get_template("index.html")
    
    sections_data = []
    config_sections = config.get("sections", [])
    
    for section_cfg in config_sections:
        sec_id = section_cfg["id"]
        filtered_posts = [p for p in posts if p["section"] == sec_id]
        
        if filtered_posts:
            sections_data.append({
                "title": section_cfg["title"],
                "posts": filtered_posts
            })
    
    index_context = global_context.copy()
    index_context.update({
        "page_title": config.get("title"),
        "sections": sections_data,
        "bottom_sections": config.get("bottom_sections", []),
        "is_home": True 
    })
    
    rendered = template.render(**index_context)
    (DIRS["site"] / "index.html").write_text(rendered, encoding="utf-8")
    print("Index generated.")

def copy_assets(config):
    theme_name = config.get("theme")
    css_src = DIRS["themes"] / theme_name
    css_dest = DIRS["site"] / theme_name
    
    if css_src.exists():
        shutil.copy(css_src, css_dest)
        print(f"Theme copied: {theme_name}")
    else:
        print(f"CRITICAL WARNING: Theme file not found at {css_src}")

def copy_media():
    src_dir = DIRS["media"]
    dest_dir = DIRS["site"] / "media"
    
    if not src_dir.exists():
        print("No _media folder found, skipping.")
        return

    dest_dir.mkdir(parents=True, exist_ok=True)
    
    count_converted = 0
    count_copied = 0

    for item in src_dir.iterdir():
        if item.is_file():
            if item.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                try:
                    with Image.open(item) as img:
                        new_filename = item.with_suffix('.webp').name
                        dest_path = dest_dir / new_filename
                        
                        img.save(dest_path, format="WEBP", quality=85)
                        count_converted += 1
                except Exception as e:
                    print(f"Error converting {item.name}: {e}")
            else:
                shutil.copy2(item, dest_dir / item.name)
                count_copied += 1
    
    print(f"Media processed: {count_converted} converted to WebP, {count_copied} copied.")

def main():
    print(f"Starting build in: {BASE_DIR}")
    config = load_config()
    env = setup_environment()
    global_ctx = get_global_context(config)
    
    posts = process_posts(env, config, global_ctx)
    build_index(env, config, global_ctx, posts)
    copy_assets(config)
    copy_media()
    print("Build complete! Ready for deployment.")

if __name__ == "__main__":
    main()

import shutil
import datetime
import re
from pathlib import Path
import yaml
import frontmatter
import markdown
from liquid import Environment, FileSystemLoader

BASE_DIR = Path.cwd()
DIRS = {
    "templates": BASE_DIR / "_templates",
    "posts": BASE_DIR / "_posts",
    "site": BASE_DIR / "_site",
    "themes": BASE_DIR / "_themes",
    "config": BASE_DIR / "_config.yml"
}

def load_config():
    if not DIRS["config"].exists():
        print(f"Error: Config not found at {DIRS['config']}")
        exit(1)
        
    with open(DIRS["config"], 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def setup_environment():
    return Environment(loader=FileSystemLoader(search_path=str(DIRS["templates"])))

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
    print("Created .nojekyll file (Jekyll disabled)")

    valid_sections = [s["id"] for s in config.get("sections", [])]
    DEFAULT_CATEGORY = "blog"

    for md_file in DIRS["posts"].glob("*.md"):
        post = frontmatter.load(md_file)
        
        post_date = post.get("date")
        if not post_date:
            post_date = datetime.date.today()
        
        html_content = markdown.markdown(post.content, extensions=['fenced_code'])
        
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
        
        user_category = post.get("category", DEFAULT_CATEGORY)
        if user_category in valid_sections:
            final_category = user_category
        else:
            final_category = DEFAULT_CATEGORY

        post_context = global_context.copy()
        post_context.update({
            "page_title": post_title,
            "title": post_title,
            "date": post_date,
            "location": post.get("location"),
            "content": html_content,
            "is_post": True
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
                "category": final_category
            })
            
    posts_metadata.sort(key=lambda x: x['date'], reverse=True)
    return posts_metadata

def build_index(env, config, global_context, posts):
    template = env.get_template("index.html")
    
    sections_data = []
    config_sections = config.get("sections", [])
    
    for section_cfg in config_sections:
        sec_id = section_cfg["id"]
        filtered_posts = [p for p in posts if p["category"] == sec_id]
        
        if filtered_posts:
            sections_data.append({
                "title": section_cfg["title"],
                "posts": filtered_posts
            })
    
    index_context = global_context.copy()
    index_context.update({
        "page_title": config.get("title"),
        "sections": sections_data,
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

def main():
    print(f"Starting build in: {BASE_DIR}")
    config = load_config()
    env = setup_environment()
    global_ctx = get_global_context(config)
    
    posts = process_posts(env, config, global_ctx)
    build_index(env, config, global_ctx, posts)
    copy_assets(config)
    print("Build complete! Ready for deployment.")

if __name__ == "__main__":
    main()

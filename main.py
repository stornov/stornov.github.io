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
    "assets": BASE_DIR / "_assets"
}

ASSET_REGISTRY = []

def load_config():
    if not DIRS["config"].exists():
        print(f"Error: Config not found at {DIRS['config']}")
        exit(1)
    with open(DIRS["config"], 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def setup_environment():
    env = Environment(loader=FileSystemLoader(search_path=str(DIRS["templates"])))
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
        "baseurl": config.get("baseurl", ""),
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

    curr_sec = ""
    curr_slug = ""

    md = MarkdownIt()
    md.enable('table')
    md.enable('strikethrough')

    def render_image(self, tokens, idx, options, env):
        token = tokens[idx]
        src = token.attrs.get('src', '')
        alt = token.content
        
        if src.startswith('/assets/') and 'favicon' not in src:
            orig_path = Path(src)
            ext = orig_path.suffix.lower()
            
            if ext in ['.jpg', '.jpeg', '.png']:
                final_filename = f"{orig_path.stem}.webp"
            else:
                final_filename = orig_path.name

            new_rel_path = f"assets/{curr_sec}/{curr_slug}/{final_filename}"
            ASSET_REGISTRY.append({"src_name": orig_path.name, "dest_rel_path": new_rel_path})
            src = f"{global_context['baseurl']}/{new_rel_path}"

        return f'<img src="{src}" alt="{alt}" loading="lazy">'

    def render_link_open(self, tokens, idx, options, env):
        token = tokens[idx]
        href = token.attrs.get('href', '')
        
        if href.startswith('/assets/') and 'favicon' not in href:
            orig_path = Path(href)
            new_rel_path = f"assets/{curr_sec}/{curr_slug}/{orig_path.name}"
            ASSET_REGISTRY.append({"src_name": orig_path.name, "dest_rel_path": new_rel_path})
            token.attrs['href'] = f"{global_context['baseurl']}/{new_rel_path}"
            
        return self.renderToken(tokens, idx, options, env)

    md.add_render_rule("image", render_image)
    md.add_render_rule("link_open", render_link_open)

    for md_file in DIRS["posts"].glob("*.md"):
        post = frontmatter.load(md_file)  # type: ignore
        post_date = post.get("date") or datetime.date.today()
        
        user_section = post.get("section", DEFAULT_SECTION)
        curr_sec = user_section if user_section in valid_sections else DEFAULT_SECTION
        
        post_title = post.get("title", md_file.stem)
        curr_slug = post.get("slug") or slugify(post_title) or md_file.stem

        html_content = md.render(post.content)

        semantic_category = post.get("category", "Random") if curr_sec == "blog" else None
        category_slug = slugify(semantic_category) if semantic_category else None

        post_context = global_context.copy()
        post_context.update({
            "page_title": post_title, "title": post_title, "date": post_date,
            "location": post.get("location"), "content": html_content,
            "is_post": True, "section": curr_sec, "category": semantic_category,
            "category_slug": category_slug, "external_link": post.get("link")
        })

        output_filename = f"{curr_slug}.html"

        if post.get('template') == "page":
            dest_dir = DIRS["site"]
            relative_url = output_filename
        else:
            dest_dir = DIRS["site"] / curr_sec  # type: ignore
            dest_dir.mkdir(parents=True, exist_ok=True)
            relative_url = f"{curr_sec}/{output_filename}"
        
        dest_path = dest_dir / output_filename

        template = env.get_template(f"{post.get('template', 'post')}.html")
        dest_path.write_text(template.render(**post_context), encoding="utf-8")

        print(f"Generated: {relative_url}")

        if post.get("published", True):
            posts_metadata.append({
                "title": post_title, "date": post_date, "url": relative_url,
                "section": curr_sec, "category": semantic_category,
                "external_link": post.get("link")
            })
            
    posts_metadata.sort(key=lambda x: x['date'], reverse=True)
    return posts_metadata

def build_index(env, config, global_context, posts):
    template = env.get_template("index.html")
    sections_data = []
    for section_cfg in config.get("sections", []):
        sec_id = section_cfg["id"]
        filtered = [p for p in posts if p["section"] == sec_id]
        if sec_id == "blog": filtered = filtered[:10]
        if filtered: sections_data.append({"title": section_cfg["title"], "posts": filtered})
    
    ctx = global_context.copy()
    ctx.update({"page_title": config.get("title"), "sections": sections_data, "bottom_sections": config.get("bottom_sections", []), "is_home": True})
    (DIRS["site"] / "index.html").write_text(template.render(**ctx), encoding="utf-8")

def build_archive(env, config, global_context, posts):
    blog_posts = [p for p in posts if p.get("section") == "blog"]
    if not blog_posts: return
    grouped = {}
    for p in blog_posts:
        cat = p.get("category") or "Random"
        if cat not in grouped: grouped[cat] = []
        grouped[cat].append(p)
    
    cats = sorted([{"title": c, "slug": slugify(c), "posts": grouped[c]} for c in grouped], key=lambda x: x["title"])
    ctx = global_context.copy()
    ctx.update({"title": "Archive", "page_title": f"Archive | {config.get('author')}", "categories": cats, "posts_count": len(blog_posts)})
    (DIRS["site"] / "archive.html").write_text(env.get_template("archive.html").render(**ctx), encoding="utf-8")

def build_blog_list(env, config, global_context, posts):
    blog_posts = [p for p in posts if p.get("section") == "blog"]
    if not blog_posts: return
    years = {}
    for p in blog_posts:
        y, m = p["date"].year, p["date"].strftime("%b")
        if y not in years: years[y] = {}
        if m not in years[y]: years[y][m] = []
        years[y][m].append(p)
    
    ys = [{"year": y, "months": [{"name": m, "posts": years[y][m]} for m in years[y]]} for y in sorted(years.keys(), reverse=True)]
    ctx = global_context.copy()
    ctx.update({"title": "All Posts", "page_title": f"Blog | {config.get('author')}", "years": ys, "posts_count": len(blog_posts)})
    (DIRS["site"] / "blog.html").write_text(env.get_template("blog.html").render(**ctx), encoding="utf-8")

def copy_assets_and_themes(config):
    theme = config.get("theme")
    if (DIRS["themes"] / theme).exists():
        shutil.copy(DIRS["themes"] / theme, DIRS["site"] / theme)

    dest_assets = DIRS["site"] / "assets"
    dest_assets.mkdir(parents=True, exist_ok=True)
    if (DIRS["assets"] / "favicon.ico").exists():
        shutil.copy(DIRS["assets"] / "favicon.ico", dest_assets / "favicon.ico")

    for asset in ASSET_REGISTRY:
        src_file = DIRS["assets"] / asset["src_name"]
        if not src_file.exists(): continue
        
        dest_file = DIRS["site"] / asset["dest_rel_path"]
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        
        if src_file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            try:
                with Image.open(src_file) as img:
                    img.save(dest_file, format="WEBP", quality=85)
            except:
                shutil.copy2(src_file, dest_file)
        else:
            shutil.copy2(src_file, dest_file)
    print(f"Assets processed: {len(ASSET_REGISTRY)} files distributed.")

def main():
    config = load_config()
    print(f"Build started - baseurl: '{config.get('baseurl', '')}'")
    env = setup_environment()
    ctx = get_global_context(config)
    posts = process_posts(env, config, ctx)
    build_index(env, config, ctx, posts)
    build_archive(env, config, ctx, posts)
    build_blog_list(env, config, ctx, posts)
    copy_assets_and_themes(config)
    print("Build complete!")

if __name__ == "__main__":
    main()
import requests
import time
import re
from pathlib import Path
from datetime import datetime, timezone

# ── Налаштування ─────────────────────────────────────────
POSTS_FILE = "unique_urls.txt"
OUTPUT_DIR = "reddit_exports"
POSTS_PER_FILE = 120          # постів в кожному MD файлі
DELAY = 5                     # секунди між запитами
MAX_COMMENT_DEPTH = 6
MIN_COMMENT_SCORE = -10
COMMENT_LIMIT = 500           # скільки коментів просити (more не довантажуємо)
MAX_RETRIES = 3               # спроби при 429

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}

COOKIES = {
    "reddit_session": "PASTE_YOUR_reddit_session_COOKIE_HERE",
}
# ─────────────────────────────────────────────────────────


def extract_post_id(url: str) -> str:
    """Витягує ID поста з URL (напр. 'x84hpj' з .../comments/x84hpj/...)."""
    m = re.search(r'/comments/([a-z0-9]+)', url)
    return m.group(1) if m else ""


def load_done_ids() -> set:
    """Читає ID вже збережених постів з усіх MD-файлів у папці."""
    done = set()
    for p in Path(OUTPUT_DIR).glob("posts_part_*.md"):
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue
        # ID зберігається у рядку-маркері <!-- id:XXXX -->
        for m in re.finditer(r'<!-- id:([a-z0-9]+) -->', text):
            done.add(m.group(1))
    return done


def fetch_post_with_comments(url: str, retries: int = 0):
    clean_url = re.sub(r'\?.*$', '', url.rstrip("/"))
    json_url = clean_url + f".json?limit={COMMENT_LIMIT}"
    print(f"  → {json_url}")

    try:
        response = requests.get(json_url, headers=HEADERS, cookies=COOKIES, timeout=15)
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Помилка з'єднання: {e}")
        return None

    if response.status_code == 200:
        try:
            data = response.json()
            if isinstance(data, list) and len(data) >= 2:
                return data
            print("  ✗ Неочікувана структура відповіді")
            return None
        except Exception as e:
            print(f"  ✗ Помилка JSON: {e}")
            return None
    elif response.status_code == 429:
        if retries >= MAX_RETRIES:
            print("  ✗ Rate limit не знявся після кількох спроб")
            return None
        print(f"  ⚠ Rate limit! Чекаємо 60 сек... (спроба {retries + 1})")
        time.sleep(60)
        return fetch_post_with_comments(url, retries + 1)
    elif response.status_code == 404:
        print("  ✗ Пост не знайдено або видалено")
        return None
    elif response.status_code == 403:
        print("  ✗ 403 — доступ заборонено (перевір cookie!)")
        return None
    else:
        print(f"  ✗ HTTP {response.status_code}")
        return None


def parse_comments(comments_data: list, depth: int = 0) -> str:
    if depth > MAX_COMMENT_DEPTH:
        return ""
    result = ""
    indent = "  " * depth
    for item in comments_data:
        if not isinstance(item, dict) or item.get("kind") != "t1":
            continue
        d = item.get("data", {})
        body = d.get("body", "").strip()
        score = d.get("score", 0)
        author = d.get("author", "невідомо")
        if body in ("[deleted]", "[removed]", ""):
            continue
        if isinstance(score, int) and score < MIN_COMMENT_SCORE:
            continue
        result += f"{indent}**u/{author}** (👍 {score})\n{indent}{body}\n\n"
        replies = d.get("replies", "")
        if isinstance(replies, dict):
            children = replies.get("data", {}).get("children", [])
            result += parse_comments(children, depth + 1)
    return result


def post_to_markdown(raw_data: list, post_index: int) -> str:
    try:
        post_data = raw_data[0]["data"]["children"][0]["data"]
    except (KeyError, IndexError) as e:
        print(f"  ✗ Помилка читання поста: {e}")
        return ""

    post_id      = post_data.get("id", "")
    title        = post_data.get("title", "Без назви")
    author       = post_data.get("author", "невідомо")
    subreddit    = post_data.get("subreddit_name_prefixed", "r/?")
    body         = post_data.get("selftext", "").strip()
    score        = post_data.get("score", 0)
    num_comments = post_data.get("num_comments", 0)
    url          = post_data.get("url", "")
    permalink    = "https://reddit.com" + post_data.get("permalink", "")
    created      = datetime.fromtimestamp(post_data.get("created_utc", 0), timezone.utc)
    date_str     = created.strftime("%Y-%m-%d %H:%M UTC")

    if body in ("[deleted]", "[removed]"):
        body = "_Текст поста видалено_"
    elif not body:
        body = f"_Пост-посилання: {url}_"

    try:
        comments_raw = raw_data[1]["data"]["children"]
        comments_md = parse_comments(comments_raw)
    except (KeyError, IndexError):
        comments_md = ""

    if not comments_md.strip():
        comments_md = "_Коментарів немає або всі видалено_"

    return f"""
{'='*60}
<!-- id:{post_id} -->
# ПОСТ {post_index}: {title}

- **Сабредіт:** {subreddit}
- **Автор:** u/{author}
- **Дата:** {date_str}
- **Upvotes:** {score:,}
- **Коментарів:** {num_comments:,}
- **Посилання:** {permalink}

## Текст поста

{body}

## Коментарі

{comments_md}
"""


def get_output_filename(part_number: int, total_parts: int) -> str:
    return str(Path(OUTPUT_DIR) / f"posts_part_{part_number:03d}_of_{total_parts:03d}.md")


def write_file_header(filepath: str, part_number: int, total_parts: int,
                      post_from: int, post_to: int, total_posts: int):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"""# REDDIT ПОСТИ — ЧАСТИНА {part_number} з {total_parts}

**Дата експорту:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Пости у цьому файлі:** {post_from}–{post_to} з {total_posts}
**Джерело:** Reddit JSON API

---

""")


def main():
    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    if not Path(POSTS_FILE).exists():
        print(f"❌ Файл '{POSTS_FILE}' не знайдено!")
        return

    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    total = len(urls)
    total_parts = (total + POSTS_PER_FILE - 1) // POSTS_PER_FILE

    # ── SKIP_EXISTING: які пости вже зібрані ──
    done_ids = load_done_ids()
    if done_ids:
        print(f"↻ Знайдено вже зібраних постів: {len(done_ids)} — пропускаю їх\n")

    print(f"📋 Постів у списку: {total}")
    print(f"📁 Файлів (максимум): {total_parts} (по {POSTS_PER_FILE} постів)")
    print(f"📂 Папка: {OUTPUT_DIR}/")
    print(f"⏱ Затримка: {DELAY} сек | Глибина коментів: {MAX_COMMENT_DEPTH}\n")

    success = 0
    skipped = 0
    failed = []
    current_part = 0
    current_file = None
    file_announced = False
    post_from = post_to = 0

    for i, url in enumerate(urls, start=1):

        # Номер частини рахуємо за позицією ДО перевірки на пропуск,
        # щоб при повторному запуску current_file не лишався порожнім.
        part_no = (i - 1) // POSTS_PER_FILE + 1
        if part_no != current_part:
            current_part = part_no
            post_from = (part_no - 1) * POSTS_PER_FILE + 1
            post_to = min(part_no * POSTS_PER_FILE, total)
            current_file = get_output_filename(current_part, total_parts)
            file_announced = False

        pid = extract_post_id(url)
        if pid and pid in done_ids:
            skipped += 1
            print(f"[{i}/{total}] ⏭ вже є ({pid})")
            continue

        if not Path(current_file).exists():
            write_file_header(current_file, current_part, total_parts,
                              post_from, post_to, total)
        if not file_announced:
            print(f"\n📄 Файл: {current_file} (пости {post_from}–{post_to})\n")
            file_announced = True

        print(f"[{i}/{total}] {url}")

        raw_data = fetch_post_with_comments(url)

        if raw_data:
            md_block = post_to_markdown(raw_data, i)
            if md_block:
                with open(current_file, "a", encoding="utf-8") as f:
                    f.write(md_block)
                if pid:
                    done_ids.add(pid)
                success += 1
                print(f"  ✅ Збережено → {current_file}")
            else:
                failed.append(url)
        else:
            failed.append(url)

        if i < total:
            time.sleep(DELAY)

    # ── Підсумок ──
    print(f"\n{'='*40}")
    print(f"✅ Успішно цього разу: {success}")
    print(f"⏭ Пропущено (вже було): {skipped}")
    print(f"❌ Не вдалось: {len(failed)}")
    print(f"📁 Файли: ./{OUTPUT_DIR}/")

    print(f"\nРозміри файлів:")
    total_size = 0
    for p in sorted(Path(OUTPUT_DIR).glob("posts_part_*.md")):
        size_kb = p.stat().st_size / 1024
        total_size += size_kb
        print(f"  {p.name}: {size_kb:.0f} KB")
    print(f"  Загалом: {total_size/1024:.1f} MB")

    if failed:
        failed_file = Path(OUTPUT_DIR) / "failed_urls.txt"
        with open(failed_file, "w", encoding="utf-8") as f:
            f.write("\n".join(failed))
        print(f"\n❌ Список невдалих збережено у: {failed_file}")
        print("   (можна запустити скрипт ще раз — вже зібрані пропустяться)")


if __name__ == "__main__":
    main()

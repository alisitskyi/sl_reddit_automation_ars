#!/usr/bin/env python3
"""
Витягує всі reddit-URL з усіх .xlsx файлів у папці.

Використання:
    python extract_urls.py                  # бере файли з поточної папки
    python extract_urls.py /шлях/до/папки    # бере файли зі вказаної папки

Результат:
    all_urls.csv   — колонки: file, url  (усі URL, з якого файлу)
    unique_urls.txt — унікальні URL, по одному в рядку
"""

import sys
import glob
import os
import re
import csv

import pandas as pd

URL_RE = re.compile(r'https?://[^\s"\'<>|]+')

def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else "."
    files = sorted(glob.glob(os.path.join(folder, "*.xlsx")))
    if not files:
        print(f"Не знайдено жодного .xlsx у: {os.path.abspath(folder)}")
        return

    rows = []            # (file, url)
    seen = set()
    unique = []

    for path in files:
        fname = os.path.basename(path)
        try:
            # читаємо всі листи, все як текст, без заголовків
            sheets = pd.read_excel(path, sheet_name=None, header=None, dtype=str)
        except Exception as e:
            print(f"[пропущено] {fname}: {e}")
            continue

        found_in_file = 0
        for df in sheets.values():
            for val in df.values.ravel():
                if not isinstance(val, str):
                    continue
                for url in URL_RE.findall(val):
                    # відкидаємо картинки-іконки та інший медіа-шум
                    if "redditmedia.com" in url or "styles.reddit" in url:
                        continue
                    # лишаємо тільки посилання на конкретні пости
                    if "/comments/" not in url:
                        continue
                    url = url.rstrip(".,)")
                    rows.append((fname, url))
                    found_in_file += 1
                    if url not in seen:
                        seen.add(url)
                        unique.append(url)
        print(f"{fname}: {found_in_file} посилань")

    with open("all_urls.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["file", "url"])
        w.writerows(rows)

    with open("unique_urls.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(unique))

    print(f"\nГотово. Усього посилань: {len(rows)}, унікальних: {len(unique)}")
    print("Файли: all_urls.csv, unique_urls.txt")

if __name__ == "__main__":
    main()

# Reddit Parser AL: Technical Documentation and Setup Guide

Oct 7, 2026 · @Anton

## 1. Purpose and result

Reddit Parser AL collects Reddit posts and all their comments by keyword and saves them as text files you can hand over for analysis (for example, to Claude). It runs locally on your computer as a small website at `localhost:5000`.

**Why it exists.** Voice of Customer research means reading thousands of real discussions. Doing that by hand is not realistic, and the official Reddit API is closed to small projects. The tool therefore reads public data the same way a signed-in user sees it in a browser.

**Input:**

- a list of keywords (for example, `"ABM"`, `"LinkedIn ads"`);
- a list of subreddits (for example, `marketing`, `AmazonFBA`), or empty to search all of Reddit;
- search parameters: sort order, time period, post limit;
- a Reddit session cookie (explained in section 5).

**Output:**

- Count mode: an Excel `.xlsx` table with three columns: subreddit, keyword, number of posts found;
- Full collection mode: `.md` files (120 posts each) with the post text and the comment tree, plus a ZIP archive of all of them.

**Typical workflow:**

1. Run Count mode first to see how many posts exist per keyword, and drop queries that are too broad.
2. Run Full collection on the keywords you kept.
3. Download the ZIP and pass the files on for analysis.

**Version history.** Current version: v6. Compared with v4 it fixes the layout (the hint under the Start button no longer overlaps it) and resuming a collection after a break (section 9). In Count mode the progress counter now says "combinations" instead of "posts".

## 2. What you need before you start

You need four things. No paid services are involved.

| What | Why | Where to get it |
| --- | --- | --- |
| A Windows 10 or 11 computer | The instructions target Windows (the `run.bat` launcher works only there) | you already have it |
| Python 3 | The language the tool is written in | python.org (section 3) |
| Google Chrome | Running the interface and getting the cookie | you already have it |
| A secondary Reddit account | Its session is used to access the data | reddit.com (section 5) |

**Use a secondary account, not a work account.** Reddit forbids automated collection without permission (details in section 11). If the account gets restricted, your company account stays safe.

**Skills.** No programming is needed. You only have to open a folder, double-click a file and paste text into a field.

## 3. Installing Python on Windows

You install Python once. Checking takes a minute, installing about five.

**First, check whether it is already installed.**

1. Press `Win + R`, type `cmd` and press Enter. A black window (the command prompt) opens.
2. Type `py --version` and press Enter.
3. If you see something like `Python 3.12.4`, Python is installed: go to section 4. If you get an error, install it with the steps below.

**Installation:**

1. Open python.org, go to Downloads and download the current Python 3 for Windows.
2. Run the downloaded file.
3. On the first screen **tick "Add python.exe to PATH"** (at the bottom), then click "Install Now".
4. Wait for "Setup was successful" and close the window.
5. Close and reopen the command prompt and run `py --version` again. It should now show a version.

**Why every command here uses `py` and not `python`.** Windows ships a placeholder named `python` that opens the Microsoft Store and prints "Python was not found; run without arguments to install from the Microsoft Store". That is exactly what happened on the first run. The `py` command (the Python Launcher) bypasses the placeholder and works reliably, so every command below starts with `py`.

**Do not install the extra libraries by hand.** The `run.bat` file installs the required packages (`flask`, `requests`, `openpyxl`) on first launch.

## 4. Project files and first launch

The web tool consists of four files that must stay together in one folder (for example, `C:\folder\JOB\reddit_tool`). They are in the `app` folder of the archive `Reddit_parser_AL_v6_package.zip`: unzip it with right click and "Extract All".

| File | Purpose |
| --- | --- |
| `app.py` | The whole program: search, collection, interface, server (about 1,100 lines, one file) |
| `run.bat` | Double-click launcher: installs libraries, opens the browser, starts `app.py` |
| `requirements.txt` | Library list: `flask`, `requests`, `openpyxl` |
| `README.md` | Short user instructions |

The archive also contains the `console_scripts` folder (older command-line scripts, section 13) and the `docs` folder (this documentation in Ukrainian and English).

Two things are created automatically, you do not make them by hand:

| What | When it appears | What is inside |
| --- | --- | --- |
| The `output/` folder | At first start | All results |
| The `saved_settings.json` file | After the first click on Start | Settings of the last run (without the cookie) |

**First launch, step by step:**

1. Open the folder with the files.
2. Double-click `run.bat`. A black window opens. The first time it spends a few seconds installing libraries, then prints "Запускаю сервер..." (starting the server).
3. The browser opens `http://localhost:5000` by itself. If it does not, type this address into Chrome.
4. **Do not close the black window.** It is the server. If you close it, the page stops working.
5. To stop the program, close the black window or press `Ctrl + C` in it.

**Alternative launch without `run.bat`.** Open a command prompt in the project folder and run `py -m pip install -r requirements.txt`, then `py app.py`.

**Windows may show a SmartScreen warning** for `run.bat`. Click "More info", then "Run anyway". The file is simple and consists of a few short commands, you can open it in Notepad and check.

**Results are stored like this:**

- `output/<project name>.xlsx`: the count table;
- `output/<project name>/`: a folder with files such as `posts_part_001_of_003.md`, plus `search_found_urls.txt` (all links found) and `failed_urls.txt` (links that failed to download, created only if there were errors);
- `output/<project name>.zip`: an archive of that folder, served by the Download button.

## 5. The `reddit_session` cookie: access to the data

Without a cookie, Reddit answers every request with a 403 error, so the tool will not work.

**Why.** In May 2026 Reddit closed its public JSON addresses to requests without authorization. The official API (OAuth) needs manual approval, and small projects are usually declined. The only working option is the same JSON addresses with the cookie of a signed-in user. The tool adds it to every request.

**What a cookie is.** A long string that tells Reddit you are signed in. For the site it works like a password.

**How to get it, step by step:**

1. Create a secondary Reddit account (or use an existing non-work one) and sign in to it in Chrome on reddit.com.
2. Press `F12`. The developer panel opens at the bottom or side.
3. Find the **Application** tab at the top of the panel. If you do not see it, click `>>` on the right, it is in the hidden menu.
4. On the left expand **Cookies** and choose `https://www.reddit.com`.
5. In the table find the row named `reddit_session`.
6. Double-click its value in the Value column, select all (`Ctrl + A`) and copy (`Ctrl + C`).
7. Paste it into the "Reddit session cookie" field on the tool's page.

**Safety rules:**

- Never share the cookie or paste it into chats or documents. Whoever has it acts as that account.
- Use a separate account. Reddit may restrict an account that is used for automated collection.
- The tool does not write the cookie to disk. It lives in memory while the black server window is open. After a restart you must paste it again.
- If you sign out of the account in the browser, the cookie most likely stops working. For collection it is convenient to keep a separate Chrome profile or an incognito window.

**When the cookie stops working.** Its lifetime is not fixed. During a long collection (thousands of posts, hours of work) it may expire. Requests then start returning 403. After three such errors in a row the tool **pauses itself**, and the run page shows a "Refresh session cookie" block. Get a new value using the steps above, paste it into that block and click "Refresh and continue". The work continues from the same place, already collected posts are not repeated.

## 6. Using the interface

The `localhost:5000` page has five blocks. **The interface text is in Ukrainian**, so each field below is shown with its on-screen name and an English translation.

### Block "Проєкт" (Project)

| Field | What to enter | Default |
| --- | --- | --- |
| Назва файлу / проєкту (File / project name) | Name of the result. Letters, digits, `-` and `_`. Other characters become `_` | `reddit_project` |
| Mode (radio buttons) | "Тільки підрахунок" (Count only) or "Повний збір" (Full collection) | Count only |

### Block "Що шукати" (What to search)

| Field | What to enter |
| --- | --- |
| Ключові слова (Keywords) | One per line. Without quotes: broad search. In quotes (`"ABM strategy"`): exact phrase match |
| Сабредіти (Subreddits) | One per line, without `r/` (for example, `marketing`). Empty: search all of Reddit |

The tool adds nothing to your words and removes nothing. Whatever you type on a line goes to Reddit as the search query. So write single-word terms (`ABM`) without quotes, and put multi-word phrases in quotes to avoid junk.

### Block "Параметри пошуку" (Search parameters)

| Field | Values | Default |
| --- | --- | --- |
| Сортування (Sort) | `new`, `relevance`, `top`, `comments` | `new` |
| Період (Period) | `all`, `year`, `month`, `week`, `day` | `all` |
| Останні N місяців (Last N months) | Cuts off older posts. 0 = no limit | 0 |
| Ліміт постів на ключове слово (Post limit per keyword) | Maximum posts for each "keyword + subreddit" pair | 1000 |

The **"Тест: 10"** button (Test: 10) sets the limit to 10. Use it for the first trial run.

The "Last N months" field works reliably only with `new` sorting: the search goes from newest to oldest and stops when it meets a post older than the cutoff. With other sort orders posts are not in date order, so the cutoff is inexact.

### Block "Параметри збору" (Collection parameters, visible only in Full collection mode)

| Field | Meaning | Default |
| --- | --- | --- |
| Глибина коментарів (Comment depth) | How many levels of nested replies to take | 6 |
| Мін. рейтинг коментаря (Min comment score) | Comments with a lower score are skipped | -10 |
| Затримка між постами, сек (Delay between posts, sec) | Pause between requests. Lower is faster but raises the chance of blocking | 5 |
| Постів на 1 MD-файл (Posts per MD file) | Batch size per file | 120 |

### Block "Доступ" (Access)

One field: the cookie (section 5). It is masked with dots.

### Starting and the run page

Click **"▶ Почати"** (Start). The run page opens:

- a status (`running`, `paused`, `stopped`, `done`, `error`) and a counter such as "124 / 960 постів • 3,540 коментарів" (posts and comments; in Count mode it says "комбінацій", combinations, instead of "постів");
- a progress bar and an estimate of the remaining time;
- the **"Пауза / Продовжити"** button (Pause / Resume): pauses between requests;
- the **"Стоп"** button (Stop): ends the run early, everything already collected is kept (during text collection a ZIP archive is created too);
- the **"← Нові налаштування"** button (New settings): returns to the main page without stopping the work;
- the **"Оновити cookie сесії"** block (Refresh session cookie, section 5);
- a live log of all events;
- the **"⬇ Завантажити"** button (Download) once the work is finished.

You may close the run page: collection continues as long as the black server window is open. To return, open `localhost:5000/progress`.

**Only one task can run at a time.**

### Recommended order of work

1. Count mode with your chosen keywords and subreddits. It is fast and shows the scale.
2. Remove words that returned 0 or far too much noise (several thousand).
3. Full collection with a limit of 10 as a trial. Open the result and check that the posts are relevant.
4. Full collection with the real limit.

**How long it takes.** Each post is processed with a pause (5 seconds by default) plus the request time. As a guide, 1,000 posts take roughly 1.5 to 2 hours and 5,000 posts about 7 hours.

## 7. Technical specification: architecture

The tool is a single Python process: a Flask web server that serves two HTML pages and starts collection in a background thread. There is no database, everything is kept in memory and on disk in the `output/` folder.

&#91;embedded content: architecture · 4 levels\]

The page only shows state and sends commands, so closing the tab does not stop collection: it lives in the background thread.

**Stack and why each library is used:**

| Library | Role |
| --- | --- |
| `flask` | Web server and the interface routes (addresses) |
| `requests` | HTTP requests to Reddit |
| `openpyxl` | Creates the Excel file in Count mode |
| `threading`, `json`, `re`, `shutil`, `pathlib` | Python standard modules: background thread, settings file, finding IDs in text, ZIP, paths |

**Server.** It listens only on `127.0.0.1`, port `5000`, so other computers on the network cannot reach it. Debug mode is off.

**Background thread.** Clicking Start launches `run_job_thread` in a separate (daemon) thread. The pages only show state and send commands, so closing the tab does not stop the collection.

**Shared in-memory state** (reset when the program restarts):

| Variable | What it holds |
| --- | --- |
| `job` | Status, post and comment counters, the log (last 2,000 lines), the list of files to download, the mode |
| `job_lock` | A lock so the collection thread and page requests do not corrupt `job` at the same time |
| `pause_event` | The pause flag: while set, the thread waits |
| `stop_event` | The stop flag: the thread ends at the next check |
| `session_cookie` | The cookie added to every request. It can be replaced without restarting the task |
| `consecutive_403` | Counter of 403 errors in a row for the auto-pause |

**Settings between runs.** Before starting, the form fields are written to `saved_settings.json` (the cookie is not included). When the main page opens, the values are read back into the form. If the file is damaged or missing, the `DEFAULT_SETTINGS` set is used. To reset, delete the file.

**Interface inside `app.py`.** The HTML of both pages sits in the variables `INDEX_HTML` and `PROGRESS_HTML`. Values are inserted into the main page through markers such as `@@KEYWORDS@@`. The run page asks `/status` once a second and draws progress, counters and the log.

**Look and feel.** Dark theme: background `#101828`, cards `#1A2438`, borders `#2E3B57`, accent `#B8F500` (lime), main text white, secondary `#7A8499`. Font Calibri, Consolas in the log.

**Task statuses:**

| Status | When |
| --- | --- |
| `idle` | Nothing is running |
| `running` | Work is in progress |
| `paused` | Paused: manually or automatically (three 403s in a row) |
| `stopped` | The user clicked Stop |
| `done` | Everything finished |
| `error` | Nothing found, or an exception in the code |

## 8. Technical specification: routes and parameters

The server has nine addresses. In the browser you open only the main page and the run page directly. JavaScript on the pages calls the rest.

| Address | Method | What it does |
| --- | --- | --- |
| `/` | GET | Main page. Fills the form with saved settings |
| `/start` | POST | Validates the fields, saves settings, starts the background thread. Replies `{"ok": true}` or a 400 error with text |
| `/progress` | GET | The run page |
| `/status` | GET | JSON with the state: `status`, `current`, `total`, `comments`, `mode`, `log` (last 400 lines), `result_files` |
| `/pause` | POST | Sets `pause_event` |
| `/resume` | POST | Clears `pause_event` |
| `/stop` | POST | Sets `stop_event` and clears the pause so the thread does not hang |
| `/update_cookie` | POST | Takes the `cookie` field, replaces `session_cookie`, resets the 403 counter, clears the pause |
| `/download/<file>` | GET | Serves a file from the `output/` folder |

**Checks at start (`/start`):**

- a task is already running: refused with "Задача вже виконується" (a task is already running);
- no keywords: refused;
- empty cookie: refused;
- Count mode with no subreddit: refused (a subreddit is required for counting, empty is allowed only for Full collection);
- the project name is cleaned: everything except letters, digits, `-` and `_` becomes `_`.

**Form parameters passed into the task:**

| Parameter | Type | Mode |
| --- | --- | --- |
| `mode` | `count` or `scrape` | both |
| `base_name` | string | both |
| `keywords`, `subreddits` | lists of strings | both |
| `sort`, `time_filter` | `new`/`relevance`/`top`/`comments`, `all`/`year`/`month`/`week`/`day` | both |
| `months_back`, `limit` | integers | both |
| `cookie` | string | both |
| `max_depth`, `min_score` | integers | Full collection |
| `delay`, `posts_per_file` | integers | Full collection |

**Constants fixed in the code, not changeable in the interface:**

| Constant | Value | Purpose |
| --- | --- | --- |
| Comment limit per request | 500 | The `limit=500` parameter in the post address |
| Request timeout | 15 sec | Do not hang forever if Reddit is silent |
| Retries on 429 | 3 | How many times to wait and try again |
| Wait on 429 | 60 sec | Four steps of 15 sec, the log shows a line each time saying this is not a freeze |
| Search page size | up to 100 | The most Reddit returns per request |
| Pause between search pages | 1 sec | Spares the server |
| Pause between search queries | 2 sec | Same |
| Auto-pause | 3 consecutive 403 errors | Signal that the cookie is stale |
| Log kept in memory | 2,000 lines | Older lines are dropped |
| Request headers | Chrome 131 on Windows User-Agent | The request looks like a normal browser |

## 9. Technical specification: how collection works

### Post search (shared by both modes)

The `search_paginated` function walks the Reddit result pages and returns links and the number found.

**Request URL:**

- with a subreddit: `reddit.com/r/<subreddit>/search.json?q=<keyword>&restrict_sr=1&sort=<sort>&t=<period>&limit=<page size>`;
- without a subreddit: `reddit.com/search.json?q=<keyword>&sort=...&t=...&limit=...`;
- `restrict_sr=1` restricts the search to that subreddit;
- following pages are requested with the `after` parameter returned by Reddit.

The keyword goes into the query exactly as typed, quotes included.

**When the search stops:**

1. The post limit for this "keyword + subreddit" pair is reached.
2. Reddit returns nothing more (empty page or no `after`).
3. A post older than the "Last N months" boundary is met (the boundary is N x 30 days back from now).
4. The user clicks Stop.

In practice Reddit does not return more than about 1000 results per search query, even if the limit in the form is higher. This is a Reddit limitation.

**Search errors:**

| Reddit response | What the tool does |
| --- | --- |
| 200 | Reads the results |
| 403 | Stops this search and logs "cookie is not valid or expired". There is no auto-pause at this stage |
| 429 | Waits 60 seconds and repeats the same page. The number of retries during search is unlimited |
| Other | Stops this search and logs the error code |

**Count mode.** For each "subreddit + keyword" pair it runs the search but stores no links, it only counts. There is a 2 second pause between pairs. If the count reaches the limit, the log shows "(possibly more)". The result is written to Excel: three columns, blue header, autofilter, frozen first row.

### Full collection: two steps

**Step 1: collecting links.**

1. For every keyword and every subreddit (or "all" if empty) a search is started.
2. Links are merged into one list without duplicates, in order of first discovery.
3. For every link the tool remembers which keywords found it. A post found by two keywords will show both in the result.
4. The list is saved to `search_found_urls.txt`.
5. If nothing is found, the status becomes `error`.

**Step 2: downloading text and comments.** For every link in turn:

1. Stop and pause check.
2. If the post ID is already among the collected ones, the post is skipped (resume, below).
3. `.json?limit=500` is appended to the link and the request is made.
4. The response is parsed: title, author, subreddit, date, score, text, comment tree.
5. The block is appended to the current `.md` file.
6. A pause of `delay` seconds, then the next post.

**Reddit responses in step 2:**

| Response | What happens |
| --- | --- |
| 200 with the expected structure | The post is saved |
| 404 | Post deleted, goes to `failed_urls.txt` |
| 429 | Waits 60 seconds (4 times 15), retries, up to 3 times. Then the post goes to failed |
| 403 | The post goes to failed, the 403 counter grows |
| Connection error, not JSON, unexpected structure | The post goes to failed |

**Auto-pause on 403.** Three 403 errors in a row put the collection on pause with a message in the log. Any non-403 response in between resets the counter. After a new cookie is pasted, the collection continues. The three posts that triggered 403 land in `failed_urls.txt`. They will be collected on a re-run.

### How comments are parsed

The `parse_comments` function walks the tree recursively:

- it does not go deeper than `max_depth` (6 levels by default);
- it skips deleted (`[deleted]`, `[removed]`) and empty comments;
- it skips comments with a score below the threshold (-10 by default);
- each nesting level is shifted by two spaces;
- it counts comments for the live counter.

**Limitation.** Reddit folds large branches into a "show more" button. The tool does not expand these buttons. A single request takes up to 500 comments. For typical discussions (5-30 comments) this is enough, but in huge threads some comments may be missing.

### Resuming after an interruption

Every saved post gets a service marker `<!-- id:abc123 -->`. Before step 2 the tool reads all `posts_part_*.md` files in the project folder and collects these IDs. Posts with known IDs are skipped.

To continue after a crash, a closed window or a stop:

1. Start the tool again.
2. Enter **the same project name**. Results live in `output/<name>/`, and that is where the tool looks for what is already collected.
3. Enter the same keywords and subreddits and a new cookie.
4. The log will show "Already collected posts found: N, skipping them".

Several things affect resuming:

- Step 1 (search) is executed again, so the set of links may differ slightly if new posts appeared on Reddit. The "POST N" numbering and the split into parts are calculated from the position in the new list.
- File names contain the total number of parts (`..._of_003.md`). If that number changed, new posts go into files with new names and the old ones stay. There are no duplicates, because skipping is done by ID.
- `failed_urls.txt` is not deleted on a successful re-run. It is the history of the previous attempt.
- If you change keywords or subreddits but keep the project name, new posts are added to the old ones in the same folder.

## 10. Output file formats

The result of count mode is an Excel table, the result of full collection mode is a set of text files in Markdown format. They are easy for a person to read and to hand over to a language model for analysis.

### Excel table (count mode)

File `output/<name>.xlsx`, one sheet named "Матриця" (Matrix):

| Column | Content |
| --- | --- |
| Сабредіт (Subreddit) | Name without `r/` |
| Ключове слово (Keyword) | As typed, with quotes if there were any |
| Кількість постів (Post count) | A number. If it equals the limit, there may be more real posts. The word `ПОМИЛКА` (ERROR) means the search for this pair failed |

### Markdown files (full collection)

The folder `output/<name>/` contains files `posts_part_001_of_00N.md`. Each holds up to 120 posts (the number can be changed in the form). Each file starts with a header:

```
# REDDIT ПОСТИ - ЧАСТИНА 1 з 3

**Дата експорту:** 2026-10-07 11:58
**Ключові слова:** ABM, "LinkedIn ads"
**Сабредіти:** marketing
**Пости у цьому файлі:** 1-120 з 312
**Джерело:** Reddit Search JSON API
```

In the real files this header uses long and short dashes instead of hyphens, which is only styling. The labels are in Ukrainian (POSTS, PART 1 of 3, Export date, Keywords, Subreddits, Posts in this file, Source). After the header come the posts. Each post has this structure:

```
============================================================
<!-- id:102d6nc -->
# ПОСТ 1: Post title

- **Знайдено за запитом:** ABM
- **Сабредіт:** r/marketing
- **Автор:** u/example
- **Дата:** 2023-01-03 17:01 UTC
- **Upvotes:** 1
- **Коментарів:** 6
- **Посилання:** https://reddit.com/r/marketing/comments/102d6nc/abm_gifting/

## Текст поста

Text written by the author.

## Коментарі

**u/author1** (👍 2)
First level comment text.

  **u/author2** (👍 1)
  A reply to it, shifted by two spaces.
```

**What the fields mean:**

| Field | Explanation |
| --- | --- |
| `<!-- id:... -->` | Service marker for resuming collection (section 9). Do not delete it |
| ПОСТ N (POST N) | Sequence number in the list of this run |
| Знайдено за запитом (Found by query) | Only the keywords that found this particular post |
| Upvotes, Коментарів (Comments) | Values at the time of collection. The comment count is the total on Reddit, not the number that made it into the file |
| (👍 N) next to a comment | The comment score |

**Special cases:**

- deleted post: "Текст поста видалено" (post text deleted) instead of the text;
- link post without text: "Пост-посилання: URL" (link post: URL);
- no comments or all deleted: "Коментарів немає або всі видалено" (no comments or all deleted).

The text may contain entities such as `&amp;` instead of `&`. This is how Reddit returns it, the tool does not change it.

### Other files in the project folder

| File | Content |
| --- | --- |
| `search_found_urls.txt` | All found links, one per line |
| `failed_urls.txt` | Links that could not be downloaded. Appears only if there were errors |
| `<name>.zip` (next to it, in `output/`) | Archive of the whole project folder |

**Size.** About 3000 posts with comments is 20-30 MB of text. Analyzing that as one file is inconvenient, which is why the data is split into parts. For analysis, upload the parts one by one or several together, depending on the limit of the analysis tool.

## 11. Limits, risks and Reddit rules

The main risk of the tool is not technical but legal: it operates in a gray zone of Reddit's rules. The other limits are manageable.

### Legal and platform risks

- **Reddit rules.** Since the end of May 2026 Reddit closed public JSON addresses for unauthenticated requests, and its rules forbid automated collection without permission. A cookie of a regular account technically gives access to the same data, but does not make such collection permitted. For commercial use (research for a company) consult a lawyer.
- **Account ban.** Reddit may restrict or ban the account used for automated collection. That is why a separate account is needed (section 5), not the company's working account.
- **Changes on Reddit's side.** Addresses, responses and rules may change without notice. If all requests suddenly return 403 even with a fresh cookie, most likely the access policy changed and the tool is not broken.
- **Personal data.** The files contain author names (`u/...`). In reports and presentations quote the text without names and do not publish the files as a whole.

### How to reduce the risk of being blocked

- do not reduce the delay below 5 seconds between posts;
- do not run two copies of the tool with the same cookie;
- collect only what the research needs: clearly formulated keywords, a limited period;
- do the count first, then the full collection;
- do not leave a long collection unattended: check the log every few hours.

### Technical limits

| Limit | Details |
| --- | --- |
| Result ceiling | Reddit returns up to about 1000 results per search query. To cover more, split the query into several keywords or periods |
| Folded comments | "Show more" buttons are not expanded, large discussions are incomplete |
| Speed | One task, one thread, a pause between requests. 5000 posts take about 7 hours |
| Cookie | Lives a limited time, a long collection needs a refresh (auto-pause helps) |
| State in memory | After the black window is closed, the log on the progress page and the cookie are gone. Files in `output/` remain |
| Windows only | `run.bat` works only on Windows. On Mac and Linux start `python3 app.py` manually |
| Retry on 429 in search | Has no upper bound. If Reddit does not lift the limit for a long time, the search may wait for hours. Stop it with the Stop button |
| Text only | Images and videos from posts are not downloaded |
| Reddit search is imprecise | Results include irrelevant posts. Review a sample before analysis |

### Local server security

The server listens only on `127.0.0.1`, so it is not reachable from the network. There is no authentication: any program on the same computer can talk to it. The `/download/<file>` address does not sanitize the path, which is acceptable for a local app but makes it unwise to expose the port externally. Do not change `host` to `0.0.0.0`.

## 12. Common errors and what to do

The most frequent problems are collected in one table. First find the message you see in the first column. The tool's own messages are in Ukrainian, the English meaning is given in brackets.

| What you see | Cause | What to do |
| --- | --- | --- |
| `Python was not found; run without arguments to install from the Microsoft Store` | The Windows `python` stub was triggered | Use the `py` command, not `python`. If `py` is not found either, install Python (section 3) |
| The black `run.bat` window flashed and vanished | Python is not installed or `run.bat` did not find `py` | Open a command prompt in the project folder, run `py app.py` and read the error |
| `ModuleNotFoundError: No module named 'flask'` | Libraries were not installed | Run `py -m pip install -r requirements.txt`, then `py app.py` |
| The page `localhost:5000` does not open | The server is not running or the black window was closed | Start `run.bat`, keep the black window open, open the address manually |
| `Address already in use`, port 5000 is busy | Another copy of the tool or another program is running | Close other black windows of this tool, wait a minute, start again |
| Message "Вкажи cookie сесії" (Enter the session cookie) | The cookie field is empty | Paste the `reddit_session` value (section 5) |
| "Для режиму підрахунку потрібен хоча б один сабредіт" (Count mode needs at least one subreddit) | Count mode, subreddit field empty | Fill in subreddits. An empty field is allowed only for full collection |
| "Задача вже виконується" (A task is already running) | The previous run is still going | Open `localhost:5000/progress` and wait for it to finish or press Stop |
| Log: "403 cookie не діє або застаріла" (cookie invalid or expired), count shows `ПОМИЛКА` everywhere | The cookie is invalid, expired or copied incompletely | Take a new value from the browser, paste it completely, start again |
| Auto-pause: "Три 403-помилки підряд" (Three 403 errors in a row) | The cookie expired in the middle of collection | Paste a fresh cookie into the "Update session cookie" block and press "Update and continue". Failed posts will be collected on a re-run |
| "Пошук не дав жодного результату" (Search gave no results) | Keywords misspelled, subreddit does not exist, period too narrow, expired cookie | Check the same keywords in the search on reddit.com, remove the "Last N months" limit, try a new cookie |
| Long waits "Rate limit, чекаємо 60 сек" (waiting 60 s) | Reddit limits request frequency (error 429) | This is normal, the log shows "still waiting" lines. If it happens often, raise the delay to 8-10 seconds |
| `ConnectionError` or "Помилка з'єднання" (connection error) | No internet, a VPN, firewall or antivirus is interfering | Check the internet, turn off the VPN, allow Python network access |
| `PermissionError` when saving `.xlsx` | That Excel file is open in Excel | Close the file in Excel and start again |
| `TypeError: expected str, bytes or os.PathLike object, not NoneType` on re-run | A bug in versions v4 and v5 when resuming collection | Use version v6 |
| Many irrelevant posts | Keywords without quotes are searched broadly | Put multi-word phrases in quotes, run "Count" first and review a sample |
| The form shows old values | Settings are taken from `saved_settings.json` | Change the fields or delete that file |
| Most comments are missing from the file | Score threshold, low depth or folded branches | Increase depth, lower the minimum score (for example to -100). Folded branches are not expanded (section 9) |

**Where to find the error message.** There are two places: the black window (technical errors are printed there) and the log block on the progress page. If something goes wrong, copy the last lines from both places and show them to whoever is helping.

## 13. Appendix

### Reproduction checklist from scratch

- [ ] Python 3 is installed, the `py --version` command shows a version
- [ ] The archive `Reddit_parser_AL_v6_package.zip` is unpacked into a separate folder
- [ ] Double click on `run.bat` (in the `app` folder), the black window stays open and prints "Starting server..."
- [ ] The page `localhost:5000` is open, you see a dark form with a lime button
- [ ] You have an extra Reddit account, logged in in Chrome
- [ ] The `reddit_session` cookie is copied (F12, Application, Cookies)
- [ ] Trial run: "Count only" mode, one keyword, one subreddit, limit "Test: 10"
- [ ] An `.xlsx` appeared in the `output/` folder and a "Download" button
- [ ] Trial full collection with limit 10: `output/<name>/` contains the file `posts_part_001_of_001.md` with posts and comments
- [ ] Full collection on real data

If all steps are done, the tool is fully reproduced.

### Console scripts the tool grew out of

Before the web interface there were separate Python scripts. Two of them are in the archive in the `console_scripts` folder (`reddit_posts_exporter_2.py` and `extract_urls.py`), because they cover a scenario the web version does not have. The keyword search and count scripts were replaced by the web version, their files are not in the archive.

| Script | What it does | In the web version? |
| --- | --- | --- |
| `reddit_posts_exporter_2.py` | Takes a ready list of links from `unique_urls.txt` and collects texts and comments into `reddit_exports/` | No. In the web version links come only from keyword search |
| `reddit_keyword_search_exporter.py` | Keyword search, then full collection | Yes, "Full collection" mode |
| `reddit_keyword_matrix.py` | Counts posts per "subreddit + keyword" pair | Yes, "Count only" mode |

The old link-list scenario had three stages: the Chrome extension Instant Data Scraper collected links from a subreddit feed into a table, the script `extract_urls.py` merged several tables into one file `unique_urls.txt` without duplicates, and `reddit_posts_exporter_2.py` collected the posts from it. All scripts are started with `py <name>.py` in the script folder and need the same cookie.

**How to run the console scripts.** First install the libraries: `py -m pip install requests pandas openpyxl`. The script `extract_urls.py` is started in a folder with `.xlsx` tables (Instant Data Scraper exports) and creates `unique_urls.txt`. In `reddit_posts_exporter_2.py` the cookie is written directly in the code: open the file in Notepad, find the `COOKIES` block and replace `PASTE_YOUR_reddit_session_COOKIE_HERE` with your value. Never pass on a file with a cookie written into it. The copy in the archive also has the resume bug fixed (the same one the web version had before v6).

### Glossary

| Term | In plain words |
| --- | --- |
| Subreddit | A topic section of Reddit, for example `r/marketing` |
| Cookie | A small file by which a site recognizes that you are logged in |
| JSON | A text format in which Reddit returns data (posts, comments) |
| API | An official way for a program to get data from a service |
| Command prompt (cmd) | The black window where text commands are typed |
| PATH | The list of folders where Windows looks for programs. Python must be in it |
| localhost | The address of your own computer. `localhost:5000` is a page served by the program from inside |
| Port | The number of a "door" on the computer. Here it is 5000 |
| Background thread | A part of the program that works separately while you use the page |
| Pagination | Reading results in portions (page by page) |
| 403 | Response code "access denied". Here it almost always means the cookie is invalid |
| 429 | Response code "too many requests". You need to wait |
| 404 | Response code "not found". The post was deleted |
| Markdown (`.md`) | A simple text format with marks for headings and emphasis |
| ZIP | An archive that packs several files into one |
| Traceback | A long error message in the black window, with the error name line at the end |
| VoC (Voice of Customer) | Research of customer opinions in their own words |

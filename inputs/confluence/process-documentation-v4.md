# Reddit Reply Lane | Process Documentation

Source: https://sellerlogic.atlassian.net/wiki/spaces/AIBOT/pages/2891579393
Version: 4, 2026-10-16. Retrieved: 2026-10-19.
Note: connector Markdown conversion loses date/macro elements; use the HTML and JSON snapshots for those.

## 1. Overview

The Reddit reply lane helps the official SELLERLOGIC account **u/sellerlogic\_support** answer Amazon sellers on Reddit. Every hour it finds new posts in seven seller communities, sorts them, reads the replies under each post, and writes a reply draft that passed the three self-checks from the account guidelines. Anton Lisitskyi reviews every draft in Asana and posts it himself: **the lane never posts, comments or votes on Reddit.**

---

## 2. Architecture Overview

- **Trigger / Schedule:** three n8n workflows, all published .
    - `RD - Discovery`: hourly at minute 7.
    - `RD - Drafter`: hourly at minute 27.
    - `RD - Asana Sync`: every 15 minutes.
- **Data sources:**
    - Reddit's public feed of new posts for the 7 communities in the guidelines (no login).
    - The replies under each post, read with the login cookie of a **company Reddit reading account** (not u/sellerlogic\_support, not a personal account).
    - The account guidelines "Reddit u/sellerlogic\_support Guidelines" v3.2 (Drive `1_dSnW9GPrAq7ts1erL4Y703XB7oTILMa`), built into the prompts.
    - The account's own last 30 comments (table `rd_account_comments`), for self-check 1.
- **Outputs:**
    - Asana tasks on the board [Content | Reddit](https://app.asana.com/1/292294265665759/project/1218967280298844), assigned to Anton.
    - Database rows in the `rd_` tables (every post, decision and draft).
    - A row per change of state in Anton's sheet "Reddit Seeding / SL", tab "Lane log" (the lane writes only that tab).
- **Workflows involved:** `RD - Discovery`, `RD - Drafter`, `RD - Asana Sync`. Errors go to `JTA: Error Handler`.

---

## 3. Workflow Phases

### Phase 1: Discovery (RD - Discovery, hourly)

- Reads the newest 100 posts across the 7 communities in one request and stores each post once.
- Sets aside every post older than 48 hours that has not reached review yet.
- Takes up to 6 waiting posts, oldest first.
- Reads the replies under each post with the reading account's cookie:
    - first ONE test request; if Reddit refuses it, comment reading stops (`comments_mode = cookie_paused`), the run continues without replies, and an alert task is raised (section 4);
    - if the test passes, one request per post, 65 seconds apart (at most 6 an hour).
- Gemini sorts each post into RELEVANT, NEEDS\_REVIEW or IRRELEVANT using the guidelines' topics, exclusions and stop signals, and lists facts from the post, missing information and risk flags.
- Open questions to the community on an in-scope topic ("How do you all handle X?") count as replyable (decision with Anton, ).
- If the same person posted 3 or more times within 24 hours, the post gets the flag `same_author_burst`.

### Phase 2: Drafting (RD - Drafter, hourly)

- Takes up to 4 posts: RELEVANT ones, plus NEEDS\_REVIEW ones Anton asked a draft for.
- Gemini writes one draft in the voice and reply order of the guidelines (40 to 180 words), with the replies under the post in view: it adds what is missing, or skips the post if the answer is already there.
- Three separate self-checks, each rewriting the draft:
    1. AI patterns and repetition, against the account's last 30 comments;
    2. accuracy and value, against the post and the replies;
    3. human naturalness.
- Hard checks in code: dashes replaced by the plain hyphen; no links; no SELLERLOGIC mention, product pitch or DM invitation; no invented personal experience; 40 to 180 words; a detail from the post and a next step (judged by self-check 2).
- Passed: status DRAFTED. Failed: status BLOCKED with every reason, draft kept.

### Phase 3: Review in Asana (RD - Asana Sync, every 15 minutes)

One task per post on [Content | Reddit](https://app.asana.com/1/292294265665759/project/1218967280298844):

| Section | What it holds | What Anton does |
| --- | --- | --- |
| Draft ready | a draft that passed every check | edits if needed, posts it himself, moves the task to Posted and adds a comment with the link to his Reddit comment |
| Blocked | a draft a hard check stopped, with the reason | may still use the text; moves it to Posted or Rejected |
| Needs review | a post that may be worth a reply, no draft | moves it to "Draft it" for a draft within about an hour, or to Rejected |
| Draft it | his request for a draft | nothing; the draft arrives as a task comment |
| Posted | posted by him | nothing more; the lane records the link from his comment |
| Rejected | not posted | a comment with the reason helps |

- Each task shows the post link, the draft, the reasons for and against, risk flags, the original post, and a box when the same author posted several times within 24 hours (with links to the other posts).
- Comments the lane writes start with `[RD lane]`.
- Posted drafts are added to `rd_account_comments`, so self-check 1 compares new drafts with what the account said recently.

---

## 4. When the reading account's cookie stops working

- The lane creates the task **"\[ACTION\] Reddit cookie stopped working"** in Blocked, assigned to the owner of the reading account (`rd_config.cookie_owner`, Arsenii Kovsh), with the reason.
- Renewal: log in to the reading account in Chrome, copy the cookie `reddit_session` (F12, Application, Cookies), and paste it into the n8n credential "Reddit session (reading account)" as `reddit_session=<value>`. Then complete the task: the next Discovery run reads replies again.

The cookie value is never sent through chat, Slack, documents or tasks. If it stops again soon after a new cookie, Reddit may be refusing the account itself: do not keep renewing.

---

## 5. Technical Reference

| Item | Value |
| --- | --- |
| Workflow files (source of truth) | shared repo `management-claude-instructions`, folder `n8n/workflows/reddit/`. Generated by `generators/build_discovery.py`, `build_drafter.py`, `build_asana_sync.py`; never hand-edit the JSON. Behaviour test: `generators/test_rd_code_nodes.js` (82 checks) |
| How a change reaches n8n | commit and push, then `python3.13 scripts\n8n_api.py upload "<file>"` (it compares the result with the file) |
| n8n workflow ids | Discovery `EQAN6qNTLJZHazSD` · Drafter `tn7Qf5LP6Zrw0Edv` · Asana Sync `fjoEl0cs03mrLRgR` |
| DB tables (bot database) | `rd_posts` (every post, sorting, draft, decision) · `rd_config` (settings and Asana ids) · `rd_subreddits` (the 7 communities) · `rd_run_log` (one row per run) · `rd_account_comments` (what the account said, for self-check 1) |
| Settings (rd\_config) | `comments_mode` (cookie · cookie\_paused · off · rss), `max_post_age_hours` 48, `classify_per_run` 6, `draft_per_run` 4, `asana_assignee` (Anton), `cookie_owner` (Arsenii), `sheet_enabled` (true), `sheet_id`, `sheet_tab` (Lane log) |
| n8n credential ids | Postgres `mmfGQjTIlXfCF7E7` · Gemini `Uj5F5uHp0rBd02qE` · Asana `j6XUm8QTDARIRMis` · Google service account `xF1E3bzHLPWgqFJ1` · Reddit session (reading account) `ihqmGYakmB4krPs3` |
| Asana board | Content \| Reddit, project `1218967280298844` |
| Activity sheet | "Reddit Seeding / SL" `1FXAAXNywMMq0tT2-e0OhIj8Oc1aqXvnOSFcsoZie0Sk`, tab "Lane log" (`rd_config.sheet_id`, `sheet_tab`) |
| Error workflow | `JTA: Error Handler` `0L5gnWWi89qdTajZmQ_FE`, posts to the n8n errors Slack channel |
| Model | `gemini-3-flash-preview`, up to 24,576 output tokens per call |

---

## 6. Known Gaps / Pending

- **Activity sheet log is on** since 2026-10-15 15:00 UTC (the first run wrote 97 rows, one per post sorted so far). Sheet "Reddit Seeding / SL" (`1FXAAXNywMMq0tT2-e0OhIj8Oc1aqXvnOSFcsoZie0Sk`), tab "Lane log", written by the automation's Google account (`n8n-drive-reader@rising-parser-490607-u3.iam.gserviceaccount.com`). Anton's tabs "r/ Comments", "Stealth Agents" and "info" are never written.
- **No written approval from Reddit** for scheduled reading of its data. Going live without it was a management decision on . The lane identifies itself honestly as SELLERLOGIC's automation and reads at most about 7 pages an hour.
- **What Anton actually posted is not read back from Reddit.** Self-check 1 learns from the draft of a posted reply, not from his edited text.
- **The detail-from-the-post and next-step checks are judged by AI**, not by code.
- **Posts sorted while comment reading was paused** carry the warning "replies not read"; Anton reads the thread before posting.


# Reddit Demand Generation | Build Reddit Post Discovery and Reply Drafting Automation

Source: https://app.asana.com/1/292294265665759/task/1218958869038776
Retrieved: 2026-10-19

Create an automation for the u/sellerlogic_support Reddit workflow.
The automation must support three main stages:

1. Post discovery and classification

    Check the approved Amazon seller subreddits every 60 minutes.
    Collect new posts and relevant metadata.
    Prevent duplicate processing.
    Analyze the post and existing comments.
    Classify each post as:
        RELEVANT
        NEEDS_REVIEW
        IRRELEVANT
    Apply the topic and exclusion rules defined in the attached Reddit u/sellerlogic_support Guidelines.

2. Reply draft generation

For every RELEVANT post:
    Prepare a reply draft from the perspective of a knowledgeable SELLERLOGIC employee.
    Use the specific context and details of the post.
    Provide practical value to the Amazon seller.
    Do not advertise SELLERLOGIC products.
    Do not fabricate facts, cases, results, or personal experience.
    Clearly separate confirmed facts from assumptions.
    Run the three AI quality checks defined in the guidelines.
    Never use an em dash or en dash.
For NEEDS_REVIEW posts:
    Provide the post URL and text.
    Explain why the post may or may not be relevant.
    Ask whether a reply draft should be prepared.
IRRELEVANT posts should be logged but should not be sent for approval.

3. Human approval

Send the following information for review:
    Full Reddit post URL
    Subreddit
    Original post or target comment text
    Relevance category
    Reason for classification
    Final reply draft
    Any risk flags or missing information
The automation must stop after submitting the draft for approval.
It must not publish comments on Reddit. The final review, editing, and publication are performed manually.

Expected result

A working process that:
    Finds relevant Reddit discussions every 60 minutes.
    Filters irrelevant or risky posts.
    Creates accurate and natural reply drafts.
    Sends drafts to the responsible person for approval.
    Logs all processed posts and decisions.
    Never publishes anything automatically.

Reference documents

Reddit u/sellerlogic_support Guidelines https://drive.google.com/file/d/1_dSnW9GPrAq7ts1erL4Y703XB7oTILMa/view?usp=drive_link
Reddit u/sellerlogic_support Activity Log https://docs.google.com/spreadsheets/d/1S9WkCn1NcsNx8hg1gAyyqjBnAnEVySBR6uPogMb5NlM/edit?gid=1815536610#gid=1815536610

## Comments

### 2026-10-02T13:46:12.661Z | Arsenii Kovsh | 1219102813155221

https://app.asana.com/1/292294265665759/profile/1205842675820111
Need your decision on whether to request Reddit API access, as anything automated will run under your account.

Reddit requires explicit approval before any automated access to its data, and written approval for commercial use. We already hit this: a test run collected 100 posts, then Reddit refused all 6 comment requests with "You've been blocked by network security".

The request is filed by the account owner here, with "I'm an enterprise partner/commercial developer" already selected: https://support.reddithelp.com/hc/en-us/requests/new?ticket_form_id=14868593862164&tf_42139884615700=api_request_type_enterprise_clone It asks for company details, the purpose, what we deliver with the data (nothing, internal use only) and a data budget (lowest bracket "< $500/month"). Reddit's policy behind it: https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy
Expected answer time is 2 to 4 weeks, sometimes no answer at all, and cost is around $0.24 per 1,000 calls. For us that is roughly 5,000 calls a month. (Timing and price were researched with AI from third-party sources, not confirmed by Reddit.)

Two rules in Reddit's policy affect your account directly: 
    App accounts can only be used for the app ("no mixed use accounts"), so the automation likely needs its own account next to u/sellerlogic_support. 
    Multiple accounts or requests for the same use case are prohibited. The aged accounts, proxy and antidetect browser in the parent task go directly against this and put u/sellerlogic_support at risk.

Without API access, this can still be automated: You paste a post and its visible comments into an Asana task, and within about 15 minutes you get its category with reasons and risk flags, plus a reply draft that passed the three checks from the guidelines and the hard checks (no dashes, no product pitch, no links, 40 to 180 words). Every post, draft, your final text and the comment URL are logged in the activity sheet. A weekly digest of topics and pain points for blog and email ideas.
What it cannot do without the API is find posts for you every hour. That part stays manual.

Threre are also ways to make this easier on the Claude side (skills & some tools) but honest assessment - without API (and even with, with said Reddit rules) - this process wont be efficient

### 2026-10-07T12:27:33.988Z | Anton Lisitskyi | 1219257194868318

https://app.asana.com/1/292294265665759/profile/1199659962164875
here is the full non-API project documentation

### 2026-10-14T15:15:38.631Z | Arsenii Kovsh | 1219507764996836

https://app.asana.com/1/292294265665759/profile/1205842675820111 the Reddit lane is live from today. Every hour it reads new posts in the 7 subreddits from your guidelines, sorts them, reads the replies under each post, and writes a draft that passed the three self-checks. Nothing is ever posted automatically.

The tasks come to you on the board "Content | Reddit":
    Draft ready: the draft passed every check. Edit it if needed and post it yourself, then move the task to Posted and add a comment with the link to your Reddit comment.
    Blocked: a hard check stopped the draft, the reason is in the task. The text is still there to use.
    Needs review: may be worth a reply. Move it to "Draft it" to get a draft within about an hour, or to Rejected.
    Rejected: not posting it. A comment with the reason helps.

When one person posts several times in a day, each task says so, with links to the other posts.

One thing from your side: please share the Activity Log sheet as Editor with n8n-drive-reader@rising-parser-490607-u3.iam.gserviceaccount.com and with me, so the automation can log to its own new tab "Lane log". Your "r/ Comments" tab stays untouched.

### 2026-10-15T13:44:49.996Z | Anton Lisitskyi | 1219544952941532

https://app.asana.com/1/292294265665759/profile/1199659962164875 the Editor excess is shared

### 2026-10-15T15:03:27.032Z | Arsenii Kovsh | 1219548707403263

https://app.asana.com/0/1205842675820115/ thanks, it works. The lane logs into your "Reddit Seeding / SL" file, in its own tab "Lane log". The first run today at 15:00 UTC wrote 97 rows, one per post sorted so far, and from now on it adds a row each time a post changes state. Your "r/ Comments", "Stealth Agents" and "info" tabs are never written.

Closing this build task: the lane has been live since October 14, drafts come to you on "Content | Reddit", and nothing is posted automatically.

### 2026-10-16T08:39:20.073Z | Anton Lisitskyi | 1219572593021506

https://app.asana.com/1/292294265665759/profile/1199659962164875 Thank you!
13 comments have been posted already)
One more ask (for Claude) - to summarize the doc with all project setup data (System Architecture & Deployment Guide) and put it here.

### 2026-10-16T09:21:29.842Z | Arsenii Kovsh | 1219573647892731

https://app.asana.com/0/1205842675820115/ here is the setup summary. The full version is the Confluence page "Reddit Reply Lane | Process Documentation": https://sellerlogic.atlassian.net/wiki/spaces/AIBOT/pages/2891579393

What it is
Three n8n workflows on the company n8n server, a set of tables in the bot database, Gemini for sorting and drafting, Asana for your review, and your sheet for the log. Nothing in it can post, comment or vote on Reddit.

How it runs
    RD - Discovery, hourly at :07: reads the newest 100 posts across the 7 subreddits in one request (no login), stores each post once, sets aside anything older than 48 hours, then takes up to 6 posts, reads the replies under each with the company reading account's cookie (one request per post, 65 seconds apart) and sorts them with Gemini into RELEVANT, NEEDS_REVIEW or IRRELEVANT against your guidelines v3.2.
    RD - Drafter, hourly at :27: takes up to 4 posts (RELEVANT, plus NEEDS_REVIEW ones you moved to "Draft it"), writes one draft of 40 to 180 words, runs the three self-checks from the guidelines, then hard checks in code (no dashes, no links, no SELLERLOGIC mention or DM invite, no invented experience). Pass goes to "Draft ready", fail to "Blocked" with the reasons.
    RD - Asana Sync, every 15 minutes: creates the tasks on Content | Reddit, reads your section moves and comments back, and writes one row per change to the "Lane log" tab.
    Subreddits: AmazonFBA, AmazonFBATips, amazonprivatelabel, AmazonSeller, Amazonsellercentral, amazonsellers, FulfillmentByAmazon.

Where things live
    Workflow files: shared GitLab repo management-claude-instructions, folder n8n/workflows/reddit/. They are generated by three scripts in that folder; a change is made there, tested, and uploaded to n8n from the file, never edited in n8n directly.
    n8n workflow ids: Discovery EQAN6qNTLJZHazSD, Drafter tn7Qf5LP6Zrw0Edv, Asana Sync fjoEl0cs03mrLRgR. Errors go to the "JTA: Error Handler" workflow and the n8n errors Slack channel.
    n8n credentials: Postgres, Gemini, Asana, the Google service account (writes the sheet), and "Reddit session (reading account)".
    Database tables: rd_posts (every post, its sorting, draft and your decision), rd_config (settings), rd_subreddits (the 7 communities), rd_run_log (one row per run), rd_account_comments (what the account said recently, for self-check 1).
    Board: Content | Reddit. Sheet: "Reddit Seeding / SL", only the "Lane log" tab is written.
    Model: gemini-3-flash-preview.

Settings (each one a single database change, through me)
Posts sorted per run 6, drafts per run 4, max post age 48 hours, who gets the tasks (you), the subreddit list.

When the reading cookie stops working
If Reddit refuses the test request, reply reading pauses: the lane carries on without replies and raises "[ACTION] Reddit cookie stopped working" to me. I renew the cookie in n8n; it never passes through chat, Slack or tasks. Until then, tasks say "replies not read", so read the thread before posting.

Known limits
    No written approval from Reddit for scheduled reading; going live without it was a management decision. The lane identifies itself as SELLERLOGIC's automation and reads about 7 pages an hour.
    Your posted text is not read back from Reddit, so self-check 1 learns from the draft, not from your edit.
    The "detail from the post" and "next step" checks are judged by AI, not by code.


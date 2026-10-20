# Що потрібно отримати

## 1. Оригінальний код із GitLab - пріоритет

Потрібне посилання або ZIP репозиторію management-claude-instructions.
Мінімальний набір:

- n8n/workflows/reddit/ цілком, з усіма workflow JSON.
- generators/build_discovery.py, build_drafter.py, build_asana_sync.py.
- generators/test_rd_code_nodes.js та тестові fixtures.
- Усі імпортовані prompts, бібліотеки, SQL, config і requirements/lock-файли.
- scripts/n8n_api.py та документація його конфігурації без секретів.
- Commit SHA / tag і дата версії, яка зараз розгорнута.

Шлях generators трактувати відносно оригінального reddit-каталогу за документацією; звірити в репозиторії.

## 2. Експорт із n8n

JSON трьох workflow (Discovery / Drafter / Asana Sync) і JTA: Error Handler.
Потрібні також n8n version, timezone, спосіб запуску/хостингу, потрібні community nodes та залежності.
Зберегти без секретів. JSON із UI корисний для звірки deployed/source, але source of truth - генератори.

## 3. База даних

DDL / migrations для п'яти rd_* таблиць: колонки, типи, індекси, constraints.
Санітизовані початкові rd_config і rd_subreddits.
Для повного перенесення історії - окремий захищений backup rd_posts, rd_run_log, rd_account_comments.
Назви таблиць у документації не замінюють їх схему.

## 4. Інфраструктура й доступи

Назва/URL n8n сервера, repo URL, інструкції отримання доступу та credential mapping у цільовому середовищі.
Ключі API, cookies, service account JSON і паролі не надсилати в чат; власник налаштовує їх через захищений credential store.

## 5. Додаткові матеріали

ОТРИМАНО: вкладення Reddit_parser_AL_v6_package.zip з задачі побудови. Оригінал збережено в inputs/asana/attachments/, розпаковано в inputs/legacy/. Це окремий Python/Flask-парсер, не комплект трьох n8n workflow. Деталі: ASANA-ATTACHMENT-FINDINGS.md.
Повний експорт вкладень Confluence/Asana не отримано.
За потреби оригінальні матеріали попереднього процесу можна додати окремо в inputs/legacy/ після перевірки на секрети.

## Короткий запит для власника системи

Please provide a sanitized ZIP or repository access for management-claude-instructions, including n8n/workflows/reddit/, its generators, prompts, tests and dependencies, plus scripts/n8n_api.py. Also needed: exported deployed JSON for the 3 RD workflows and JTA error handler, rd_* database schema/migrations and sanitized config seeds, deployed commit SHA, n8n version/timezone and setup instructions. No passwords, API keys, Reddit cookies or service account private keys.


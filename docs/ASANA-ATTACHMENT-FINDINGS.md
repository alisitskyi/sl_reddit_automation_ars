# Знайдене вкладення Asana

Перевірено: 19.10.2026.

## Отримано

- Файл: Reddit_parser_AL_v6_package.zip.
- Attachment ID: 1219257194868315.
- Джерело: https://app.asana.com/app/asana/-/get_asset?asset_id=1219257194868315
- Задача: https://app.asana.com/1/292294265665759/task/1218958869038776
- Контекст: коментар від 07.10.2026 про full non-API project documentation.
- Оригінальний ZIP: inputs/asana/attachments/Reddit_parser_AL_v6_package.zip.
- Розпакована копія: inputs/legacy/Reddit_parser_AL_v6_package/.

## Що всередині

- app/app.py: Python/Flask-застосунок Reddit Research Tool.
- app/requirements.txt, app/run.bat, app/README.md.
- console_scripts/extract_urls.py і reddit_posts_exporter_2.py.
- docs/Reddit_Parser_AL_EN.md та Reddit_Parser_AL_UA.md.
- Англійська й українська DOCX-версії документації; збережено без окремого аналізу вмісту DOCX.

## Значення для поточного проєкту

Це пакет окремого ручного парсера v6 з інтерфейсом localhost:5000. Він містить вихідний код і повні інструкції саме цього інструмента.

У переліку ZIP немає n8n workflow JSON, build_discovery.py, build_drafter.py, build_asana_sync.py, test_rd_code_nodes.js або міграцій rd_*.
Отже, пакет доповнює історію проєкту, але не замінює вихідні файли поточного Reddit Reply Lane, описаного в Confluence як три серверні n8n workflow.

Локальний запуск користувачем не планується. Файли лише збережено й прочитано; Python/BAT не виконувалися, залежності не встановлювалися.

## Перевірені місця

- У задачі побудови повернуто одне вкладення, наступної сторінки немає.
- У батьківській задачі Reddit Demand Generation вкладень не повернуто.
- На рівні проєкту Content | Reddit вкладень не повернуто.
- У прочитаних описах/коментарях задачі побудови й батьківської задачі немає прямого URL GitLab або окремих експортів n8n. Є назва management-claude-instructions і шлях n8n/workflows/reddit/.

Це висновок для перевірених об'єктів, а не для всіх задач Asana компанії.

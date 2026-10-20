# Початок роботи

1. Відкрий у VS Code папку C:\folder\JOB\VS_Code_AL\sl_reddit_sellerlogic_support через File > Open Folder.
2. Прочитай README.md і docs/PROJECT-STATUS.md.
3. Для ручного аналізу Reddit використовуй AGENTS.md, PDF у inputs/guidelines/ та templates/reddit-review.md. Результати зберігай у working/ або outputs/.
4. Для розгортання або відновлення на сервері використовуй docs/SERVER-DEPLOYMENT-GUIDE.md. Перелік потрібних оригіналів: docs/MISSING-FILES.md.
5. Після додавання нових джерел запиши походження та дату в references/SOURCES.md.
6. Перед завершенням сесії заповни короткий запис за templates/session-handoff.md у chats/codex/ або chats/claude/.

Перевірка збережених файлів у PowerShell з кореня проєкту:
```powershell
powershell -NoProfile -File .\scripts\Verify-Archive.ps1
```

Локальний запуск не планується. Ця папка зберігає матеріали та інструкції для роботи із серверною автоматизацією.
Для оновлення коду використовуй оригінальні генератори з GitLab; JSON workflow не редагуй вручну.


# Repairs Knowledge Base

Django web application for housing repairs advisors: look up procedures, questions to ask, Emergency / Urgent / Routine rules, and short resident guidance.

This sits beside the [Housing Repairs Diagnostic Tool](https://github.com/jomoz-dev/housing-repairs-diagnostic-tool). The diagnostic tool decides the job. This knowledge base explains **why** and **what to tell the resident**. Categories match the same six repair types.

It is a portfolio piece for Systems Officer, Application Support and Business Analyst roles, and a product that can be offered to private clients (housing teams, landlords, consultants) who need a lightweight procedure library without a full housing-management system.

---

## What this version does

- Sign-in (Django auth)
- Seven categories: call handling (who to send, gas, stopcock) plus the six repair types
- Advisor procedure and resident guidance for every repair type
- Articles tagged as advisor procedure or resident guidance
- Related priority: Emergency, Urgent, Routine, or depends on answers
- Search across title, summary and body
- Audience filter on search and category pages (all / advisor procedure / resident guidance)
- Django admin for adding and editing articles
- Document control: last reviewed date, reviewer, unpublished drafts, and a 12-month review-due flag for staff
- SQLite
- Seeded starter content and pytest coverage

This is **not** a case-management system. Cases and works orders belong in the later Housing Case Management project.

---

## Run locally

Python 3.9+. Django 4.2 LTS.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_knowledge
python manage.py runserver
```

Open http://127.0.0.1:8000/

| User | Password | Role |
| --- | --- | --- |
| `advisor` | `changeme` | Read procedures |
| `admin` | `changeme` | Django admin (`/admin/`) |

```bash
python -m pytest
```

---

## How it maps to advisor work

```text
Repair reported
      |
      v
Look up category / search the knowledge base
      |
      v
Ask the listed questions
      |
      v
Apply Emergency / Urgent / Routine
      |
      v
Log the job in the repairs application (or the diagnostic tool)
```

Content in this demo is operational guidance from housing repairs practice. It is not legal advice and is not a substitute for a landlord’s own policy.

---

## Project layout

| Path | Role |
| --- | --- |
| `config/` | Django project settings and URLs |
| `knowledge/` | Categories, articles, views, seed command |
| `templates/` | Advisor screens |
| `static/style.css` | Same navy housing-ICT look as the diagnostic tool |

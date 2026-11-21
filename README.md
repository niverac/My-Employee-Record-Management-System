# EMS Frontend Practice Template

A frontend-only starter based on your screenshot. It includes:
- `base.html` shared sidebar, top bar, and page layout (Jinja inheritance)
- `dashboard.html`, `employees.html`, `vacations.html`, `users.html`
- standalone `login.html`
- shared responsive CSS and small JavaScript for sidebar + table search

## Suggested Flask routes
The templates expect these endpoint names:
- `dashboard`
- `employees`
- `departments`
- `vacations`
- `users`
- `login`

Example route shape (adapt to your own app):
```python
@app.route("/")
def dashboard():
    return render_template(
        "dashboard.html",
        active_page="dashboard",
        on_vacation=[],
        total_employees=0,
        total_departments=0,
        vacation_count=0,
    )
```
For the other pages, pass `active_page` and the matching list (`employees`, `vacations`, or `users`). These templates intentionally contain no database code.

## Jinja notes
- Child pages use `{% extends "base.html" %}` and fill `{% block content %}`.
- Use `url_for('static', filename='css/style.css')` for static files.
- Replace sample field names with your SQLAlchemy model fields.
- Login uses a POST form with `username` and `password`; implement authentication and CSRF protection in your backend.
- Buttons marked `data-demo-action` are placeholders and currently show an alert.

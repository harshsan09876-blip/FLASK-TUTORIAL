# Flask CRUD — Quick Notes

**CRUD means Create, Read, Update, Delete.** `User` in `app.py` is the database model; `index.html` contains the forms and displays the users.

- **Create — POST `/`:** The Add User form sends `username` and `email`. Read them with `request.form.get(...)`, create a `User`, then `db.session.add()` and `db.session.commit()`.
- **Read — GET `/`:** `User.query.order_by(User.id).all()` fetches users. Pass them to the page with `render_template(..., users=users)`; Jinja displays them with `{% for user in users %}`.
- **Update — POST `/update/<user_id>`:** The URL supplies `user_id`; the form supplies `username` and `email`. Find the record, assign the changed fields, then `db.session.commit()`.
- **Delete — POST `/delete/<user_id>`:** The URL supplies the record ID. Find it, call `db.session.delete(user)`, then `db.session.commit()`.
- **Remember:** HTML `name="username"` and `name="email"` must match the keys used in `request.form`. These are form fields, not route parameters. `user_id` is a route parameter.
- The app calls `db.create_all()` when run directly, creating the database tables if they do not exist.

**Flow:** HTML form → Flask route → database session → redirect to `/` → updated user list.

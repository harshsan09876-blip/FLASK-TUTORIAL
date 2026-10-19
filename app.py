from datetime import datetime, timezone

from flask import Flask, abort, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    date_created = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


# CREATE (POST) and READ (GET)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # These keys match the HTML inputs' name="username" and name="email".
        # They are submitted form fields, not URL/route parameters.
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        if not username or not email:
            abort(400, description="Username and email are required.")

        new_user = User()
        new_user.username = username
        new_user.email = email
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("index"))

    users = User.query.order_by(User.id).all()
    return render_template("index.html", users=users)


# UPDATE: user_id comes from the URL; username/email come from the submitted form.
@app.route("/update/<int:user_id>", methods=["POST"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    # user_id comes from the URL; username and email come from the submitted form.
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    if not username or not email:
        abort(400, description="Username and email are required.")

    user.username = username
    user.email = email
    db.session.commit()
    return redirect(url_for("index"))


# DELETE: user_id comes from the URL.
@app.route("/delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

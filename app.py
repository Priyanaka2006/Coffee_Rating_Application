import os
import sqlite3
from pathlib import Path

from flask import Flask, current_app, g, jsonify, render_template


COFFEES = [
    {
        "id": "ethiopia",
        "name": "Daybreak",
        "origin": "Yirgacheffe, Ethiopia",
        "roast": "Light roast",
        "notes": "Jasmine · bergamot · peach",
        "image": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=1100&q=85",
        "alt": "Freshly brewed coffee in a ceramic cup",
    },
    {
        "id": "colombia",
        "name": "Soft Landing",
        "origin": "Huila, Colombia",
        "roast": "Medium roast",
        "notes": "Red apple · caramel · cocoa",
        "image": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=1100&q=85",
        "alt": "A cup of coffee on a wooden café table",
    },
    {
        "id": "brazil",
        "name": "Sunday Best",
        "origin": "Cerrado, Brazil",
        "roast": "Medium-dark roast",
        "notes": "Hazelnut · milk chocolate · fig",
        "image": "https://images.unsplash.com/photo-1511920170033-f8396924c348?auto=format&fit=crop&w=1100&q=85",
        "alt": "Latte art in a freshly poured coffee",
    },
    {
        "id": "kenya",
        "name": "Good Trouble",
        "origin": "Nyeri, Kenya",
        "roast": "Light-medium roast",
        "notes": "Blackcurrant · hibiscus · lime",
        "image": "https://images.unsplash.com/photo-1442512595331-e89e73853f31?auto=format&fit=crop&w=1100&q=85",
        "alt": "Coffee being poured at a café",
    },
]


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "coffee-ratings.sqlite"),
    )
    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    init_db(app)

    @app.teardown_appcontext
    def close_db(_error=None):
        database = g.pop("database", None)
        if database is not None:
            database.close()

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/coffees")
    def list_coffees():
        coffees = get_db().execute(
            "SELECT id, name, origin, roast, notes, image, alt, votes "
            "FROM coffees ORDER BY position"
        ).fetchall()
        return jsonify([dict(coffee) for coffee in coffees])

    @app.post("/api/coffees/<coffee_id>/vote")
    def vote_for_coffee(coffee_id):
        database = get_db()
        cursor = database.execute(
            "UPDATE coffees SET votes = votes + 1 WHERE id = ?", (coffee_id,)
        )
        if cursor.rowcount == 0:
            return jsonify({"error": "Coffee not found"}), 404
        database.commit()
        coffee = database.execute(
            "SELECT id, votes FROM coffees WHERE id = ?", (coffee_id,)
        ).fetchone()
        return jsonify(dict(coffee))

    return app


def get_db():
    if "database" not in g:
        g.database = sqlite3.connect(current_app.config["DATABASE"])
        g.database.row_factory = sqlite3.Row
    return g.database


def init_db(app):
    with app.app_context():
        database = get_db()
        database.execute(
            """CREATE TABLE IF NOT EXISTS coffees (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                origin TEXT NOT NULL,
                roast TEXT NOT NULL,
                notes TEXT NOT NULL,
                image TEXT NOT NULL,
                alt TEXT NOT NULL,
                votes INTEGER NOT NULL DEFAULT 0,
                position INTEGER NOT NULL
            )"""
        )
        database.executemany(
            """INSERT OR IGNORE INTO coffees
               (id, name, origin, roast, notes, image, alt, position)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                (
                    coffee["id"], coffee["name"], coffee["origin"],
                    coffee["roast"], coffee["notes"], coffee["image"],
                    coffee["alt"], position,
                )
                for position, coffee in enumerate(COFFEES)
            ],
        )
        database.commit()
        database.close()


app = create_app()


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
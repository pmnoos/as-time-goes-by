from sqlalchemy import inspect, text


def add_comment_columns(engine):
    """Add guest_name, guest_email and approved to the comments table if missing."""
    existing = {c["name"] for c in inspect(engine).get_columns("comments")}
    true_val = "1" if engine.dialect.name == "sqlite" else "TRUE"

    wanted = {
        "guest_name": "VARCHAR(60)",
        "guest_email": "VARCHAR(100)",
        "approved": f"BOOLEAN NOT NULL DEFAULT {true_val}",
    }

    with engine.begin() as conn:
        for name, ddl in wanted.items():
            if name not in existing:
                conn.execute(text(f"ALTER TABLE comments ADD COLUMN {name} {ddl}"))
                print(f"Added column: {name}")
            else:
                print(f"Already there: {name}")
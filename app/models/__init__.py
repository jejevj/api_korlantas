from ..extensions import db
from flask import current_app

def bind_table(table_name: str):
    """Return reflected Table for table_name, handling schema/case safely."""
    md = db.Model.metadata

    # exact hit (no schema key)
    if table_name in md.tables:
        return md.tables[table_name]

    # try with configured schema
    schema = (current_app.config.get("DB_SCHEMA") or "").strip()
    key = f"{schema}.{table_name}" if schema else table_name
    if key in md.tables:
        return md.tables[key]

    # case-insensitive search on last segment
    lname = table_name.lower()
    for k in md.tables.keys():
        last = k.split(".")[-1].strip('"')
        if last.lower() == lname:
            return md.tables[k]

    raise KeyError(f"Table '{table_name}' not found. Available: {list(md.tables.keys())}")

def register_models():
    # ONLY import user model
    from . import user  # noqa: F401

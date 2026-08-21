"""Database initialization entry point. Run `uv run alembic upgrade head` from backend."""
import subprocess
subprocess.run(["uv","run","alembic","upgrade","head"],check=True)

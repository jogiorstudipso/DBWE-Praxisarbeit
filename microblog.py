import sqlalchemy as sa
import sqlalchemy.orm as so

from app import create_app, db
from app.models import User, Project, TaskItem

app = create_app()


@app.shell_context_processor
def make_shell_context():
    # Praktische Standard-Imports für "flask shell".
    return {
        'sa': sa,
        'so': so,
        'db': db,
        'User': User,
        'Project': Project,
        'TaskItem': TaskItem
    }

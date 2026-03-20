from datetime import datetime, timezone, timedelta, date
from typing import Optional
import secrets

import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(
        sa.String(64), index=True, unique=True
    )
    email: so.Mapped[str] = so.mapped_column(
        sa.String(120), index=True, unique=True
    )
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256)) 
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    token: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(32), index=True, unique=True
    )
    token_expiration: so.Mapped[Optional[datetime]]

    projects = db.relationship(
        'Project',
        backref='owner',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def get_token(self, expires_in: int = 3600) -> str:
        now = datetime.now(timezone.utc)
        # Bestehendes Token wiederverwenden, solange es noch >60s gültig ist.
        if (
            self.token
            and self.token_expiration
            and self.token_expiration.replace(tzinfo=timezone.utc)
            > now + timedelta(seconds=60)
        ):
            return self.token

        self.token = secrets.token_hex(16)
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self) -> None:
        self.token_expiration = datetime.now(timezone.utc) - timedelta(seconds=1)

    @staticmethod
    def check_token(token: str):
        # Liefert nur Nutzer mit gültigem (nicht abgelaufenem) API-Token.
        user = db.session.scalar(sa.select(User).where(User.token == token))
        if user is None or user.token_expiration is None:
            return None

        if user.token_expiration.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            return None
        return user


@login.user_loader
def load_user(user_id):
    # Flask-Login lädt bei jeder Session den User über dessen ID.
    return db.session.get(User, int(user_id))


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        index=True,
        nullable=False
    )

    name = db.Column(db.String(140), nullable=False)
    archived = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    tasks = db.relationship(
        'TaskItem',
        backref='project',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def progress_percent(self) -> int:
        # Fortschritt = Anteil erledigter Tasks im Projekt.
        total = self.tasks.count()
        if total == 0:
            return 0
        done = self.tasks.filter_by(done=True).count()
        return int(round((done / total) * 100))

    def has_overdue(self) -> bool:
        # True, wenn mindestens eine offene Task überfällig ist.
        today = date.today()
        return self.tasks.filter(
            TaskItem.done.is_(False),
            TaskItem.due_date.isnot(None),
            TaskItem.due_date < today
        ).count() > 0


class TaskItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(
        db.Integer,
        db.ForeignKey('project.id'),
        index=True,
        nullable=False
    )

    title = db.Column(db.String(140), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    done = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    def is_overdue(self) -> bool:
        # Eine Task ist nur überfällig, wenn sie offen ist und ein altes Due-Date hat.
        return (
            not self.done
            and self.due_date is not None
            and self.due_date < date.today()
        )

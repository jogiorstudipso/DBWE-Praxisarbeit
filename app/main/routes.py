from datetime import datetime, timezone

from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_required

from app import db
from app.main import bp
from app.main.forms import ProjectForm, TaskForm
from app.models import Project, TaskItem


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        # Last-Seen wird bei jedem Request eines eingeloggten Users aktualisiert.
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    projects = (
        current_user.projects
        .filter_by(archived=False)
        .order_by(Project.created_at.desc())
        .all()
    )
    return render_template('index.html', title='Dashboard', projects=projects)


@bp.route('/projects/new', methods=['GET', 'POST'])
@login_required
def create_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data.strip(), owner=current_user)
        db.session.add(project)
        db.session.commit()
        flash('Projekt erstellt.')
        return redirect(url_for('main.index'))
    return render_template('project_form.html', title='Neues Projekt', form=form)


@bp.route('/projects/<int:project_id>', methods=['GET', 'POST'])
@login_required
def project_detail(project_id: int):
    # Zugriffsschutz: nur Projekte des aktuell eingeloggten Users laden.
    project = Project.query.filter_by(
        id=project_id,
        user_id=current_user.id
    ).first_or_404()

    form = TaskForm()
    if form.validate_on_submit():
        task = TaskItem(
            project=project,
            title=form.title.data.strip(),
            description=form.description.data.strip() if form.description.data else None,
            due_date=form.due_date.data,
            done=False
        )
        db.session.add(task)
        db.session.commit()
        flash('Task erstellt.')
        return redirect(url_for('main.project_detail', project_id=project.id))

    tasks = project.tasks.order_by(TaskItem.created_at.desc()).all()
    return render_template(
        'project_detail.html',
        title=project.name,
        project=project,
        tasks=tasks,
        form=form
    )


@bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
@login_required
def toggle_task(task_id: int):
    # Join auf Project stellt sicher, dass nur eigene Tasks geändert werden.
    task = (
        TaskItem.query
        .join(Project)
        .filter(TaskItem.id == task_id, Project.user_id == current_user.id)
        .first_or_404()
    )

    task.done = not task.done
    if task.done:
        # Zeitstempel nur setzen, wenn tatsächlich als erledigt markiert.
        task.completed_at = datetime.now(timezone.utc)
    else:
        task.completed_at = None

    db.session.commit()
    return redirect(url_for('main.project_detail', project_id=task.project_id))


@bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id: int):
    task = (
        TaskItem.query
        .join(Project)
        .filter(TaskItem.id == task_id, Project.user_id == current_user.id)
        .first_or_404()
    )

    project_id = task.project_id
    db.session.delete(task)
    db.session.commit()
    flash('Task gelöscht.')
    return redirect(url_for('main.project_detail', project_id=project_id))

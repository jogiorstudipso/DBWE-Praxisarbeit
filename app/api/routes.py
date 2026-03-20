from datetime import datetime
from flask import jsonify, request

from app import db
from app.api import bp
from app.api.auth import token_auth
from app.models import Project, TaskItem


@bp.route('/projects', methods=['GET'])
@token_auth.login_required
def get_projects():
    user = token_auth.current_user()

    projects = (Project.query
                .filter_by(user_id=user.id, archived=False)
                .order_by(Project.created_at.desc())
                .all())

    data = []
    for project in projects:
        # API liefert nur berechnete Werte, keine interne ORM-Logik.
        data.append({
            'id': project.id,
            'name': project.name,
            'archived': project.archived,
            'created_at': project.created_at.isoformat() if project.created_at else None,
            'progress_percent': project.progress_percent(),
            'has_overdue': project.has_overdue()
        })

    return jsonify(data)


@bp.route('/projects', methods=['POST'])
@token_auth.login_required
def create_project_api():
    user = token_auth.current_user()
    data = request.get_json() or {}

    name = (data.get('name') or '').strip()
    if not name:
        return jsonify({'error': 'Projektname ist erforderlich.'}), 400

    project = Project(name=name, owner=user)
    db.session.add(project)
    db.session.commit()

    return jsonify({
        'id': project.id,
        'name': project.name,
        'archived': project.archived,
        'created_at': project.created_at.isoformat() if project.created_at else None
    }), 201


@bp.route('/projects/<int:project_id>/tasks', methods=['GET'])
@token_auth.login_required
def get_project_tasks(project_id):
    user = token_auth.current_user()

    project = (Project.query
               .filter_by(id=project_id, user_id=user.id)
               .first_or_404())

    tasks = project.tasks.order_by(TaskItem.created_at.desc()).all()

    data = []
    for task in tasks:
        data.append({
            'id': task.id,
            'project_id': task.project_id,
            'title': task.title,
            'description': task.description,
            'due_date': task.due_date.isoformat() if task.due_date else None,
            'done': task.done,
            'completed_at': task.completed_at.isoformat() if task.completed_at else None,
            'created_at': task.created_at.isoformat() if task.created_at else None,
            'is_overdue': task.is_overdue()
        })

    return jsonify({
        'project': {
            'id': project.id,
            'name': project.name,
            'progress_percent': project.progress_percent(),
            'has_overdue': project.has_overdue()
        },
        'tasks': data
    })


@bp.route('/projects/<int:project_id>/tasks', methods=['POST'])
@token_auth.login_required
def create_task_api(project_id):
    user = token_auth.current_user()

    project = (Project.query
               .filter_by(id=project_id, user_id=user.id)
               .first_or_404())

    data = request.get_json() or {}

    title = (data.get('title') or '').strip()
    description = (data.get('description') or '').strip() or None
    due_date_raw = data.get('due_date')

    if not title:
        return jsonify({'error': 'Task-Titel ist erforderlich.'}), 400

    due_date = None
    if due_date_raw:
        try:
            # Erwartetes Datumsformat für die API: ISO-ähnlich YYYY-MM-DD.
            due_date = datetime.strptime(due_date_raw, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'due_date muss im Format YYYY-MM-DD sein.'}), 400

    task = TaskItem(
        project=project,
        title=title,
        description=description,
        due_date=due_date,
        done=False
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({
        'id': task.id,
        'project_id': task.project_id,
        'title': task.title,
        'description': task.description,
        'due_date': task.due_date.isoformat() if task.due_date else None,
        'done': task.done,
        'created_at': task.created_at.isoformat() if task.created_at else None
    }), 201

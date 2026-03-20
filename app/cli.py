"""Custom Flask-CLI Kommandos fuer Uebersetzungen (Babel)."""

import os
from flask import Blueprint
import click

bp = Blueprint('cli', __name__, cli_group=None)


@bp.cli.group()
def translate():
    """Translation and localization commands."""
    pass


@translate.command()
@click.argument('lang')
def init(lang):
    """Initialize a new language."""
    # Extrahiert Übersetzungsstrings und erstellt ein neues Sprachverzeichnis.
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system(
            'pybabel init -i messages.pot -d app/translations -l ' + lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')


@translate.command()
def update():
    """Update all languages."""
    # Aktualisiert bestehende Sprachdateien anhand neuer/geaenderter Strings.
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel update -i messages.pot -d app/translations'):
        raise RuntimeError('update command failed')
    os.remove('messages.pot')


@translate.command()
def compile():
    """Compile all languages."""
    # Uebersetzt .po Dateien in auslieferbare .mo Dateien.
    if os.system('pybabel compile -d app/translations'):
        raise RuntimeError('compile command failed')

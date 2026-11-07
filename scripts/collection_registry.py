"""Shared publication contract for source, route, and coverage checks (stdlib)."""
import json
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
CONTENT = PROJECT / 'content'
LANGUAGES = ('en', 'zh', 'fr', 'ja', 'de', 'ru', 'ar', 'es')
COLLECTIONS = json.loads((PROJECT / 'data/collections.json').read_text())
SECTIONS = tuple(COLLECTIONS)
COMPONENTS = tuple(key for key, value in COLLECTIONS.items() if value.get('kind') != 'navigation')
COMPONENT_LANGUAGES = {key: tuple(value['languages']) for key, value in COLLECTIONS.items()}


def language_of(path):
    return next((lang for lang in LANGUAGES[1:] if path.name.endswith('.' + lang + '.md')), 'en')


def english_path(path):
    lang = language_of(path)
    return path if lang == 'en' else path.with_name(path.name.removesuffix('.' + lang + '.md') + '.md')


def source_route(path, language=None):
    lang = language or language_of(path)
    relative = english_path(path).relative_to(CONTENT)
    stem = relative.stem
    route = relative.parent if stem in ('index', '_index') else relative.with_name(stem)
    return ('' if lang == 'en' else '/' + lang) + '/' + route.as_posix().lower().strip('/') + '/'


def paired(path):
    parts = path.relative_to(CONTENT).parts
    return len(parts) < 2 or COLLECTIONS[parts[0]].get('paired', True)

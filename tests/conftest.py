# tests/conftest.py
import sys, os

# Добавляем корень проекта в sys.path, чтобы pytest мог импортировать domain, repository, services и т. д.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

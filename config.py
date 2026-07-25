"""
Configuration globale de TaskFlow Pro.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()

# Dossiers
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = BASE_DIR / "uploads"
EXPORTS_DIR = BASE_DIR / "exports"
TEMPLATES_DIR = BASE_DIR / "templates"
LOGS_DIR = BASE_DIR / "logs"
ASSETS_DIR = BASE_DIR / "assets"
CSS_DIR = BASE_DIR / "css"

for d in [DATA_DIR, UPLOADS_DIR, EXPORTS_DIR, TEMPLATES_DIR, LOGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Base de données
DB_PATH = DATA_DIR / "taskflow.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Application
APP_NAME = "TaskFlow Pro"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Gestion de projets et tâches - Usage personnel"
APP_AUTHOR = "TaskFlow"

# Thèmes
THEMES = {
    "light": {
        "bg": "#ffffff",
        "surface": "#f8f9fa",
        "primary": "#6366f1",
        "secondary": "#8b5cf6",
        "accent": "#06b6d4",
        "success": "#22c55e",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "info": "#3b82f6",
        "text": "#1f2937",
        "text_muted": "#6b7280",
        "border": "#e5e7eb",
        "card_shadow": "0 4px 6px -1px rgba(0,0,0,0.1)",
    },
    "dark": {
        "bg": "#0f172a",
        "surface": "#1e293b",
        "primary": "#818cf8",
        "secondary": "#a78bfa",
        "accent": "#22d3ee",
        "success": "#4ade80",
        "warning": "#fbbf24",
        "danger": "#f87171",
        "info": "#60a5fa",
        "text": "#f1f5f9",
        "text_muted": "#94a3b8",
        "border": "#334155",
        "card_shadow": "0 4px 6px -1px rgba(0,0,0,0.3)",
    }
}

# Statuts de projet
PROJECT_STATUSES = [
    ("draft", "Brouillon", "#9ca3af"),
    ("planned", "Planifié", "#3b82f6"),
    ("active", "Actif", "#22c55e"),
    ("on_hold", "En attente", "#f59e0b"),
    ("blocked", "Bloqué", "#ef4444"),
    ("in_review", "En revue", "#8b5cf6"),
    ("validated", "Validé", "#06b6d4"),
    ("completed", "Terminé", "#10b981"),
    ("cancelled", "Annulé", "#6b7280"),
    ("archived", "Archivé", "#4b5563"),
]

# Statuts de tâche
TASK_STATUSES = [
    ("backlog", "Backlog", "#6b7280"),
    ("todo", "À faire", "#3b82f6"),
    ("waiting", "En attente", "#f59e0b"),
    ("in_progress", "En cours", "#8b5cf6"),
    ("blocked", "Bloqué", "#ef4444"),
    ("in_review", "En revue", "#06b6d4"),
    ("validated", "Validé", "#10b981"),
    ("done", "Terminé", "#22c55e"),
    ("cancelled", "Annulé", "#9ca3af"),
]

# Priorités
PRIORITIES = [
    ("urgent", "Urgent", "#dc2626", 5),
    ("very_high", "Très haute", "#ea580c", 4),
    ("high", "Haute", "#f59e0b", 3),
    ("normal", "Normale", "#3b82f6", 2),
    ("low", "Basse", "#6b7280", 1),
    ("very_low", "Très basse", "#9ca3af", 0),
]

# Complexités
COMPLEXITIES = [
    ("trivial", "Trivial", "#22c55e"),
    ("easy", "Facile", "#4ade80"),
    ("medium", "Moyen", "#f59e0b"),
    ("hard", "Difficile", "#f97316"),
    ("complex", "Complexe", "#ef4444"),
]

# Couleurs de projet
PROJECT_COLORS = [
    "#ef4444", "#f97316", "#f59e0b", "#84cc16", "#22c55e",
    "#10b981", "#06b6d4", "#3b82f6", "#6366f1", "#8b5cf6",
    "#a855f7", "#d946ef", "#ec4899", "#f43f5e", "#78716c",
]

# Icônes de projet
PROJECT_ICONS = [
    "📁", "🚀", "💡", "🔬", "📊", "🤖", "💻", "🎨",
    "📱", "🌐", "⚙️", "🔧", "📈", "🎯", "🏆", "📚",
]

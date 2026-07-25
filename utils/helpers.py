"""
Utilitaires globaux pour TaskFlow Pro.
"""
import datetime
from typing import Optional, List, Any
import random


def format_date(date_obj) -> str:
    """Formate une date en français."""
    if date_obj is None:
        return "—"
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.datetime.strptime(date_obj, "%Y-%m-%d").date()
        except:
            return date_obj
    return date_obj.strftime("%d/%m/%Y")


def format_datetime(dt_obj) -> str:
    """Formate un datetime en français."""
    if dt_obj is None:
        return "—"
    return dt_obj.strftime("%d/%m/%Y %H:%M")


def format_duration(hours: float) -> str:
    """Formate une durée en heures/minutes."""
    if hours is None:
        return "0h"
    h = int(hours)
    m = int((hours - h) * 60)
    if m > 0:
        return f"{h}h {m}m"
    return f"{h}h"


def format_currency(amount) -> str:
    """Formate un montant en euros."""
    if amount is None:
        return "0,00 €"
    return f"{float(amount):,.2f} €".replace(",", " ").replace(".", ",")


def days_until(date_obj) -> int:
    """Nombre de jours jusqu'à une date."""
    if date_obj is None:
        return None
    if isinstance(date_obj, str):
        date_obj = datetime.datetime.strptime(date_obj, "%Y-%m-%d").date()
    delta = date_obj - datetime.date.today()
    return delta.days


def priority_color(priority: str) -> str:
    """Couleur associée à une priorité."""
    colors = {
        "urgent": "#dc2626",
        "very_high": "#ea580c",
        "high": "#f59e0b",
        "normal": "#3b82f6",
        "low": "#6b7280",
        "very_low": "#9ca3af",
    }
    return colors.get(priority, "#6b7280")


def status_color(status: str) -> str:
    """Couleur associée à un statut."""
    colors = {
        "backlog": "#6b7280",
        "todo": "#3b82f6",
        "waiting": "#f59e0b",
        "in_progress": "#8b5cf6",
        "blocked": "#ef4444",
        "in_review": "#06b6d4",
        "validated": "#10b981",
        "done": "#22c55e",
        "cancelled": "#9ca3af",
        "draft": "#9ca3af",
        "planned": "#3b82f6",
        "active": "#22c55e",
        "on_hold": "#f59e0b",
        "completed": "#10b981",
        "archived": "#4b5563",
    }
    return colors.get(status, "#6b7280")


def status_label(status: str) -> str:
    """Label français d'un statut."""
    labels = {
        "backlog": "Backlog", "todo": "À faire", "waiting": "En attente",
        "in_progress": "En cours", "blocked": "Bloqué", "in_review": "En revue",
        "validated": "Validé", "done": "Terminé", "cancelled": "Annulé",
        "draft": "Brouillon", "planned": "Planifié", "active": "Actif",
        "on_hold": "En attente", "completed": "Terminé", "archived": "Archivé",
    }
    return labels.get(status, status)


def priority_label(priority: str) -> str:
    """Label français d'une priorité."""
    labels = {
        "urgent": "Urgent", "very_high": "Très haute", "high": "Haute",
        "normal": "Normale", "low": "Basse", "very_low": "Très basse",
    }
    return labels.get(priority, priority)


def generate_code(prefix: str = "PRJ") -> str:
    """Génère un code unique."""
    now = datetime.datetime.now()
    return f"{prefix}-{now.year}-{now.month:02d}-{random.randint(1000, 9999)}"


def truncate_text(text: str, max_len: int = 50) -> str:
    """Tronque un texte."""
    if not text:
        return ""
    if len(text) > max_len:
        return text[:max_len] + "…"
    return text


def compute_progress(done: int, total: int) -> float:
    """Calcule un pourcentage."""
    if total == 0:
        return 0.0
    return round((done / total) * 100, 1)

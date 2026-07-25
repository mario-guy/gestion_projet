"""
Service de statistiques et KPI.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, date, timedelta
from models import Project, Task, TimeTracking, Objective, Risk


class StatsService:
    """Service de calcul des statistiques."""

    def __init__(self, db: Session):
        self.db = db

    def get_dashboard_stats(self) -> dict:
        """Statistiques pour le tableau de bord."""
        total_projects = self.db.query(Project).count()
        active_projects = self.db.query(Project).filter(
            Project.status.in_(["active", "in_review", "validated"])
        ).count()

        total_tasks = self.db.query(Task).count()
        done_tasks = self.db.query(Task).filter(Task.status == "done").count()
        in_progress_tasks = self.db.query(Task).filter(Task.status == "in_progress").count()
        blocked_tasks = self.db.query(Task).filter(Task.status == "blocked").count()

        today = date.today()
        overdue_tasks = self.db.query(Task).filter(
            and_(Task.deadline < today, Task.status != "done")
        ).count()

        # Temps total travaillé
        time_result = self.db.query(func.sum(TimeTracking.duration_minutes)).scalar()
        total_minutes = time_result or 0
        total_hours = round(total_minutes / 60, 1)

        # Progression globale
        progress_result = self.db.query(func.avg(Project.progress)).scalar()
        global_progress = round(float(progress_result or 0), 1)

        # Objectifs
        total_objectives = self.db.query(Objective).count()
        achieved_objectives = self.db.query(Objective).filter(Objective.status == "done").count()

        # Risques
        total_risks = self.db.query(Risk).count()
        active_risks = self.db.query(Risk).filter(Risk.status == "identified").count()

        return {
            "total_projects": total_projects,
            "active_projects": active_projects,
            "total_tasks": total_tasks,
            "done_tasks": done_tasks,
            "in_progress_tasks": in_progress_tasks,
            "blocked_tasks": blocked_tasks,
            "overdue_tasks": overdue_tasks,
            "total_hours": total_hours,
            "global_progress": global_progress,
            "total_objectives": total_objectives,
            "achieved_objectives": achieved_objectives,
            "total_risks": total_risks,
            "active_risks": active_risks,
        }

    def get_tasks_by_status(self) -> dict:
        """Répartition des tâches par statut."""
        from collections import Counter
        tasks = self.db.query(Task.status).all()
        statuses = [t[0] for t in tasks]
        return dict(Counter(statuses))

    def get_tasks_by_priority(self) -> dict:
        """Répartition des tâches par priorité."""
        from collections import Counter
        tasks = self.db.query(Task.priority).all()
        priorities = [t[0] for t in tasks]
        return dict(Counter(priorities))

    def get_weekly_activity(self, weeks: int = 8) -> dict:
        """Activité hebdomadaire."""
        labels = []
        values = []
        for i in range(weeks - 1, -1, -1):
            week_start = date.today() - timedelta(days=date.today().weekday() + i * 7)
            week_end = week_start + timedelta(days=6)
            labels.append(week_start.strftime("%d/%m"))
            count = self.db.query(Task).filter(
                func.date(Task.created_at) >= week_start,
                func.date(Task.created_at) <= week_end
            ).count()
            values.append(count)
        return {"labels": labels, "values": values}

    def get_burndown_data(self, project_id: int = None) -> dict:
        """Données pour le burndown chart."""
        query = self.db.query(Task)
        if project_id:
            query = query.filter(Task.project_id == project_id)

        total = query.count()
        done = query.filter(Task.status == "done").count()
        remaining = total - done

        return {
            "total": total,
            "done": done,
            "remaining": remaining,
        }

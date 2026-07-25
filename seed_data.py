"""
Données de démonstration pour TaskFlow Pro.
"""
from models import init_db, get_db, Project, Task, SubTask, Objective, Risk, DailyNote, Idea, Meeting, TimeTracking, Tag, Category, Notification
from services.crud import CRUDService
from datetime import date, datetime, timedelta
import random

init_db()
db = get_db()

project_svc = CRUDService(Project)
task_svc = CRUDService(Task)
subtask_svc = CRUDService(SubTask)
obj_svc = CRUDService(Objective)
risk_svc = CRUDService(Risk)
note_svc = CRUDService(DailyNote)
idea_svc = CRUDService(Idea)
meeting_svc = CRUDService(Meeting)
time_svc = CRUDService(TimeTracking)
tag_svc = CRUDService(Tag)
cat_svc = CRUDService(Category)
notif_svc = CRUDService(Notification)

# Catégories
categories = ["Développement", "Data Science", "IA", "Power BI", "Recherche", "Management", "Personnel"]
for c in categories:
    cat_svc.create(db, name=c, color=random.choice(["#6366f1", "#8b5cf6", "#22c55e", "#f59e0b", "#ef4444", "#06b6d4"]))

# Tags
tags = ["Urgent", "Important", "Bug", "Feature", "Documentation", "Review", "Client", "Interne"]
for t in tags:
    tag_svc.create(db, name=t, color=random.choice(["#6366f1", "#8b5cf6", "#22c55e", "#f59e0b", "#ef4444"]))

# Projets de démo
demo_projects = [
    {"name": "Plateforme ML - Prédiction churn", "code": "ML-2024-001",
     "description": "Développement d'un modèle de machine learning pour prédire le churn client.",
     "client": "Banque Nationale", "company": "DataConsulting", "department": "Data Science",
     "start_date": date(2024, 1, 15), "end_date": date(2024, 6, 30),
     "status": "active", "priority": "high", "complexity": "complex",
     "budget": 150000, "cost": 45000, "progress": 35, "color": "#6366f1", "logo": "🤖"},
    {"name": "Dashboard Power BI - Ventes", "code": "PBI-2024-002",
     "description": "Création d'un tableau de bord interactif pour le suivi des ventes.",
     "client": "RetailPlus", "company": "DataConsulting", "department": "BI",
     "start_date": date(2024, 2, 1), "end_date": date(2024, 4, 15),
     "status": "in_review", "priority": "very_high", "complexity": "medium",
     "budget": 45000, "cost": 38000, "progress": 85, "color": "#f59e0b", "logo": "📊"},
    {"name": "Recherche - LLM interne", "code": "R&D-2024-003",
     "description": "Étude de faisabilité pour un LLM interne sécurisé.",
     "client": "Interne", "company": "DataConsulting", "department": "R&D",
     "start_date": date(2024, 3, 1), "end_date": date(2024, 9, 30),
     "status": "active", "priority": "normal", "complexity": "hard",
     "budget": 80000, "cost": 12000, "progress": 15, "color": "#22c55e", "logo": "🔬"},
    {"name": "Site web portfolio", "code": "WEB-2024-004",
     "description": "Refonte du site web personnel avec Next.js et Tailwind.",
     "client": "Personnel", "company": "Freelance", "department": "Dev",
     "start_date": date(2024, 1, 1), "end_date": date(2024, 3, 31),
     "status": "completed", "priority": "low", "complexity": "easy",
     "budget": 0, "cost": 0, "progress": 100, "color": "#ec4899", "logo": "💻"},
]

project_objects = []
for p in demo_projects:
    obj = project_svc.create(db, **p)
    project_objects.append(obj)

# Tâches de démo
task_data = [
    {"title": "Collecte et nettoyage des données", "project_id": 1, "priority": "high", "status": "done",
     "deadline": date(2024, 2, 15), "estimated_duration": 40, "actual_hours": 42, "progress": 100,
     "difficulty": "medium", "category": "Data Science"},
    {"title": "Analyse exploratoire (EDA)", "project_id": 1, "priority": "high", "status": "done",
     "deadline": date(2024, 3, 1), "estimated_duration": 24, "actual_hours": 28, "progress": 100,
     "difficulty": "medium", "category": "Data Science"},
    {"title": "Feature engineering", "project_id": 1, "priority": "very_high", "status": "in_progress",
     "deadline": date(2024, 4, 15), "estimated_duration": 32, "actual_hours": 12, "progress": 38,
     "difficulty": "hard", "category": "Data Science"},
    {"title": "Entraînement modèle XGBoost", "project_id": 1, "priority": "urgent", "status": "in_progress",
     "deadline": date(2024, 5, 1), "estimated_duration": 48, "actual_hours": 8, "progress": 17,
     "difficulty": "complex", "category": "IA"},
    {"title": "Modèle de prédiction - Phase 1", "project_id": 2, "priority": "high", "status": "done",
     "deadline": date(2024, 2, 28), "estimated_duration": 60, "actual_hours": 55, "progress": 100,
     "difficulty": "medium", "category": "Power BI"},
    {"title": "Création mesures DAX", "project_id": 2, "priority": "high", "status": "done",
     "deadline": date(2024, 3, 15), "estimated_duration": 20, "actual_hours": 18, "progress": 100,
     "difficulty": "easy", "category": "Power BI"},
    {"title": "Design rapport final", "project_id": 2, "priority": "very_high", "status": "in_review",
     "deadline": date(2024, 4, 1), "estimated_duration": 16, "actual_hours": 14, "progress": 88,
     "difficulty": "easy", "category": "Design"},
    {"title": "Benchmark modèles LLM open source", "project_id": 3, "priority": "normal", "status": "todo",
     "deadline": date(2024, 4, 30), "estimated_duration": 80, "actual_hours": 0, "progress": 0,
     "difficulty": "hard", "category": "IA"},
    {"title": "Évaluation sécurité et conformité", "project_id": 3, "priority": "high", "status": "backlog",
     "deadline": date(2024, 5, 15), "estimated_duration": 40, "actual_hours": 0, "progress": 0,
     "difficulty": "complex", "category": "Recherche"},
]

for t in task_data:
    task_svc.create(db, **t)

# Sous-tâches
subtask_data = [
    {"task_id": 1, "title": "Importer CSV clients", "is_done": True, "position": 1},
    {"task_id": 1, "title": "Gérer valeurs manquantes", "is_done": True, "position": 2},
    {"task_id": 1, "title": "Normaliser features", "is_done": True, "position": 3},
    {"task_id": 3, "title": "Créer features temporelles", "is_done": True, "position": 1},
    {"task_id": 3, "title": "Encoder variables catégorielles", "is_done": False, "position": 2},
    {"task_id": 3, "title": "Feature selection (SHAP)", "is_done": False, "position": 3},
]

for s in subtask_data:
    subtask_svc.create(db, **s)

# Objectifs
objectives = [
    {"title": "Obtenir la certification AWS ML", "description": "Passer l'examen AWS Certified Machine Learning Specialty",
     "target_date": date(2024, 6, 30), "progress": 45, "status": "in_progress"},
    {"title": "Publier 3 articles de blog technique", "description": "Articles sur MLOps, LLMs et Power BI",
     "target_date": date(2024, 12, 31), "progress": 33, "status": "in_progress"},
    {"title": "Contribuer à un projet open source", "description": "Pull request acceptée sur scikit-learn ou pandas",
     "target_date": date(2024, 9, 30), "progress": 10, "status": "todo"},
]

for o in objectives:
    obj_svc.create(db, **o)

# Risques
risks = [
    {"title": "Données clients insuffisantes", "description": "Le jeu de données ne couvre que 18 mois",
     "probability": 70, "impact": 60, "criticality": 42, "status": "monitoring"},
    {"title": "Délais livraison Power BI", "description": "Le client demande des modifications fréquentes",
     "probability": 50, "impact": 80, "criticality": 40, "status": "identified"},
    {"title": "Complexité LLM interne sous-estimée", "description": "Les besoins en calcul GPU dépassent le budget",
     "probability": 40, "impact": 90, "criticality": 36, "status": "identified"},
]

for r in risks:
    risk_svc.create(db, **r)

# Notes quotidiennes
for i in range(7):
    d = date.today() - timedelta(days=i)
    moods = ["😞", "😐", "🙂", "😊", "🤩"]
    note_svc.create(db, note_date=d, content=f"Journée productive. Avancé sur les projets en cours. {random.choice(['Réunion client', 'Coding session', 'Analyse données', 'Rédaction doc'])}.", mood=random.choice(moods))

# Idées
ideas = [
    {"title": "AutoML interne", "description": "Créer un pipeline AutoML pour les projets récurrents", "category": "IA", "priority": "high"},
    {"title": "Chatbot documentation", "description": "Bot RAG pour interroger la documentation technique", "category": "IA", "priority": "very_high"},
    {"title": "Template rapports automatisés", "description": "Générer rapports PDF à partir des résultats ML", "category": "Productivité", "priority": "normal"},
]

for idea in ideas:
    idea_svc.create(db, **idea)

# Réunions
meetings = [
    {"title": "Sprint Review - ML Churn", "start_time": datetime(2024, 3, 15, 10, 0), "end_time": datetime(2024, 3, 15, 11, 30), "location": "Teams"},
    {"title": "Workshop Power BI", "start_time": datetime(2024, 3, 20, 14, 0), "end_time": datetime(2024, 3, 20, 16, 0), "location": "Salle A"},
]

for m in meetings:
    meeting_svc.create(db, **m)

# Time tracking
for i in range(20):
    task_id = random.randint(1, 7)
    start = datetime(2024, 3, random.randint(1, 20), random.randint(8, 17), 0)
    duration = random.choice([30, 60, 90, 120, 180])
    end = start + timedelta(minutes=duration)
    time_svc.create(db, task_id=task_id, start_time=start, end_time=end, duration_minutes=duration,
                   description=f"Travail sur tâche {task_id}")

# Notifications
notif_svc.create(db, type="deadline", title="Deadline approche", message="La tâche Feature engineering arrive à échéance", is_read=False)
notif_svc.create(db, type="daily_reminder", title="Rappel quotidien", message="N'oubliez pas de mettre à jour vos tâches", is_read=False)

print("✅ Données de démonstration créées avec succès !")
print(f"   - {len(demo_projects)} projets")
print(f"   - {len(task_data)} tâches")
print(f"   - {len(subtask_data)} sous-tâches")
print(f"   - {len(objectives)} objectifs")
print(f"   - {len(risks)} risques")
print(f"   - {len(ideas)} idées")
print(f"   - 7 notes quotidiennes")
print(f"   - {len(meetings)} réunions")
print(f"   - 20 entrées temps")

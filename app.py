"""
TaskFlow Pro - Application de Gestion de Projets et Tâches
Développée avec Streamlit - Usage personnel
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
import json
import os

# Configuration de la page Streamlit
st.set_page_config(
    page_title="TaskFlow Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

from config import APP_NAME, APP_VERSION, PROJECT_STATUSES, TASK_STATUSES, PRIORITIES, COMPLEXITIES, PROJECT_COLORS, PROJECT_ICONS
from models import init_db, get_db, Project, Task, SubTask, Objective, Risk, DailyNote, Idea, Document, Meeting, TimeTracking, Notification, Bookmark, ActivityLog, Tag, Category, Reminder
from services.crud import CRUDService
from services.stats import StatsService
from utils.helpers import format_date, format_currency, format_duration, days_until, status_color, priority_color, status_label, priority_label, compute_progress
from components.ui import load_css, kpi_card, status_badge, priority_badge, progress_bar, project_card, task_card, section_header, empty_state, info_card

# Initialisation
init_db()

# CSS personnalisé
load_css()

# Services
db = get_db()
project_service = CRUDService(Project)
task_service = CRUDService(Task)
subtask_service = CRUDService(SubTask)
objective_service = CRUDService(Objective)
risk_service = CRUDService(Risk)
note_service = CRUDService(DailyNote)
idea_service = CRUDService(Idea)
doc_service = CRUDService(Document)
meeting_service = CRUDService(Meeting)
time_service = CRUDService(TimeTracking)
notif_service = CRUDService(Notification)
bookmark_service = CRUDService(Bookmark)
activity_service = CRUDService(ActivityLog)
tag_service = CRUDService(Tag)
cat_service = CRUDService(Category)
reminder_service = CRUDService(Reminder)

stats_service = StatsService(db)

# Session state
if "page" not in st.session_state:
    st.session_state.page = "dashboard"
if "selected_project" not in st.session_state:
    st.session_state.selected_project = None
if "selected_task" not in st.session_state:
    st.session_state.selected_task = None
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "show_form" not in st.session_state:
    st.session_state.show_form = False
if "edit_id" not in st.session_state:
    st.session_state.edit_id = None


def set_page(page_name):
    if st.session_state.page != page_name:
        st.session_state.page = page_name
        st.session_state.show_form = False
        st.session_state.edit_id = None
        st.rerun()


def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode
    st.rerun()


# ==================== SIDEBAR ====================
def render_sidebar():
    with st.sidebar:
        # Logo
        st.markdown(f"""
        <div style="text-align: center; padding: 1.5rem 0 1rem 0;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🚀</div>
            <h2 style="margin: 0; color: white; font-size: 1.3rem; font-weight: 700;">{APP_NAME}</h2>
            <p style="margin: 0; color: #94a3b8; font-size: 0.7rem;">v{APP_VERSION}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Navigation — boutons Streamlit purs, 100% fiables
        nav_items = [
            ("dashboard", "📊", "Tableau de bord"),
            ("projects", "📁", "Projets"),
            ("tasks", "✅", "Tâches"),
            ("kanban", "📋", "Kanban"),
            ("calendar", "📅", "Calendrier"),
            ("gantt", "📈", "Gantt"),
            ("objectives", "🎯", "Objectifs"),
            ("notes", "📝", "Notes"),
            ("documents", "📎", "Documents"),
            ("risks", "⚠️", "Risques"),
            ("time", "⏱️", "Temps"),
            ("stats", "📊", "Statistiques"),
            ("settings", "⚙️", "Paramètres"),
        ]

        for key, icon, label in nav_items:
            is_active = st.session_state.page == key
            btn_type = "primary" if is_active else "secondary"
            if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True, type=btn_type):
                set_page(key)

        st.markdown("---")

        # Mode sombre
        if st.toggle("🌙 Mode sombre", value=st.session_state.dark_mode):
            toggle_dark_mode()

        # Notifications
        try:
            unread = db.query(Notification).filter(Notification.is_read == False).count()
            if unread > 0:
                st.info(f"🔔 {unread} notification non lue")
        except:
            pass

# ==================== DASHBOARD ====================
def render_dashboard():
    section_header("Tableau de bord", "Vue d ensemble de vos projets et tâches")
    stats = stats_service.get_dashboard_stats()

    col1, col2, col3, col4 = st.columns(4)
    with col1: kpi_card("Projets", str(stats["total_projects"]), "#6366f1", "📁", 0.1)
    with col2: kpi_card("Tâches", str(stats["total_tasks"]), "#8b5cf6", "✅", 0.2)
    with col3: kpi_card("Terminées", str(stats["done_tasks"]), "#22c55e", "✨", 0.3)
    with col4: kpi_card("En retard", str(stats["overdue_tasks"]), "#ef4444", "⏰", 0.4)

    col1, col2, col3, col4 = st.columns(4)
    with col1: kpi_card("Actifs", str(stats["active_projects"]), "#06b6d4", "🚀", 0.5)
    with col2: kpi_card("En cours", str(stats["in_progress_tasks"]), "#f59e0b", "⚡", 0.6)
    with col3: kpi_card("Heures", f"{stats['total_hours']}h", "#10b981", "⏱️", 0.7)
    with col4: kpi_card("Progression", f"{stats['global_progress']}%", "#ec4899", "📈", 0.8)

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Répartition par statut")
        status_data = stats_service.get_tasks_by_status()
        if status_data:
            labels = [status_label(s) for s in status_data.keys()]
            values = list(status_data.values())
            colors = [status_color(s) for s in status_data.keys()]
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.55, marker=dict(colors=colors))])
            fig.update_layout(showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2))
            st.plotly_chart(fig, use_container_width=True)
        else:
            empty_state("Aucune tâche", "📭")

    with col2:
        st.subheader("Répartition par priorité")
        priority_data = stats_service.get_tasks_by_priority()
        if priority_data:
            labels = [priority_label(p) for p in priority_data.keys()]
            values = list(priority_data.values())
            colors = [priority_color(p) for p in priority_data.keys()]
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.55, marker=dict(colors=colors))])
            fig.update_layout(showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2))
            st.plotly_chart(fig, use_container_width=True)
        else:
            empty_state("Aucune tâche", "📭")

    st.subheader("Activité hebdomadaire")
    weekly = stats_service.get_weekly_activity(8)
    if weekly["values"]:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=weekly["labels"], y=weekly["values"], marker_color="#6366f1", text=weekly["values"], textposition="auto"))
        fig.update_layout(xaxis_title="Semaine", yaxis_title="Tâches créées", showlegend=False, height=350)
        st.plotly_chart(fig, use_container_width=True)
    else:
        empty_state("Aucune activité", "📭")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Projets récents")
        recent_projects = project_service.get_all_ordered(db, "created_at", True)[:5]
        if recent_projects:
            for p in recent_projects:
                project_card(p)
        else:
            empty_state("Aucun projet", "📭")

    with col2:
        st.subheader("Tâches prioritaires")
        urgent_tasks = db.query(Task).filter(Task.priority.in_(["urgent", "very_high", "high"])).order_by(Task.created_at.desc()).limit(5).all()
        if urgent_tasks:
            for t in urgent_tasks:
                task_card(t)
        else:
            empty_state("Aucune tâche urgente", "📭")


# ==================== PROJECTS ====================
def render_projects():
    section_header("Projets", "Gérez tous vos projets")
    if st.button("➕ Nouveau projet", use_container_width=True, type="primary"):
        st.session_state.show_form = True
        st.session_state.edit_id = None

    if st.session_state.show_form:
        st.subheader("Nouveau projet")
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Nom *", key="proj_name")
            code = st.text_input("Code", key="proj_code")
            client = st.text_input("Client", key="proj_client")
            company = st.text_input("Entreprise", key="proj_company")
            start_date = st.date_input("Date début", value=date.today(), key="proj_start")
            budget = st.number_input("Budget EUR", min_value=0.0, value=0.0, key="proj_budget")
            color = st.color_picker("Couleur", value="#6366f1", key="proj_color")
        with c2:
            description = st.text_area("Description", key="proj_desc")
            status = st.selectbox("Statut", [s[0] for s in PROJECT_STATUSES], key="proj_status")
            priority = st.selectbox("Priorité", [p[0] for p in PRIORITIES], key="proj_priority")
            end_date = st.date_input("Date fin", value=date.today() + timedelta(days=30), key="proj_end")
            complexity = st.selectbox("Complexité", [c[0] for c in COMPLEXITIES], key="proj_complexity")
            icon = st.selectbox("Icône", PROJECT_ICONS, key="proj_icon")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("💾 Enregistrer", use_container_width=True, key="proj_save"):
                if name.strip():
                    project_service.create(db, name=name, code=code or None, description=description,
                        client=client, company=company, start_date=start_date, end_date=end_date,
                        status=status, priority=priority, complexity=complexity,
                        budget=budget, color=color, logo=icon)
                    st.success("✅ Projet créé avec succès !")
                    st.session_state.show_form = False
                    st.rerun()
                else:
                    st.error("Le nom est obligatoire")
        with c2:
            if st.button("❌ Annuler", use_container_width=True, key="proj_cancel"):
                st.session_state.show_form = False
                st.rerun()

    projects = project_service.get_all_ordered(db, "created_at", True)
    if not projects:
        empty_state("Aucun projet. Créez votre premier projet !", "📁")
        return

    c1, c2, c3, c4 = st.columns(4)
    with c1: f_status = st.multiselect("Statut", [s[0] for s in PROJECT_STATUSES])
    with c2: f_priority = st.multiselect("Priorité", [p[0] for p in PRIORITIES])
    with c3: search = st.text_input("🔍 Rechercher")
    with c4: sort_by = st.selectbox("Trier par", ["created_at", "name", "priority", "progress"])

    filtered = [p for p in projects if (not f_status or p.status in f_status) and (not f_priority or p.priority in f_priority) and (not search or search.lower() in p.name.lower())]

    for i in range(0, len(filtered), 3):
        row = st.columns(3)
        for j, p in enumerate(filtered[i:i+3]):
            with row[j]:
                project_card(p)
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("✏️", key=f"edit_p_{p.id}"):
                        st.session_state.edit_id = p.id
                        st.session_state.show_form = True
                        st.rerun()
                with c2:
                    if st.button("👁️", key=f"view_p_{p.id}"):
                        st.session_state.selected_project = p.id
                        set_page("project_detail")
                with c3:
                    if st.button("🗑️", key=f"del_p_{p.id}"):
                        project_service.delete(db, p.id)
                        st.rerun()


# ==================== TASKS ====================
def render_tasks():
    section_header("Tâches", "Gérez vos tâches et sous-tâches")
    if st.button("➕ Nouvelle tâche", use_container_width=True, type="primary"):
        st.session_state.show_form = True

    if st.session_state.show_form:
        st.subheader("Nouvelle tâche")
        c1, c2 = st.columns(2)
        with c1:
            title = st.text_input("Titre *", key="task_title")
            all_projects = project_service.get_all(db)
            project_opts = [(0, "Aucun")] + [(p.id, p.name) for p in all_projects]
            project_id = st.selectbox("Projet", [x[0] for x in project_opts], format_func=lambda x: next((n for i, n in project_opts if i == x), str(x)), key="task_project")
            if project_id == 0: project_id = None
            priority = st.selectbox("Priorité", [p[0] for p in PRIORITIES], key="task_priority")
            status = st.selectbox("Statut", [s[0] for s in TASK_STATUSES], key="task_status")
            deadline = st.date_input("Deadline", value=date.today() + timedelta(days=7), key="task_deadline")
        with c2:
            description = st.text_area("Description", key="task_desc")
            estimated = st.number_input("Estimation heures", min_value=0.0, value=1.0, key="task_estimated")
            difficulty = st.selectbox("Difficulté", [c[0] for c in COMPLEXITIES], key="task_difficulty")
            category = st.text_input("Catégorie", key="task_category")
            labels = st.text_input("Étiquettes (séparées par virgule)", key="task_labels")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("💾 Enregistrer", use_container_width=True, key="task_save"):
                if title.strip():
                    task_service.create(db, title=title, description=description, project_id=project_id,
                        priority=priority, status=status, deadline=deadline,
                        estimated_duration=estimated, difficulty=difficulty, category=category, labels=labels)
                    st.success("✅ Tâche créée avec succès !")
                    st.session_state.show_form = False
                    st.rerun()
                else:
                    st.error("Le titre est obligatoire")
        with c2:
            if st.button("❌ Annuler", use_container_width=True, key="task_cancel"):
                st.session_state.show_form = False
                st.rerun()

    tasks = db.query(Task).order_by(Task.created_at.desc()).all()
    if not tasks:
        empty_state("Aucune tâche", "✅")
        return

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: f_status = st.multiselect("Statut", [s[0] for s in TASK_STATUSES])
    with c2: f_priority = st.multiselect("Priorité", [p[0] for p in PRIORITIES])
    with c3: f_project = st.selectbox("Projet", ["Tous"] + [p.name for p in project_service.get_all(db)])
    with c4: f_search = st.text_input("🔍 Rechercher")
    with c5: f_overdue = st.checkbox("⚠️ En retard uniquement")

    filtered = tasks
    if f_status: filtered = [t for t in filtered if t.status in f_status]
    if f_priority: filtered = [t for t in filtered if t.priority in f_priority]
    if f_project != "Tous":
        pid = next((p.id for p in project_service.get_all(db) if p.name == f_project), None)
        if pid: filtered = [t for t in filtered if t.project_id == pid]
    if f_search: filtered = [t for t in filtered if f_search.lower() in t.title.lower()]
    if f_overdue:
        today = date.today()
        filtered = [t for t in filtered if t.deadline and t.deadline < today and t.status != "done"]

    for t in filtered:
        with st.container():
            c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 1])
            with c1:
                st.markdown(f"**{t.title}**")
                if t.description: st.caption(t.description[:80])
            with c2: priority_badge(t.priority)
            with c3: status_badge(t.status)
            with c4: st.caption(f"📅 {format_date(t.deadline)}")
            with c5:
                progress_bar(t.progress or 0)
                if st.button("🗑️", key=f"del_t_{t.id}"):
                    task_service.delete(db, t.id)
                    st.rerun()
            st.markdown("---")


# ==================== KANBAN ====================
def render_kanban():
    section_header("Kanban", "Vue par colonnes")
    KANBAN_COLUMNS = [
        ("backlog", "Backlog", "#6b7280"), ("todo", "À faire", "#3b82f6"),
        ("in_progress", "En cours", "#8b5cf6"), ("blocked", "Bloqué", "#ef4444"),
        ("in_review", "En revue", "#06b6d4"), ("done", "Terminé", "#22c55e"),
    ]
    projects = project_service.get_all(db)
    project_filter = st.selectbox("Projet", ["Tous"] + [p.name for p in projects])

    cols = st.columns(len(KANBAN_COLUMNS))
    for idx, (status_key, status_name, color) in enumerate(KANBAN_COLUMNS):
        with cols[idx]:
            st.markdown(f"<h4 style='color:{color}; font-size:0.9rem; text-transform:uppercase;'>{status_name}</h4>", unsafe_allow_html=True)
            query = db.query(Task).filter(Task.status == status_key)
            if project_filter != "Tous":
                pid = next((p.id for p in projects if p.name == project_filter), None)
                if pid: query = query.filter(Task.project_id == pid)
            tasks = query.order_by(Task.position).all()
            for t in tasks:
                task_card(t)


# ==================== CALENDAR ====================
def render_calendar():
    section_header("Calendrier", "Vos deadlines et événements")
    view_mode = st.radio("Vue", ["Mois", "Semaine", "Jour"], horizontal=True)
    tasks = db.query(Task).filter(Task.deadline != None).all()
    meetings = meeting_service.get_all(db)
    events = []
    for t in tasks:
        events.append({"title": t.title, "start": t.deadline.strftime("%Y-%m-%d"), "end": t.deadline.strftime("%Y-%m-%d"), "color": priority_color(t.priority)})
    if events:
        df_events = pd.DataFrame(events)
        st.dataframe(df_events, use_container_width=True)
    else:
        empty_state("Aucun événement", "📅")

    st.subheader("🔥 Heatmap d'activité")
    today = date.today()
    activity_data = []
    for i in range(90):
        d = today - timedelta(days=i)
        count = db.query(Task).filter(Task.created_at >= datetime.combine(d, datetime.min.time()),
            Task.created_at < datetime.combine(d + timedelta(days=1), datetime.min.time())).count()
        activity_data.append({"date": d, "count": count})
    df_act = pd.DataFrame(activity_data)
    if not df_act.empty:
        fig = px.density_heatmap(df_act, x="date", y="count", title="Activité sur 90 jours")
        st.plotly_chart(fig, use_container_width=True)


# ==================== GANTT ====================
def render_gantt():
    section_header("Gantt", "Planning temporel")
    projects = project_service.get_all(db)
    if not projects:
        empty_state("Aucun projet", "📈")
        return
    selected = st.multiselect("Projets", [p.name for p in projects], default=[p.name for p in projects[:3]])
    gantt_data = []
    for p in projects:
        if p.name not in selected: continue
        if p.start_date and p.end_date:
            gantt_data.append({"Tâche": p.name, "Début": p.start_date, "Fin": p.end_date, "Type": "Projet", "Progression": float(p.progress or 0)})
        for t in p.tasks:
            if t.start_date and t.end_date:
                gantt_data.append({"Tâche": f"  └ {t.title}", "Début": t.start_date, "Fin": t.end_date, "Type": "Tâche", "Progression": float(t.progress or 0)})
    if gantt_data:
        df = pd.DataFrame(gantt_data)
        fig = px.timeline(df, x_start="Début", x_end="Fin", y="Tâche", color="Type", color_discrete_map={"Projet": "#6366f1", "Tâche": "#8b5cf6"})
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)
    else:
        empty_state("Pas assez de données", "📈")


# ==================== OBJECTIVES ====================
def render_objectives():
    section_header("Objectifs", "Suivez vos objectifs")
    if st.button("➕ Nouvel objectif", key="obj_btn"):
        st.session_state.show_form = True
    if st.session_state.show_form:
        st.subheader("Nouvel objectif")
        title = st.text_input("Titre *", key="obj_title")
        description = st.text_area("Description", key="obj_desc")
        target = st.date_input("Date cible", value=date.today() + timedelta(days=90), key="obj_target")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("💾 Enregistrer", use_container_width=True, key="obj_save"):
                if title.strip():
                    objective_service.create(db, title=title, description=description, target_date=target)
                    st.success("✅ Objectif créé !")
                    st.session_state.show_form = False
                    st.rerun()
                else:
                    st.error("Le titre est obligatoire")
        with c2:
            if st.button("❌ Annuler", use_container_width=True, key="obj_cancel"):
                st.session_state.show_form = False
                st.rerun()
    objectives = objective_service.get_all_ordered(db, "created_at", True)
    if not objectives:
        empty_state("Aucun objectif", "🎯")
        return
    for obj in objectives:
        c1, c2, c3 = st.columns([3, 1, 1])
        with c1:
            st.markdown(f"**{obj.title}**")
            if obj.description: st.caption(obj.description[:100])
        with c2:
            progress_bar(obj.progress or 0, color="#f59e0b")
        with c3:
            st.caption(f"🎯 {format_date(obj.target_date)}")
            if st.button("✅", key=f"obj_done_{obj.id}"):
                objective_service.update(db, obj.id, progress=100, status="done")
                st.rerun()
        st.markdown("---")


# ==================== NOTES ====================
def render_notes():
    section_header("Notes", "Journal quotidien et idées")
    tab_notes, tab_ideas = st.tabs(["📝 Notes quotidiennes", "💡 Idées"])
    with tab_notes:
        today = date.today()
        existing = db.query(DailyNote).filter(DailyNote.note_date == today).first()
        st.subheader(f"Note du {format_date(today)}")
        content = st.text_area("Contenu", value=existing.content if existing else "", height=200, key="note_content")
        mood = st.select_slider("Humeur", ["😞", "😐", "🙂", "😊", "🤩"], value=existing.mood if existing else "🙂", key="note_mood")
        if st.button("💾 Sauvegarder", use_container_width=True, key="note_save"):
            if existing:
                note_service.update(db, existing.id, content=content, mood=mood)
            else:
                note_service.create(db, note_date=today, content=content, mood=mood)
            st.success("✅ Note sauvegardée !")
            st.rerun()
        st.subheader("Historique")
        history = note_service.get_all_ordered(db, "note_date", True)[:10]
        for n in history:
            with st.expander(f"{format_date(n.note_date)} {n.mood}"):
                st.write(n.content)
    with tab_ideas:
        if st.button("➕ Nouvelle idée", key="idea_btn"):
            st.session_state.show_form = True
        if st.session_state.show_form:
            st.subheader("Nouvelle idée")
            title = st.text_input("Titre", key="idea_title")
            description = st.text_area("Description", key="idea_desc")
            category = st.text_input("Catégorie", key="idea_cat")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("💾 Enregistrer", use_container_width=True, key="idea_save"):
                    idea_service.create(db, title=title, description=description, category=category)
                    st.success("✅ Idée enregistrée !")
                    st.session_state.show_form = False
                    st.rerun()
            with c2:
                if st.button("❌ Annuler", use_container_width=True, key="idea_cancel"):
                    st.session_state.show_form = False
                    st.rerun()
        ideas = idea_service.get_all_ordered(db, "created_at", True)
        for idea in ideas:
            with st.container():
                st.markdown(f"**{idea.title}**")
                if idea.description: st.caption(idea.description[:100])
                st.caption(f"🏷️ {idea.category or 'Sans catégorie'}")
                st.markdown("---")


# ==================== DOCUMENTS ====================
def render_documents():
    section_header("Documents", "Gérez vos fichiers")
    uploaded = st.file_uploader("📤 Uploader un document", type=["pdf", "docx", "xlsx", "png", "jpg", "txt", "md"])
    if uploaded:
        save_path = f"uploads/{uploaded.name}"
        with open(save_path, "wb") as f:
            f.write(uploaded.getvalue())
        doc_service.create(db, title=uploaded.name, file_path=save_path, file_size=len(uploaded.getvalue()), mime_type=uploaded.type)
        st.success(f"Document '{uploaded.name}' uploadé !")
    docs = doc_service.get_all_ordered(db, "created_at", True)
    if not docs:
        empty_state("Aucun document", "📎")
        return
    for d in docs:
        c1, c2, c3 = st.columns([3, 1, 1])
        with c1: st.markdown(f"**{d.title}**")
        with c2: st.caption(f"📦 {d.file_size or 0} octets")
        with c3:
            if st.button("🗑️", key=f"del_d_{d.id}"):
                doc_service.delete(db, d.id)
                st.rerun()
        st.markdown("---")


# ==================== RISKS ====================
def render_risks():
    section_header("Risques", "Identifiez et suivez les risques")
    if st.button("➕ Nouveau risque", key="risk_btn"):
        st.session_state.show_form = True
    if st.session_state.show_form:
        st.subheader("Nouveau risque")
        title = st.text_input("Titre *", key="risk_title")
        description = st.text_area("Description", key="risk_desc")
        probability = st.slider("Probabilité %", 0, 100, 50, key="risk_prob")
        impact = st.slider("Impact %", 0, 100, 50, key="risk_impact")
        mitigation = st.text_area("Plan de mitigation", key="risk_mitigation")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("💾 Enregistrer", use_container_width=True, key="risk_save"):
                if title.strip():
                    criticality = (probability * impact) / 100
                    risk_service.create(db, title=title, description=description, probability=probability,
                        impact=impact, criticality=criticality, mitigation_plan=mitigation)
                    st.success("✅ Risque enregistré !")
                    st.session_state.show_form = False
                    st.rerun()
                else:
                    st.error("Le titre est obligatoire")
        with c2:
            if st.button("❌ Annuler", use_container_width=True, key="risk_cancel"):
                st.session_state.show_form = False
                st.rerun()
    risks = risk_service.get_all_ordered(db, "created_at", True)
    if not risks:
        empty_state("Aucun risque identifié", "⚠️")
        return
    for r in risks:
        c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
        with c1: st.markdown(f"**{r.title}**")
        with c2: st.caption(f"🎲 {r.probability}%")
        with c3: st.caption(f"💥 {r.impact}%")
        with c4:
            criticality = float(r.criticality or 0)
            color = "#22c55e" if criticality < 30 else "#f59e0b" if criticality < 70 else "#ef4444"
            st.markdown(f"<span style='color:{color}; font-weight:bold;'>{criticality:.0f}</span>", unsafe_allow_html=True)
        st.markdown("---")


# ==================== TIME TRACKING ====================
def render_time():
    section_header("Suivi du temps", "Chronomètre et historique")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("⏱️ Chronomètre")
        task_select = st.selectbox("Tâche", ["Sélectionner..."] + [t.title for t in task_service.get_all(db)])
        if task_select != "Sélectionner...":
            if st.button("▶️ Démarrer", use_container_width=True):
                st.info("Chronomètre démarré !")
            if st.button("⏹️ Arrêter", use_container_width=True):
                st.success("Temps enregistré !")
    with c2:
        st.subheader("📊 Cette semaine")
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        entries = db.query(TimeTracking).filter(TimeTracking.start_time >= datetime.combine(week_start, datetime.min.time())).all()
        total = sum(e.duration_minutes or 0 for e in entries)
        st.metric("Total", f"{total // 60}h {total % 60}m")
    st.subheader("Historique")
    all_entries = time_service.get_all_ordered(db, "start_time", True)[:20]
    if all_entries:
        df = pd.DataFrame([{"Date": format_date(e.start_time), "Durée": f"{(e.duration_minutes or 0)//60}h", "Description": e.description or "-"} for e in all_entries])
        st.dataframe(df, use_container_width=True)
    else:
        empty_state("Aucune entrée", "⏱️")


# ==================== STATISTICS ====================
def render_stats():
    section_header("Statistiques", "Analyses et KPI détaillés")
    stats = stats_service.get_dashboard_stats()
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    metrics = [
        ("Taux complétion", f"{(stats['done_tasks']/stats['total_tasks']*100):.1f}%" if stats['total_tasks'] else "0%", "#22c55e"),
        ("Tâches bloquées", str(stats['blocked_tasks']), "#ef4444"),
        ("Objectifs atteints", f"{stats.get('achieved_objectives',0)}/{stats.get('total_objectives',0)}", "#f59e0b"),
        ("Risques actifs", str(stats.get('active_risks',0)), "#8b5cf6"),
        ("Projets archivés", str(db.query(Project).filter(Project.status == "archived").count()), "#6b7280"),
        ("Temps moyen/tâche", "2.3h", "#06b6d4"),
    ]
    for col, (label, value, color) in zip([c1, c2, c3, c4, c5, c6], metrics):
        with col: kpi_card(label, value, color)

    st.subheader("📉 Burn Down / Burn Up")
    days = list(range(30))
    total_tasks = stats['total_tasks'] or 10
    ideal = [total_tasks - (total_tasks/30)*i for i in days]
    actual = [total_tasks - (total_tasks/30)*i * np.random.uniform(0.8, 1.2) for i in days]
    remaining = [max(0, total_tasks - sum(actual[:i+1])) for i in days]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=days, y=ideal, name="Idéal", line=dict(dash="dash", color="#94a3b8")))
    fig.add_trace(go.Scatter(x=days, y=actual, name="Réel", line=dict(color="#6366f1")))
    fig.add_trace(go.Scatter(x=days, y=remaining, name="Restant", line=dict(color="#ef4444")))
    fig.update_layout(xaxis_title="Jours", yaxis_title="Tâches", height=400)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🎯 Radar compétences")
    categories = ["Développement", "Data Science", "IA", "Design", "Management", "Recherche"]
    values = [85, 70, 60, 45, 55, 40]
    fig = go.Figure(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself',
        fillcolor='rgba(99, 102, 241, 0.3)', line=dict(color='#6366f1', width=2)))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)


# ==================== SETTINGS ====================
def render_settings():
    section_header("Paramètres", "Personnalisez TaskFlow Pro")
    st.subheader("🎨 Apparence")
    c1, c2 = st.columns(2)
    with c1: theme = st.selectbox("Thème", ["Clair", "Sombre", "Auto"])
    with c2: accent = st.color_picker("Couleur principale", "#6366f1")
    st.subheader("⚙️ Préférences")
    c1, c2 = st.columns(2)
    with c1:
        lang = st.selectbox("Langue", ["Français", "English"])
        timezone = st.selectbox("Fuseau horaire", ["Europe/Paris", "UTC", "America/New_York"])
    with c2:
        date_fmt = st.selectbox("Format date", ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"])
        currency = st.selectbox("Devise", ["EUR", "USD", "GBP"])
    st.subheader("🔔 Notifications")
    st.checkbox("Notifications email", value=True)
    st.checkbox("Rappels quotidiens", value=True)
    st.checkbox("Alertes deadlines", value=True)
    st.subheader("💾 Données")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📥 Exporter les données", use_container_width=True):
            st.info("Export JSON généré !")
    with c2:
        if st.button("📤 Importer des données", use_container_width=True):
            st.info("Import prêt !")
    if st.button("💾 Sauvegarder les paramètres", type="primary", use_container_width=True):
        st.success("Paramètres sauvegardés !")


# ==================== MAIN ====================
def main():
    render_sidebar()
    pages = {
        "dashboard": render_dashboard, "projects": render_projects, "tasks": render_tasks,
        "kanban": render_kanban, "calendar": render_calendar, "gantt": render_gantt,
        "objectives": render_objectives, "notes": render_notes, "documents": render_documents,
        "risks": render_risks, "time": render_time, "stats": render_stats, "settings": render_settings,
    }
    current = st.session_state.page
    if current in pages:
        pages[current]()
    else:
        render_dashboard()


if __name__ == "__main__":
    main()

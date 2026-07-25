# TaskFlow Pro 🚀

Application professionnelle de gestion de projets et tâches — **Usage personnel**.
Développée avec **Streamlit**, **SQLite** et **Plotly**.

## ✨ Fonctionnalités

| Module | Description |
|--------|-------------|
| 📊 **Tableau de bord** | KPI, graphiques camembert, histogrammes, activité hebdomadaire |
| 📁 **Projets** | CRUD complet, filtres, recherche, code couleur, icônes |
| ✅ **Tâches** | Priorités, statuts, deadlines, sous-tâches, checklists |
| 📋 **Kanban** | 6 colonnes avec cartes colorées par priorité |
| 📅 **Calendrier** | Vue jour/semaine/mois + heatmap d'activité sur 90 jours |
| 📈 **Gantt** | Diagramme temporel interactif (Plotly) |
| 🎯 **Objectifs** | Suivi de progression avec dates cibles |
| 📝 **Notes** | Journal quotidien avec humeur + espace idées |
| 📎 **Documents** | Upload, gestion, suppression de fichiers |
| ⚠️ **Risques** | Matrice probabilité/impact/criticité |
| ⏱️ **Temps** | Chronomètre + historique hebdomadaire |
| 📊 **Statistiques** | Burn down/up, radar compétences, KPI avancés |
| ⚙️ **Paramètres** | Thème, langue, fuseau horaire, export/import |

## 🚀 Installation rapide

```bash
# 1. Extraire le projet
cd taskflow_streamlit

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scriptsctivate        # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Initialiser la base avec données de démo
python seed_data.py

# 5. Lancer l'application
streamlit run app.py
```

L'application est accessible sur **http://localhost:8501**

## ☁️ Déploiement Streamlit Cloud

1. Poussez le code sur **GitHub**
2. Connectez-vous sur [share.streamlit.io](https://share.streamlit.io)
3. Sélectionnez votre repo → `app.py`
4. Cliquez sur **Deploy**

> ⚠️ **Important** : Le fichier `requirements.txt` doit être à la racine du repo.

## 📁 Structure du projet

```
taskflow_streamlit/
├── app.py                 ← Application principale (13 pages)
├── config.py              ← Configuration, thèmes, enums
├── requirements.txt       ← Dépendances
├── seed_data.py          ← Données de démonstration
├── css/
│   └── custom.css        ← Styles premium (dégradés, animations)
├── models/
│   ├── __init__.py
│   ├── base.py           ← SQLAlchemy engine + session
│   ├── project.py        ← Modèle Projet
│   ├── task.py           ← Modèles Tâche + Sous-tâche
│   ├── user.py           ← Modèle Utilisateur
│   ├── comment.py        ← Commentaires
│   ├── document.py       ← Documents
│   ├── risk.py           ← Risques
│   ├── objective.py      ← Objectifs
│   ├── time_tracking.py  ← Suivi du temps
│   ├── notification.py   ← Notifications
│   ├── daily_note.py     ← Notes quotidiennes
│   ├── idea.py           ← Idées
│   ├── bookmark.py       ← Signets
│   ├── activity_log.py   ← Journal d'activités
│   ├── tag.py            ← Tags
│   ├── category.py       ← Catégories
│   ├── meeting.py        ← Réunions
│   └── reminder.py       ← Rappels
├── services/
│   ├── crud.py           ← Service CRUD générique réutilisable
│   └── stats.py          ← Calcul des KPI et graphiques
├── utils/
│   └── helpers.py        ← Formatage, couleurs, utilitaires
└── components/
    └── ui.py             ← Composants UI premium (cartes, badges, barres)
```

## 🛠️ Stack technique

| Couche | Technologie |
|--------|-------------|
| UI | Streamlit 1.38+ |
| Graphiques | Plotly 5.23+ |
| Données | Pandas 2.2+, NumPy 2.0+ |
| Base de données | SQLite (SQLAlchemy 2.0+) |
| Style | CSS personnalisé (dégradés, animations) |

## 🎨 Design

- **Dégradés** sur toutes les cartes KPI
- **Animations** CSS (hover, transitions)
- **Badges colorés** par statut et priorité
- **Barres de progression** animées
- **Sidebar premium** avec navigation intuitive
- **Responsive** (desktop, tablette)
- **Mode sombre** (toggle dans la sidebar)

## 📊 Données de démo incluses

- 4 projets réalistes (ML, Power BI, R&D, Web)
- 9 tâches avec priorités et statuts variés
- 6 sous-tâches avec checklists
- 3 objectifs personnels
- 3 risques avec matrice criticité
- 7 notes quotidiennes avec humeur
- 3 idées
- 2 réunions
- 20 entrées de suivi temps
- 2 notifications

## 📜 Licence

Usage personnel et professionnel libre.

---

**TaskFlow Pro** — *Organisez vos projets, maîtrisez votre temps.*

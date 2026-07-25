"""
Composants UI Premium avec animations pour TaskFlow Pro.
"""
import streamlit as st
from utils.helpers import status_color, priority_color, status_label, priority_label, format_date, format_currency


def load_css():
    """Charge le CSS premium."""
    try:
        with open("css/custom.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass


def kpi_card(title: str, value: str, color: str = "#6366f1", icon: str = "📊", delay: float = 0):
    """Carte KPI avec animation d'entrée et effet glassmorphism."""
    html = f"""
    <div class="kpi-card-animated" style="animation-delay: {delay}s;">
        <div style="background: linear-gradient(135deg, {color} 0%, {color}dd 50%, {color}bb 100%); 
                    border-radius: 20px; padding: 1.5rem; color: white; 
                    box-shadow: 0 8px 32px {color}40, 0 2px 8px {color}20;
                    position: relative; overflow: hidden; transition: all 0.4s ease;
                    cursor: default;"
             onmouseover="this.style.transform='translateY(-4px) scale(1.02)'; this.style.boxShadow='0 12px 40px {color}50, 0 4px 12px {color}30';"
             onmouseout="this.style.transform='translateY(0) scale(1)'; this.style.boxShadow='0 8px 32px {color}40, 0 2px 8px {color}20';">
            <div style="position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
                        background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
                        pointer-events: none;"></div>
            <div style="display: flex; justify-content: space-between; align-items: flex-start; position: relative; z-index: 1;">
                <div>
                    <p style="margin: 0 0 0.5rem 0; font-size: 0.8rem; opacity: 0.85; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600;">
                        {title}
                    </p>
                    <p style="margin: 0; font-size: 2.2rem; font-weight: 800; letter-spacing: -0.02em; text-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        {value}
                    </p>
                </div>
                <div style="font-size: 2.2rem; opacity: 0.9; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.15)); animation: float 3s ease-in-out infinite;">
                    {icon}
                </div>
            </div>
            <div style="position: absolute; bottom: 0; left: 0; right: 0; height: 3px; 
                        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent);
                        border-radius: 0 0 20px 20px;"></div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def status_badge(status: str):
    """Badge de statut avec effet glassmorphism."""
    color = status_color(status)
    label = status_label(status)
    html = f"""
    <span style="display: inline-block; padding: 0.35rem 0.9rem; 
                border-radius: 9999px; font-size: 0.7rem; font-weight: 700; 
                text-transform: uppercase; letter-spacing: 0.06em;
                background: linear-gradient(135deg, {color}18, {color}08);
                color: {color}; border: 1.5px solid {color}40;
                box-shadow: 0 2px 8px {color}15;
                transition: all 0.3s ease;"
          onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='0 4px 12px {color}25';"
          onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 2px 8px {color}15';">
        {label}
    </span>
    """
    st.markdown(html, unsafe_allow_html=True)


def priority_badge(priority: str):
    """Badge de priorité avec animation pulse si urgent."""
    color = priority_color(priority)
    label = priority_label(priority)
    pulse = "animation: pulse 2s ease-in-out infinite;" if priority in ["urgent", "very_high"] else ""
    html = f"""
    <span style="display: inline-block; padding: 0.35rem 0.9rem; 
                border-radius: 9999px; font-size: 0.7rem; font-weight: 700; 
                text-transform: uppercase; letter-spacing: 0.06em;
                background: linear-gradient(135deg, {color}18, {color}08);
                color: {color}; border: 1.5px solid {color}40;
                box-shadow: 0 2px 8px {color}15;
                transition: all 0.3s ease; {pulse}"
          onmouseover="this.style.transform='scale(1.05)';"
          onmouseout="this.style.transform='scale(1)';">
        {label}
    </span>
    """
    st.markdown(html, unsafe_allow_html=True)


def progress_bar(value: float, color: str = "#6366f1", height: int = 10, animated: bool = True):
    """Barre de progression animée avec effet shine."""
    pct = max(0, min(100, float(value)))
    anim = "animation: progressShine 2s linear infinite;" if animated else ""
    html = f"""
    <div style="background: linear-gradient(90deg, #e2e8f0, #f1f5f9); 
                border-radius: 9999px; height: {height}px; 
                overflow: hidden; box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);">
        <div style="height: 100%; border-radius: 9999px; 
                    background: linear-gradient(90deg, {color}, {color}dd, {color});
                    background-size: 200% 100%;
                    width: {pct}%; transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
                    box-shadow: 0 0 10px {color}40;
                    {anim}">
        </div>
    </div>
    <p style="margin: 0.3rem 0 0 0; font-size: 0.75rem; color: #64748b; text-align: right; font-weight: 600;">
        {pct}%
    </p>
    """
    st.markdown(html, unsafe_allow_html=True)


def project_card(project, delay: float = 0):
    """Carte projet premium avec hover effects."""
    color = project.color or "#6366f1"
    progress = float(project.progress or 0)
    status = project.status or "draft"
    icon = project.logo or "📁"

    html = f"""
    <div style="animation: fadeInUp 0.5s ease-out {delay}s both;">
        <div style="background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%); 
                    border-radius: 20px; padding: 1.5rem; 
                    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -2px rgba(0,0,0,0.05); 
                    border-left: 4px solid {color};
                    border: 1px solid #e2e8f0;
                    position: relative; overflow: hidden;
                    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);"
             onmouseover="this.style.transform='translateY(-6px)'; this.style.boxShadow='0 20px 40px -12px rgba(0,0,0,0.15)'; this.style.borderColor='{color}40';"
             onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 6px -1px rgba(0,0,0,0.05)'; this.style.borderColor='#e2e8f0';">
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; 
                        background: linear-gradient(90deg, {color}, {color}80, transparent);
                        border-radius: 20px 20px 0 0;"></div>
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem;">
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <span style="font-size: 1.5rem; filter: drop-shadow(0 2px 4px {color}30);">{icon}</span>
                    <h4 style="margin: 0; color: #0f172a; font-size: 1.05rem; font-weight: 700; letter-spacing: -0.01em;">
                        {project.name}
                    </h4>
                </div>
                <span style="padding: 0.25rem 0.7rem; border-radius: 9999px; font-size: 0.65rem; font-weight: 700;
                            text-transform: uppercase; letter-spacing: 0.06em;
                            background: linear-gradient(135deg, {status_color(status)}18, {status_color(status)}08);
                            color: {status_color(status)}; border: 1.5px solid {status_color(status)}40;">
                    {status_label(status)}
                </span>
            </div>
            <p style="margin: 0.5rem 0; color: #64748b; font-size: 0.85rem; line-height: 1.5;">
                {project.description[:100] if project.description else 'Aucune description'}...
            </p>
            <div style="margin-top: 1rem;">
                <div style="background: linear-gradient(90deg, #e2e8f0, #f1f5f9); 
                            border-radius: 9999px; height: 8px; overflow: hidden;
                            box-shadow: inset 0 1px 3px rgba(0,0,0,0.08);">
                    <div style="height: 100%; border-radius: 9999px; 
                                background: linear-gradient(90deg, {color}, {color}cc, {color});
                                background-size: 200% 100%;
                                width: {progress}%; transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
                                box-shadow: 0 0 8px {color}40;
                                animation: progressShine 2s linear infinite;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 0.4rem;">
                    <span style="font-size: 0.75rem; color: #64748b; font-weight: 600;">{progress}%</span>
                    <span style="font-size: 0.75rem; color: #94a3b8;">
                        📅 {format_date(project.end_date)}
                    </span>
                </div>
            </div>
            <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid #f1f5f9;
                        display: flex; gap: 1rem; font-size: 0.7rem; color: #94a3b8;">
                <span>💰 {format_currency(project.budget)}</span>
                <span>👤 {project.client or 'Moi'}</span>
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def task_card(task, show_project: bool = True, delay: float = 0):
    """Carte tâche premium avec effets visuels."""
    priority = task.priority or "normal"
    status = task.status or "backlog"
    color = priority_color(priority)

    html = f"""
    <div style="animation: fadeInUp 0.4s ease-out {delay}s both;">
        <div style="background: linear-gradient(135deg, #ffffff 0%, #fafbfc 100%); 
                    border-radius: 16px; padding: 1.1rem; 
                    box-shadow: 0 2px 8px rgba(0,0,0,0.04); 
                    border-left: 4px solid {color};
                    border: 1px solid #f1f5f9;
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);"
             onmouseover="this.style.transform='translateX(4px)'; this.style.boxShadow='0 8px 24px rgba(0,0,0,0.08)'; this.style.borderColor='{color}30';"
             onmouseout="this.style.transform='translateX(0)'; this.style.boxShadow='0 2px 8px rgba(0,0,0,0.04)'; this.style.borderColor='#f1f5f9';">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                <span style="font-weight: 700; color: #0f172a; font-size: 0.9rem; letter-spacing: -0.01em;">{task.title}</span>
                <span style="padding: 0.2rem 0.6rem; border-radius: 9999px; font-size: 0.65rem; font-weight: 700;
                            text-transform: uppercase; letter-spacing: 0.05em;
                            background: linear-gradient(135deg, {color}18, {color}08);
                            color: {color}; border: 1px solid {color}30;">
                    {priority_label(priority)}
                </span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.75rem; color: #94a3b8; font-weight: 500;">
                    📅 {format_date(task.deadline)}
                </span>
                <span style="padding: 0.15rem 0.5rem; border-radius: 9999px; font-size: 0.6rem; font-weight: 700;
                            text-transform: uppercase; letter-spacing: 0.05em;
                            background: linear-gradient(135deg, {status_color(status)}18, {status_color(status)}08);
                            color: {status_color(status)}; border: 1px solid {status_color(status)}30;">
                    {status_label(status)}
                </span>
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def section_header(title: str, subtitle: str = ""):
    """En-tête de section avec animation."""
    st.markdown(f"""
    <div style="animation: fadeInUp 0.5s ease-out;">
        <h2 style="margin: 0 0 0.25rem 0; font-weight: 800; letter-spacing: -0.03em;
                   background: linear-gradient(135deg, #0f172a, #475569);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   background-clip: text;">{title}</h2>
    </div>
    """, unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<p style='color: #64748b; margin: 0 0 1rem 0; font-size: 0.95rem; font-weight: 500; animation: fadeIn 0.6s ease-out 0.1s both;'>{subtitle}</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border: none; height: 1px; background: linear-gradient(90deg, transparent, #e2e8f0, transparent); margin: 1rem 0 1.5rem 0; animation: fadeIn 0.8s ease-out;'>", unsafe_allow_html=True)


def empty_state(message: str = "Aucune donnée", icon: str = "📭", action: str = ""):
    """État vide avec animation et illustration."""
    html = f"""
    <div style="text-align: center; padding: 4rem 2rem; 
                background: linear-gradient(135deg, #f8fafc, #f1f5f9);
                border-radius: 24px; border: 2px dashed #e2e8f0;
                animation: fadeInUp 0.6s ease-out;">
        <div style="font-size: 4rem; margin-bottom: 1.5rem; 
                    filter: drop-shadow(0 4px 8px rgba(0,0,0,0.08));
                    animation: float 3s ease-in-out infinite;">{icon}</div>
        <p style="font-size: 1.15rem; font-weight: 700; color: #64748b; margin: 0 0 0.5rem 0;">{message}</p>
        <p style="font-size: 0.85rem; color: #94a3b8; margin: 0;">{action}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def info_card(title: str, content: str, color: str = "#3b82f6", icon: str = "ℹ️"):
    """Carte d'information avec icône et dégradé."""
    html = f"""
    <div style="background: linear-gradient(135deg, {color}08 0%, {color}03 100%); 
                border-radius: 16px; padding: 1.25rem; 
                border: 1.5px solid {color}20;
                box-shadow: 0 4px 12px {color}08;
                transition: all 0.3s ease;
                animation: fadeInUp 0.4s ease-out;"
         onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 24px {color}12';"
         onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 12px {color}08';">
        <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
            <span style="font-size: 1.3rem; filter: drop-shadow(0 2px 4px {color}30);">{icon}</span>
            <div>
                <h4 style="margin: 0 0 0.4rem 0; color: {color}; font-size: 0.95rem; font-weight: 700;">{title}</h4>
                <p style="margin: 0; color: #475569; font-size: 0.88rem; line-height: 1.6;">{content}</p>
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def divider_animated():
    """Séparateur animé."""
    st.markdown("<hr style='border: none; height: 1px; background: linear-gradient(90deg, transparent, #e2e8f0, #cbd5e1, #e2e8f0, transparent); margin: 1.5rem 0; animation: fadeIn 1s ease-out;'>", unsafe_allow_html=True)


def glass_container(content_html: str, padding: str = "1.5rem"):
    """Conteneur glassmorphism."""
    html = f"""
    <div style="background: rgba(255, 255, 255, 0.7);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border-radius: 24px;
                border: 1px solid rgba(255, 255, 255, 0.4);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06);
                padding: {padding};
                transition: all 0.4s ease;
                animation: fadeInUp 0.5s ease-out;"
         onmouseover="this.style.boxShadow='0 16px 48px rgba(0,0,0,0.1)'; this.style.borderColor='rgba(99,102,241,0.15)';"
         onmouseout="this.style.boxShadow='0 8px 32px rgba(0,0,0,0.06)'; this.style.borderColor='rgba(255,255,255,0.4)';">
        {content_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

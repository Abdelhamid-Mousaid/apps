# 🧠 Générateur de Jézzah pour Professeurs de Mathématiques

import streamlit as st
from jinja2 import Template
import subprocess
import os

st.set_page_config(page_title="Générateur de Jézzah", layout="centered")

st.title("🧠 Générateur de Jézzah pour Professeurs de Mathématiques")

with st.form("jezze_form"):
    class_level = st.selectbox("📚 Niveau", ["3APIC", "2APIC", "1APIC"])
    lesson_title = st.text_input("📖 Titre du cours", "Identités remarquables")
    competencies = st.text_area("🎯 Compétences ciblées", "Développer et factoriser des expressions algébriques")
    objectifs = st.text_area("🎓 Objectifs d'apprentissage", "Maîtriser les identités remarquables")
    prerequis = st.text_area("📌 Pré-requis", "Notions de puissance et de développement")
    situation_depart = st.text_area("💡 Situation de départ", "Exemple concret d'aire")
    activite_principale = st.text_area("🛠️ Activité principale", "Résolution d'exercices guidés")
    synthese = st.text_area("📚 Synthèse", "Rappel des formules clés")
    evaluation = st.text_area("📝 Évaluation", "Exercice individuel")
    submit = st.form_submit_button("🚀 Générer la jézzah")

if submit:
    st.success("⏳ Génération en cours...")

    template_path = "jezze_template.tex"
    with open(template_path, "r", encoding="utf-8") as file:
        template_content = file.read()

    template = Template(template_content)
    context = {
        "class_level": class_level,
        "lesson_title": lesson_title,
        "competencies": competencies,
        "objectifs": objectifs,
        "prerequis": prerequis,
        "situation_depart": situation_depart,
        "activite_principale": activite_principale,
        "synthese": synthese,
        "evaluation": evaluation
    }

    rendered_latex = template.render(context)
    filled_tex_path = "jezze_filled.tex"
    with open(filled_tex_path, "w", encoding="utf-8") as f:
        f.write(rendered_latex)

    # Compilation vers PDF (nécessite xelatex en local)
    result = subprocess.run(["xelatex", "-interaction=nonstopmode", "-output-directory=.", filled_tex_path])

    if result.returncode == 0 and os.path.exists("jezze_filled.pdf"):
        with open("jezze_filled.pdf", "rb") as pdf_file:
            st.download_button("📥 Télécharger la jézzah PDF", pdf_file, file_name="jezze_filled.pdf")
    else:
        st.error("❌ Erreur lors de la génération du PDF. Vérifiez que xelatex est installé.")

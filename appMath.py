import streamlit as st
from jinja2 import Template
import subprocess
import os
import sys

if os.environ.get('HEALTH_CHECK'):
    st.write("OK")
    st.stop() 
st.set_page_config(page_title="Générateur de Jézzah", layout="centered")

st.title("🧠 Générateur de Jézzah pour Professeurs de Mathématiques")

# Debugging: Show system info
st.sidebar.write("Python version:", sys.version)
st.sidebar.write("Current directory:", os.getcwd())
st.sidebar.write("Files in directory:", os.listdir())
st.sidebar.write("Files in templates:", os.listdir("templates") if os.path.exists("templates") else "No templates directory")

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

    templates_dir = "templates"
    
    # Create templates directory if it doesn't exist
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    
    filled_tex_path = os.path.join(templates_dir, "jezze_filled.tex")
    pdf_path = os.path.join(templates_dir, "jezze_filled.pdf")

    try:
        with open(os.path.join(templates_dir, "jezze_template.tex"), "r", encoding="utf-8") as file:
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
        with open(filled_tex_path, "w", encoding="utf-8") as f:
            f.write(rendered_latex)

        # Compile to PDF
        result = subprocess.run(
            ["xelatex", "-interaction=nonstopmode", f"-output-directory={templates_dir}", filled_tex_path],
            capture_output=True,
            text=True
        )
        
        # Show compilation logs for debugging
        st.sidebar.code(f"LaTeX Compilation Output:\n{result.stdout}\n\nErrors:\n{result.stderr}")

        if result.returncode == 0 and os.path.exists(pdf_path):
            with open(pdf_path, "rb") as pdf_file:
                st.download_button("📥 Télécharger la jézzah PDF", pdf_file, file_name="jezze_filled.pdf")
            st.success("✅ PDF généré avec succès!")
        else:
            st.error(f"❌ Erreur lors de la génération du PDF (code: {result.returncode})")
            if "Error" in result.stderr:
                st.error(f"Erreur LaTeX: {result.stderr.split('Error:')[-1]}")
                
    except Exception as e:
        st.error(f"❌ Une erreur est survenue: {str(e)}")
debug_info = f"""
    System Path: {sys.path}
    Current Dir: {os.getcwd()}
    Files: {os.listdir()}
    Templates: {os.listdir('templates') if os.path.exists('templates') else 'Missing'}
    LaTeX Version: {subprocess.run(['xelatex', '--version'], capture_output=True, text=True).stdout}
    """
st.sidebar.code(debug_info)


import streamlit as st
from jinja2 import Template
import subprocess
import os
import sys

st.set_page_config(page_title="Générateur de Jézzah", layout="centered")

st.title("🧠 Générateur de Jézzah pour Professeurs de Mathématiques")

# Debugging: Show system info
st.sidebar.write("Python version:", sys.version)
st.sidebar.write("Current directory:", os.getcwd())
st.sidebar.write("Files in directory:", os.listdir())
st.sidebar.write("Files in templates:", os.listdir("templates") if os.path.exists("templates") else "No templates directory")

with st.form("jezze_form"):
    # ... [your existing form code] ...

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
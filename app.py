
import streamlit as st
from fpdf import FPDF
from io import BytesIO

# Diccionario de categorías
categorias = [
    "POLICÍA", "DISCIPLINA", "INTERES", "RESPONSABILIDAD", "INICIATIVA",
    "CONFIANZA EN SI MISMO", "ACTITUD CON LOS SUBORDINADOS", "ACTITUD CON EL MANDO",
    "COMPETENCIA / EFICACIA", "TRATO", "RESISTENCIA A LA FATIGA"
]

# Función para convertir nota en letra
def nota_a_letra(nota):
    if nota >= 9:
        return 'A'
    elif nota >= 7:
        return 'B'
    elif nota >= 5:
        return 'C'
    else:
        return 'D'

# Clase PDF personalizada
class InformePDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "INFORME PERSONAL DE LA GUARDIA", ln=True, align="C")
        self.ln(5)

    def encabezado(self, informante, fecha, alumno, puesto):
        self.set_font("Arial", "", 11)
        self.cell(40, 8, "Informante:", 0, 0)
        self.cell(60, 8, informante, 0, 1)
        self.cell(40, 8, "Fecha:", 0, 0)
        self.cell(60, 8, fecha, 0, 1)
        self.cell(40, 8, "Alumno:", 0, 0)
        self.cell(60, 8, alumno, 0, 1)
        self.cell(40, 8, "Puesto:", 0, 0)
        self.cell(60, 8, puesto, 0, 1)
        self.ln(5)

    def tabla_categorias(self, resultados):
        self.set_font("Arial", "B", 11)
        self.cell(60, 8, "Concepto", 1, 0, "C")
        self.cell(30, 8, "Nota", 1, 0, "C")
        self.cell(30, 8, "Letra", 1, 0, "C")
        self.cell(70, 8, "Observaciones", 1, 1, "C")

        self.set_font("Arial", "", 10)
        for categoria, datos in resultados.items():
            nota, letra, observacion = datos
            self.cell(60, 8, categoria, 1)
            self.cell(30, 8, str(nota), 1, 0, "C")
            self.cell(30, 8, letra, 1, 0, "C")
            self.multi_cell(70, 8, observacion, 1)

    def seccion_final(self, nota_media, letra_media, observaciones_generales):
        self.ln(5)
        self.set_font("Arial", "B", 11)
        self.cell(50, 8, f"Nota media: {nota_media} ({letra_media})", ln=True)
        self.ln(2)
        self.cell(0, 8, "Observaciones generales / Justificación", ln=True)
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 8, observaciones_generales)

# Streamlit UI
st.title("Formulario de Evaluación")

informante = st.text_input("Informante")
fecha = st.date_input("Fecha").strftime("%d.%m.%Y")
alumno = st.text_input("Alumno")
puesto = st.text_input("Puesto")

st.markdown("### Evaluación por Categoría")

resultados = {}
total = 0

for cat in categorias:
    st.subheader(cat)
    nota = st.slider(f"Nota (1-10) para {cat}", 1, 10, 5, key=f"{cat}_nota")
    letra = nota_a_letra(nota)
    observacion = st.text_area(f"Observaciones para {cat}", key=f"{cat}_obs")
    resultados[cat] = (nota, letra, observacion)
    total += nota

nota_media = round(total / len(categorias), 2)
letra_media = nota_a_letra(nota_media)

st.markdown("### Observaciones generales / Justificación")
obs_general = st.text_area("Escribe aquí tus observaciones generales")

if st.button("Generar PDF"):
    pdf = InformePDF()
    pdf.add_page()
    pdf.encabezado(informante, fecha, alumno, puesto)
    pdf.tabla_categorias(resultados)
    pdf.seccion_final(nota_media, letra_media, obs_general)

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)

    st.download_button(
        label="📥 Descargar Informe en PDF",
        data=buffer,
        file_name=f"Informe_{alumno}.pdf",
        mime="application/pdf"
    )

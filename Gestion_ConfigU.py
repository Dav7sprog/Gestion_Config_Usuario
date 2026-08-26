from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    Image, ListFlowable, ListItem, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

OUT = "/home/claude/lab1_config_app/Documento_Laboratorio1.pdf"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TituloPortada", fontSize=20, leading=26, alignment=TA_CENTER, spaceAfter=6, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="SubtituloPortada", fontSize=13, leading=18, alignment=TA_CENTER, textColor=colors.HexColor("#444444")))
styles.add(ParagraphStyle(name="H1", fontSize=15, leading=19, spaceBefore=16, spaceAfter=8, fontName="Helvetica-Bold", textColor=colors.HexColor("#1a3d63")))
styles.add(ParagraphStyle(name="H2", fontSize=12.5, leading=16, spaceBefore=10, spaceAfter=6, fontName="Helvetica-Bold", textColor=colors.HexColor("#2c3e50")))
styles.add(ParagraphStyle(name="Cuerpo", fontSize=10.3, leading=14.5, alignment=TA_JUSTIFY, spaceAfter=6))
styles.add(ParagraphStyle(name="CodeBlock", fontName="Courier", fontSize=8, leading=10.2, backColor=colors.HexColor("#f4f4f4"), borderPadding=6, leftIndent=4))

def code_block(text):
    return Paragraph(text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>").replace(" ", "&nbsp;"), styles["CodeBlock"])

story = []

story.append(Spacer(1, 3*cm))
story.append(Paragraph("Universidad Rafael Landívar", styles["SubtituloPortada"]))
story.append(Paragraph("Campus San Alberto Hurtado, S.J. — Quetzaltenango", styles["SubtituloPortada"]))
story.append(Paragraph("Facultad de Ingeniería — Ingeniería en Informática y Sistemas", styles["SubtituloPortada"]))
story.append(Spacer(1, 2*cm))
story.append(Paragraph("Laboratorio No. 1", styles["TituloPortada"]))
story.append(Paragraph("Manejo e Implementación de Archivos", styles["TituloPortada"]))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("Aplicación de Escritorio con Gestión de Configuración de Usuario", styles["SubtituloPortada"]))
story.append(Spacer(1, 3*cm))
story.append(Paragraph("Agosto de 2026", styles["SubtituloPortada"]))
story.append(PageBreak())

story.append(Paragraph("1. Formato de almacenamiento elegido y justificación", styles["H1"]))
story.append(Paragraph(
    "Se eligió <b>JSON</b> (JavaScript Object Notation) como formato de almacenamiento del "
    "archivo de configuración de usuario. A continuación se compara contra <b>XML</b>, la "
    "alternativa descartada, usando los criterios técnicos solicitados.", styles["Cuerpo"]))

tabla_datos = [
    ["Criterio", "JSON (elegido)", "XML (descartado)"],
    ["Tamaño del archivo", "Muy compacto: solo pares clave-valor,\nsin etiquetas de apertura/cierre repetidas.",
     "Más pesado: cada valor requiere\netiqueta de apertura y de cierre."],
    ["Legibilidad humana", "Alta; estructura anidada clara y\nmenos ruido visual.",
     "Aceptable, pero más verboso y con\nmás caracteres de marcado."],
    ["Facilidad de parseo\nen Python", "Nativo: módulo json de la\nbiblioteca estándar (json.load /\njson.dump), sin dependencias extra.",
     "Requiere xml.etree.ElementTree u\notra librería, y mapear manualmente\nnodos a un diccionario de configuración."],
    ["Robustez ante\ncorrupción", "Un JSON mal formado falla de forma\npredecible con json.JSONDecodeError,\nfácil de capturar y manejar.",
     "Un XML mal formado también falla,\npero el árbol de nodos es más\npropenso a errores de anidamiento\ny cierre de etiquetas."],
    ["Soporte de tipos", "Soporta nativamente string, número,\nbooleano, listas y objetos anidados,\nsuficiente para esta configuración.",
     "Todo es texto; tipos como enteros\no booleanos deben convertirse\nmanualmente."],
    ["Adecuación al\ncaso de uso", "Ideal para configuraciones planas\no poco anidadas como esta (7 campos\nsimples).", "Más apropiado para documentos con\nmetadatos, atributos y esquemas de\nvalidación complejos (XSD), lo cual\nes innecesario aquí."],
]
t = Table(tabla_datos, colWidths=[3.4*cm, 6.3*cm, 6.3*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1a3d63")),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 8.3),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f7f9fb")]),
    ("LEFTPADDING", (0,0), (-1,-1), 5),
    ("RIGHTPADDING", (0,0), (-1,-1), 5),
    ("TOPPADDING", (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
]))
story.append(t)
story.append(Spacer(1, 8))
story.append(Paragraph(
    "<b>Conclusión:</b> para un archivo de configuración plano de 7 campos, sin necesidad de "
    "validación por esquema ni de espacios de nombres, JSON ofrece menor tamaño, parseo nativo "
    "en Python con manejo de errores predecible (json.JSONDecodeError) y mayor legibilidad, por "
    "lo que resulta la opción técnicamente más adecuada frente a XML.", styles["Cuerpo"]))

story.append(Paragraph("2. Implementación de la escritura segura y el respaldo", styles["H1"]))
story.append(Paragraph(
    "El guardado nunca sobrescribe <font face='Courier'>config.json</font> directamente. El flujo "
    "implementado en <font face='Courier'>ConfigManager.guardar()</font> es:", styles["Cuerpo"]))
story.append(ListFlowable([
    ListItem(Paragraph("Se valida que exista permiso de escritura en la carpeta destino.", styles["Cuerpo"])),
    ListItem(Paragraph("Se serializa la configuración completa a <font face='Courier'>config.json.tmp</font> "
                        "(UTF-8, con <font face='Courier'>ensure_ascii=False</font> para no escapar tildes/ñ), "
                        "seguido de <font face='Courier'>flush()</font> y <font face='Courier'>os.fsync()</font> "
                        "para forzar la escritura física a disco.", styles["Cuerpo"])),
    ListItem(Paragraph("Si ya existía un <font face='Courier'>config.json</font> anterior, se copia a "
                        "<font face='Courier'>config.json.bak</font> ANTES de reemplazar (respaldo).", styles["Cuerpo"])),
    ListItem(Paragraph("Se reemplaza el archivo final con <font face='Courier'>os.replace(tmp, final)</font>, "
                        "operación atómica del sistema operativo: si el proceso se interrumpe abruptamente "
                        "en cualquier punto anterior al replace, el config.json original permanece intacto; "
                        "y una vez iniciado el replace, este no queda en un estado intermedio observable.", styles["Cuerpo"])),
], bulletType="1"))

story.append(Paragraph("Fragmento de código relevante (config_manager.py):", styles["H2"]))
story.append(code_block(
"""def guardar(self, config: UserConfig) -> None:
    carpeta = os.path.dirname(os.path.abspath(self.config_path)) or "."
    os.makedirs(carpeta, exist_ok=True)

    if not os.access(carpeta, os.W_OK):
        raise ConfigPermisosError(
            f"No se tienen permisos de escritura en la carpeta '{carpeta}'."
        )

    # 1) Escritura a archivo temporal (UTF-8 explicito)
    with open(self.tmp_path, "w", encoding="utf-8") as f:
        json.dump(config.to_dict(), f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())

    # 2) Respaldo del archivo anterior ANTES de reemplazar
    if os.path.exists(self.config_path):
        shutil.copy2(self.config_path, self.bak_path)

    # 3) Reemplazo atomico: config.tmp -> config.json
    os.replace(self.tmp_path, self.config_path)"""
))
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Gestion_ConfigU import ConfigManager, UserConfig
from ventana import SettingsWindow

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "config.json")
CONFIG_PATH = os.path.abspath(CONFIG_PATH)

TEMAS = {
    "claro": {"bg": "#f5f5f5", "fg_default": "#000000"},
    "oscuro": {"bg": "#1e1e1e", "fg_default": "#f0f0f0"},
}


class AplicacionPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicación de Escritorio - Gestión de Configuración")
        self.geometry("720x480")

        self.config_manager = ConfigManager(CONFIG_PATH)
        self.config_actual, mensaje_carga = self.config_manager.cargar()

        self._construir_menu()
        self._construir_cuerpo()
        self._aplicar_config_visual()

        self.after(200, lambda: self._mostrar_estado_carga(mensaje_carga))

    def _construir_menu(self):
        barra = tk.Menu(self)

        menu_archivo = tk.Menu(barra, tearoff=0)
        menu_archivo.add_command(label="Nuevo (simulado)")
        menu_archivo.add_command(label="Abrir (simulado)")
        menu_archivo.add_command(label="Guardar (simulado)")
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.destroy)
        barra.add_cascade(label="Archivo", menu=menu_archivo)

        menu_edicion = tk.Menu(barra, tearoff=0)
        menu_edicion.add_command(label="Cortar (simulado)")
        menu_edicion.add_command(label="Copiar (simulado)")
        menu_edicion.add_command(label="Pegar (simulado)")
        barra.add_cascade(label="Edición", menu=menu_edicion)

        menu_ver = tk.Menu(barra, tearoff=0)
        menu_ver.add_command(label="Zoom + (simulado)")
        menu_ver.add_command(label="Zoom - (simulado)")
        barra.add_cascade(label="Ver", menu=menu_ver)

        menu_settings = tk.Menu(barra, tearoff=0)
        menu_settings.add_command(label="Abrir Settings...", command=self._abrir_settings)
        barra.add_cascade(label="Settings", menu=menu_settings)

        self.config(menu=barra)

    def _construir_cuerpo(self):
        self.frame_cuerpo = tk.Frame(self)
        self.frame_cuerpo.pack(fill="both", expand=True)

        self.lbl_bienvenida = tk.Label(self.frame_cuerpo, text="", pady=20)
        self.lbl_bienvenida.pack()

        self.lbl_detalle = tk.Label(self.frame_cuerpo, text="", justify="left")
        self.lbl_detalle.pack(pady=6)

        self.lbl_foto = tk.Label(self.frame_cuerpo, text="")
        self.lbl_foto.pack(pady=10)

    def _aplicar_config_visual(self):
        cfg = self.config_actual
        tema = TEMAS.get(cfg.tema_interfaz, TEMAS["claro"])

        self.frame_cuerpo.configure(bg=tema["bg"])
        self.lbl_bienvenida.configure(
            text=f"Bienvenido/a, {cfg.nombre_usuario}",
            bg=tema["bg"], fg=cfg.color_letra,
            font=("TkDefaultFont", cfg.tamano_fuente, "bold"),
        )
        self.lbl_detalle.configure(
            text=(
                f"Idioma: {cfg.idioma}\n"
                f"Tema: {cfg.tema_interfaz}\n"
                f"Tamaño de fuente: {cfg.tamano_fuente}"
            ),
            bg=tema["bg"], fg=cfg.color_letra,
            font=("TkDefaultFont", cfg.tamano_fuente),
        )

        foto_txt = os.path.basename(cfg.foto_perfil) if cfg.foto_perfil else "(sin foto de perfil)"
        self.lbl_foto.configure(text=f"Foto de perfil: {foto_txt}", bg=tema["bg"], fg=cfg.color_letra)

        if hasattr(self, "franja_menu"):
            self.franja_menu.destroy()
        self.franja_menu = tk.Frame(self, bg=cfg.color_barra_menu, height=8)
        self.franja_menu.pack(side="top", fill="x")

    def _mostrar_estado_carga(self, mensaje: str):
        if "correctamente" not in mensaje:
            messagebox.showwarning("Carga de configuración", mensaje)

    def _abrir_settings(self):
        SettingsWindow(
            self, self.config_manager, self.config_actual, on_saved=self._on_settings_guardado
        )

    def _on_settings_guardado(self, nueva_config: UserConfig):
        self.config_actual = nueva_config
        self._aplicar_config_visual()


if __name__ == "__main__":
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    app = AplicacionPrincipal()
    app.mainloop()

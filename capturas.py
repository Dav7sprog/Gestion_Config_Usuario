import sys, os, time, subprocess
sys.path.insert(0, "/home/claude/lab1_config_app/src")
os.environ["DISPLAY"] = ":99"

import main as appmod
from ventana import SettingsWindow

OUT = "/home/claude/lab1_config_app/screenshots"
os.makedirs(OUT, exist_ok=True)


def capture(win_id_getter, filename):
    time.sleep(0.6)
    win_id = win_id_getter()
    subprocess.run(["import", "-window", str(win_id), os.path.join(OUT, filename)], check=True)


application = appmod.AplicacionPrincipal()
application.update_idletasks()
application.update()
time.sleep(0.5)
application.update()

wid = application.winfo_id()
capture(lambda: wid, "01_ventana_principal.png")

settings = SettingsWindow(application, application.config_manager, application.config_actual, on_saved=application._on_settings_guardado)
settings.update_idletasks()
settings.update()
time.sleep(0.5)
settings.update()
swid = settings.winfo_id()
capture(lambda: swid, "02_settings.png")

settings.destroy()
application.update()
time.sleep(0.3)

print("Capturas listas.")
application.destroy()

import os
import sys
import builtins
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from Gestion_ConfigU import ConfigManager, UserConfig, ConfigPermisosError, ConfigError

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
DATA_DIR = os.path.abspath(DATA_DIR)
CONFIG_PATH = os.path.join(DATA_DIR, "config.json")


def separador(titulo):
    print("\n" + "=" * 70)
    print(titulo)
    print("=" * 70)


def limpiar():
    for p in [CONFIG_PATH, CONFIG_PATH + ".bak", CONFIG_PATH + ".tmp"]:
        if os.path.exists(p):
            os.chmod(p, 0o644)
            os.remove(p)


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    limpiar()
    cm = ConfigManager(CONFIG_PATH)

    separador("CASO 1: Archivo ausente (primer arranque de la app)")
    cfg, msg = cm.cargar()
    print("Mensaje:", msg)
    print("Config obtenida (valores por defecto):", cfg)

    separador("GUARDADO NORMAL con caracteres acentuados y ñ (evidencia UTF-8)")
    cfg_usuario = UserConfig(
        nombre_usuario="José Ángel Muñoz Pérez",
        tema_interfaz="oscuro",
        idioma="es-ES",
        tamano_fuente=14,
        color_barra_menu="#34495e",
        color_letra="#ecf0f1",
        foto_perfil="/home/usuario/fotos/perfil_josé.png",
    )
    cm.guardar(cfg_usuario)
    print("Guardado exitoso. Contenido de config.json:")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        print(f.read())

    separador("SEGUNDO GUARDADO (genera config.bak con la versión anterior)")
    cfg_usuario2 = UserConfig(
        nombre_usuario="María José Ñíguez",
        tema_interfaz="claro",
        idioma="es",
        tamano_fuente=16,
        color_barra_menu="#2c3e50",
        color_letra="#111111",
        foto_perfil="/home/usuario/fotos/perfil2.png",
    )
    cm.guardar(cfg_usuario2)
    print("config.json actualizado. Existe config.bak?:", os.path.exists(cm.bak_path))
    print("Contenido de config.bak (respaldo del guardado anterior):")
    with open(cm.bak_path, "r", encoding="utf-8") as f:
        print(f.read())
    separador("CASO 2: Archivo corrupto / formato inválido")
    cm.simular_archivo_corrupto()
    print("Contenido forzado a JSON inválido en config.json.")
    cfg_recuperada, msg = cm.cargar()
    print("Mensaje:", msg)
    print("Config obtenida tras recuperación:", cfg_recuperada)

    cm.guardar(cfg_usuario2)

    separador("CASO 3: Falta de permisos de lectura (intento real con chmod 0o000)")
    cm.simular_sin_permisos()
    print("Permisos del archivo puestos en 0o000 (sin lectura/escritura).")
    try:
        cfg_sin_permiso, msg = cm.cargar()
        print("Mensaje:", msg)
        print("Config obtenida:", cfg_sin_permiso)
        print(
            "NOTA: en este entorno de pruebas el proceso corre como root, por lo\n"
            "que el sistema operativo IGNORA los bits de permisos (root puede leer\n"
            "cualquier archivo). Por eso a continuación se fuerza el mismo error\n"
            "mediante una prueba controlada (mock), que sí ejercita la rama de\n"
            "código 'except PermissionError' de forma determinística."
        )
    finally:
        cm.restaurar_permisos()

    separador("CASO 3 (simulado con mock): PermissionError real al LEER")
    real_open = builtins.open

    def open_que_falla(path, *args, **kwargs):
        if path == CONFIG_PATH and "r" in args[0] if args else True:
            raise PermissionError("[Errno 13] Permission denied (simulado)")
        return real_open(path, *args, **kwargs)

    with mock.patch("builtins.open", side_effect=PermissionError("[Errno 13] Permission denied (simulado)")):
        cfg_sim, msg = cm.cargar()
    print("Mensaje:", msg)
    print("Config obtenida (degradado a valores por defecto):", cfg_sim)

    separador("CASO 3b (simulado con mock): PermissionError real al ESCRIBIR")
    with mock.patch("builtins.open", side_effect=PermissionError("[Errno 13] Permission denied (simulado)")):
        try:
            cm.guardar(cfg_usuario2)
            print("ERROR: se esperaba una excepción de permisos y no ocurrió.")
        except ConfigPermisosError as e:
            print("Excepción controlada correctamente ->", e)

    separador("GUARDADO FINAL (deja config.json y config.json.bak limpios como ejemplo de entrega)")
    cm.guardar(cfg_usuario) 
    cm.guardar(cfg_usuario2)
    os.chmod(CONFIG_PATH, 0o644)
    print("config.json final:")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        print(f.read())
    print("\nconfig.json.bak final:")
    with open(cm.bak_path, "r", encoding="utf-8") as f:
        print(f.read())

    separador("FIN DE LAS PRUEBAS")
    print("Revise el log detallado en:", os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.log"))


if __name__ == "__main__":
    main()

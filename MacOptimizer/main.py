import os
import subprocess


def ejecutar_comando_sudo(comando):
    """Ejecuta un comando con privilegios sudo."""
    try:
        # Solicitar la contraseña de sudo para ejecutar el comando
        print(f"Ejecutando comando con sudo: {' '.join(comando)}")
        proceso = subprocess.Popen(['sudo', '-S'] + comando, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        # Asegúrate de introducir la contraseña aquí si la quieres automatizar (no recomendado por seguridad)
        # Si deseas que el script pida la contraseña interactiva, puedes ejecutarlo desde la terminal con 'sudo python3 script.py'

        # A continuación se permite que el usuario ingrese la contraseña manualmente
        # Si prefieres, puedes comentar la siguiente línea y seguir la Opción 2
        proceso.communicate(input=b'YOUR_PASSWORD\n')  # Sustituye YOUR_PASSWORD por tu contraseña

        print(f"Comando ejecutado exitosamente: {' '.join(comando)}")
    except Exception as e:
        print(f"Error al ejecutar el comando sudo: {e}")


def limpiar_cache():
    print("Limpiando caché de aplicaciones...")
    cache_dirs = [
        "/Library/Caches/",
        "/Users/tu_usuario/Library/Caches/"
    ]
    for cache_dir in cache_dirs:
        try:
            for root, dirs, files in os.walk(cache_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
            print(f"Cache en {cache_dir} eliminada.")
        except Exception as e:
            print(f"Error al limpiar cache: {e}")


def limpiar_archivos_temporales():
    print("Limpiando archivos temporales del sistema...")
    temp_dir = "/private/tmp/"
    try:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
        print(f"Archivos temporales en {temp_dir} eliminados.")
    except Exception as e:
        print(f"Error al limpiar archivos temporales: {e}")


def reparar_permisos():
    print("Reparando permisos del sistema...")
    try:
        # Ejecuta el comando diskutil repairPermissions con sudo
        ejecutar_comando_sudo(['diskutil', 'repairPermissions', '/'])
        print("Permisos reparados exitosamente.")
    except Exception as e:
        print(f"Error al reparar permisos: {e}")


def eliminar_archivos_grandes():
    print("Buscando y eliminando archivos grandes no necesarios...")
    dirs_to_check = ["/Users/tu_usuario", "/Library", "/private"]
    for directory in dirs_to_check:
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.getsize(file_path) > 500 * 1024 * 1024:  # Archivos mayores a 500MB
                        print(f"Eliminando archivo grande: {file_path}")
                        os.remove(file_path)
            print(f"Archivos grandes en {directory} eliminados.")
        except Exception as e:
            print(f"Error al eliminar archivos grandes: {e}")


def optimizar_sistema():
    print("Optimizando el sistema de archivos...")
    try:
        # Ejecuta el comando diskutil repairVolume con sudo
        ejecutar_comando_sudo(['diskutil', 'repairVolume', '/'])
        print("Sistema de archivos optimizado.")
    except Exception as e:
        print(f"Error al optimizar el sistema de archivos: {e}")


def cerrar_procesos_innecesarios():
    print("Cerrando procesos innecesarios...")
    try:
        result = subprocess.run(['ps', '-e', '-o', 'pid,comm'], capture_output=True, text=True)
        processes = result.stdout.splitlines()
        for process in processes:
            pid, name = process.split()
            if "name_del_proceso_no_deseado" in name:  # Reemplazar con el nombre del proceso a cerrar
                subprocess.run(['kill', pid])
                print(f"Proceso {name} (PID {pid}) cerrado.")
    except Exception as e:
        print(f"Error al cerrar procesos: {e}")


if __name__ == "__main__":
    # Llamar las funciones para optimizar el sistema
    limpiar_cache()
    limpiar_archivos_temporales()
    reparar_permisos()
    eliminar_archivos_grandes()
    optimizar_sistema()
    cerrar_procesos_innecesarios()
    print("Optimización del sistema completada.")
import sqlite3
from sqlite3 import Error

# Conexion a la base de datos SQLite
def create_connection():
    try:
        conn = sqlite3.connect('recetario.db')
        return conn
    except Error as e:
        print(e)
    return None

# Crear tablas si no existen
def create_tables(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS recta (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          nombre TEXT NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS ingrdnt (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          recta_id INTEGER NOT NULL,
                          nombre TEXT NOT NULL,
                          FOREIGN KEY(recta_id) REFERENCES recta(id))''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS paso (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          recta_id INTEGER NOT NULL,
                          descripcion TEXT NOT NULL,
                          FOREIGN KEY(recta_id) REFERENCES recta(id))''')
        conn.commit()
    except Error as e:
        print(e)

# Agregar una nueva rect.
def agregar_rect(conn):
    nombre = input("Introduce el nombre de la rect: ")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO recta (nombre) VALUES (?)', (nombre,))
    recta_id = cursor.lastrowid
    conn.commit()

    print("\n--- Ingredientes ---")
    while True:
        ingrdnt = input("Introduce un ingrdnt (deja vacio pa' terminar): ")
        if ingrdnt == "":
            break
        cursor.execute('INSERT INTO ingrdnt (recta_id, nombre) VALUES (?, ?)', (recta_id, ingrdnt))
        conn.commit()

    print("\n--- Pasos ---")
    while True:
        paso = input("Introduce un paso (deja vacio pa' terminar): ")
        if paso == "":
            break
        cursor.execute('INSERT INTO paso (recta_id, descripcion) VALUES (?, ?)', (recta_id, paso))
        conn.commit()

# Ver el listado de rect.
def ver_rects(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre FROM recta')
    rects = cursor.fetchall()
    if rects:
        print("\n--- Listado de rect. ---")
        for rect in rects:
            print(f"{rect[0]}. {rect[1]}")
    else:
        print("No hay rects registradas.")

# Buscar ingrdnts y pasos de una recta sin pedir ID
def buscar_rect(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre FROM recta')
    rects = cursor.fetchall()

    if not rects:
        print("No hay rects registradas.")
        return

    # Mostrar todas las rects y permitir elegir una
    print("\n--- Selecciona una recta pa' ver los detalles ---")
    for rect in rects:
        print(f"{rect[0]}. {rect[1]}")

    try:
        recta_id = int(input("\nSelecciona el num de la rect que deseas consultar: "))
        cursor.execute('SELECT nombre FROM recta WHERE id=?', (recta_id,))
        rect = cursor.fetchone()

        if rect:
            print(f"\nRecta: {rect[0]}")

            # Mostrar ingrdnts de la rect seleccionada
            cursor.execute('SELECT nombre FROM ingrdnt WHERE recta_id=?', (recta_id,))
            ingrdnts = cursor.fetchall()
            print("\n--- Ingredientes ---")
            if ingrdnts:
                for ingrdnt in ingrdnts:
                    print(ingrdnt[0])
            else:
                print("No hay ingrdnts registrados pa' esta rect.")

            # Mostrar pasos de la rect seleccionada
            cursor.execute('SELECT descripcion FROM paso WHERE recta_id=?', (recta_id,))
            pasos = cursor.fetchall()
            print("\n--- Pasos ---")
            if pasos:
                for paso in pasos:
                    print(paso[0])
            else:
                print("No hay pasos registrados pa' esta rect.")
        else:
            print("No se encontro una rect con ese ID.")

    except ValueError:
        print("Introduce un num valido.")

# Actualizar una rect.
def actualizar_rect(conn):
    recta_id = input("Introduce el ID de la rect a actualizar: ")
    nuevo_nombre = input("Introduce el nuevo nombre de la rect: ")
    cursor = conn.cursor()
    cursor.execute('UPDATE recta SET nombre=? WHERE id=?', (nuevo_nombre, recta_id))
    conn.commit()
    print("Rect actualizada correctamente.")

# Eliminar una rect.
def eliminar_rect(conn):
    recta_id = input("Introduce el ID de la rect a eliminar: ")
    cursor = conn.cursor()
    cursor.execute('DELETE FROM recta WHERE id=?', (recta_id,))
    cursor.execute('DELETE FROM ingrdnt WHERE recta_id=?', (recta_id,))
    cursor.execute('DELETE FROM paso WHERE recta_id=?', (recta_id,))
    conn.commit()
    print("Rect eliminada correctamente.")

# Menu de opciones
def menu():
    conn = create_connection()
    create_tables(conn)

    while True:
        print("\n--- Menu ---")
        print("a) Agregar nueva recta")
        print("b) Ver listado de rects")
        print("c) Actualizar receta existente")
        print("d) Eliminar receta existente")
        print("e) Buscar ingredientesy pasos de recetas")
        print("f) Salir")

        opcion = input("Selecciona una opcion: ").lower()

        if opcion == 'a':
            agregar_rect(conn)
        elif opcion == 'b':
            ver_rects(conn)
        elif opcion == 'c':
            actualizar_rect(conn)
        elif opcion == 'd':
            eliminar_rect(conn)
        elif opcion == 'e':
            buscar_rect(conn)
        elif opcion == 'f':
            conn.close()
            print("Saliendo del programa.")
            break
        else:
            print("Opcion no valida, intenta de nuevo.")

# Ejecucion del programa
if __name__ == "__main__":
    menu()

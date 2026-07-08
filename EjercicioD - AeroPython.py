def procesar_ruta(ruta, matriz):
    # Escribe aquí tu lógica para recorrer la ruta ingresada.
    # Debes verificar si es factible y calcular el costo total.
    # Si la ruta no es factible, imprime el mensaje correspondiente.

    # --- TIPS IMPORTANTES ---
    # 1. Tipos de dato: Los elementos de 'ruta' son texto (ej: "0", "1"). 
    #    Para usarlos como índices en la matriz, recuerda convertirlos a enteros con int().
    #
    # 2. Salida anticipada: Puedes usar 'return' (sin nada más) para detener 
    #    y salir de la función inmediatamente en cuanto detectes un error.
    #    Ejemplo:
    #        if vuelo_no_existe:
    #            print("Ruta no factible")
    #            return
    # ------------------------
    
    # --- INICIO DE TU CÓDIGO ---
    
    
    
    # --- FIN DE TU CÓDIGO ---

# ==========================================
# BLOQUE PRINCIPAL (MAIN)
# ==========================================
if __name__ == "__main__":
    # Matriz de vuelos (No modificar)
    matriz_vuelos = [
        [ 0,  5, -1,  7, -1],
        [-1,  0, -1, -1,  2],
        [-1,  8,  0,  4, -1],
        [-1, -1,  4,  0, -1],
        [-1,  3,  5, -1,  0]
    ]
    
    # Solicitud de los datos al usuario
    ruta_ingresada = input("Ingrese ruta de ciudades: ")
    
    # Llamado a la función
    procesar_ruta(ruta_ingresada, matriz_vuelos)
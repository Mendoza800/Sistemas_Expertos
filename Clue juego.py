# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 15:48:13 2025

@author: usr
"""

# -*- coding: utf-8 -*-
"""
Juego Simulador de CLUE (Versión 2.1 con Investigación y Repetir Juego)

Este script simula el juego de mesa Clue, incorporando la mecánica
clave de "suposiciones" para investigar.

REGLAS DE ESTA SIMULACIÓN:
1.  Se definen 5 personajes, 5 armas y 5 locaciones.
2.  Se definen 5 HISTORIAS (combinaciones exactas).
3.  El juego elige 1 de las 5 historias al azar como la SOLUCIÓN SECRETA.
4.  El resto de las cartas (12) se reparten entre el jugador y 2 BOTS.
5.  El jugador puede "Moverse" (elegir una locación) para hacer una "Suposición".
6.  Los BOTS responderán si tienen alguna de las cartas de la suposición.
7.  El jugador usa esta información para deducir la solución.
8.  Cuando el jugador está seguro, puede hacer una "Acusación Final".
9.  Al terminar, el jugador puede elegir jugar de nuevo.
"""

import random
import time
import os

# --- 1. Definición de Componentes ---

# 5 Personajes (Nombre y Profesión)
PERSONAJES = {
    "Profesor Morales": "Arqueólogo",
    "Doña Elvira": "Heredera",
    "Dr. Fausto": "Médico",
    "Sargento Ramírez": "Policía retirado",
    "Señorita Amapola": "Actriz"
}

# 5 Locaciones
LOCACIONES = [
    "La Biblioteca",
    "El Salón de Baile",
    "El Conservatorio",
    "La Cocina",
    "El Sótano"
]

# 5 Armas
ARMAS = [
    "El Candelabro",
    "La Daga",
    "La Cuerda",
    "El Veneno",
    "La Llave Inglesa"
]

# --- 2. Definición de las 5 Historias (Finales) ---
# El juego elegirá UNA de estas como la solución.

HISTORIAS = [
    {
        "culpable": "Señorita Amapola",
        "arma": "La Daga",
        "lugar": "El Salón de Baile",
        "narrativa": (
            "La Señorita Amapola, en un arrebato de celos tras una discusión "
            "sobre el papel principal, usó la Daga (utilería de su última obra) "
            "en el Salón de Baile, escondiendo el cuerpo detrás del gran piano."
        )
    },
    {
        "culpable": "Dr. Fausto",
        "arma": "El Veneno",
        "lugar": "La Cocina",
        "narrativa": (
            "El Dr. Fausto, temiendo que la víctima revelara su mala praxis médica, "
            "preparó un té con Veneno en la Cocina y se lo ofreció amablemente, "
            "observando cómo su problema desaparecía silenciosamente."
        )
    },
    {
        "culpable": "Profesor Morales",
        "arma": "El Candelabro",
        "lugar": "La Biblioteca",
        "narrativa": (
            "El Profesor Morales fue descubierto falsificando un hallazgo arqueológico. "
            "Para silenciar a la víctima, usó lo primero que encontró en la "
            "Biblioteca: el pesado Candelabro de bronce."
        )
    },
    {
        "culpable": "Sargento Ramírez",
        "arma": "La Llave Inglesa",
        "lugar": "El Sótano",
        "narrativa": (
            "El Sargento Ramírez, acorralado por una vieja deuda de juego, "
            "citó a la víctima en el Sótano con la excusa de revisar la caldera. "
            "La discusión escaló y usó una Llave Inglesa de la caja de herramientas."
        )
    },
    {
        "culpable": "Doña Elvira",
        "arma": "La Cuerda",
        "lugar": "El Conservatorio",
        "narrativa": (
            "Doña Elvira, impaciente por recibir su herencia y cansada de ser "
            "ignorada, atrajo a la víctima al Conservatorio con la excusa de "
            "ver las raras orquídeas. Allí, usó la Cuerda del viejo tendedero."
        )
    }
]

# --- 3. Funciones Auxiliares ---

def limpiar_pantalla():
    """Limpia la consola para mayor legibilidad."""
    # 'nt' es para Windows, 'posix' para Mac/Linux
    os.system('cls' if os.name == 'nt' else 'clear')

def elegir_opcion(opciones, tipo_seleccion, solicitar_profesion=False):
    """
    Muestra un menú de opciones y pide al usuario que elija una.
    Si 'solicitar_profesion' es True, usa el diccionario PERSONAJES.
    """
    print(f"\n--- Selecciona un {tipo_seleccion} ---")
    
    lista_opciones = []
    if solicitar_profesion:
        for nombre, profesion in opciones.items():
            lista_opciones.append(f"{nombre} ({profesion})")
    else:
        lista_opciones = list(opciones) # Convertir dict_keys a lista si es necesario
    
    # Mostrar menú
    for i, opcion in enumerate(lista_opciones, 1):
        print(f"  {i}. {opcion}")
    
    # Validar entrada
    while True:
        try:
            eleccion = int(input(f"\nElige el número (1-{len(lista_opciones)}): "))
            if 1 <= eleccion <= len(lista_opciones):
                # Si era un diccionario, devolvemos solo la llave (el nombre)
                if solicitar_profesion:
                    return list(opciones.keys())[eleccion-1]
                else:
                    return lista_opciones[eleccion-1]
            else:
                print(f"Error: Debes elegir un número entre 1 y {len(lista_opciones)}.")
        except ValueError:
            print("Error: Por favor, introduce solo un número.")

def mostrar_hoja_pistas(hoja_pistas):
    """Muestra el estado actual de la hoja de pistas del jugador."""
    print("\n--- HOJA DE PISTAS (Detective) ---")
    
    print("\n[ PERSONAJES ]")
    for personaje in PERSONAJES.keys():
        print(f"  - {personaje:<20} : {hoja_pistas[personaje]}")
        
    print("\n[ ARMAS ]")
    for arma in ARMAS:
        print(f"  - {arma:<20} : {hoja_pistas[arma]}")
        
    print("\n[ LOCACIONES ]")
    for locacion in LOCACIONES:
        print(f"  - {locacion:<20} : {hoja_pistas[locacion]}")
    print("-------------------------------------")

# --- 4. Funciones Principales del Juego ---

def hacer_suposicion(hoja_pistas, mano_bot1, mano_bot2):
    """
    Mecánica de investigación. El jugador hace una suposición
    y los BOTS la refutan si pueden.
    """
    print("\n--- Hacer una Suposición ---")
    print("Debes moverte a una locación para investigar.")
    
    # 1. El jugador "se mueve" a una locación
    lugar_supuesto = elegir_opcion(LOCACIONES, "locación a la que te mueves")
    
    # 2. El jugador elige sospechoso y arma
    culpable_supuesto = elegir_opcion(PERSONAJES, "personaje", solicitar_profesion=True)
    arma_supuesta = elegir_opcion(ARMAS, "arma")
    
    suposicion = [culpable_supuesto, arma_supuesta, lugar_supuesto]
    
    print(f"\nTu suposición: 'Fue {culpable_supuesto} con {arma_supuesta} en {lugar_supuesto}'")
    print("Consultando a los otros jugadores...")
    time.sleep(2)
    
    # 3. Simular la respuesta de los BOTS (como en las reglas)
    
    # Bot 1 (a tu izquierda) revisa
    cartas_en_mano_bot1 = [carta for carta in suposicion if carta in mano_bot1]
    if cartas_en_mano_bot1:
        carta_mostrada = random.choice(cartas_en_mano_bot1)
        print(f"\n¡PISTA! El Bot 1 te muestra en secreto su carta: '{carta_mostrada}'")
        hoja_pistas[carta_mostrada] = "NO (Bot 1 la tiene)"
        return

    # Bot 2 revisa (solo si Bot 1 no tenía nada)
    cartas_en_mano_bot2 = [carta for carta in suposicion if carta in mano_bot2]
    if cartas_en_mano_bot2:
        carta_mostrada = random.choice(cartas_en_mano_bot2)
        print(f"\n¡PISTA! El Bot 2 te muestra en secreto su carta: '{carta_mostrada}'")
        hoja_pistas[carta_mostrada] = "NO (Bot 2 la tiene)"
        return

    # Si nadie tiene nada
    print("\n...Nadie pudo refutar tu suposición.")
    print("Esto es muy interesante... Quizás estas 3 cartas estén en el sobre...")
    print("O quizás tú tienes alguna de ellas.")

def hacer_acusacion_final(solucion_secreta):
    """Mecánica de victoria/derrota. El jugador hace una acusación final."""
    print("\n--- ACUSACIÓN FINAL ---")
    print("Esta es tu última oportunidad. Si fallas, el caso quedará cerrado.")
    
    culpable_final = elegir_opcion(PERSONAJES, "culpable", solicitar_profesion=True)
    arma_final = elegir_opcion(ARMAS, "arma")
    lugar_final = elegir_opcion(LOCACIONES, "locación")
    
    print(f"\nTu acusación final es: '{culpable_final} con {arma_final} en {lugar_final}'")
    print("Revisando el sobre secreto...")
    time.sleep(3)
    
    # Comprobar la acusación
    if (culpable_final == solucion_secreta["culpable"] and
        arma_final == solucion_secreta["arma"] and
        lugar_final == solucion_secreta["lugar"]):
        
        limpiar_pantalla()
        print("\n¡ACUSACIÓN CORRECTA! Ha resuelto el misterio.")
        print("==================================================")
        print("LA HISTORIA VERDADERA:")
        print(solucion_secreta["narrativa"])
        print("==================================================")
        return True # Victoria
    else:
        limpiar_pantalla()
        print("\n¡ACUSACIÓN INCORRECTA! El verdadero culpable ha escapado.")
        print("El caso ha quedado sin resolver...")
        print("\nLa solución correcta era:")
        print(f"Culpable: {solucion_secreta['culpable']}")
        print(f"Arma:     {solucion_secreta['arma']}")
        print(f"Lugar:    {solucion_secreta['lugar']}")
        return True # Fin del juego (derrota)

def jugar():
    """Loop principal del juego."""
    
    # --- Preparación del Juego ---
    limpiar_pantalla()
    print("======================================")
    print("    BIENVENIDO AL SIMULADOR DE CLUE   ")
    print("======================================")
    print("Preparando el misterio...")

    # 1. Elegir la solución (una de las 5 historias)
    solucion = random.choice(HISTORIAS)
    sobre_secreto = [solucion['culpable'], solucion['arma'], solucion['lugar']]
    
    # (Debug: Descomenta la siguiente línea si quieres ver la solución)
    # print(f"[DEBUG] Solución: {sobre_secreto}")

    # 2. Crear el mazo completo y repartir las cartas restantes
    mazo_completo = list(PERSONAJES.keys()) + ARMAS + LOCACIONES
    
    # Quitar las 3 cartas del sobre
    cartas_restantes = [carta for carta in mazo_completo if carta not in sobre_secreto]
    random.shuffle(cartas_restantes)
    
    # Repartir las 12 cartas restantes (4 para cada jugador de 3)
    mano_jugador = cartas_restantes[0:4]
    mano_bot1 = cartas_restantes[4:8]
    mano_bot2 = cartas_restantes[8:12]

    # 3. Preparar la hoja de pistas del jugador
    hoja_de_pistas = {}
    for item in mazo_completo:
        hoja_de_pistas[item] = "¿?" # Inicialmente no sabe nada

    # El jugador marca sus propias cartas (lo primero que haces en Clue)
    for carta in mano_jugador:
        hoja_de_pistas[carta] = "NO (Tú la tienes)"
        
    print("Se ha cometido un crimen. Se han repartido las pistas.")
    print("Estas son las cartas en tu mano (no pueden estar en el sobre):")
    for carta in mano_jugador:
        print(f"  - {carta}")
    print("\nPresiona Enter para comenzar tu primer turno...")
    input()
    
    # --- Comienza el Juego ---
    while True:
        limpiar_pantalla()
        mostrar_hoja_pistas(hoja_de_pistas)
        
        print("\n--- Es tu turno ---")
        print("¿Qué deseas hacer?")
        print("  1. Moverme y hacer una 'Suposición' (Investigar)")
        print("  2. Hacer una 'Acusación Final' (Resolver el caso)")
        
        opcion = ""
        while opcion not in ['1', '2']:
            opcion = input("Elige una opción (1 o 2): ")

        if opcion == '1':
            hacer_suposicion(hoja_de_pistas, mano_bot1, mano_bot2)
            
            # Simular turnos de los BOTS (solo texto)
            print("\n...Turno del Bot 1...")
            time.sleep(1.5)
            print("...Turno del Bot 2...")
            time.sleep(1.5)
            
            print("\nPresiona Enter para continuar con tu siguiente turno...")
            input()
            
        elif opcion == '2':
            if hacer_acusacion_final(solucion):
                break # Termina el juego (victoria o derrota)

    print("\n--- Fin del Juego ---")

# --- 5. Ejecutar el juego ---
if __name__ == "__main__":
    while True:
        jugar() # Llama a la función principal del juego
        
        # --- Preguntar si quiere jugar de nuevo ---
        respuesta = ""
        while respuesta not in ['s', 'si', 'sí', 'n', 'no']:
            respuesta = input("\n¿Quieres jugar otra partida? (s/n): ").lower().strip()
        
        if respuesta.startswith('n'):
            print("\n¡Gracias por jugar! Hasta la próxima.")
            break
        # Si la respuesta empieza con 's', el loop se repite
        # y llama a jugar() para una nueva partida.
        
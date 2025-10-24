import json
import os

# Nombre del archivo donde el Genio guarda su memoria
ARCHIVO_MEMORIA = 'conocimiento.json'

def cargar_conocimiento():
    """Carga la memoria del Genio desde un archivo JSON."""
    if os.path.exists(ARCHIVO_MEMORIA):
        with open(ARCHIVO_MEMORIA, 'r', encoding='utf-8') as f:
            print("... El Genio ha cargado sus recuerdos ...")
            return json.load(f)
    else:
        # Si no hay memoria guardada, empieza con estos conocimientos básicos.
        return [
            {'nombre': 'león', 'es_mamifero': True, 'vive_en_la_sabana': True, 'es_carnivoro': True, 'tiene_rayas': False, 'puede_volar': False},
            {'nombre': 'águila', 'es_mamifero': False, 'vive_en_la_sabana': False, 'es_carnivoro': True, 'tiene_rayas': False, 'puede_volar': True},
            {'nombre': 'pingüino', 'es_mamifero': False, 'vive_en_la_sabana': False, 'es_carnivoro': True, 'tiene_rayas': False, 'puede_volar': False},
            {'nombre': 'cebra', 'es_mamifero': True, 'vive_en_la_sabana': True, 'es_carnivoro': False, 'tiene_rayas': True, 'puede_volar': False},
            {'nombre': 'delfín', 'es_mamifero': True, 'vive_en_la_sabana': False, 'es_carnivoro': True, 'tiene_rayas': False, 'puede_volar': False},
        ]

def guardar_conocimiento(conocimiento_actualizado):
    """Guarda la memoria del Genio en el archivo JSON."""
    with open(ARCHIVO_MEMORIA, 'w', encoding='utf-8') as f:
        json.dump(conocimiento_actualizado, f, indent=4, ensure_ascii=False)
    print("... El Genio ha guardado un nuevo recuerdo ...")

def obtener_respuesta(pregunta):
    """Función para obtener una respuesta válida (s/n) del usuario."""
    while True:
        respuesta = input(f"{pregunta} (s/n): ").lower()
        if respuesta in ['s', 'si', 'sí']:
            return True
        elif respuesta in ['n', 'no']:
            return False
        else:
            print("Por favor, responde solo con 's' (sí) o 'n' (no).")

def aprender(candidatos_restantes, conocimiento_actual):
    """Función que se activa cuando el Genio no puede adivinar."""
    print("\¡Me rindo! Me has vencido... por ahora.")

    animal_incorrecto = None
    if len(candidatos_restantes) == 1:
        animal_incorrecto = candidatos_restantes[0]
        print(f"Mi última suposición hubiera sido: {animal_incorrecto['nombre'].capitalize()}")

    nombre_nuevo_animal = input("¿Cuál era el animal en el que estabas pensando?: ").lower()
    
    pregunta_distintiva = input(f"Por favor, escribe una pregunta de sí/no que diferencie a un '{nombre_nuevo_animal}' de un '{animal_incorrecto['nombre'] if animal_incorrecto else 'otro animal'}': ")
    
    respuesta_distintiva = obtener_respuesta(f"¿Y cuál sería la respuesta (s/n) para '{nombre_nuevo_animal}' a esa pregunta?")

    nuevo_animal = {}
    if animal_incorrecto:
        nuevo_animal = animal_incorrecto.copy()
    
    nuevo_animal['nombre'] = nombre_nuevo_animal
    
    clave_pregunta = pregunta_distintiva.lower().replace(" ", "_").replace("¿", "").replace("?", "")
    nuevo_animal[clave_pregunta] = respuesta_distintiva

    if animal_incorrecto:
        for animal in conocimiento_actual:
            if animal['nombre'] == animal_incorrecto['nombre']:
                animal[clave_pregunta] = not respuesta_distintiva
                break

    conocimiento_actual.append(nuevo_animal)
    guardar_conocimiento(conocimiento_actual) # ¡La parte más importante! Guardar el nuevo conocimiento.
    print("\n¡Gracias! He aprendido algo nuevo. ¡Juguemos de nuevo!\n")

def jugar():
    """Función principal del juego del Genio."""
    conocimiento = cargar_conocimiento()
    
    print("--- Genio Adivinador de Animales ---")
    print("Piensa en un animal y responde a mis preguntas. ¡Intentaré leer tu mente!")
    print(f"Actualmente conozco {len(conocimiento)} animales.")
    print("-------------------------------------")

    candidatos = conocimiento.copy()
    preguntas_hechas = set(['nombre'])

    while len(candidatos) > 1:
        # Estrategia de preguntas: encontrar la que mejor divida a los candidatos (simplificado)
        mejor_pregunta = None
        for animal in candidatos:
            for caracteristica in animal.keys():
                if caracteristica not in preguntas_hechas:
                    mejor_pregunta = caracteristica
                    break
            if mejor_pregunta:
                break
        
        if not mejor_pregunta:
            break

        preguntas_hechas.add(mejor_pregunta)
        
        pregunta_bonita = "¿Tu animal " + mejor_pregunta.replace("_", " ") + "?"
        
        respuesta_usuario = obtener_respuesta(pregunta_bonita.capitalize())

        candidatos = [c for c in candidatos if c.get(mejor_pregunta) == respuesta_usuario]

    if len(candidatos) == 1:
        suposicion = candidatos[0]['nombre']
        if obtener_respuesta(f"¡Ya sé! ¿Estás pensando en un {suposicion.capitalize()}?"):
            print("¡Sí! ¡Soy el mejor!")
        else:
            aprender(candidatos, conocimiento)
    else:
        aprender(candidatos, conocimiento)

if __name__ == "__main__":
    while True:
        jugar()
        if not obtener_respuesta("\n¿Quieres desafiarme otra vez?"):
            print("¡Hasta la próxima!")
            break
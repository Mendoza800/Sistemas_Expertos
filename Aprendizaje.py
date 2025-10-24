# Nuevo bloque de código con memoria expandida

def cargar_conocimiento():
    """Carga la memoria del Genio desde un archivo JSON."""
    if os.path.exists(ARCHIVO_MEMORIA):
        with open(ARCHIVO_MEMORIA, 'r', encoding='utf-8') as f:
            print("... El Genio ha cargado sus recuerdos ...")
            return json.load(f)
    else:
        # ¡NUEVA MEMORIA INICIAL EXPANDIDA!
        return [
            # Mamíferos
            {'nombre': 'león', 'es_mamifero': True, 'es_carnivoro': True, 'vive_en_la_sabana': True, 'es_domestico': False, 'tiene_rayas': False, 'tiene_trompa': False},
            {'nombre': 'cebra', 'es_mamifero': True, 'es_carnivoro': False, 'vive_en_la_sabana': True, 'es_domestico': False, 'tiene_rayas': True, 'tiene_trompa': False},
            {'nombre': 'delfín', 'es_mamifero': True, 'es_carnivoro': True, 'vive_en_el_mar': True, 'es_domestico': False},
            {'nombre': 'perro', 'es_mamifero': True, 'es_carnivoro': True, 'vive_en_la_sabana': False, 'es_domestico': True},
            {'nombre': 'elefante', 'es_mamifero': True, 'es_carnivoro': False, 'vive_en_la_sabana': True, 'es_domestico': False, 'tiene_rayas': False, 'tiene_trompa': True},
            {'nombre': 'gato', 'es_mamifero': True, 'es_carnivoro': True, 'vive_en_la_sabana': False, 'es_domestico': True},
            {'nombre': 'koala', 'es_mamifero': True, 'es_carnivoro': False, 'vive_en_australia': True, 'come_eucalipto': True},
            
            # Aves
            {'nombre': 'águila', 'es_ave': True, 'es_carnivoro': True, 'puede_volar': True, 'es_domestico': False},
            {'nombre': 'pingüino', 'es_ave': True, 'es_carnivoro': True, 'puede_volar': False, 'vive_en_climas_frios': True},
            {'nombre': 'tucán', 'es_ave': True, 'es_carnivoro': False, 'puede_volar': True, 'vive_en_la_selva': True, 'tiene_pico_de_colores': True},

            # Reptiles
            {'nombre': 'serpiente', 'es_reptil': True, 'tiene_escamas': True, 'es_carnivoro': True, 'no_tiene_patas': True},
            {'nombre': 'tortuga', 'es_reptil': True, 'tiene_escamas': True, 'es_carnivoro': False, 'tiene_caparazon': True},

            # Insectos
            {'nombre': 'mariposa', 'es_insecto': True, 'puede_volar': True, 'tiene_alas_de_colores': True},
            {'nombre': 'abeja', 'es_insecto': True, 'puede_volar': True, 'produce_miel': True, 'es_amarillo_y_negro': True},
            
            # Peces
            {'nombre': 'tiburón', 'es_pez': True, 'vive_en_el_mar': True, 'es_carnivoro': True, 'es_peligroso': True}
        ]

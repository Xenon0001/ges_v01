"""
Script de inicialización de estructura académica por defecto.
Se ejecuta al iniciar el programa para crear aulas básicas si no existen.
"""

from database.repository import level_repo, grade_repo, classroom_repo


def initialize_default_academic_structure():
    """
    Crea la estructura académica por defecto si no existe.
    - Primaria: 1º a 6º grado, aula A, turno Mañana
    - Secundaria: 1º a 4º grado, aula A, turno Mañana
    - Bachillerato: 1º y 2º grado, aula A, turno Mañana
    - Prescolar: No se modifica
    """
    try:
        # Verificar si ya existen aulas
        existing_classrooms = classroom_repo.get_all()
        if existing_classrooms:
            # Ya hay aulas, no crear por defecto
            return

        created_count = 0

        # Definir niveles y sus grados
        default_structure = {
            "Primaria": ["Primero", "Segundo", "Tercero", "Cuarto", "Quinto", "Sexto"],
            "Secundaria": ["Primero", "Segundo", "Tercero", "Cuarto"],
            "Bachillerato": ["Primero", "Segundo"]
        }

        # Crear niveles y grados si no existen
        for level_name, grades in default_structure.items():
            # Crear nivel si no existe
            existing_level = level_repo.find_by('name', level_name)
            if not existing_level:
                level_id = level_repo.create({'name': level_name})
            else:
                level_id = existing_level[0]['id']

            # Crear grados para este nivel
            for grade_name in grades:
                # Verificar si el grado ya existe
                existing_grade = grade_repo.find_by('name', grade_name)
                grade_exists = False
                grade_id = None
                
                if existing_grade:
                    # Verificar que pertenezca al nivel correcto
                    for grade in existing_grade:
                        if grade['level_id'] == level_id:
                            grade_exists = True
                            grade_id = grade['id']
                            break
                
                if not grade_exists:
                    grade_id = grade_repo.create({
                        'level_id': level_id,
                        'name': grade_name
                    })

                # Crear aula para este grado
                classroom_data = {
                    'grade_id': grade_id,
                    'name': 'A',
                    'shift': 'Mañana'
                }
                classroom_repo.create(classroom_data)
                created_count += 1

        print(f"Estructura académica por defecto inicializada: {created_count} aulas creadas.")

    except Exception as e:
        print(f"Error inicializando estructura académica: {str(e)}")


if __name__ == "__main__":
    initialize_default_academic_structure()
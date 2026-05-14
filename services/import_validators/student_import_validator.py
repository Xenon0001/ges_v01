from typing import Any, Dict, List, Optional, Tuple
from datetime import date


class StudentImportValidator:
    """Valida filas del importador de estudiantes."""

    REQUIRED_COLUMNS = [
        'nombre',
        'apellido',
        'nivel',
        'curso',
        'aula',
        'turno',
        'año escolar'
    ]

    def normalize_text(self, value: Any) -> str:
        if value is None:
            return ''
        return str(value).strip()

    def validate_row_data(self, row_data: Dict[str, Any], row_number: int) -> Tuple[bool, Optional[str]]:
        nombre = self.normalize_text(row_data.get('nombre'))
        apellido = self.normalize_text(row_data.get('apellido'))
        curso = self.normalize_text(row_data.get('curso'))
        aula = self.normalize_text(row_data.get('aula'))
        turno = self.normalize_text(row_data.get('turno'))
        anio = row_data.get('año escolar')

        if not nombre:
            return False, 'Nombre es obligatorio'
        if not apellido:
            return False, 'Apellido es obligatorio'
        if not curso:
            return False, 'Curso es obligatorio'
        if not aula:
            return False, 'Aula es obligatoria'
        if not turno:
            return False, 'Turno es obligatorio'
        nivel = self.normalize_text(row_data.get('nivel'))
        if not nivel:
            return False, 'Nivel es obligatorio'

        if anio is None or self.normalize_text(anio) == '':
            return False, 'Año Escolar es obligatorio'

        try:
            anio_int = int(anio)
            if anio_int < 1900 or anio_int > 2100:
                return False, 'Año Escolar no es válido'
        except (TypeError, ValueError):
            return False, 'Año Escolar debe ser un número válido'

        fecha_nacimiento = row_data.get('fechanacimiento')
        if fecha_nacimiento is not None and self.normalize_text(fecha_nacimiento) != '':
            if not self._validate_date_value(fecha_nacimiento):
                return False, 'FechaNacimiento debe ser fecha válida o texto YYYY-MM-DD'

        return True, None

    def _validate_date_value(self, value: Any) -> bool:
        if isinstance(value, date):
            return True
        text = self.normalize_text(value)
        if not text:
            return False
        try:
            if '-' in text:
                year, month, day = text.split('-')
                date(int(year), int(month), int(day))
                return True
        except Exception:
            return False
        return False

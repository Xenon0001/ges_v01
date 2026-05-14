from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ImportError:
    row_number: int
    student_name: str
    field: str
    error_type: str
    message: str


@dataclass
class ImportedRow:
    row_number: int
    first_name: str
    last_name: str
    classroom_name: Optional[str]
    academic_year: Optional[int]
    status: str
    notes: Optional[str] = None
    raw_data: Optional[Dict[str, Any]] = None


@dataclass
class PreviewRow:
    row_number: int
    raw_data: Dict[str, Any]
    validation_message: Optional[str] = None


@dataclass
class ImportResult:
    total_rows: int
    imported_count: int
    omitted_count: int
    error_count: int
    errors: List[ImportError]
    omitted_rows: List[ImportedRow]
    success_rows: List[ImportedRow]

    def get_summary(self) -> str:
        return (
            f"Importación completada: {self.imported_count} importados, "
            f"{self.omitted_count} omitidos, {self.error_count} errores de {self.total_rows} filas"
        )

from typing import List, Dict, Optional
from repositories.grade_repository import GradeRepository, GradeRecordRepository
from repositories.student_repository import StudentRepository
from database.models.school import GradeModel
from database.models.person import StudentModel


class GradeService:
    def __init__(self):
        self.grade_repo = GradeRepository()
        self.grade_record_repo = GradeRecordRepository()
        self.student_repo = StudentRepository()
    
    def create_grade(self, grade: GradeModel) -> GradeModel:
        """Create new grade level"""
        return self.grade_repo.create(grade)
    
    def get_all_grades(self) -> List[GradeModel]:
        """Get all grades"""
        return self.grade_repo.get_all()
    
    def get_grades_by_academic_year(self, academic_year: str) -> List[GradeModel]:
        """Get grades by academic year"""
        return self.grade_repo.get_by_academic_year(academic_year)
    
    def get_grades_by_level(self, level: str) -> List[GradeModel]:
        """Get grades by level (primary/secondary)"""
        return self.grade_repo.get_by_level(level)
    
    def get_grade_statistics(self, grade_id: int, academic_year: str, trimester: Optional[int] = None) -> Dict:
        """Get statistics for a grade"""
        students = self.student_repo.get_by_grade(grade_id)
        
        if not students:
            return {
                'total_students': 0,
                'average_grade': 0.0,
                'passed_count': 0,
                'failed_count': 0,
                'pass_rate': 0.0
            }
        
        total_students = len(students)
        passed_count = 0
        total_grades = 0.0
        grade_count = 0
        
        for student in students:
            grades = self.grade_record_repo.get_student_grades(student.id, academic_year, trimester)
            if grades:
                student_average = sum(g.grade_value for g in grades) / len(grades)
                total_grades += student_average
                grade_count += 1
                
                if student_average >= 5.0:
                    passed_count += 1
        
        average_grade = total_grades / grade_count if grade_count > 0 else 0.0
        failed_count = total_students - passed_count
        pass_rate = (passed_count / total_students * 100) if total_students > 0 else 0.0
        
        return {
            'total_students': total_students,
            'average_grade': round(average_grade, 2),
            'passed_count': passed_count,
            'failed_count': failed_count,
            'pass_rate': round(pass_rate, 2)
        }

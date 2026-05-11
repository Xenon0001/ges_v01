"""
Academic Service - Gestión de operaciones académicas
Combina repository y core engine para análisis académico
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from database.repository import (
    score_repo, student_repo, subject_repo, 
    teacher_repo, classroom_repo
)
from core.engine import CoreEngine, AcademicMetrics, Alert, AlertType


class AcademicService:
    """Servicio para gestión académica"""
    
    def __init__(self):
        self.score_repo = score_repo
        self.student_repo = student_repo
        self.subject_repo = subject_repo
        self.teacher_repo = teacher_repo
        self.classroom_repo = classroom_repo
        self.engine = CoreEngine()
    
    def add_score(self, score_data: Dict[str, Any]) -> int:
        """Agrega una nueva calificación"""
        
        # Validaciones
        if not all(key in score_data for key in ['student_id', 'subject_id', 'teacher_id', 'trimester', 'academic_year']):
            raise ValueError("Faltan campos obligatorios para la calificación")
        
        # Validar rango de calificación
        if score_data.get('score') is not None:
            if not (0 <= score_data['score'] <= self.engine.MAX_GRADE):
                raise ValueError(f"La calificación debe estar entre 0 y {self.engine.MAX_GRADE}")
        
        # Validar trimestre
        if score_data['trimester'] not in [1, 2, 3]:
            raise ValueError("El trimestre debe ser 1, 2 o 3")
        
        # Crear calificación
        score_id = self.score_repo.create(score_data)
        return score_id
    
    def update_score(self, score_id: int, data: Dict[str, Any]) -> bool:
        """Actualiza una calificación existente"""
        
        # Validar que exista
        score = self.score_repo.get_by_id(score_id)
        if not score:
            return False
        
        # Validar calificación si se actualiza
        if 'score' in data and data['score'] is not None:
            if not (0 <= data['score'] <= self.engine.MAX_GRADE):
                raise ValueError(f"La calificación debe estar entre 0 y {self.engine.MAX_GRADE}")
        
        # Actualizar
        rows_affected = self.score_repo.update(score_id, data)
        return rows_affected > 0
    
    def get_student_scores(self, student_id: int, academic_year: int, trimester: Optional[int] = None) -> List[Dict[str, Any]]:
        """Obtiene calificaciones de un estudiante"""
        return self.score_repo.get_by_student(student_id, academic_year)
    
    def get_subject_scores(self, subject_id: int, trimester: int, academic_year: int) -> List[Dict[str, Any]]:
        """Obtiene calificaciones de una materia"""
        return self.score_repo.get_by_subject(subject_id, trimester, academic_year)
    
    def get_student_academic_summary(self, student_id: int, academic_year: int) -> Dict[str, Any]:
        """Obtiene resumen académico completo de un estudiante"""
        
        # Obtener calificaciones
        scores = self.get_student_scores(student_id, academic_year)
        
        if not scores:
            return {'error': 'No se encontraron calificaciones para el estudiante'}
        
        # Calcular métricas por trimestre
        trimester_summaries = {}
        for trimester_num in [1, 2, 3]:
            trimester_scores = [s for s in scores if s['trimester'] == trimester_num]
            
            if trimester_scores:
                metrics = self.engine.calculate_academic_metrics(
                    student_id, trimester_scores, academic_year, trimester_num
                )
                
                trimester_summaries[f'trimester_{trimester_num}'] = {
                    'average': metrics.average,
                    'passed_subjects': metrics.passed_subjects,
                    'failed_subjects': metrics.failed_subjects,
                    'recovery_count': metrics.recovery_count,
                    'subject_count': metrics.subject_count
                }
        
        # Métricas anuales
        annual_metrics = self.engine.calculate_academic_metrics(student_id, scores, academic_year)
        
        # Alertas académicas
        alerts = self.engine.detect_academic_alerts(annual_metrics)
        
        return {
            'student_id': student_id,
            'academic_year': academic_year,
            'annual_summary': {
                'average': annual_metrics.average,
                'total_subjects': annual_metrics.subject_count,
                'passed_subjects': annual_metrics.passed_subjects,
                'failed_subjects': annual_metrics.failed_subjects,
                'recovery_count': annual_metrics.recovery_count
            },
            'trimester_breakdown': trimester_summaries,
            'detailed_scores': scores,
            'academic_alerts': alerts,
            'academic_status': self._determine_academic_status(annual_metrics)
        }
    
    def get_classroom_academic_summary(self, classroom_id: int, academic_year: int, trimester: Optional[int] = None) -> Dict[str, Any]:
        """Obtiene resumen académico de un aula"""
        
        # Obtener estudiantes del aula
        students = self.student_repo.get_by_classroom(classroom_id)
        active_students = [s for s in students if s['enrollment_status'] == 'activo']
        
        if not active_students:
            return {'error': 'No hay estudiantes activos en este aula'}
        
        # Obtener calificaciones de todos los estudiantes
        students_scores = {}
        for student in active_students:
            scores = self.get_student_scores(student['id'], academic_year, trimester)
            if scores:
                students_scores[student['id']] = scores
        
        # Calcular métricas del aula
        classroom_performance = self.engine.calculate_classroom_performance(
            students_scores, academic_year, trimester
        )
        
        # Identificar estudiantes en riesgo
        at_risk_students = []
        top_performers = []
        
        for student_id, scores in students_scores.items():
            metrics = self.engine.calculate_academic_metrics(
                student_id, scores, academic_year, trimester
            )
            
            student_info = next(s for s in active_students if s['id'] == student_id)
            
            if metrics.average and metrics.average < self.engine.MIN_PASSING_GRADE:
                at_risk_students.append({
                    'student_info': student_info,
                    'average': metrics.average,
                    'failed_subjects': metrics.failed_subjects
                })
            elif metrics.average and metrics.average >= 8.0:
                top_performers.append({
                    'student_info': student_info,
                    'average': metrics.average,
                    'passed_subjects': metrics.passed_subjects
                })
        
        return {
            'classroom_id': classroom_id,
            'academic_year': academic_year,
            'trimester': trimester,
            'total_students': len(active_students),
            'performance_metrics': classroom_performance,
            'students_at_risk': at_risk_students,
            'top_performers': top_performers,
            'subject_performance': self._get_classroom_subject_performance(
                classroom_id, academic_year, trimester
            )
        }
    
    def get_subject_performance_analysis(self, subject_id: int, academic_year: int) -> Dict[str, Any]:
        """Analiza rendimiento por materia"""
        
        subject_info = self.subject_repo.get_by_id(subject_id)
        if not subject_info:
            return {'error': 'Materia no encontrada'}
        
        # Obtener calificaciones por trimestre
        trimester_analyses = {}
        all_scores = []
        
        for trimester_num in [1, 2, 3]:
            trimester_scores = self.get_subject_scores(subject_id, trimester_num, academic_year)
            
            if trimester_scores:
                all_scores.extend(trimester_scores)
                
                performance = self.engine.calculate_subject_performance(
                    trimester_scores, academic_year, trimester_num
                )
                
                trimester_analyses[f'trimester_{trimester_num}'] = performance
        
        # Análisis anual
        annual_performance = self.engine.calculate_subject_performance(all_scores, academic_year)
        
        # Identificar patrones problemáticos
        issues = []
        if annual_performance.get('pass_rate', 0) < 0.7:
            issues.append("Tasa de aprobación baja (< 70%)")
        
        if annual_performance.get('students_at_risk', 0) > annual_performance.get('student_count', 0) * 0.3:
            issues.append("Alto número de estudiantes en riesgo")
        
        return {
            'subject_info': subject_info,
            'academic_year': academic_year,
            'annual_performance': annual_performance,
            'trimester_breakdown': trimester_analyses,
            'identified_issues': issues,
            'recommendations': self._generate_subject_recommendations(annual_performance)
        }
    
    def get_teacher_performance(self, teacher_id: int, academic_year: int) -> Dict[str, Any]:
        """Analiza rendimiento de un profesor"""
        
        teacher_info = self.teacher_repo.get_by_id(teacher_id)
        if not teacher_info:
            return {'error': 'Profesor no encontrado'}
        
        # Obtener materia del profesor
        subject_info = self.subject_repo.get_by_id(teacher_info['subject_id'])
        
        # Analizar rendimiento de su materia
        if subject_info:
            subject_analysis = self.get_subject_performance_analysis(
                teacher_info['subject_id'], academic_year
            )
        else:
            subject_analysis = {}
        
        return {
            'teacher_info': teacher_info,
            'subject_info': subject_info,
            'performance_analysis': subject_analysis,
            'academic_year': academic_year
        }
    
    def get_academic_dashboard_data(self, academic_year: int) -> Dict[str, Any]:
        """Genera datos para dashboard académico"""
        
        # Obtener todos los estudiantes activos
        active_students = self.student_repo.get_active_students()
        
        # Calcular métricas generales
        all_metrics = []
        all_alerts = []
        
        for student in active_students:
            scores = self.get_student_scores(student['id'], academic_year)
            if scores:
                metrics = self.engine.calculate_academic_metrics(
                    student['id'], scores, academic_year
                )
                all_metrics.append(metrics)
                all_alerts.extend(self.engine.detect_academic_alerts(metrics))
        
        # Resumen general
        dashboard_summary = self.engine.generate_dashboard_summary(
            all_metrics, [], all_alerts
        )
        
        # Rendimiento por materia
        subjects = self.subject_repo.get_all()
        subject_performances = {}
        
        for subject in subjects:
            all_subject_scores = []
            for trimester in [1, 2, 3]:
                scores = self.get_subject_scores(subject['id'], trimester, academic_year)
                all_subject_scores.extend(scores)
            
            if all_subject_scores:
                performance = self.engine.calculate_subject_performance(
                    all_subject_scores, academic_year
                )
                subject_performances[subject['name']] = performance
        
        return {
            'academic_year': academic_year,
            'summary': dashboard_summary,
            'subject_performances': subject_performances,
            'total_active_students': len(active_students),
            'critical_alerts': [a for a in all_alerts if a.severity == 'high'],
            'generated_at': datetime.now().isoformat()
        }
    
    def _determine_academic_status(self, metrics: AcademicMetrics) -> str:
        """Determina el estado académico de un estudiante"""
        if metrics.average is None:
            return 'sin_datos'
        
        if metrics.average >= 8.0:
            return 'excelente'
        elif metrics.average >= 6.0:
            return 'bueno'
        elif metrics.average >= self.engine.MIN_PASSING_GRADE:
            return 'regular'
        else:
            return 'riesgo'
    
    def _get_classroom_subject_performance(self, classroom_id: int, academic_year: int, trimester: Optional[int] = None) -> Dict[str, Any]:
        """Obtiene rendimiento por materia de un aula"""
        
        students = self.student_repo.get_by_classroom(classroom_id)
        active_students = [s for s in students if s['enrollment_status'] == 'activo']
        
        subject_scores = {}
        for student in active_students:
            scores = self.get_student_scores(student['id'], academic_year, trimester)
            for score in scores:
                subject_id = score['subject_id']
                if subject_id not in subject_scores:
                    subject_scores[subject_id] = []
                subject_scores[subject_id].append(score)
        
        subject_performances = {}
        for subject_id, scores in subject_scores.items():
            if scores:
                performance = self.engine.calculate_subject_performance(scores, academic_year, trimester)
                subject_info = self.subject_repo.get_by_id(subject_id)
                subject_performances[subject_info['name'] if subject_info else f"Subject {subject_id}"] = performance
        
        return subject_performances
    
    def _generate_subject_recommendations(self, performance: Dict[str, Any]) -> List[str]:
        """Genera recomendaciones basadas en rendimiento de materia"""
        
        recommendations = []
        
        pass_rate = performance.get('pass_rate', 0)
        average = performance.get('average', 0)
        
        if pass_rate < 0.6:
            recommendations.append("Revisar metodología de enseñanza")
            recommendations.append("Considerar tutorías adicionales")
        elif pass_rate < 0.8:
            recommendations.append("Monitorear estudiantes con dificultades")
        
        if average < 5.0:
            recommendations.append("Evaluar nivel de dificultad de evaluaciones")
        
        students_at_risk = performance.get('students_at_risk', 0)
        if students_at_risk > 0:
            recommendations.append(f"Intervenir con {students_at_risk} estudiantes en riesgo")
        
        return recommendations


# Instancia global del servicio
academic_service = AcademicService()

"""
Core Engine - Lógica de negocio pura para GES
Contiene cálculos académicos y financieros sin dependencias de base de datos
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import statistics
from datetime import datetime


class EnrollmentStatus(Enum):
    ACTIVO = "activo"
    RETIRADO = "retirado"
    GRADUADO = "graduado"


class PaymentStatus(Enum):
    PENDIENTE = "pendiente"
    PAGADO = "pagado"
    RETRASADO = "retrasado"


class AlertType(Enum):
    RENDIMIENTO = "rendimiento"
    MOROSIDAD = "morosidad"
    ABANDONO = "abandono"


@dataclass
class AcademicMetrics:
    """Métricas académicas de un estudiante"""
    student_id: int
    academic_year: int
    trimester: Optional[int]
    average: Optional[float]
    subject_count: int
    passed_subjects: int
    failed_subjects: int
    recovery_count: int


@dataclass
class FinancialMetrics:
    """Métricas financieras de un estudiante"""
    student_id: int
    total_due: float
    total_paid: float
    outstanding: float
    overdue_count: int
    last_payment_date: Optional[str]


@dataclass
class Alert:
    """Alerta del sistema"""
    type: AlertType
    reference_id: int
    message: str
    severity: str  # 'low', 'medium', 'high'


class CoreEngine:
    """Motor central de lógica de negocio de GES"""
    
    # Constantes académicas
    MIN_PASSING_GRADE = 5.0
    MAX_GRADE = 10.0
    TRIMESTERS_PER_YEAR = 3
    
    # Constantes financieras
    OVERDUE_DAYS_THRESHOLD = 30
    
    @staticmethod
    def calculate_student_average(scores: List[Dict[str, Any]]) -> Optional[float]:
        """Calcula el promedio de calificaciones de un estudiante"""
        if not scores:
            return None
        
        valid_scores = [s['score'] for s in scores if s['score'] is not None]
        if not valid_scores:
            return None
        
        return round(statistics.mean(valid_scores), 2)
    
    @staticmethod
    def calculate_academic_metrics(
        student_id: int,
        scores: List[Dict[str, Any]],
        academic_year: int,
        trimester: Optional[int] = None
    ) -> AcademicMetrics:
        """Calcula métricas académicas completas de un estudiante"""
        
        # Filtrar por año y trimestre si se especifica
        filtered_scores = [
            s for s in scores 
            if s['academic_year'] == academic_year and
               (trimester is None or s['trimester'] == trimester)
        ]
        
        # Calcular promedio
        average = CoreEngine.calculate_student_average(filtered_scores)
        
        # Contar materias
        subject_count = len(set(s['subject_id'] for s in filtered_scores))
        
        # Contar aprobados y reprobados
        passed_subjects = 0
        failed_subjects = 0
        recovery_count = 0
        
        for score in filtered_scores:
            if score['score'] is not None:
                if score['score'] >= CoreEngine.MIN_PASSING_GRADE:
                    passed_subjects += 1
                else:
                    failed_subjects += 1
                    if score['recovery_score'] is not None:
                        recovery_count += 1
                        if score['recovery_score'] >= CoreEngine.MIN_PASSING_GRADE:
                            passed_subjects += 1
                            failed_subjects -= 1
        
        return AcademicMetrics(
            student_id=student_id,
            academic_year=academic_year,
            trimester=trimester,
            average=average,
            subject_count=subject_count,
            passed_subjects=passed_subjects,
            failed_subjects=failed_subjects,
            recovery_count=recovery_count
        )
    
    @staticmethod
    def calculate_financial_metrics(
        student_id: int,
        payments: List[Dict[str, Any]]
    ) -> FinancialMetrics:
        """Calcula métricas financieras de un estudiante"""
        
        total_due = sum(p['amount_due'] for p in payments)
        total_paid = sum(p['amount_paid'] for p in payments)
        outstanding = sum(
            (p['amount_due'] - p['amount_paid']) 
            for p in payments 
            if p['status'] != 'pagado'
        )
        
        # Contar pagos vencidos
        overdue_count = 0
        last_payment_date = None
        
        for payment in payments:
            if payment['status'] == 'retrasado':
                overdue_count += 1
            
            if payment['amount_paid'] > 0:
                if last_payment_date is None or payment['due_date'] > last_payment_date:
                    last_payment_date = payment['due_date']
        
        return FinancialMetrics(
            student_id=student_id,
            total_due=total_due,
            total_paid=total_paid,
            outstanding=outstanding,
            overdue_count=overdue_count,
            last_payment_date=last_payment_date
        )
    
    @staticmethod
    def detect_academic_alerts(metrics: AcademicMetrics) -> List[Alert]:
        """Detecta alertas académicas basadas en métricas"""
        alerts = []
        
        # Alerta por promedio bajo
        if metrics.average is not None and metrics.average < CoreEngine.MIN_PASSING_GRADE:
            severity = 'high' if metrics.average < 4.0 else 'medium'
            alerts.append(Alert(
                type=AlertType.RENDIMIENTO,
                reference_id=metrics.student_id,
                message=f"Promedio bajo: {metrics.average}",
                severity=severity
            ))
        
        # Alerta por muchas materias reprobadas
        if metrics.failed_subjects > 2:
            alerts.append(Alert(
                type=AlertType.RENDIMIENTO,
                reference_id=metrics.student_id,
                message=f"{metrics.failed_subjects} materias reprobadas",
                severity='high'
            ))
        
        # Alerta por recuperaciones frecuentes
        if metrics.recovery_count > 1:
            alerts.append(Alert(
                type=AlertType.RENDIMIENTO,
                reference_id=metrics.student_id,
                message=f"{metrics.recovery_count} recuperaciones necesarias",
                severity='medium'
            ))
        
        return alerts
    
    @staticmethod
    def detect_financial_alerts(metrics: FinancialMetrics) -> List[Alert]:
        """Detecta alertas financieras basadas en métricas"""
        alerts = []
        
        # Alerta por morosidad alta
        if metrics.outstanding > 0:
            severity = 'high' if metrics.outstanding > 200 else 'medium'
            alerts.append(Alert(
                type=AlertType.MOROSIDAD,
                reference_id=metrics.student_id,
                message=f"Deuda pendiente: {metrics.outstanding:.2f}",
                severity=severity
            ))
        
        # Alerta por pagos vencidos
        if metrics.overdue_count > 0:
            alerts.append(Alert(
                type=AlertType.MOROSIDAD,
                reference_id=metrics.student_id,
                message=f"{metrics.overdue_count} pagos vencidos",
                severity='high'
            ))
        
        return alerts
    
    @staticmethod
    def calculate_classroom_performance(
        students_scores: Dict[int, List[Dict[str, Any]]],
        academic_year: int,
        trimester: Optional[int] = None
    ) -> Dict[str, Any]:
        """Calcula rendimiento general de un aula"""
        
        all_metrics = []
        for student_id, scores in students_scores.items():
            metrics = CoreEngine.calculate_academic_metrics(
                student_id, scores, academic_year, trimester
            )
            all_metrics.append(metrics)
        
        if not all_metrics:
            return {}
        
        # Calcular estadísticas del aula
        averages = [m.average for m in all_metrics if m.average is not None]
        passed_counts = [m.passed_subjects for m in all_metrics]
        failed_counts = [m.failed_subjects for m in all_metrics]
        
        return {
            'student_count': len(all_metrics),
            'classroom_average': statistics.mean(averages) if averages else None,
            'pass_rate': sum(passed_counts) / (sum(passed_counts) + sum(failed_counts)) if (sum(passed_counts) + sum(failed_counts)) > 0 else 0,
            'students_at_risk': len([m for m in all_metrics if m.average and m.average < CoreEngine.MIN_PASSING_GRADE]),
            'top_performers': len([m for m in all_metrics if m.average and m.average >= 8.0])
        }
    
    @staticmethod
    def calculate_subject_performance(
        subject_scores: List[Dict[str, Any]],
        academic_year: int,
        trimester: Optional[int] = None
    ) -> Dict[str, Any]:
        """Calcula rendimiento por materia"""
        
        filtered_scores = [
            s for s in subject_scores
            if s['academic_year'] == academic_year and
               (trimester is None or s['trimester'] == trimester)
        ]
        
        if not filtered_scores:
            return {}
        
        valid_scores = [s['score'] for s in filtered_scores if s['score'] is not None]
        
        if not valid_scores:
            return {}
        
        passed_count = len([s for s in valid_scores if s >= CoreEngine.MIN_PASSING_GRADE])
        
        return {
            'student_count': len(valid_scores),
            'average': statistics.mean(valid_scores),
            'pass_rate': passed_count / len(valid_scores),
            'highest_score': max(valid_scores),
            'lowest_score': min(valid_scores),
            'students_at_risk': len([s for s in valid_scores if s < 4.0])
        }
    
    @staticmethod
    def generate_dashboard_summary(
        academic_metrics: List[AcademicMetrics],
        financial_metrics: List[FinancialMetrics],
        alerts: List[Alert]
    ) -> Dict[str, Any]:
        """Genera resumen para dashboard principal"""
        
        # Métricas académicas generales
        academic_averages = [m.average for m in academic_metrics if m.average is not None]
        
        # Métricas financieras generales
        total_outstanding = sum(m.outstanding for m in financial_metrics)
        students_with_debt = len([m for m in financial_metrics if m.outstanding > 0])
        
        # Alertas por tipo
        alert_counts = {}
        for alert in alerts:
            alert_counts[alert.type.value] = alert_counts.get(alert.type.value, 0) + 1
        
        return {
            'total_students': len(academic_metrics),
            'average_performance': statistics.mean(academic_averages) if academic_averages else None,
            'students_at_risk_academic': len([m for m in academic_metrics if m.average and m.average < CoreEngine.MIN_PASSING_GRADE]),
            'total_outstanding_debt': total_outstanding,
            'students_with_debt': students_with_debt,
            'alert_summary': alert_counts,
            'critical_alerts': len([a for a in alerts if a.severity == 'high'])
        }

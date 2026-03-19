"""
Finance Service - Gestión de operaciones financieras
Combina repository y core engine para gestión de pagos y morosidad
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, date, timedelta
from dataclasses import dataclass

from database.repository import (
    payment_repo, student_repo, payment_calendar_repo, 
    payment_installment_repo, student_calendar_repo, enrollment_price_repo
)
from database.connection import db
from core.engine import CoreEngine, FinancialMetrics, Alert, AlertType, PaymentStatus


@dataclass
class PaymentSummary:
    """Resumen de pagos"""
    total_students: int
    total_due: float
    total_paid: float
    total_outstanding: float
    collection_rate: float
    overdue_payments: int
    overdue_amount: float


@dataclass
class TutorPaymentGroup:
    """Grupo de pagos por tutor"""
    tutor_name: str
    students_count: int
    total_due: float
    total_paid: float
    outstanding: float
    overdue_count: int


@dataclass
class CalendarInstallment:
    """Cuota de calendario de pago"""
    installment_number: int
    amount: float
    due_date: str
    status: str = 'pendiente'


@dataclass
class PaymentCalendar:
    """Calendario de pagos"""
    id: int
    tutor_name: str
    tutor_phone: Optional[str]
    total_amount: float
    discount_amount: float
    final_amount: float
    academic_year: int
    status: str
    created_at: str
    updated_at: str


class FinanceService:
    """Servicio para gestión financiera"""
    
    def __init__(self):
        self.payment_repo = payment_repo
        self.student_repo = student_repo
        self.payment_calendar_repo = payment_calendar_repo
        self.payment_installment_repo = payment_installment_repo
        self.student_calendar_repo = student_calendar_repo
        self.enrollment_price_repo = enrollment_price_repo
        self.engine = CoreEngine()
    
    def create_payment(self, payment_data: Dict[str, Any]) -> int:
        """Crea un nuevo registro de pago"""
        
        # Validaciones
        if not all(key in payment_data for key in ['student_id', 'amount_due']):
            raise ValueError("Estudiante y monto debido son obligatorios")
        
        # Validar que el estudiante exista
        student = self.student_repo.get_by_id(payment_data['student_id'])
        if not student:
            raise ValueError("El estudiante especificado no existe")
        
        # Validar montos
        if payment_data['amount_due'] <= 0:
            raise ValueError("El monto debido debe ser mayor a 0")
        
        if payment_data.get('amount_paid', 0) < 0:
            raise ValueError("El monto pagado no puede ser negativo")
        
        # Establecer estado por defecto
        if 'status' not in payment_data:
            if payment_data.get('amount_paid', 0) >= payment_data['amount_due']:
                payment_data['status'] = PaymentStatus.PAGADO.value
            else:
                payment_data['status'] = PaymentStatus.PENDIENTE.value
        
        # Crear pago
        payment_id = self.payment_repo.create(payment_data)
        
        # Actualizar estado si es necesario
        self._update_payment_status(payment_id)
        
        return payment_id
    
    def update_payment(self, payment_id: int, data: Dict[str, Any]) -> bool:
        """Actualiza un registro de pago"""
        
        # Validar que exista
        payment = self.payment_repo.get_by_id(payment_id)
        if not payment:
            return False
        
        # Validar montos si se actualizan
        if 'amount_due' in data and data['amount_due'] <= 0:
            raise ValueError("El monto debido debe ser mayor a 0")
        
        if 'amount_paid' in data and data['amount_paid'] < 0:
            raise ValueError("El monto pagado no puede ser negativo")
        
        # Actualizar
        rows_affected = self.payment_repo.update(payment_id, data)
        
        if rows_affected > 0:
            # Actualizar estado automáticamente
            self._update_payment_status(payment_id)
            return True
        
        return False
    
    def record_payment(self, payment_id: int, amount: float) -> bool:
        """Registra un pago parcial o completo"""
        
        payment = self.payment_repo.get_by_id(payment_id)
        if not payment:
            return False
        
        new_amount_paid = payment['amount_paid'] + amount
        
        # Validar que no exceda el monto debido
        if new_amount_paid > payment['amount_due']:
            raise ValueError("El monto pagado excede el monto debido")
        
        # Actualizar
        return self.update_payment(payment_id, {'amount_paid': new_amount_paid})
    
    def get_student_payments(self, student_id: int) -> List[Dict[str, Any]]:
        """Obtiene todos los pagos de un estudiante"""
        return self.payment_repo.get_by_student(student_id)
    
    def get_student_financial_summary(self, student_id: int) -> Dict[str, Any]:
        """Obtiene resumen financiero de un estudiante"""
        
        # Obtener estudiante (versión simplificada)
        student = self.student_repo.get_by_id(student_id)
        if not student:
            raise ValueError(f"Estudiante con ID {student_id} no encontrado")
        
        # Calcular métricas financieras
        metrics = self.engine.calculate_financial_metrics(
            student_id, self.get_student_payments(student_id)
        )
        
        # Alertas financieras
        alerts = self.engine.detect_financial_alerts(metrics)
        
        # Detalles de pagos
        payments = self.get_student_payments(student_id)
        
        summary = {
            'student_info': student,
            'financial_metrics': metrics,
            'alerts': alerts,
            'payment_details': payments,
            'payment_status': self._determine_payment_status(metrics),
            'risk_level': self._calculate_financial_risk(metrics)
        }
        
        return summary
    
    def get_overdue_payments(self) -> List[Dict[str, Any]]:
        """Obtiene pagos vencidos"""
        return self.payment_repo.get_overdue_payments()
    
    def get_pending_payments(self) -> List[Dict[str, Any]]:
        """Obtiene pagos pendientes"""
        return self.payment_repo.get_pending_payments()
    
    def get_tutor_payment_groups(self) -> List[TutorPaymentGroup]:
        """Agrupa pagos por tutor para seguimiento"""
        
        # Obtener todos los estudiantes con pagos pendientes
        pending_payments = self.get_pending_payments()
        
        # Agrupar por tutor
        tutor_groups = {}
        
        for payment in pending_payments:
            student_id = payment['student_id']
            student = self.student_repo.get_by_id(student_id)
            
            if student and student.get('tutor_name'):
                tutor_name = student['tutor_name']
                
                if tutor_name not in tutor_groups:
                    tutor_groups[tutor_name] = {
                        'tutor_name': tutor_name,
                        'students_count': 0,
                        'total_due': 0,
                        'total_paid': 0,
                        'outstanding': 0,
                        'overdue_count': 0
                    }
                
                group = tutor_groups[tutor_name]
                group['students_count'] += 1
                group['total_due'] += payment['amount_due']
                group['total_paid'] += payment['amount_paid']
                group['outstanding'] += (payment['amount_due'] - payment['amount_paid'])
                
                if payment['status'] == 'retrasado':
                    group['overdue_count'] += 1
        
        # Convertir a objetos TutorPaymentGroup
        return [
            TutorPaymentGroup(**group_data)
            for group_data in tutor_groups.values()
        ]
    
    def get_financial_dashboard_data(self) -> Dict[str, Any]:
        """Genera datos para dashboard financiero"""
        
        # Resumen general
        summary = self.get_payment_summary()
        
        # Pagos vencidos
        overdue_payments = self.get_overdue_payments()
        
        # Grupos por tutor
        tutor_groups = self.get_tutor_payment_groups()
        
        # Estudiantes con problemas financieros
        students_at_risk = self.get_students_financial_risk()
        
        # Tendencias de cobro (últimos 6 meses)
        collection_trends = self._calculate_collection_trends()
        
        return {
            'summary': summary,
            'overdue_payments': overdue_payments[:10],  # Limitar a 10 más recientes
            'tutor_groups': [self._tutor_group_to_dict(g) for g in tutor_groups],
            'students_at_risk': students_at_risk[:15],  # Limitar a 15
            'collection_trends': collection_trends,
            'critical_alerts': self._get_critical_financial_alerts(),
            'generated_at': datetime.now().isoformat()
        }
    
    def get_payment_summary(self) -> PaymentSummary:
        """Obtiene resumen general de pagos"""
        
        # Obtener todos los estudiantes activos
        active_students = self.student_repo.get_active_students()
        
        total_due = 0
        total_paid = 0
        total_outstanding = 0
        overdue_payments = 0
        overdue_amount = 0
        
        for student in active_students:
            payments = self.get_student_payments(student['id'])
            
            for payment in payments:
                total_due += payment['amount_due']
                total_paid += payment['amount_paid']
                
                if payment['status'] != 'pagado':
                    outstanding = payment['amount_due'] - payment['amount_paid']
                    total_outstanding += outstanding
                    
                    if payment['status'] == 'retrasado':
                        overdue_payments += 1
                        overdue_amount += outstanding
        
        collection_rate = (total_paid / total_due * 100) if total_due > 0 else 0
        
        return PaymentSummary(
            total_students=len(active_students),
            total_due=total_due,
            total_paid=total_paid,
            total_outstanding=total_outstanding,
            collection_rate=collection_rate,
            overdue_payments=overdue_payments,
            overdue_amount=overdue_amount
        )
    
    def get_students_financial_risk(self) -> List[Dict[str, Any]]:
        """Identifica estudiantes en riesgo financiero"""
        
        at_risk_students = []
        active_students = self.student_repo.get_active_students()
        
        for student in active_students:
            summary = self.get_student_financial_summary(student['id'])
            
            if summary['risk_level'] in ['medium', 'high']:
                at_risk_students.append(summary)
        
        # Ordenar por monto pendiente (mayor a menor)
        at_risk_students.sort(
            key=lambda x: x['financial_metrics'].outstanding, 
            reverse=True
        )
        
        return at_risk_students
    
    def generate_payment_report(self, student_id: int = None, tutor_name: str = None) -> Dict[str, Any]:
        """Genera reporte de pagos"""
        
        if student_id:
            return self.get_student_financial_summary(student_id)
        elif tutor_name:
            return self._generate_tutor_payment_report(tutor_name)
        else:
            return self._generate_general_payment_report()
    
    def _update_payment_status(self, payment_id: int) -> None:
        """Actualiza el estado de un pago basado en los montos"""
        
        payment = self.payment_repo.get_by_id(payment_id)
        if not payment:
            return
        
        new_status = payment['status']
        
        # Determinar estado basado en montos
        if payment['amount_paid'] >= payment['amount_due']:
            new_status = PaymentStatus.PAGADO.value
        elif payment['amount_paid'] > 0:
            new_status = PaymentStatus.PENDIENTE.value
        
        # Verificar si está vencido
        if payment['due_date'] and payment['status'] != 'pagado':
            due_date = datetime.strptime(payment['due_date'], '%Y-%m-%d').date()
            if due_date < date.today():
                new_status = PaymentStatus.RETRASADO.value
        
        # Actualizar si cambió
        if new_status != payment['status']:
            self.payment_repo.update(payment_id, {'status': new_status})
    
    def _determine_payment_status(self, metrics: FinancialMetrics) -> str:
        """Determina el estado general de pagos de un estudiante"""
        
        if metrics.outstanding == 0:
            return 'al_dia'
        elif metrics.overdue_count > 0:
            return 'moroso'
        else:
            return 'pendiente'
    
    def _calculate_financial_risk(self, metrics: FinancialMetrics) -> str:
        """Calcula nivel de riesgo financiero"""
        
        if metrics.overdue_count > 2 or metrics.outstanding > 300:
            return 'high'
        elif metrics.overdue_count > 0 or metrics.outstanding > 100:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_collection_trends(self) -> List[Dict[str, Any]]:
        """Calcula tendencias de cobro de los últimos 6 meses"""
        
        trends = []
        today = date.today()
        
        for i in range(6):
            month_start = today.replace(day=1) - timedelta(days=30 * i)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            # Aquí se calcularían las cobranzas del mes
            # Por ahora, datos de ejemplo
            trends.append({
                'month': month_start.strftime('%Y-%m'),
                'collected': 0,  # Se implementaría con consultas reales
                'expected': 0,
                'collection_rate': 0
            })
        
        return trends
    
    def _get_critical_financial_alerts(self) -> List[Dict[str, Any]]:
        """Obtiene alertas financieras críticas"""
        
        critical_alerts = []
        
        # Pagos muy vencidos
        overdue_payments = self.get_overdue_payments()
        for payment in overdue_payments:
            if payment['due_date']:
                due_date = datetime.strptime(payment['due_date'], '%Y-%m-%d').date()
                days_overdue = (date.today() - due_date).days
                
                if days_overdue > 60:
                    critical_alerts.append({
                        'type': 'payment_overdue',
                        'severity': 'high',
                        'message': f"Pago vencido hace {days_overdue} días - Estudiante ID: {payment['student_id']}",
                        'reference_id': payment['id']
                    })
        
        return critical_alerts
    
    def _tutor_group_to_dict(self, group: TutorPaymentGroup) -> Dict[str, Any]:
        """Convierte TutorPaymentGroup a diccionario"""
        return {
            'tutor_name': group.tutor_name,
            'students_count': group.students_count,
            'total_due': group.total_due,
            'total_paid': group.total_paid,
            'outstanding': group.outstanding,
            'overdue_count': group.overdue_count
        }
    
    def _generate_tutor_payment_report(self, tutor_name: str) -> Dict[str, Any]:
        """Genera reporte de pagos para un tutor específico"""
        
        # Obtener estudiantes del tutor
        all_students = self.student_repo.get_all()
        tutor_students = [s for s in all_students if s.get('tutor_name') == tutor_name]
        
        if not tutor_students:
            return {'error': f'No se encontraron estudiantes para el tutor: {tutor_name}'}
        
        # Calcular métricas del grupo
        total_due = 0
        total_paid = 0
        total_outstanding = 0
        student_summaries = []
        
        for student in tutor_students:
            summary = self.get_student_financial_summary(student['id'])
            student_summaries.append(summary)
            
            metrics = summary['financial_metrics']
            total_due += metrics.total_due
            total_paid += metrics.total_paid
            total_outstanding += metrics.outstanding
        
        return {
            'tutor_name': tutor_name,
            'students_count': len(tutor_students),
            'total_due': total_due,
            'total_paid': total_paid,
            'total_outstanding': total_outstanding,
            'collection_rate': (total_paid / total_due * 100) if total_due > 0 else 0,
            'student_details': student_summaries,
            'generated_at': datetime.now().isoformat()
        }
    
    def _generate_general_payment_report(self) -> Dict[str, Any]:
        """Genera reporte general de pagos"""
        
        summary = self.get_payment_summary()
        tutor_groups = self.get_tutor_payment_groups()
        
        return {
            'summary': summary,
            'tutor_groups': [self._tutor_group_to_dict(g) for g in tutor_groups],
            'overdue_payments_count': len(self.get_overdue_payments()),
            'students_at_risk_count': len(self.get_students_financial_risk()),
            'generated_at': datetime.now().isoformat()
        }
    
    # === MÉTODOS DE CALENDARIOS DE PAGO ===
    
    def create_payment_calendar(self, tutor_name: str, tutor_phone: str, 
                              student_ids: List[int], discount: float = 0, 
                              academic_year: int = None) -> int:
        """Crea un calendario de pago para un tutor"""
        
        if academic_year is None:
            academic_year = date.today().year
        
        # Verificar que no exista calendario activo para este tutor y año
        existing = self.get_calendar_by_tutor(tutor_name, academic_year)
        if existing:
            raise ValueError(f"El tutor {tutor_name} ya tiene un calendario activo para el año {academic_year}")
        
        # Calcular total sumando precios de matrícula
        total_amount = 0
        for student_id in student_ids:
            student = self.student_repo.get_by_id(student_id)
            if not student:
                raise ValueError(f"Estudiante con ID {student_id} no encontrado")
            
            # Obtener precio según nivel del estudiante
            price = self._get_student_enrollment_price(student_id, academic_year)
            total_amount += price
        
        # Aplicar descuento
        final_amount = total_amount - discount
        if final_amount < 0:
            raise ValueError("El descuento no puede ser mayor al monto total")
        
        # Crear calendario
        calendar_data = {
            'tutor_name': tutor_name,
            'tutor_phone': tutor_phone,
            'total_amount': total_amount,
            'discount_amount': discount,
            'final_amount': final_amount,
            'academic_year': academic_year,
            'status': 'activo'
        }
        
        calendar_id = self.payment_calendar_repo.create(calendar_data)
        
        # Añadir estudiantes al calendario
        for student_id in student_ids:
            price = self._get_student_enrollment_price(student_id, academic_year)
            self.student_calendar_repo.add_student_to_calendar(student_id, calendar_id, price)
        
        return calendar_id
    
    def add_installments(self, calendar_id: int, installments_list: List[Dict[str, Any]]) -> bool:
        """Añade cuotas a un calendario de pago"""
        
        # Verificar que el calendario exista
        calendar = self.payment_calendar_repo.get_by_id(calendar_id)
        if not calendar:
            raise ValueError(f"Calendario con ID {calendar_id} no encontrado")
        
        # Verificar que no existan cuotas previas
        existing_installments = self.payment_installment_repo.get_by_calendar(calendar_id)
        if existing_installments:
            raise ValueError("El calendario ya tiene cuotas definidas")
        
        # Crear cuotas
        for i, installment in enumerate(installments_list, 1):
            installment_data = {
                'calendar_id': calendar_id,
                'installment_number': i,
                'amount': installment['amount'],
                'due_date': installment['due_date'],
                'status': 'pendiente'
            }
            self.payment_installment_repo.create(installment_data)
        
        return True
    
    def get_calendar_by_tutor(self, tutor_name: str, academic_year: int = None) -> Optional[Dict[str, Any]]:
        """Obtiene calendario activo de un tutor"""
        
        if academic_year is None:
            academic_year = date.today().year
        
        calendars = self.payment_calendar_repo.get_by_tutor(tutor_name, academic_year)
        
        # Retornar el primer calendario activo
        for calendar in calendars:
            if calendar['status'] == 'activo':
                return self.payment_calendar_repo.get_with_details(calendar['id'])
        
        return None
    
    def assign_student_to_calendar(self, student_id: int, calendar_id: int) -> bool:
        """Añade estudiante a calendario existente y recalcula total"""
        
        # Verificar que existan
        student = self.student_repo.get_by_id(student_id)
        calendar = self.payment_calendar_repo.get_by_id(calendar_id)
        
        if not student:
            raise ValueError(f"Estudiante con ID {student_id} no encontrado")
        if not calendar:
            raise ValueError(f"Calendario con ID {calendar_id} no encontrado")
        
        # Obtener precio del estudiante
        price = self._get_student_enrollment_price(student_id, calendar['academic_year'])
        
        # Añadir estudiante
        self.student_calendar_repo.add_student_to_calendar(student_id, calendar_id, price)
        
        # Recalcular total
        students = self.student_calendar_repo.get_calendar_students(calendar_id)
        new_total = sum(s['enrollment_price'] for s in students)
        new_final = new_total - calendar['discount_amount']
        
        # Actualizar calendario
        self.payment_calendar_repo.update(calendar_id, {
            'total_amount': new_total,
            'final_amount': new_final,
            'updated_at': datetime.now().isoformat()
        })
        
        return True
    
    def pay_installment(self, installment_id: int, amount: float, paid_date: str = None) -> bool:
        """Registra el pago de una cuota"""
        
        installment = self.payment_installment_repo.get_by_id(installment_id)
        if not installment:
            raise ValueError(f"Cuota con ID {installment_id} no encontrada")
        
        if installment['status'] == 'pagado':
            raise ValueError("Esta cuota ya está pagada")
        
        # Validar monto
        if amount > installment['amount']:
            raise ValueError("El monto pagado excede el monto de la cuota")
        
        # Marcar como pagada
        success = self.payment_installment_repo.mark_as_paid(installment_id, amount)
        
        if success and paid_date:
            self.payment_installment_repo.update(installment_id, {'paid_date': paid_date})
        
        # Verificar si todas las cuotas están pagas para actualizar estado del calendario
        self._update_calendar_status(installment['calendar_id'])
        
        return success
    
    def _get_student_enrollment_price(self, student_id: int, academic_year: int) -> float:
        """Obtiene precio de matrícula de un estudiante según su nivel"""
        
        student = self.student_repo.get_by_id(student_id)
        if not student:
            raise ValueError(f"Estudiante con ID {student_id} no encontrado")
        
        # Obtener level_id del estudiante a través de classroom
        if not student.get('classroom_id'):
            raise ValueError(f"El estudiante {student['first_name']} {student['last_name']} no tiene aula asignada")
        
        # Obtener classroom para luego obtener level_id
        classroom_query = f"""
            SELECT c.*, g.level_id 
            FROM classrooms c
            JOIN grades g ON c.grade_id = g.id
            WHERE c.id = ?
        """
        classrooms = db.execute_query(classroom_query, (student['classroom_id'],))
        
        if not classrooms:
            raise ValueError("No se pudo determinar el nivel del estudiante")
        
        level_id = classrooms[0]['level_id']
        
        # Obtener precio del nivel
        prices = self.enrollment_price_repo.get_by_year(academic_year)
        for price in prices:
            if price['level_id'] == level_id:
                return price['price']
        
        # Si no hay precio definido, usar valor por defecto
        return 0.0
    
    def _update_calendar_status(self, calendar_id: int) -> None:
        """Actualiza el estado de un calendario basado en sus cuotas"""
        
        installments = self.payment_installment_repo.get_by_calendar(calendar_id)
        
        if not installments:
            return
        
        # Contar estados
        paid_count = sum(1 for i in installments if i['status'] == 'pagado')
        total_count = len(installments)
        
        # Determinar nuevo estado
        if paid_count == total_count:
            new_status = 'completado'
        elif paid_count > 0:
            new_status = 'activo'
        else:
            new_status = 'activo'
        
        # Actualizar si cambió
        calendar = self.payment_calendar_repo.get_by_id(calendar_id)
        if calendar and calendar['status'] != new_status:
            self.payment_calendar_repo.update(calendar_id, {
                'status': new_status,
                'updated_at': datetime.now().isoformat()
            })


# Instancia global del servicio
finance_service = FinanceService()

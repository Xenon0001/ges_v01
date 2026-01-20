"""
Export service for GES application
Handles data export to Excel format
"""

import pandas as pd
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Optional
from app.services.student_service import StudentService
from app.services.enrollment_service import EnrollmentService
from app.services.payment_service import PaymentService
from app.services.school_service import SchoolService


class ExportService:
    """Service for exporting data to Excel"""
    
    def __init__(self):
        self.student_service = StudentService()
        self.enrollment_service = EnrollmentService()
        self.payment_service = PaymentService()
        self.school_service = SchoolService()
    
    def export_students_to_excel(self, academic_year_id: Optional[int] = None) -> Dict:
        """Export students data to Excel"""
        try:
            # Get students data
            if academic_year_id:
                enrollments = self.enrollment_service.get_enrollments_by_filters(
                    academic_year_id=academic_year_id
                )
                # Get unique students from enrollments
                student_ids = list(set([e.student_id for e in enrollments if e.student_id]))
                students = []
                for student_id in student_ids:
                    student = self.student_service.get_student_by_id(student_id)
                    if student:
                        students.append(student)
            else:
                students = self.student_service.search_students()
            
            # Prepare data for DataFrame
            students_data = []
            for student in students:
                if student.person:
                    # Calculate age
                    age = "Desconocida"
                    if student.person.birth_date:
                        age = (date.today() - student.person.birth_date).days // 365
                    
                    student_data = {
                        'ID Estudiante': student.student_id,
                        'Nombre': student.person.name,
                        'Apellidos': student.person.last_name,
                        'Email': student.person.email or '',
                        'Teléfono': student.person.phone or '',
                        'Dirección': student.person.address or '',
                        'Fecha de Nacimiento': student.person.birth_date.strftime('%d/%m/%Y') if student.person.birth_date else '',
                        'Edad': age,
                        'Fecha de Matrícula': student.enrollment_date.strftime('%d/%m/%Y') if student.enrollment_date else '',
                        'Centro de Procedencia': student.previous_school or '',
                        'Información Médica': student.medical_info or '',
                        'Contacto de Emergencia': student.emergency_contact or ''
                    }
                    students_data.append(student_data)
            
            # Create DataFrame
            df = pd.DataFrame(students_data)
            
            # Generate filename
            school = self.school_service.get_school()
            school_name = school.name if school else "Centro"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{school_name}_Estudiantes_{timestamp}.xlsx"
            
            return {
                'success': True,
                'dataframe': df,
                'filename': filename,
                'sheet_name': 'Estudiantes',
                'record_count': len(students_data)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def export_enrollments_to_excel(self, academic_year_id: Optional[int] = None) -> Dict:
        """Export enrollments data to Excel"""
        try:
            # Get enrollments data
            if academic_year_id:
                enrollments = self.enrollment_service.get_enrollments_by_filters(
                    academic_year_id=academic_year_id
                )
            else:
                enrollments = self.enrollment_service.get_enrollments_by_filters()
            
            # Prepare data for DataFrame
            enrollments_data = []
            for enrollment in enrollments:
                # Get payment summary
                try:
                    payment_summary = self.payment_service.get_payment_summary(enrollment.id)
                except:
                    payment_summary = {
                        'total_required': 0,
                        'total_paid': 0,
                        'total_pending': 0
                    }
                
                enrollment_data = {
                    'Número de Matrícula': enrollment.enrollment_number,
                    'ID Estudiante': enrollment.student.student_id if enrollment.student else '',
                    'Nombre Estudiante': f"{enrollment.student.person.name} {enrollment.student.person.last_name}" if enrollment.student and enrollment.student.person else '',
                    'Grado': enrollment.grade.name if enrollment.grade else '',
                    'Curso': enrollment.course or '',
                    'Aula': enrollment.classroom or '',
                    'Turno': enrollment.shift or '',
                    'Fecha de Matrícula': enrollment.enrollment_date.strftime('%d/%m/%Y') if enrollment.enrollment_date else '',
                    'Estado': enrollment.status,
                    'Total Requerido': payment_summary['total_required'],
                    'Total Pagado': payment_summary['total_paid'],
                    'Total Pendiente': payment_summary['total_pending'],
                    'Porcentaje Pagado': f"{(payment_summary['total_paid'] / payment_summary['total_required'] * 100):.1f}%" if payment_summary['total_required'] > 0 else "0%",
                    'Observaciones': enrollment.observations or ''
                }
                enrollments_data.append(enrollment_data)
            
            # Create DataFrame
            df = pd.DataFrame(enrollments_data)
            
            # Generate filename
            school = self.school_service.get_school()
            school_name = school.name if school else "Centro"
            year_name = ""
            if academic_year_id:
                academic_year = self.school_service.get_academic_year_by_id(academic_year_id)
                year_name = f"_{academic_year.name}" if academic_year else ""
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{school_name}_Matriculas{year_name}_{timestamp}.xlsx"
            
            return {
                'success': True,
                'dataframe': df,
                'filename': filename,
                'sheet_name': 'Matrículas',
                'record_count': len(enrollments_data)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def export_payments_to_excel(self, academic_year_id: Optional[int] = None) -> Dict:
        """Export payments data to Excel"""
        try:
            # Get enrollments for the year
            if academic_year_id:
                enrollments = self.enrollment_service.get_enrollments_by_filters(
                    academic_year_id=academic_year_id
                )
            else:
                enrollments = self.enrollment_service.get_enrollments_by_filters()
            
            # Get all payments
            payments_data = []
            for enrollment in enrollments:
                try:
                    payments = self.payment_service.get_payments_by_enrollment(enrollment.id)
                    
                    for payment in payments:
                        payment_data = {
                            'ID Pago': payment.id,
                            'Número de Matrícula': enrollment.enrollment_number,
                            'ID Estudiante': enrollment.student.student_id if enrollment.student else '',
                            'Nombre Estudiante': f"{enrollment.student.person.name} {enrollment.student.person.last_name}" if enrollment.student and enrollment.student.person else '',
                            'Grado': enrollment.grade.name if enrollment.grade else '',
                            'Monto': payment.amount,
                            'Fecha de Vencimiento': payment.due_date.strftime('%d/%m/%Y') if payment.due_date else '',
                            'Fecha de Pago': payment.payment_date.strftime('%d/%m/%Y') if payment.payment_date else '',
                            'Estado': payment.status,
                            'Método de Pago': payment.payment_method or '',
                            'Descripción': payment.description or ''
                        }
                        payments_data.append(payment_data)
                        
                except Exception as e:
                    print(f"Error getting payments for enrollment {enrollment.id}: {e}")
                    continue
            
            # Create DataFrame
            df = pd.DataFrame(payments_data)
            
            # Generate filename
            school = self.school_service.get_school()
            school_name = school.name if school else "Centro"
            year_name = ""
            if academic_year_id:
                academic_year = self.school_service.get_academic_year_by_id(academic_year_id)
                year_name = f"_{academic_year.name}" if academic_year else ""
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{school_name}_Pagos{year_name}_{timestamp}.xlsx"
            
            return {
                'success': True,
                'dataframe': df,
                'filename': filename,
                'sheet_name': 'Pagos',
                'record_count': len(payments_data)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def export_financial_summary_to_excel(self, academic_year_id: Optional[int] = None) -> Dict:
        """Export financial summary to Excel"""
        try:
            # Get enrollments for the year
            if academic_year_id:
                enrollments = self.enrollment_service.get_enrollments_by_filters(
                    academic_year_id=academic_year_id
                )
            else:
                enrollments = self.enrollment_service.get_enrollments_by_filters()
            
            # Calculate financial summary by grade
            grade_summary = {}
            total_required = 0
            total_paid = 0
            total_pending = 0
            
            for enrollment in enrollments:
                try:
                    payment_summary = self.payment_service.get_payment_summary(enrollment.id)
                    grade_name = enrollment.grade.name if enrollment.grade else 'Sin grado'
                    
                    if grade_name not in grade_summary:
                        grade_summary[grade_name] = {
                            'total_required': 0,
                            'total_paid': 0,
                            'total_pending': 0,
                            'enrollment_count': 0
                        }
                    
                    grade_summary[grade_name]['total_required'] += payment_summary['total_required']
                    grade_summary[grade_name]['total_paid'] += payment_summary['total_paid']
                    grade_summary[grade_name]['total_pending'] += payment_summary['total_pending']
                    grade_summary[grade_name]['enrollment_count'] += 1
                    
                    total_required += payment_summary['total_required']
                    total_paid += payment_summary['total_paid']
                    total_pending += payment_summary['total_pending']
                    
                except Exception as e:
                    print(f"Error getting payment summary for enrollment {enrollment.id}: {e}")
                    continue
            
            # Prepare data for DataFrame
            summary_data = []
            for grade_name, data in grade_summary.items():
                payment_rate = (data['total_paid'] / data['total_required'] * 100) if data['total_required'] > 0 else 0
                summary_data.append({
                    'Grado': grade_name,
                    'Número de Matrículas': data['enrollment_count'],
                    'Total Requerido': data['total_required'],
                    'Total Pagado': data['total_paid'],
                    'Total Pendiente': data['total_pending'],
                    'Tasa de Pago (%)': round(payment_rate, 1)
                })
            
            # Add total row
            overall_payment_rate = (total_paid / total_required * 100) if total_required > 0 else 0
            summary_data.append({
                'Grado': 'TOTAL GENERAL',
                'Número de Matrículas': len(enrollments),
                'Total Requerido': total_required,
                'Total Pagado': total_paid,
                'Total Pendiente': total_pending,
                'Tasa de Pago (%)': round(overall_payment_rate, 1)
            })
            
            # Create DataFrame
            df = pd.DataFrame(summary_data)
            
            # Generate filename
            school = self.school_service.get_school()
            school_name = school.name if school else "Centro"
            year_name = ""
            if academic_year_id:
                academic_year = self.school_service.get_academic_year_by_id(academic_year_id)
                year_name = f"_{academic_year.name}" if academic_year else ""
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{school_name}_Resumen_Financiero{year_name}_{timestamp}.xlsx"
            
            return {
                'success': True,
                'dataframe': df,
                'filename': filename,
                'sheet_name': 'Resumen Financiero',
                'record_count': len(summary_data)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def export_complete_data_to_excel(self, academic_year_id: Optional[int] = None) -> Dict:
        """Export all data to multiple Excel sheets"""
        try:
            # Get all exports
            students_result = self.export_students_to_excel(academic_year_id)
            enrollments_result = self.export_enrollments_to_excel(academic_year_id)
            payments_result = self.export_payments_to_excel(academic_year_id)
            financial_result = self.export_financial_summary_to_excel(academic_year_id)
            
            # Check for errors
            errors = []
            if not students_result['success']:
                errors.append(f"Estudiantes: {students_result['error']}")
            if not enrollments_result['success']:
                errors.append(f"Matrículas: {enrollments_result['error']}")
            if not payments_result['success']:
                errors.append(f"Pagos: {payments_result['error']}")
            if not financial_result['success']:
                errors.append(f"Resumen financiero: {financial_result['error']}")
            
            if errors:
                return {
                    'success': False,
                    'error': '; '.join(errors)
                }
            
            # Generate filename
            school = self.school_service.get_school()
            school_name = school.name if school else "Centro"
            year_name = ""
            if academic_year_id:
                academic_year = self.school_service.get_academic_year_by_id(academic_year_id)
                year_name = f"_{academic_year.name}" if academic_year else ""
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{school_name}_Datos_Completos{year_name}_{timestamp}.xlsx"
            
            # Create Excel writer with multiple sheets
            dataframes = {
                students_result['sheet_name']: students_result['dataframe'],
                enrollments_result['sheet_name']: enrollments_result['dataframe'],
                payments_result['sheet_name']: payments_result['dataframe'],
                financial_result['sheet_name']: financial_result['dataframe']
            }
            
            return {
                'success': True,
                'dataframes': dataframes,
                'filename': filename,
                'total_records': (
                    students_result['record_count'] +
                    enrollments_result['record_count'] +
                    payments_result['record_count'] +
                    financial_result['record_count']
                )
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def save_excel_file(self, export_result: Dict, save_path: Optional[str] = None) -> Dict:
        """Save export result to Excel file"""
        try:
            if not export_result['success']:
                return export_result
            
            # Determine save path
            if save_path:
                file_path = Path(save_path)
            else:
                # Default to Downloads folder
                downloads_path = Path.home() / "Downloads"
                downloads_path.mkdir(exist_ok=True)
                file_path = downloads_path / export_result['filename']
            
            # Save Excel file
            if 'dataframes' in export_result:
                # Multiple sheets
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    for sheet_name, df in export_result['dataframes'].items():
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
            else:
                # Single sheet
                export_result['dataframe'].to_excel(
                    file_path, 
                    sheet_name=export_result['sheet_name'], 
                    index=False
                )
            
            return {
                'success': True,
                'file_path': str(file_path),
                'file_size': file_path.stat().st_size
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Error al guardar archivo Excel: {str(e)}"
            }
    
    def get_available_exports(self) -> List[Dict]:
        """Get list of available export types"""
        return [
            {
                'id': 'students',
                'name': 'Estudiantes',
                'description': 'Exportar lista completa de estudiantes',
                'method': 'export_students_to_excel'
            },
            {
                'id': 'enrollments',
                'name': 'Matrículas',
                'description': 'Exportar matrículas con información financiera',
                'method': 'export_enrollments_to_excel'
            },
            {
                'id': 'payments',
                'name': 'Pagos',
                'description': 'Exportar todos los pagos registrados',
                'method': 'export_payments_to_excel'
            },
            {
                'id': 'financial_summary',
                'name': 'Resumen Financiero',
                'description': 'Exportar resumen financiero por grado',
                'method': 'export_financial_summary_to_excel'
            },
            {
                'id': 'complete_data',
                'name': 'Datos Completos',
                'description': 'Exportar toda la información en múltiples hojas',
                'method': 'export_complete_data_to_excel'
            }
        ]

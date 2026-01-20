"""
Academic History service for GES application
Handles annual academic history generation and persistence
"""

import json
import os
from datetime import date
from typing import Dict, List, Optional
from pathlib import Path

from app.services.student_service import StudentService
from app.services.enrollment_service import EnrollmentService
from app.services.payment_service import PaymentService
from app.services.school_service import SchoolService


class AcademicHistoryService:
    """Service for managing academic history"""
    
    def __init__(self):
        self.student_service = StudentService()
        self.enrollment_service = EnrollmentService()
        self.payment_service = PaymentService()
        self.school_service = SchoolService()
        
        # History directory
        self.history_dir = Path("historial")
        self.history_dir.mkdir(exist_ok=True)
    
    def generate_academic_history(self, academic_year_id: int) -> Dict:
        """Generate complete academic history for a year"""
        try:
            # Get academic year info
            academic_year = self.school_service.get_academic_year_by_id(academic_year_id)
            if not academic_year:
                raise ValueError("Año académico no encontrado")
            
            # Get school info
            school = self.school_service.get_school()
            school_name = school.name if school else "Centro Educativo"
            
            # Create history directory
            year_folder_name = f"{school_name}_{academic_year.name}"
            year_folder = self.history_dir / year_folder_name
            year_folder.mkdir(exist_ok=True)
            
            # Generate data files
            students_data = self._generate_students_data(academic_year_id)
            enrollments_data = self._generate_enrollments_data(academic_year_id)
            payments_data = self._generate_payments_data(academic_year_id)
            summary_data = self._generate_summary_data(
                students_data, enrollments_data, payments_data, academic_year
            )
            
            # Save files
            files_created = []
            
            # Save students
            students_file = year_folder / "estudiantes.json"
            with open(students_file, 'w', encoding='utf-8') as f:
                json.dump(students_data, f, ensure_ascii=False, indent=2, default=str)
            files_created.append(str(students_file))
            
            # Save enrollments
            enrollments_file = year_folder / "matriculas.json"
            with open(enrollments_file, 'w', encoding='utf-8') as f:
                json.dump(enrollments_data, f, ensure_ascii=False, indent=2, default=str)
            files_created.append(str(enrollments_file))
            
            # Save payments
            payments_file = year_folder / "pagos.json"
            with open(payments_file, 'w', encoding='utf-8') as f:
                json.dump(payments_data, f, ensure_ascii=False, indent=2, default=str)
            files_created.append(str(payments_file))
            
            # Save summary
            summary_file = year_folder / "resumen.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary_data, f, ensure_ascii=False, indent=2, default=str)
            files_created.append(str(summary_file))
            
            return {
                'success': True,
                'year_folder': str(year_folder),
                'files_created': files_created,
                'summary': summary_data
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _generate_students_data(self, academic_year_id: int) -> List[Dict]:
        """Generate students data for the year"""
        try:
            # Get enrollments for the year
            enrollments = self.enrollment_service.get_enrollments_by_filters(
                academic_year_id=academic_year_id
            )
            
            students_data = []
            unique_students = set()
            
            for enrollment in enrollments:
                if enrollment.student_id and enrollment.student_id not in unique_students:
                    unique_students.add(enrollment.student_id)
                    
                    student = enrollment.student
                    if student and student.person:
                        student_data = {
                            'student_id': student.student_id,
                            'name': student.person.name,
                            'last_name': student.person.last_name,
                            'birth_date': student.person.birth_date.isoformat() if student.person.birth_date else None,
                            'email': student.person.email,
                            'phone': student.person.phone,
                            'address': student.person.address,
                            'enrollment_date': student.enrollment_date.isoformat() if student.enrollment_date else None,
                            'previous_school': student.previous_school,
                            'medical_info': student.medical_info,
                            'emergency_contact': student.emergency_contact
                        }
                        students_data.append(student_data)
            
            return students_data
            
        except Exception as e:
            print(f"Error generating students data: {e}")
            return []
    
    def _generate_enrollments_data(self, academic_year_id: int) -> List[Dict]:
        """Generate enrollments data for the year"""
        try:
            enrollments = self.enrollment_service.get_enrollments_by_filters(
                academic_year_id=academic_year_id
            )
            
            enrollments_data = []
            
            for enrollment in enrollments:
                enrollment_data = {
                    'enrollment_number': enrollment.enrollment_number,
                    'enrollment_date': enrollment.enrollment_date.isoformat() if enrollment.enrollment_date else None,
                    'status': enrollment.status,
                    'course': enrollment.course,
                    'classroom': enrollment.classroom,
                    'shift': enrollment.shift,
                    'observations': enrollment.observations,
                    'student_info': {
                        'student_id': enrollment.student.student_id if enrollment.student else None,
                        'name': enrollment.student.person.name if enrollment.student and enrollment.student.person else None,
                        'last_name': enrollment.student.person.last_name if enrollment.student and enrollment.student.person else None
                    },
                    'grade_info': {
                        'grade_id': enrollment.grade.id if enrollment.grade else None,
                        'grade_name': enrollment.grade.name if enrollment.grade else None
                    },
                    'academic_year_info': {
                        'year_id': enrollment.academic_year.id if enrollment.academic_year else None,
                        'year_name': enrollment.academic_year.name if enrollment.academic_year else None
                    }
                }
                enrollments_data.append(enrollment_data)
            
            return enrollments_data
            
        except Exception as e:
            print(f"Error generating enrollments data: {e}")
            return []
    
    def _generate_payments_data(self, academic_year_id: int) -> List[Dict]:
        """Generate payments data for the year"""
        try:
            # Get enrollments for the year
            enrollments = self.enrollment_service.get_enrollments_by_filters(
                academic_year_id=academic_year_id
            )
            
            payments_data = []
            
            for enrollment in enrollments:
                try:
                    payments = self.payment_service.get_payments_by_enrollment(enrollment.id)
                    
                    for payment in payments:
                        payment_data = {
                            'payment_id': payment.id,
                            'amount': payment.amount,
                            'payment_date': payment.payment_date.isoformat() if payment.payment_date else None,
                            'due_date': payment.due_date.isoformat() if payment.due_date else None,
                            'status': payment.status,
                            'payment_method': payment.payment_method,
                            'description': payment.description,
                            'enrollment_info': {
                                'enrollment_number': enrollment.enrollment_number,
                                'student_name': f"{enrollment.student.person.name} {enrollment.student.person.last_name}" if enrollment.student and enrollment.student.person else None
                            }
                        }
                        payments_data.append(payment_data)
                        
                except Exception as e:
                    print(f"Error getting payments for enrollment {enrollment.id}: {e}")
                    continue
            
            return payments_data
            
        except Exception as e:
            print(f"Error generating payments data: {e}")
            return []
    
    def _generate_summary_data(self, students_data: List[Dict], enrollments_data: List[Dict], 
                              payments_data: List[Dict], academic_year) -> Dict:
        """Generate summary data for the year"""
        try:
            # Calculate totals
            total_students = len(students_data)
            total_enrollments = len(enrollments_data)
            
            # Calculate financial totals
            total_required = 0
            total_paid = 0
            total_pending = 0
            
            for payment in payments_data:
                total_required += payment.get('amount', 0)
                if payment.get('status') == 'PAID':
                    total_paid += payment.get('amount', 0)
                else:
                    total_pending += payment.get('amount', 0)
            
            # Grade distribution
            grade_distribution = {}
            for enrollment in enrollments_data:
                grade_name = enrollment.get('grade_info', {}).get('grade_name', 'Sin grado')
                grade_distribution[grade_name] = grade_distribution.get(grade_name, 0) + 1
            
            # Payment status distribution
            payment_status = {'PAGADO': 0, 'PENDIENTE': 0, 'VENCIDO': 0, 'CANCELADO': 0}
            for payment in payments_data:
                status = payment.get('status', 'PENDIENTE')
                if status == 'PAID':
                    payment_status['PAGADO'] += 1
                elif status == 'PENDING':
                    payment_status['PENDIENTE'] += 1
                elif status == 'OVERDUE':
                    payment_status['VENCIDO'] += 1
                elif status == 'CANCELLED':
                    payment_status['CANCELADO'] += 1
            
            summary_data = {
                'generation_date': date.today().isoformat(),
                'academic_year': {
                    'id': academic_year.id,
                    'name': academic_year.name,
                    'start_date': academic_year.start_date.isoformat() if academic_year.start_date else None,
                    'end_date': academic_year.end_date.isoformat() if academic_year.end_date else None
                },
                'totals': {
                    'total_students': total_students,
                    'total_enrollments': total_enrollments,
                    'total_required': total_required,
                    'total_paid': total_paid,
                    'total_pending': total_pending,
                    'payment_rate': (total_paid / total_required * 100) if total_required > 0 else 0
                },
                'grade_distribution': grade_distribution,
                'payment_status_distribution': payment_status,
                'files_included': [
                    'estudiantes.json',
                    'matriculas.json', 
                    'pagos.json',
                    'resumen.json'
                ]
            }
            
            return summary_data
            
        except Exception as e:
            print(f"Error generating summary data: {e}")
            return {}
    
    def get_existing_histories(self) -> List[Dict]:
        """Get list of existing academic histories"""
        try:
            histories = []
            
            if not self.history_dir.exists():
                return histories
            
            for folder in self.history_dir.iterdir():
                if folder.is_dir():
                    # Try to read summary file
                    summary_file = folder / "resumen.json"
                    if summary_file.exists():
                        try:
                            with open(summary_file, 'r', encoding='utf-8') as f:
                                summary = json.load(f)
                            
                            histories.append({
                                'folder_name': folder.name,
                                'folder_path': str(folder),
                                'summary': summary
                            })
                        except Exception as e:
                            print(f"Error reading summary from {folder}: {e}")
                            continue
            
            # Sort by generation date (newest first)
            histories.sort(key=lambda x: x['summary'].get('generation_date', ''), reverse=True)
            
            return histories
            
        except Exception as e:
            print(f"Error getting existing histories: {e}")
            return []
    
    def history_exists(self, academic_year_id: int) -> bool:
        """Check if history already exists for academic year"""
        try:
            academic_year = self.school_service.get_academic_year_by_id(academic_year_id)
            if not academic_year:
                return False
            
            school = self.school_service.get_school()
            school_name = school.name if school else "Centro Educativo"
            
            year_folder_name = f"{school_name}_{academic_year.name}"
            year_folder = self.history_dir / year_folder_name
            
            # Check if summary file exists
            summary_file = year_folder / "resumen.json"
            return summary_file.exists()
            
        except Exception as e:
            print(f"Error checking history existence: {e}")
            return False
    
    def get_history_summary(self, academic_year_id: int) -> Optional[Dict]:
        """Get summary of existing history for academic year"""
        try:
            academic_year = self.school_service.get_academic_year_by_id(academic_year_id)
            if not academic_year:
                return None
            
            school = self.school_service.get_school()
            school_name = school.name if school else "Centro Educativo"
            
            year_folder_name = f"{school_name}_{academic_year.name}"
            year_folder = self.history_dir / year_folder_name
            
            summary_file = year_folder / "resumen.json"
            if summary_file.exists():
                with open(summary_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            return None
            
        except Exception as e:
            print(f"Error getting history summary: {e}")
            return None
    
    def delete_history(self, academic_year_id: int) -> bool:
        """Delete history folder for academic year"""
        try:
            academic_year = self.school_service.get_academic_year_by_id(academic_year_id)
            if not academic_year:
                return False
            
            school = self.school_service.get_school()
            school_name = school.name if school else "Centro Educativo"
            
            year_folder_name = f"{school_name}_{academic_year.name}"
            year_folder = self.history_dir / year_folder_name
            
            if year_folder.exists():
                import shutil
                shutil.rmtree(year_folder)
                return True
            
            return False
            
        except Exception as e:
            print(f"Error deleting history: {e}")
            return False

"""
Report service for GES application
Handles chart generation and data analysis
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
from typing import Dict, List, Optional, Tuple
import io
import base64
from datetime import date
from app.services.student_service import StudentService
from app.services.enrollment_service import EnrollmentService
from app.services.payment_service import PaymentService
from app.services.school_service import SchoolService


class ReportService:
    """Service for generating reports and charts"""
    
    def __init__(self):
        self.student_service = StudentService()
        self.enrollment_service = EnrollmentService()
        self.payment_service = PaymentService()
        self.school_service = SchoolService()
        
        # Configure matplotlib for simple charts
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.rcParams['font.size'] = 10
    
    def get_general_performance_data(self, academic_year_id: Optional[int] = None) -> Dict:
        """Get general performance data for charts"""
        try:
            # Get enrollments for the year
            if academic_year_id:
                enrollments = self.enrollment_service.get_enrollments_by_filters(
                    academic_year_id=academic_year_id
                )
            else:
                enrollments = self.enrollment_service.get_enrollments_by_filters()
            
            # For MVP, simulate performance data
            # In real implementation, this would come from grades/evaluations
            total_students = len(enrollments)
            
            # Simulate performance (70% pass rate for demo)
            passed = int(total_students * 0.7)
            failed = total_students - passed
            
            return {
                'total_students': total_students,
                'passed': passed,
                'failed': failed,
                'pass_rate': (passed / total_students * 100) if total_students > 0 else 0
            }
            
        except Exception as e:
            return {
                'total_students': 0,
                'passed': 0,
                'failed': 0,
                'pass_rate': 0,
                'error': str(e)
            }
    
    def get_performance_by_grade_data(self, academic_year_id: Optional[int] = None) -> Dict:
        """Get performance data by grade"""
        try:
            # Get grades
            grades = self.school_service.get_grades()
            
            grade_data = {}
            for grade in grades:
                # Get enrollments for this grade
                if academic_year_id:
                    enrollments = self.enrollment_service.get_enrollments_by_filters(
                        academic_year_id=academic_year_id,
                        grade_id=grade.id
                    )
                else:
                    enrollments = self.enrollment_service.get_enrollments_by_filters(
                        grade_id=grade.id
                    )
                
                total = len(enrollments)
                # Simulate performance (60-80% pass rate by grade)
                pass_rate = 0.6 + (grade.id % 3) * 0.1  # Vary by grade
                passed = int(total * pass_rate)
                failed = total - passed
                
                grade_data[grade.name] = {
                    'total': total,
                    'passed': passed,
                    'failed': failed
                }
            
            return grade_data
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_enrollments_by_year_data(self) -> Dict:
        """Get enrollment data by academic year"""
        try:
            academic_years = self.school_service.get_academic_years()
            
            year_data = {}
            for year in academic_years:
                enrollments = self.enrollment_service.get_enrollments_by_filters(
                    academic_year_id=year.id
                )
                year_data[year.name] = len(enrollments)
            
            return year_data
            
        except Exception as e:
            return {'error': str(e)}
    
    def generate_performance_chart(self, academic_year_id: Optional[int] = None) -> str:
        """Generate general performance chart (bar chart)"""
        try:
            data = self.get_general_performance_data(academic_year_id)
            
            if 'error' in data:
                return ""
            
            # Create bar chart
            fig, ax = plt.subplots(figsize=(8, 6))
            
            categories = ['Aprobados', 'Suspensos']
            values = [data['passed'], data['failed']]
            colors = ['#2ecc71', '#e74c3c']
            
            bars = ax.bar(categories, values, color=colors)
            
            # Add value labels on bars
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                       f'{value}', ha='center', va='bottom')
            
            ax.set_title(f'Rendimiento General - {data["total_students"]} estudiantes')
            ax.set_ylabel('Número de Estudiantes')
            
            # Add pass rate as text
            ax.text(0.02, 0.98, f'Tasa de aprobación: {data["pass_rate"]:.1f}%',
                   transform=ax.transAxes, va='top', ha='left',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            
            plt.tight_layout()
            
            # Convert to base64 for UI display
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return image_base64
            
        except Exception as e:
            print(f"Error generating performance chart: {e}")
            return ""
    
    def generate_performance_by_grade_chart(self, academic_year_id: Optional[int] = None) -> str:
        """Generate performance by grade chart (grouped bar chart)"""
        try:
            data = self.get_performance_by_grade_data(academic_year_id)
            
            if 'error' in data:
                return ""
            
            grades = list(data.keys())
            passed = [data[grade]['passed'] for grade in grades]
            failed = [data[grade]['failed'] for grade in grades]
            
            x = range(len(grades))
            width = 0.35
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            bars1 = ax.bar([i - width/2 for i in x], passed, width, 
                          label='Aprobados', color='#2ecc71')
            bars2 = ax.bar([i + width/2 for i in x], failed, width,
                          label='Suspensos', color='#e74c3c')
            
            ax.set_xlabel('Grados')
            ax.set_ylabel('Número de Estudiantes')
            ax.set_title('Rendimiento por Grado')
            ax.set_xticks(x)
            ax.set_xticklabels(grades, rotation=45)
            ax.legend()
            
            # Add value labels
            for bars in [bars1, bars2]:
                for bar in bars:
                    height = bar.get_height()
                    if height > 0:
                        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                               f'{int(height)}', ha='center', va='bottom', fontsize=8)
            
            plt.tight_layout()
            
            # Convert to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return image_base64
            
        except Exception as e:
            print(f"Error generating grade performance chart: {e}")
            return ""
    
    def generate_enrollments_by_year_chart(self) -> str:
        """Generate enrollments by year chart (line chart)"""
        try:
            data = self.get_enrollments_by_year_data()
            
            if 'error' in data:
                return ""
            
            years = list(data.keys())
            enrollments = list(data.values())
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Create line chart with markers
            ax.plot(years, enrollments, marker='o', linewidth=2, markersize=8, color='#3498db')
            
            # Add value labels
            for i, (year, value) in enumerate(zip(years, enrollments)):
                ax.annotate(f'{value}', (i, value), textcoords="offset points",
                           xytext=(0,10), ha='center', fontsize=9)
            
            ax.set_xlabel('Año Académico')
            ax.set_ylabel('Número de Matrículas')
            ax.set_title('Evolución de Matrículas por Año Académico')
            ax.grid(True, alpha=0.3)
            
            # Rotate x-axis labels if needed
            plt.xticks(rotation=45)
            
            plt.tight_layout()
            
            # Convert to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return image_base64
            
        except Exception as e:
            print(f"Error generating enrollments chart: {e}")
            return ""
    
    def generate_financial_summary_chart(self, academic_year_id: Optional[int] = None) -> str:
        """Generate financial summary chart (pie chart)"""
        try:
            # Get all enrollments for the year
            if academic_year_id:
                enrollments = self.enrollment_service.get_enrollments_by_filters(
                    academic_year_id=academic_year_id
                )
            else:
                enrollments = self.enrollment_service.get_enrollments_by_filters()
            
            total_paid = 0
            total_pending = 0
            
            for enrollment in enrollments:
                try:
                    summary = self.payment_service.get_payment_summary(enrollment.id)
                    total_paid += summary['total_paid']
                    total_pending += summary['total_pending']
                except:
                    continue
            
            if total_paid + total_pending == 0:
                return ""
            
            # Create pie chart
            fig, ax = plt.subplots(figsize=(8, 6))
            
            labels = ['Pagado', 'Pendiente']
            sizes = [total_paid, total_pending]
            colors = ['#2ecc71', '#f39c12']
            explode = (0.05, 0)  # Explode the 'Paid' slice
            
            wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                                            autopct='%1.1f%%', shadow=True, startangle=90)
            
            # Add total amount as title
            total = total_paid + total_pending
            ax.set_title(f'Resumen Financiero\nTotal: {total:,.0f} XAF')
            
            # Equal aspect ratio ensures that pie is drawn as a circle
            ax.axis('equal')
            
            plt.tight_layout()
            
            # Convert to base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return image_base64
            
        except Exception as e:
            print(f"Error generating financial chart: {e}")
            return ""
    
    def get_available_charts(self) -> List[Dict]:
        """Get list of available charts with descriptions"""
        return [
            {
                'id': 'performance',
                'name': 'Rendimiento General',
                'description': 'Aprobados vs Suspensos totales',
                'method': 'generate_performance_chart'
            },
            {
                'id': 'performance_by_grade',
                'name': 'Rendimiento por Grado',
                'description': 'Desempeño académico por cada grado',
                'method': 'generate_performance_by_grade_chart'
            },
            {
                'id': 'enrollments_by_year',
                'name': 'Matrículas por Año',
                'description': 'Evolución de matrículas anuales',
                'method': 'generate_enrollments_by_year_chart'
            },
            {
                'id': 'financial_summary',
                'name': 'Resumen Financiero',
                'description': 'Estado de pagos vs pendientes',
                'method': 'generate_financial_summary_chart'
            }
        ]
    
    def generate_chart(self, chart_id: str, academic_year_id: Optional[int] = None) -> str:
        """Generate specific chart by ID"""
        chart_methods = {
            'performance': self.generate_performance_chart,
            'performance_by_grade': self.generate_performance_by_grade_chart,
            'enrollments_by_year': self.generate_enrollments_by_year_chart,
            'financial_summary': self.generate_financial_summary_chart
        }
        
        method = chart_methods.get(chart_id)
        if method:
            return method(academic_year_id)
        else:
            return ""

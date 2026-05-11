"""
Report Service - Generación de PDFs para reportes académicos y financieros
Integra AcademicService y FinanceService para crear reportes descargables
"""

import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from services.academic_service import AcademicService
from services.finance_service import FinanceService


class ReportService:
    """Servicio para generación de reportes PDF"""
    
    def __init__(self):
        self.academic_service = AcademicService()
        self.finance_service = FinanceService()
        self.output_dir = "reports"
        self._ensure_output_directory()
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _ensure_output_directory(self):
        """Crea directorio de reportes si no existe"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.output_dir = os.path.join(base_dir, "reports")
        subdirs = ['academic', 'financial', 'classroom']
        for subdir in subdirs:
            dir_path = os.path.join(self.output_dir, subdir)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
    
    def _setup_custom_styles(self):
        """Configura estilos personalizados para los reportes"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkblue
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6
        ))
    
    def generate_student_academic_report(self, student_id: int, academic_year: int, trimester: Optional[int] = None) -> str:
        """
        Genera reporte académico de un estudiante
        
        Args:
            student_id: ID del estudiante
            academic_year: Año académico
            trimester: Trimestre específico (opcional)
            
        Returns:
            str: Ruta del PDF generado
        """
        # Importar student_repo
        from database.repository import student_repo
        
        # Obtener datos del estudiante
        student = student_repo.get_by_id(student_id)
        if not student:
            raise ValueError(f"No se encontró el estudiante {student_id}")
        
        # Obtener datos académicos
        student_data = self.academic_service.get_student_academic_summary(student_id, academic_year)
        
        if 'error' in student_data:
            raise ValueError(student_data['error'])
        
        # Nombre del estudiante
        student_name = f"{student.get('first_name', '')} {student.get('last_name', '')}"
        
        # Crear nombre de archivo con self.output_dir
        trimester_str = f"_trimester{trimester}" if trimester else "_complete"
        filename = os.path.join(self.output_dir, f"academic/student_{student_id}_{academic_year}{trimester_str}.pdf")
        
        # Crear documento
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        # Título
        title = f"REPORTE ACADÉMICO - {student_name.upper()}"
        story.append(Paragraph(title, self.styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        # Información del estudiante
        story.append(Paragraph("INFORMACIÓN DEL ESTUDIANTE", self.styles['CustomHeading']))
        student_info = [
            ['Nombre:', student_name],
            ['ID:', str(student['id'])],
            ['Aula:', student.get('classroom', 'N/A')],
            ['Año Académico:', str(academic_year)],
            ['Trimestre:', str(trimester) if trimester else 'Todos']
        ]
        
        student_table = Table(student_info, colWidths=[2*inch, 4*inch])
        student_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(student_table)
        story.append(Spacer(1, 20))
        
        # Calificaciones
        story.append(Paragraph("CALIFICACIONES", self.styles['CustomHeading']))
        
        if student_data['detailed_scores']:
            # Filtrar por trimestre si es necesario
            scores = student_data['detailed_scores']
            if trimester:
                scores = [s for s in scores if s.get('trimester') == trimester]
            
            if scores:
                grades_data = [['Materia', 'Trimestre', 'Calificación', 'Estado']]
                for score in scores:
                    grade = score.get('score', 0)
                    status = 'Aprobado' if grade >= 5.0 else 'Reprobado'
                    grades_data.append([
                        score.get('subject_name', 'N/A'),
                        str(score.get('trimester', 'N/A')),
                        str(grade),
                        status
                    ])
                
                grades_table = Table(grades_data, colWidths=[2.5*inch, 1.2*inch, 1.2*inch, 1.2*inch])
                grades_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(grades_table)
            else:
                story.append(Paragraph("No hay calificaciones para el trimestre especificado.", self.styles['CustomNormal']))
        else:
            story.append(Paragraph("No hay calificaciones registradas.", self.styles['CustomNormal']))
        
        story.append(Spacer(1, 20))
        
        # Resumen académico
        story.append(Paragraph("RESUMEN ACADÉMICO", self.styles['CustomHeading']))
        summary_data = [
            ['Promedio General:', f"{student_data['annual_summary'].get('average', 0):.2f}"],
            ['Materias Aprobadas:', str(student_data['annual_summary'].get('passed_subjects', 0))],
            ['Materias Reprobadas:', str(student_data['annual_summary'].get('failed_subjects', 0))],
            ['Estado Académico:', student_data.get('academic_status', 'N/A')]
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 1.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(summary_table)
        
        # Generar PDF
        doc.build(story)
        return filename
    
    def generate_delinquency_report(self, include_overdue_only: bool = True) -> str:
        """
        Genera reporte de morosidad
        
        Args:
            include_overdue_only: Si True, solo pagos vencidos
            
        Returns:
            str: Ruta del PDF generado
        """
        # Obtener datos financieros
        if include_overdue_only:
            payments = self.finance_service.get_overdue_payments()
            report_type = "vencidos"
        else:
            payments = self.finance_service.get_pending_payments()
            report_type = "pendientes"
        
        summary = self.finance_service.get_payment_summary()
        
        # Crear nombre de archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.output_dir, f"financial/delinquency_{report_type}_{timestamp}.pdf")
        
        # Crear documento
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        # Título
        title = f"REPORTE DE MOROSIDAD - PAGOS {report_type.upper()}"
        story.append(Paragraph(title, self.styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        # Fecha de generación
        story.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", self.styles['CustomNormal']))
        story.append(Spacer(1, 20))
        
        # Resumen ejecutivo
        story.append(Paragraph("RESUMEN EJECUTIVO", self.styles['CustomHeading']))
        summary_data = [
            ['Total Estudiantes:', str(summary.total_students)],
            ['Total Deuda:', f"{summary.total_due:,.2f} FCFA"],
            ['Total Pagado:', f"{summary.total_paid:,.2f} FCFA"],
            ['Total Pendiente:', f"{summary.total_outstanding:,.2f} FCFA"],
            ['Tasa de Cobro:', f"{summary.collection_rate:.1f}%"],
            ['Pagos Vencidos:', str(summary.overdue_payments)],
            ['Monto Vencido:', f"{summary.overdue_amount:,.2f} FCFA"]
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Detalle de pagos
        story.append(Paragraph("DETALLE DE PAGOS", self.styles['CustomHeading']))
        
        if payments:
            payments_data = [['Estudiante', 'Tutor', 'Monto Due', 'Monto Pagado', 'Pendiente', 'Estado', 'Fecha Vencimiento']]
            
            for payment in payments:
                student_name = payment.get('student_name', 'N/A')
                tutor_name = payment.get('tutor_name', 'N/A')
                amount_due = payment.get('amount_due', 0)
                amount_paid = payment.get('amount_paid', 0)
                outstanding = amount_due - amount_paid
                status = payment.get('status', 'N/A')
                due_date = payment.get('due_date', 'N/A')
                
                payments_data.append([
                    student_name,
                    tutor_name,
                    f"{amount_due:,.2f} FCFA",
                    f"{amount_paid:,.2f} FCFA",
                    f"{outstanding:,.2f} FCFA",
                    status,
                    due_date
                ])
            
            payments_table = Table(payments_data, colWidths=[1.8*inch, 1.5*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1.2*inch])
            payments_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(payments_table)
        else:
            story.append(Paragraph("No hay pagos para mostrar.", self.styles['CustomNormal']))
        
        # Generar PDF
        doc.build(story)
        return filename
    
    def generate_classroom_performance_report(self, classroom_id: int, academic_year: int, trimester: Optional[int] = None) -> str:
        """
        Genera reporte de rendimiento por aula
        
        Args:
            classroom_id: ID del aula
            academic_year: Año académico
            trimester: Trimestre específico (opcional)
            
        Returns:
            str: Ruta del PDF generado
        """
        # Importar classroom_repo
        from database.repository import classroom_repo
        
        # Obtener datos del aula
        classroom = classroom_repo.get_by_id(classroom_id)
        if not classroom:
            raise ValueError(f"No se encontró el aula {classroom_id}")
        classroom_name = classroom.get('name', f'Aula {classroom_id}')
        
        # Obtener datos del aula
        classroom_data = self.academic_service.get_classroom_academic_summary(classroom_id, academic_year, trimester)
        
        if 'error' in classroom_data:
            raise ValueError(classroom_data['error'])
        
        # Crear nombre de archivo
        trimester_str = f"_trimester{trimester}" if trimester else "_complete"
        filename = os.path.join(self.output_dir, f"classroom/classroom_{classroom_id}_{academic_year}{trimester_str}.pdf")
        
        # Crear documento
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        # Título
        title = f"REPORTE DE RENDIMIENTO - {classroom_name.upper()}"
        story.append(Paragraph(title, self.styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        # Información del aula
        story.append(Paragraph("INFORMACIÓN DEL AULA", self.styles['CustomHeading']))
        classroom_info = [
            ['Nombre:', classroom_name],
            ['Profesor:', classroom.get('teacher_name', 'N/A')],
            ['Año Académico:', str(academic_year)],
            ['Trimestre:', str(trimester) if trimester else 'Todos'],
            ['Total Estudiantes:', str(classroom_data['total_students'])]
        ]
        
        classroom_table = Table(classroom_info, colWidths=[2*inch, 4*inch])
        classroom_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(classroom_table)
        story.append(Spacer(1, 20))
        
        # Estadísticas generales
        story.append(Paragraph("ESTADÍSTICAS GENERALES", self.styles['CustomHeading']))
        metrics = classroom_data['performance_metrics']
        stats_data = [
            ['Promedio General:', f"{metrics.get('classroom_average', 0):.2f}"],
            ['Estudiantes Aprobados:', str(metrics.get('passed_students', 0))],
            ['Estudiantes Reprobados:', str(metrics.get('failed_students', 0))],
            ['Tasa de Aprobación:', f"{metrics.get('pass_rate', 0):.1f}%"],
            ['Estudiantes en Riesgo:', str(len(classroom_data['students_at_risk']))],
            ['Mejores Estudiantes:', str(len(classroom_data['top_performers']))]
        ]
        
        stats_table = Table(stats_data, colWidths=[2.5*inch, 2*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(stats_table)
        story.append(Spacer(1, 20))
        
        # Rendimiento por materia
        if classroom_data.get('subject_performance'):
            story.append(Paragraph("RENDIMIENTO POR MATERIA", self.styles['CustomHeading']))
            subjects_data = [['Materia', 'Promedio', 'Aprobados', 'Reprobados', 'Tasa Aprobación']]
            
            for subject in classroom_data['subject_performance']:
                subjects_data.append([
                    subject.get('subject_name', 'N/A'),
                    f"{subject.get('average', 0):.2f}",
                    str(subject.get('passed_count', 0)),
                    str(subject.get('failed_count', 0)),
                    f"{subject.get('pass_rate', 0):.1f}%"
                ])
            
            subjects_table = Table(subjects_data, colWidths=[2*inch, 1*inch, 1*inch, 1*inch, 1.2*inch])
            subjects_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(subjects_table)
            story.append(Spacer(1, 20))
        
        # Estudiantes en riesgo
        if classroom_data.get('students_at_risk'):
            story.append(Paragraph("ESTUDIANTES EN RIESGO", self.styles['CustomHeading']))
            risk_data = [['Estudiante', 'Promedio', 'Materias Reprobadas', 'Estado']]
            
            for student_risk in classroom_data['students_at_risk']:
                student_info = student_risk.get('student_info', {})
                risk_data.append([
                    f"{student_info.get('first_name', '')} {student_info.get('last_name', '')}",
                    f"{student_risk.get('average', 0):.2f}",
                    str(student_risk.get('failed_subjects', 0)),
                    'En Riesgo'
                ])
            
            risk_table = Table(risk_data, colWidths=[2.5*inch, 1*inch, 1.5*inch, 1.2*inch])
            risk_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkred),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightcoral),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(risk_table)
        
        # Generar PDF
        doc.build(story)
        return filename

"""
API Client - Cliente HTTP para conectar GES UI con servidor remoto
"""

import requests
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import os

class GESApiClient:
    """Cliente HTTP para comunicarse con el servidor GES"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.base_url = f"http://{config.get('server_ip', 'localhost')}:{config.get('server_port', 8000)}"
        self.token = None
        self.session = requests.Session()
        
        # Headers por defecto
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Maneja respuestas del servidor
        """
        try:
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                raise Exception("Token inválido o expirado")
            elif response.status_code == 403:
                raise Exception("Permisos insuficientes")
            else:
                raise Exception(f"Error del servidor: {response.status_code}")
        except json.JSONDecodeError:
            raise Exception("Respuesta inválida del servidor")
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Autentica usuario y guarda token
        """
        try:
            response = self.session.post(
                f"{self.base_url}/auth/login",
                json={"username": username, "password": password}
            )
            
            data = self._handle_response(response)
            
            # Guardar token para requests futuras
            self.token = data.get('token')
            
            return data.get('user_data', {})
            
        except Exception as e:
            raise Exception(f"Error de login: {str(e)}")
    
    def get_all_students(self) -> List[Dict[str, Any]]:
        """
        Obtiene lista de estudiantes
        """
        if not self.token:
            raise Exception("No hay token de sesión")
        
        try:
            response = self.session.get(
                f"{self.base_url}/students/",
                headers={'Authorization': f'Bearer {self.token}'}
            )
            
            return self._handle_response(response)
            
        except Exception as e:
            raise Exception(f"Error obteniendo estudiantes: {str(e)}")
    
    def create_student(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea nuevo estudiante
        """
        if not self.token:
            raise Exception("No hay token de sesión")
        
        try:
            response = self.session.post(
                f"{self.base_url}/students/",
                json=student_data,
                headers={'Authorization': f'Bearer {self.token}'}
            )
            
            return self._handle_response(response)
            
        except Exception as e:
            raise Exception(f"Error creando estudiante: {str(e)}")
    
    def get_academic_dashboard_data(self, year: int) -> Dict[str, Any]:
        """
        Obtiene datos académicos del dashboard
        """
        if not self.token:
            raise Exception("No hay token de sesión")
        
        try:
            response = self.session.get(
                f"{self.base_url}/dashboard/",
                headers={'Authorization': f'Bearer {self.token}'}
            )
            
            data = self._handle_response(response)
            return data.get('academic', {})
            
        except Exception as e:
            raise Exception(f"Error obteniendo datos académicos: {str(e)}")
    
    def get_financial_dashboard_data(self) -> Dict[str, Any]:
        """
        Obtiene datos financieros del dashboard
        """
        if not self.token:
            raise Exception("No hay token de sesión")
        
        try:
            response = self.session.get(
                f"{self.base_url}/dashboard/",
                headers={'Authorization': f'Bearer {self.token}'}
            )
            
            data = self._handle_response(response)
            return data.get('financial', {})
            
        except Exception as e:
            raise Exception(f"Error obteniendo datos financieros: {str(e)}")

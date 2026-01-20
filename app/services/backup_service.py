"""
Backup service for GES application
Handles system backup and restoration
"""

import os
import shutil
import zipfile
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from app.services.settings_service import SettingsService


class BackupService:
    """Service for system backup and restoration"""
    
    def __init__(self):
        self.settings_service = SettingsService()
        
        # Default paths
        self.project_root = Path.cwd()
        self.db_path = self.project_root / "ges_database.db"
        self.history_path = self.project_root / "historial"
        self.config_path = self.project_root / "config"
        
        # Ensure config directory exists
        self.config_path.mkdir(exist_ok=True)
    
    def create_backup(self, backup_path: Optional[str] = None) -> Dict:
        """Create a complete system backup"""
        try:
            # Get backup path
            if not backup_path:
                settings = self.settings_service.load_settings()
                backup_dir = settings.get('backup_path', str(self.project_root / "backups"))
                backup_dir_path = Path(backup_dir)
                backup_dir_path.mkdir(exist_ok=True)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_filename = f"ges_backup_{timestamp}.zip"
                backup_path = backup_dir_path / backup_filename
            else:
                backup_path = Path(backup_path)
            
            # Create backup
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
                # Add database
                if self.db_path.exists():
                    backup_zip.write(self.db_path, "ges_database.db")
                
                # Add history folder
                if self.history_path.exists():
                    for file_path in self.history_path.rglob('*'):
                        if file_path.is_file():
                            arcname = file_path.relative_to(self.project_root)
                            backup_zip.write(file_path, arcname)
                
                # Add config files
                if self.config_path.exists():
                    for file_path in self.config_path.rglob('*'):
                        if file_path.is_file():
                            arcname = file_path.relative_to(self.project_root)
                            backup_zip.write(file_path, arcname)
                
                # Add backup metadata
                metadata = {
                    'backup_date': datetime.now().isoformat(),
                    'version': '1.0',
                    'description': 'GES System Backup',
                    'files_included': []
                }
                
                # List files in backup
                with zipfile.ZipFile(backup_path, 'r') as zip_ref:
                    metadata['files_included'] = zip_ref.namelist()
                
                # Add metadata file
                metadata_json = json.dumps(metadata, indent=2, default=str)
                backup_zip.writestr("backup_metadata.json", metadata_json)
            
            # Get file size
            file_size = backup_path.stat().st_size
            file_size_mb = file_size / (1024 * 1024)
            
            return {
                'success': True,
                'backup_path': str(backup_path),
                'file_size': file_size,
                'file_size_mb': round(file_size_mb, 2),
                'backup_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def restore_backup(self, backup_path: str) -> Dict:
        """Restore system from backup"""
        try:
            backup_path = Path(backup_path)
            
            if not backup_path.exists():
                raise ValueError("El archivo de backup no existe")
            
            # Read metadata first
            with zipfile.ZipFile(backup_path, 'r') as backup_zip:
                if "backup_metadata.json" in backup_zip.namelist():
                    metadata_content = backup_zip.read("backup_metadata.json")
                    metadata = json.loads(metadata_content.decode('utf-8'))
                else:
                    metadata = {
                        'backup_date': 'Desconocido',
                        'version': 'Desconocido',
                        'files_included': backup_zip.namelist()
                    }
            
            # Confirm restoration
            return {
                'success': True,
                'metadata': metadata,
                'backup_path': str(backup_path),
                'requires_confirmation': True
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def confirm_restore(self, backup_path: str) -> Dict:
        """Confirm and execute restoration"""
        try:
            backup_path = Path(backup_path)
            
            # Create temporary restore directory
            temp_restore_path = self.project_root / "temp_restore"
            temp_restore_path.mkdir(exist_ok=True)
            
            # Extract backup
            with zipfile.ZipFile(backup_path, 'r') as backup_zip:
                backup_zip.extractall(temp_restore_path)
            
            # Restore files
            restored_files = []
            
            # Restore database
            db_backup_path = temp_restore_path / "ges_database.db"
            if db_backup_path.exists():
                # Close database connections if any
                shutil.copy2(db_backup_path, self.db_path)
                restored_files.append("Base de datos")
            
            # Restore history folder
            history_backup_path = temp_restore_path / "historial"
            if history_backup_path.exists():
                if self.history_path.exists():
                    shutil.rmtree(self.history_path)
                shutil.copytree(history_backup_path, self.history_path)
                restored_files.append("Historial académico")
            
            # Restore config files
            config_backup_path = temp_restore_path / "config"
            if config_backup_path.exists():
                for file_path in config_backup_path.rglob('*'):
                    if file_path.is_file():
                        dest_path = self.config_path / file_path.name
                        shutil.copy2(file_path, dest_path)
                restored_files.append("Configuración")
            
            # Clean up temporary directory
            shutil.rmtree(temp_restore_path)
            
            return {
                'success': True,
                'restored_files': restored_files,
                'restore_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            # Clean up on error
            temp_restore_path = self.project_root / "temp_restore"
            if temp_restore_path.exists():
                shutil.rmtree(temp_restore_path)
            
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_existing_backups(self) -> List[Dict]:
        """Get list of existing backups"""
        try:
            settings = self.settings_service.load_settings()
            backup_dir = settings.get('backup_path', str(self.project_root / "backups"))
            backup_dir_path = Path(backup_dir)
            
            if not backup_dir_path.exists():
                return []
            
            backups = []
            
            for backup_file in backup_dir_path.glob("*.zip"):
                try:
                    # Get file info
                    stat = backup_file.stat()
                    file_size = stat.st_size
                    file_size_mb = round(file_size / (1024 * 1024), 2)
                    
                    # Try to read metadata
                    metadata = None
                    try:
                        with zipfile.ZipFile(backup_file, 'r') as zip_ref:
                            if "backup_metadata.json" in zip_ref.namelist():
                                metadata_content = zip_ref.read("backup_metadata.json")
                                metadata = json.loads(metadata_content.decode('utf-8'))
                    except:
                        pass
                    
                    backup_info = {
                        'filename': backup_file.name,
                        'path': str(backup_file),
                        'size': file_size,
                        'size_mb': file_size_mb,
                        'created_date': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        'modified_date': datetime.fromtimestamp(stat.st_mtime).isoformat()
                    }
                    
                    if metadata:
                        backup_info['backup_date'] = metadata.get('backup_date')
                        backup_info['version'] = metadata.get('version')
                        backup_info['description'] = metadata.get('description')
                        backup_info['files_count'] = len(metadata.get('files_included', []))
                    else:
                        backup_info['backup_date'] = backup_info['created_date']
                        backup_info['version'] = 'Desconocido'
                        backup_info['description'] = 'Backup del sistema'
                        backup_info['files_count'] = 0
                    
                    backups.append(backup_info)
                    
                except Exception as e:
                    print(f"Error reading backup {backup_file}: {e}")
                    continue
            
            # Sort by date (newest first)
            backups.sort(key=lambda x: x['backup_date'], reverse=True)
            
            return backups
            
        except Exception as e:
            print(f"Error getting existing backups: {e}")
            return []
    
    def delete_backup(self, backup_path: str) -> bool:
        """Delete a backup file"""
        try:
            backup_path = Path(backup_path)
            if backup_path.exists():
                backup_path.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error deleting backup: {e}")
            return False
    
    def validate_backup(self, backup_path: str) -> Dict:
        """Validate backup file integrity"""
        try:
            backup_path = Path(backup_path)
            
            if not backup_path.exists():
                return {
                    'valid': False,
                    'error': 'El archivo no existe'
                }
            
            # Try to read zip file
            with zipfile.ZipFile(backup_path, 'r') as backup_zip:
                # Check if it's a valid zip
                files = backup_zip.namelist()
                
                # Check for essential files
                has_db = "ges_database.db" in files
                has_metadata = "backup_metadata.json" in files
                
                # Read metadata if available
                metadata = None
                if has_metadata:
                    metadata_content = backup_zip.read("backup_metadata.json")
                    metadata = json.loads(metadata_content.decode('utf-8'))
                
                return {
                    'valid': True,
                    'files_count': len(files),
                    'has_database': has_db,
                    'has_metadata': has_metadata,
                    'metadata': metadata,
                    'file_size': backup_path.stat().st_size
                }
                
        except zipfile.BadZipFile:
            return {
                'valid': False,
                'error': 'El archivo no es un backup válido (ZIP corrupto)'
            }
        except Exception as e:
            return {
                'valid': False,
                'error': f'Error al validar backup: {str(e)}'
            }

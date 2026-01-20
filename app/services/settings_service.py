"""
Settings service for GES application
Handles system configuration and preferences
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from app.services.school_service import SchoolService


class SettingsService:
    """Service for managing system settings"""
    
    def __init__(self):
        self.school_service = SchoolService()
        
        # Settings file path
        self.project_root = Path.cwd()
        self.config_dir = self.project_root / "config"
        self.settings_file = self.config_dir / "settings.json"
        
        # Ensure config directory exists
        self.config_dir.mkdir(exist_ok=True)
        
        # Default settings
        self.default_settings = {
            'school_info': {
                'name': '',
                'address': '',
                'phone': '',
                'email': '',
                'website': ''
            },
            'academic_settings': {
                'active_academic_year_id': None,
                'default_grade_id': None,
                'enrollment_fee': 50000,
                'currency': 'XAF'
            },
            'paths': {
                'backup_path': str(self.project_root / "backups"),
                'history_path': str(self.project_root / "historial"),
                'export_path': str(Path.home() / "Downloads")
            },
            'ui_preferences': {
                'theme': 'light',  # light, dark, system
                'language': 'es',
                'auto_save_interval': 300,  # seconds
                'show_confirmations': True
            },
            'system': {
                'version': '1.0.0',
                'first_run': True,
                'last_backup_date': None,
                'data_migration_version': '1.0.0'
            }
        }
    
    def load_settings(self) -> Dict[str, Any]:
        """Load settings from file"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                # Merge with defaults to ensure all keys exist
                return self._merge_settings(self.default_settings, settings)
            else:
                # Create default settings file
                self.save_settings(self.default_settings)
                return self.default_settings.copy()
                
        except Exception as e:
            print(f"Error loading settings: {e}")
            return self.default_settings.copy()
    
    def save_settings(self, settings: Dict[str, Any]) -> bool:
        """Save settings to file"""
        try:
            # Ensure all required keys exist
            merged_settings = self._merge_settings(self.default_settings, settings)
            
            # Add system metadata
            merged_settings['system']['last_saved'] = self._get_timestamp()
            
            # Save to file
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(merged_settings, f, ensure_ascii=False, indent=2, default=str)
            
            return True
            
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get_setting(self, key_path: str, default: Any = None) -> Any:
        """Get a specific setting by key path (e.g., 'school_info.name')"""
        try:
            settings = self.load_settings()
            keys = key_path.split('.')
            value = settings
            
            for key in keys:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    return default
            
            return value
            
        except Exception as e:
            print(f"Error getting setting {key_path}: {e}")
            return default
    
    def update_setting(self, key_path: str, value: Any) -> bool:
        """Update a specific setting by key path"""
        try:
            settings = self.load_settings()
            keys = key_path.split('.')
            current = settings
            
            # Navigate to the parent of the target key
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            
            # Set the value
            current[keys[-1]] = value
            
            return self.save_settings(settings)
            
        except Exception as e:
            print(f"Error updating setting {key_path}: {e}")
            return False
    
    def update_multiple_settings(self, updates: Dict[str, Any]) -> bool:
        """Update multiple settings at once"""
        try:
            settings = self.load_settings()
            
            for key_path, value in updates.items():
                keys = key_path.split('.')
                current = settings
                
                # Navigate to the parent of the target key
                for key in keys[:-1]:
                    if key not in current:
                        current[key] = {}
                    current = current[key]
                
                # Set the value
                current[keys[-1]] = value
            
            return self.save_settings(settings)
            
        except Exception as e:
            print(f"Error updating multiple settings: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """Reset all settings to defaults"""
        try:
            # Mark as not first run anymore
            default_settings = self.default_settings.copy()
            default_settings['system']['first_run'] = False
            
            return self.save_settings(default_settings)
            
        except Exception as e:
            print(f"Error resetting settings: {e}")
            return False
    
    def export_settings(self, export_path: str) -> bool:
        """Export settings to specified path"""
        try:
            settings = self.load_settings()
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2, default=str)
            
            return True
            
        except Exception as e:
            print(f"Error exporting settings: {e}")
            return False
    
    def import_settings(self, import_path: str) -> Dict:
        """Import settings from specified path"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                imported_settings = json.load(f)
            
            # Validate imported settings
            validated_settings = self._validate_settings(imported_settings)
            
            return {
                'success': True,
                'settings': validated_settings,
                'message': 'Configuración importada exitosamente'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Error al importar configuración: {str(e)}"
            }
    
    def apply_imported_settings(self, imported_settings: Dict[str, Any]) -> bool:
        """Apply imported settings"""
        try:
            # Merge with current settings to preserve system metadata
            current_settings = self.load_settings()
            
            # Preserve system metadata
            system_metadata = current_settings.get('system', {})
            imported_settings['system'] = {
                **imported_settings.get('system', {}),
                **system_metadata,  # Current system metadata takes precedence
                'last_imported': self._get_timestamp()
            }
            
            return self.save_settings(imported_settings)
            
        except Exception as e:
            print(f"Error applying imported settings: {e}")
            return False
    
    def get_school_info(self) -> Dict[str, Any]:
        """Get school information from settings and database"""
        try:
            # Get from settings
            settings_school_info = self.get_setting('school_info', {})
            
            # Get from database
            db_school = self.school_service.get_school()
            
            # Merge and prioritize database
            school_info = {
                'name': db_school.name if db_school else settings_school_info.get('name', ''),
                'address': db_school.address if db_school else settings_school_info.get('address', ''),
                'phone': db_school.phone if db_school else settings_school_info.get('phone', ''),
                'email': db_school.email if db_school else settings_school_info.get('email', ''),
                'website': db_school.website if db_school else settings_school_info.get('website', '')
            }
            
            return school_info
            
        except Exception as e:
            print(f"Error getting school info: {e}")
            return {}
    
    def update_school_info(self, school_info: Dict[str, Any]) -> bool:
        """Update school information"""
        try:
            # Update in database
            school = self.school_service.get_school()
            if school:
                school.name = school_info.get('name', school.name)
                school.address = school_info.get('address', school.address)
                school.phone = school_info.get('phone', school.phone)
                school.email = school_info.get('email', school.email)
                school.website = school_info.get('website', school.website)
                self.school_service.update_school(school)
            
            # Update in settings as backup
            return self.update_setting('school_info', school_info)
            
        except Exception as e:
            print(f"Error updating school info: {e}")
            return False
    
    def get_academic_settings(self) -> Dict[str, Any]:
        """Get academic settings"""
        return self.get_setting('academic_settings', {})
    
    def update_academic_settings(self, academic_settings: Dict[str, Any]) -> bool:
        """Update academic settings"""
        return self.update_setting('academic_settings', academic_settings)
    
    def get_ui_preferences(self) -> Dict[str, Any]:
        """Get UI preferences"""
        return self.get_setting('ui_preferences', {})
    
    def update_ui_preferences(self, ui_preferences: Dict[str, Any]) -> bool:
        """Update UI preferences"""
        return self.update_setting('ui_preferences', ui_preferences)
    
    def get_path_settings(self) -> Dict[str, Any]:
        """Get path settings"""
        return self.get_setting('paths', {})
    
    def update_path_settings(self, path_settings: Dict[str, Any]) -> bool:
        """Update path settings"""
        return self.update_setting('paths', path_settings)
    
    def _merge_settings(self, defaults: Dict, current: Dict) -> Dict:
        """Merge current settings with defaults"""
        result = defaults.copy()
        
        for key, value in current.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_settings(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def _validate_settings(self, settings: Dict) -> Dict:
        """Validate and clean imported settings"""
        try:
            # Ensure required structure exists
            validated = self._merge_settings(self.default_settings, settings)
            
            # Validate specific values
            if 'academic_settings' in validated:
                academic = validated['academic_settings']
                
                # Validate enrollment fee
                if 'enrollment_fee' in academic:
                    try:
                        academic['enrollment_fee'] = float(academic['enrollment_fee'])
                        if academic['enrollment_fee'] < 0:
                            academic['enrollment_fee'] = self.default_settings['academic_settings']['enrollment_fee']
                    except (ValueError, TypeError):
                        academic['enrollment_fee'] = self.default_settings['academic_settings']['enrollment_fee']
                
                # Validate IDs
                for id_field in ['active_academic_year_id', 'default_grade_id']:
                    if id_field in academic:
                        try:
                            academic[id_field] = int(academic[id_field]) if academic[id_field] else None
                        except (ValueError, TypeError):
                            academic[id_field] = None
            
            if 'ui_preferences' in validated:
                ui = validated['ui_preferences']
                
                # Validate theme
                if 'theme' in ui:
                    if ui['theme'] not in ['light', 'dark', 'system']:
                        ui['theme'] = self.default_settings['ui_preferences']['theme']
                
                # Validate auto-save interval
                if 'auto_save_interval' in ui:
                    try:
                        ui['auto_save_interval'] = int(ui['auto_save_interval'])
                        if ui['auto_save_interval'] < 60:  # Minimum 1 minute
                            ui['auto_save_interval'] = 60
                    except (ValueError, TypeError):
                        ui['auto_save_interval'] = self.default_settings['ui_preferences']['auto_save_interval']
            
            return validated
            
        except Exception as e:
            print(f"Error validating settings: {e}")
            return self.default_settings.copy()
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_settings_summary(self) -> Dict[str, Any]:
        """Get a summary of current settings"""
        try:
            settings = self.load_settings()
            
            return {
                'school_name': settings['school_info'].get('name', 'No configurado'),
                'active_academic_year': settings['academic_settings'].get('active_academic_year_id', 'No configurado'),
                'theme': settings['ui_preferences'].get('theme', 'light'),
                'backup_path': settings['paths'].get('backup_path', 'No configurado'),
                'last_saved': settings['system'].get('last_saved', 'Nunca'),
                'version': settings['system'].get('version', 'Desconocido')
            }
            
        except Exception as e:
            print(f"Error getting settings summary: {e}")
            return {}

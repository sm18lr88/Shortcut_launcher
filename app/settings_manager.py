# app/settings_manager.py

import json
import os
import sys
import logging

def get_data_path():
    """Get the base path for data files"""
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, 'data')

def get_style_path():
    """Get the base path for style files"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, 'app', 'styles')

class SettingsManager:        
    def __init__(self):
        data_dir = get_data_path()
        os.makedirs(data_dir, exist_ok=True)
        self.file_path = os.path.join(data_dir, 'settings.json')
        self.settings = {}
        self.load_settings()

    def load_settings(self):
        try:
            if not os.path.exists(self.file_path):
                self.settings = {'theme': 'dark'}
                self.save_settings()
            else:
                with open(self.file_path, 'r') as f:
                    self.settings = json.load(f)
        except Exception as e:
            logging.error(f"Error loading settings: {e}")
            self.settings = {'theme': 'dark'}
            self.save_settings()

    def save_settings(self):
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            logging.error(f"Error saving settings: {e}")

    def get_style_sheet(self):
        try:
            theme = self.settings.get('theme', 'dark')
            style_file = os.path.join(get_style_path(), f'{theme}.qss')
            if not os.path.exists(style_file):
                logging.warning(f"Style file not found: {style_file}")
                return ""
            with open(style_file, 'r') as f:
                return f.read()
        except Exception as e:
            logging.error(f"Error loading style sheet: {e}")
            return ""

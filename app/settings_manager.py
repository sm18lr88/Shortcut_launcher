# app/settings_manager.py

import json
import os
import logging

class SettingsManager:        
    def __init__(self):
        self.file_path = os.path.join('data', 'settings.json')
        os.makedirs('data', exist_ok=True)
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
            style_file = os.path.join('app', 'styles', f'{theme}.qss')
            if not os.path.exists(style_file):
                logging.warning(f"Style file not found: {style_file}")
                return ""
            with open(style_file, 'r') as f:
                return f.read()
        except Exception as e:
            logging.error(f"Error loading style sheet: {e}")
            return ""

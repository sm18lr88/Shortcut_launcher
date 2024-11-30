# app/shortcut_manager.py

import json
import os
import logging

class ShortcutManager:
    def __init__(self):
        self.file_path = os.path.join('data', 'shortcuts.json')
        os.makedirs('data', exist_ok=True)
        self.shortcuts = {}
        self.load_shortcuts()

    def load_shortcuts(self):
        try:
            if not os.path.exists(self.file_path):
                self.shortcuts = {}
                self.save_shortcuts()
            else:
                with open(self.file_path, 'r') as f:
                    self.shortcuts = json.load(f)
                if not isinstance(self.shortcuts, dict):
                    raise ValueError("Invalid shortcuts file format")
        except Exception as e:
            logging.error(f"Error loading shortcuts: {e}")
            self.shortcuts = {}
            self.save_shortcuts()

    def save_shortcuts(self):
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self.shortcuts, f, indent=4)
        except Exception as e:
            logging.error(f"Error saving shortcuts: {e}")

    def get_command(self, category, shortcut_name):
        """Get the command for a specific shortcut in a category."""
        try:
            for shortcut in self.shortcuts.get(category, []):
                if shortcut['name'] == shortcut_name:
                    return shortcut['command']
            return None
        except Exception as e:
            logging.error(f"Error getting command: {e}")
            return None

    def get_categories(self):
        return list(self.shortcuts.keys())

    def add_category(self, category_name):
        if category_name not in self.shortcuts:
            self.shortcuts[category_name] = []
            self.save_shortcuts()

    def rename_category(self, old_name, new_name):
        if old_name in self.shortcuts:
            self.shortcuts[new_name] = self.shortcuts.pop(old_name)
            self.save_shortcuts()

    def delete_category(self, category_name):
        if category_name in self.shortcuts:
            del self.shortcuts[category_name]
            self.save_shortcuts()

    def get_shortcuts(self, category):
        return self.shortcuts.get(category, [])

    def add_shortcut(self, category, name, command):
        if category not in self.shortcuts:
            self.shortcuts[category] = []
        self.shortcuts[category].append({'name': name, 'command': command})
        self.save_shortcuts()

    def get_shortcut(self, category, name):
        for shortcut in self.shortcuts.get(category, []):
            if shortcut['name'] == name:
                return shortcut
        return None

    def edit_shortcut(self, category, old_name, new_name, new_command):
        for shortcut in self.shortcuts.get(category, []):
            if shortcut['name'] == old_name:
                shortcut['name'] = new_name
                shortcut['command'] = new_command
                self.save_shortcuts()
                break

    def delete_shortcut(self, category, name):
        shortcuts = self.shortcuts.get(category, [])
        for i, shortcut in enumerate(shortcuts):
            if shortcut['name'] == name:
                del shortcuts[i]
                self.save_shortcuts()
                break

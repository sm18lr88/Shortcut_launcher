# app/main_window.py

import sys
import logging
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
    QPushButton, QMessageBox, QHBoxLayout, QInputDialog, QLineEdit, QMenu
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from .shortcut_manager import ShortcutManager
from .command_executor import CommandExecutor
from .settings_manager import SettingsManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shortcut Launcher")
        self.setGeometry(100, 100, 800, 600)
        self.settings = SettingsManager()
        self.apply_styles()
        self.shortcut_manager = ShortcutManager()
        self.init_ui()

    def apply_styles(self):
        style_sheet = self.settings.get_style_sheet()
        self.setStyleSheet(style_sheet)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.itemDoubleClicked.connect(self.execute_shortcut)
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.open_context_menu)
        layout.addWidget(self.tree)

        self.load_shortcuts()

        # Buttons
        button_layout = QHBoxLayout()
        add_category_btn = QPushButton("Add Category")
        add_category_btn.clicked.connect(self.add_category)
        add_shortcut_btn = QPushButton("Add Shortcut")
        add_shortcut_btn.clicked.connect(self.add_shortcut)

        button_layout.addWidget(add_category_btn)
        button_layout.addWidget(add_shortcut_btn)
        layout.addLayout(button_layout)

    def load_shortcuts(self):
        self.tree.clear()
        try:
            categories = self.shortcut_manager.get_categories()
            for category_name in categories:
                category_item = QTreeWidgetItem([category_name])
                category_item.setExpanded(True)
                self.tree.addTopLevelItem(category_item)
                shortcuts = self.shortcut_manager.get_shortcuts(category_name)
                for shortcut in shortcuts:
                    shortcut_item = QTreeWidgetItem([shortcut['name']])
                    category_item.addChild(shortcut_item)
        except Exception as e:
            logging.error("Failed to load shortcuts: %s", e)
            QMessageBox.critical(self, "Error", "Failed to load shortcuts.")

    def execute_shortcut(self, item, column):
        try:
            parent = item.parent()
            if parent:
                category = parent.text(0)
                shortcut_name = item.text(0)
                command = self.shortcut_manager.get_command(category, shortcut_name)
                if command:
                    executor = CommandExecutor()
                    executor.run_command(command)
                else:
                    QMessageBox.warning(self, "Warning", "Command not found.")
        except Exception as e:
            logging.error(f"Error executing shortcut: {e}")
            QMessageBox.critical(self, "Error", f"Failed to execute shortcut: {str(e)}")

    def add_category(self):
        text, ok = QInputDialog.getText(self, "Add Category", "Category Name:")
        if ok and text:
            self.shortcut_manager.add_category(text)
            self.load_shortcuts()

    def add_shortcut(self):
        categories = self.shortcut_manager.get_categories()
        if not categories:
            QMessageBox.warning(self, "Warning", "Please add a category first.")
            return
        category, ok = QInputDialog.getItem(self, "Select Category", "Category:", categories, 0, False)
        if ok and category:
            name, ok = QInputDialog.getText(self, "Add Shortcut", "Shortcut Name:")
            if ok and name:
                command, ok = QInputDialog.getText(self, "Add Shortcut", "Command:")
                if ok and command:
                    self.shortcut_manager.add_shortcut(category, name, command)
                    self.load_shortcuts()

    def open_context_menu(self, position):
        item = self.tree.itemAt(position)
        if item:
            menu = QMenu()
            if item.parent() is None:
                # Category level
                add_shortcut_action = QAction("Add Shortcut", self)
                edit_category_action = QAction("Edit Category", self)
                delete_category_action = QAction("Delete Category", self)

                add_shortcut_action.triggered.connect(lambda: self.add_shortcut_to_category(item))
                edit_category_action.triggered.connect(lambda: self.edit_category(item))
                delete_category_action.triggered.connect(lambda: self.delete_category(item))

                menu.addAction(add_shortcut_action)
                menu.addAction(edit_category_action)
                menu.addAction(delete_category_action)
            else:
                # Shortcut level
                edit_shortcut_action = QAction("Edit Shortcut", self)
                delete_shortcut_action = QAction("Delete Shortcut", self)

                edit_shortcut_action.triggered.connect(lambda: self.edit_shortcut(item))
                delete_shortcut_action.triggered.connect(lambda: self.delete_shortcut(item))

                menu.addAction(edit_shortcut_action)
                menu.addAction(delete_shortcut_action)
            menu.exec(self.tree.viewport().mapToGlobal(position))

    def add_shortcut_to_category(self, category_item):
        category = category_item.text(0)
        name, ok = QInputDialog.getText(self, "Add Shortcut", "Shortcut Name:")
        if ok and name:
            command, ok = QInputDialog.getText(self, "Add Shortcut", "Command:")
            if ok and command:
                self.shortcut_manager.add_shortcut(category, name, command)
                self.load_shortcuts()

    def edit_category(self, category_item):
        old_name = category_item.text(0)
        new_name, ok = QInputDialog.getText(self, "Edit Category", "New Category Name:", QLineEdit.EchoMode.Normal, old_name)
        if ok and new_name:
            self.shortcut_manager.rename_category(old_name, new_name)
            self.load_shortcuts()

    def delete_category(self, category_item):
        category = category_item.text(0)
        reply = QMessageBox.question(self, "Delete Category",
                                   f"Are you sure you want to delete the category '{category}'?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                   QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.shortcut_manager.delete_category(category)
            self.load_shortcuts()

    def edit_shortcut(self, shortcut_item):
        parent_item = shortcut_item.parent()
        category = parent_item.text(0)
        old_name = shortcut_item.text(0)
        shortcut = self.shortcut_manager.get_shortcut(category, old_name)

        new_name, ok = QInputDialog.getText(self, "Edit Shortcut", "New Shortcut Name:", QLineEdit.EchoMode.Normal, old_name)
        if ok and new_name:
            new_command, ok = QInputDialog.getText(self, "Edit Shortcut", "New Command:", QLineEdit.EchoMode.Normal, shortcut['command'])
            if ok and new_command:
                self.shortcut_manager.edit_shortcut(category, old_name, new_name, new_command)
                self.load_shortcuts()

    def delete_shortcut(self, shortcut_item):
        parent_item = shortcut_item.parent()
        category = parent_item.text(0)
        shortcut_name = shortcut_item.text(0)
        reply = QMessageBox.question(self, "Delete Shortcut",
                                   f"Are you sure you want to delete the shortcut '{shortcut_name}'?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                   QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.shortcut_manager.delete_shortcut(category, shortcut_name)
            self.load_shortcuts()

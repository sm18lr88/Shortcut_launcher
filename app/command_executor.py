# app/command_executor.py

import subprocess
import threading
import logging
import sys
import os

class CommandExecutor:
    def __init__(self):
        pass

    def create_batch_file(self, command):
        # Create a unique batch file name based on the command hash
        command_hash = abs(hash(command))
        batch_file_name = f'run_command_{command_hash}.bat'
        batch_file_path = os.path.join('temp_scripts', batch_file_name)
        os.makedirs('temp_scripts', exist_ok=True)
        with open(batch_file_path, 'w') as f:
            f.write(f'@echo off\n')
            f.write(f'{command}\n')
        return batch_file_path

    def run_command(self, command):
        def target():
            try:
                if sys.platform.startswith('win'):
                    batch_file = self.create_batch_file(command)
                    # Use 'start' to open a new cmd window and run the batch file
                    cmd = f'start "" "{batch_file}"'
                    subprocess.Popen(cmd, shell=True)
                else:
                    # For Unix-like systems
                    # Create a shell script and execute it in a new terminal
                    shell_script = self.create_shell_script(command)
                    cmd = f'x-terminal-emulator -e bash "{shell_script}"'
                    subprocess.Popen(cmd, shell=True)
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                self.show_error(e)

        thread = threading.Thread(target=target)
        thread.start()

    def create_shell_script(self, command):
        script_hash = abs(hash(command))
        script_file_name = f'run_command_{script_hash}.sh'
        script_file_path = os.path.join('temp_scripts', script_file_name)
        os.makedirs('temp_scripts', exist_ok=True)
        with open(script_file_path, 'w') as f:
            f.write(f'#!/bin/bash\n')
            f.write(f'{command}\n')
            f.write('read -p "Press enter to exit..."')  # Keeps the terminal open
        os.chmod(script_file_path, 0o755)  # Make it executable
        return script_file_path

    def show_error(self, error):
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.critical(None, "Command Execution Error", str(error))
        
def cleanup_temp_files(self):
        try:
            if os.path.exists('temp_scripts'):
                for file in os.listdir('temp_scripts'):
                    try:
                        os.remove(os.path.join('temp_scripts', file))
                    except:
                        pass
                os.rmdir('temp_scripts')
        except Exception as e:
            logging.error(f"Error cleaning up temp files: {e}")



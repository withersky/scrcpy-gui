#!/usr/bin/env python3
"""
Scrcpy GUI - A simple PySide6 interface for ADB WiFi connections and scrcpy.
"""

import sys
import os
import subprocess
import re
import locale
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox,
    QGroupBox, QMessageBox, QFrame, QStatusBar,
    QToolBar, QSystemTrayIcon, QMenu, QDialog, QFormLayout,
    QTabWidget, QTextBrowser
)
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtGui import QIcon, QFont, QPalette, QColor, QAction


# Translations dictionary
TRANSLATIONS = {
    'en': {
        'title': 'Scrcpy GUI - ADB WiFi Manager',
        'connection_group': 'ADB WiFi Connection',
        'device_label': 'Device IP:Port:',
        'device_placeholder': 'e.g., 192.168.0.40:5555',
        'connect_btn': 'Connect',
        'disconnect_btn': 'Disconnect',
        'pair_btn': 'Pair (Android 11+)',
        'refresh_btn': 'Refresh',
        'devices_group': 'Connected Devices',
        'no_device': 'No device selected',
        'selected_device': 'Selected: ',
        'scrcpy_group': 'Scrcpy Control',
        'bitrate_label': 'Bitrate (Mbps):',
        'max_size_label': 'Max Size:',
        'no_limit': 'No limit',
        'start_scrcpy': 'Start Scrcpy',
        'stop_scrcpy': 'Stop Scrcpy',
        'log_group': 'Log',
        'clear_log': 'Clear Log',
        'log_cleared': 'Log cleared',
        'ready': 'Ready',
        'adb_installed': 'ADB is installed',
        'adb_not_found': 'ADB not found! Please install Android SDK Platform Tools.',
        'adb_not_found_title': 'ADB Not Found',
        'scrcpy_installed': 'Scrcpy is installed',
        'scrcpy_installed_local': 'Scrcpy is installed (local: ',
        'scrcpy_installed_system': 'Scrcpy is installed (system)',
        'scrcpy_not_found': 'Scrcpy not found! Please install scrcpy.',
        'scrcpy_not_found_title': 'Scrcpy Not Found',
        'devices_found': 'Found ',
        'devices_found_suffix': ' connected device(s)',
        'no_devices': 'No connected devices found',
        'error_refresh': 'Error refreshing devices: ',
        'input_error': 'Input Error',
        'enter_ip_port': 'Please enter a device IP:Port',
        'enter_ip_port_format': 'Please enter IP:Port format (e.g., 192.168.0.40:5555)',
        'connecting': 'Connecting to ',
        'disconnecting': 'Disconnecting from ',
        'no_device_title': 'No Device',
        'select_device': 'Please select a device first',
        'starting_scrcpy': 'Starting scrcpy for ',
        'command': 'Command: ',
        'scrcpy_started': 'Scrcpy started successfully',
        'scrcpy_not_found_error': 'Scrcpy not found! Please install scrcpy.',
        'error_starting': 'Error starting scrcpy: ',
        'scrcpy_stopped': 'Scrcpy stopped',
        'scrcpy_ended': 'Scrcpy process ended',
        'pairing_title': 'ADB Wireless Pairing',
        'pairing_instructions': '''
        <h3>ADB Wireless Pairing (Android 11+)</h3>
        <p><b>Step 1:</b> Enable Developer Options on your phone</p>
        <ul>
            <li>Go to Settings > About Phone</li>
            <li>Tap "Build Number" 7 times</li>
        </ul>
        
        <p><b>Step 2:</b> Enable Wireless Debugging</p>
        <ul>
            <li>Go to Settings > Developer Options</li>
            <li>Enable "Wireless Debugging"</li>
            <li>Tap on "Wireless Debugging" to see pairing info</li>
        </ul>
        
        <p><b>Step 3:</b> Get Pairing Code</p>
        <ul>
            <li>Tap "Pair device with pairing code"</li>
            <li>Note the pairing code shown on your phone</li>
            <li>Note the IP address and port (e.g., 192.168.1.100:37659)</li>
        </ul>
        
        <p><b>Step 4:</b> Enter the information below to pair</p>
        ''',
        'pairing_info_group': 'Pairing Information',
        'ip_address': 'IP Address:',
        'ip_placeholder': 'e.g., 192.168.1.100',
        'pairing_port': 'Pairing Port:',
        'pairing_port_placeholder': 'e.g., 37659',
        'pairing_code': 'Pairing Code:',
        'pairing_code_placeholder': '6-digit code',
        'connect_port': 'Connect Port:',
        'connect_port_placeholder': 'e.g., 33559 (shown after pairing)',
        'pair_device': 'Pair Device',
        'connect_after_pair': 'Connect After Pairing',
        'fill_all_fields': 'Please fill in IP address, pairing port, and pairing code.',
        'pairing': 'Pairing...',
        'paired_success': 'Device paired successfully!\n\nNow enter the connect port (shown on your phone after pairing) and click \'Connect After Pairing\'.',
        'paired_success_label': 'Paired successfully! Now connect using the connect port.',
        'pairing_failed': 'Pairing Failed',
        'failed_to_pair': 'Failed to pair:\n',
        'fill_ip_connect': 'Please fill in IP address and connect port.',
        'connecting_after_pair': 'Connecting...',
        'connected_success': 'Connected successfully!',
        'connected_to': 'Connected to ',
        'connection_failed': 'Connection Failed',
        'failed_to_connect': 'Failed to connect:\n',
        'error': 'Error',
        'success': 'Success',
        'unknown_error': 'Unknown error',
    },
    'ru': {
        'title': 'Scrcpy GUI - ADB WiFi Менеджер',
        'connection_group': 'ADB WiFi Подключение',
        'device_label': 'IP:Порт устройства:',
        'device_placeholder': 'например, 192.168.0.40:5555',
        'connect_btn': 'Подключить',
        'disconnect_btn': 'Отключить',
        'pair_btn': 'Сопряжение (Android 11+)',
        'refresh_btn': 'Обновить',
        'devices_group': 'Подключенные устройства',
        'no_device': 'Устройство не выбрано',
        'selected_device': 'Выбрано: ',
        'scrcpy_group': 'Управление Scrcpy',
        'bitrate_label': 'Битрейт (Мбит/с):',
        'max_size_label': 'Макс. размер:',
        'no_limit': 'Без ограничений',
        'start_scrcpy': 'Запустить Scrcpy',
        'stop_scrcpy': 'Остановить Scrcpy',
        'log_group': 'Лог',
        'clear_log': 'Очистить лог',
        'log_cleared': 'Лог очищен',
        'ready': 'Готово',
        'adb_installed': 'ADB установлен',
        'adb_not_found': 'ADB не найден! Пожалуйста, установите Android SDK Platform Tools.',
        'adb_not_found_title': 'ADB не найден',
        'scrcpy_installed': 'Scrcpy установлен',
        'scrcpy_installed_local': 'Scrcpy установлен (локально: ',
        'scrcpy_installed_system': 'Scrcpy установлен (системный)',
        'scrcpy_not_found': 'Scrcpy не найден! Пожалуйста, установите scrcpy.',
        'scrcpy_not_found_title': 'Scrcpy не найден',
        'devices_found': 'Найдено ',
        'devices_found_suffix': ' подключенное(ых) устройство(а)',
        'no_devices': 'Подключенные устройства не найдены',
        'error_refresh': 'Ошибка обновления устройств: ',
        'input_error': 'Ошибка ввода',
        'enter_ip_port': 'Пожалуйста, введите IP:Порт устройства',
        'enter_ip_port_format': 'Пожалуйста, введите формат IP:Порт (например, 192.168.0.40:5555)',
        'connecting': 'Подключение к ',
        'disconnecting': 'Отключение от ',
        'no_device_title': 'Нет устройства',
        'select_device': 'Пожалуйста, сначала выберите устройство',
        'starting_scrcpy': 'Запуск scrcpy для ',
        'command': 'Команда: ',
        'scrcpy_started': 'Scrcpy успешно запущен',
        'scrcpy_not_found_error': 'Scrcpy не найден! Пожалуйста, установите scrcpy.',
        'error_starting': 'Ошибка запуска scrcpy: ',
        'scrcpy_stopped': 'Scrcpy остановлен',
        'scrcpy_ended': 'Процесс Scrcpy завершен',
        'pairing_title': 'Беспроводное сопряжение ADB',
        'pairing_instructions': '''
        <h3>Беспроводное сопряжение ADB (Android 11+)</h3>
        <p><b>Шаг 1:</b> Включите опции разработчика на телефоне</p>
        <ul>
            <li>Перейдите в Настройки > О телефоне</li>
            <li>Нажмите "Номер сборки" 7 раз</li>
        </ul>
        
        <p><b>Шаг 2:</b> Включите беспроводную отладку</p>
        <ul>
            <li>Перейдите в Настройки > Для разработчиков</li>
            <li>Включите "Беспроводная отладка"</li>
            <li>Нажмите на "Беспроводная отладка" чтобы увидеть информацию о сопряжении</li>
        </ul>
        
        <p><b>Шаг 3:</b> Получите код сопряжения</p>
        <ul>
            <li>Нажмите "Сопряжение устройства по коду"</li>
            <li>Запишите код сопряжения, показанный на телефоне</li>
            <li>Запишите IP-адрес и порт (например, 192.168.1.100:37659)</li>
        </ul>
        
        <p><b>Шаг 4:</b> Введите информацию ниже для сопряжения</p>
        ''',
        'pairing_info_group': 'Информация о сопряжении',
        'ip_address': 'IP-адрес:',
        'ip_placeholder': 'например, 192.168.1.100',
        'pairing_port': 'Порт сопряжения:',
        'pairing_port_placeholder': 'например, 37659',
        'pairing_code': 'Код сопряжения:',
        'pairing_code_placeholder': '6-значный код',
        'connect_port': 'Порт подключения:',
        'connect_port_placeholder': 'например, 33559 (показывается после сопряжения)',
        'pair_device': 'Сопряжение устройства',
        'connect_after_pair': 'Подключить после сопряжения',
        'fill_all_fields': 'Пожалуйста, заполните IP-адрес, порт сопряжения и код сопряжения.',
        'pairing': 'Сопряжение...',
        'paired_success': 'Устройство успешно сопряжено!\n\nТеперь введите порт подключения (показывается на телефоне после сопряжения) и нажмите \'Подключить после сопряжения\'.',
        'paired_success_label': 'Сопряжено успешно! Теперь подключитесь используя порт подключения.',
        'pairing_failed': 'Сопряжение не удалось',
        'failed_to_pair': 'Не удалось сопрячь:\n',
        'fill_ip_connect': 'Пожалуйста, заполните IP-адрес и порт подключения.',
        'connecting_after_pair': 'Подключение...',
        'connected_success': 'Успешно подключено!',
        'connected_to': 'Подключено к ',
        'connection_failed': 'Подключение не удалось',
        'failed_to_connect': 'Не удалось подключиться:\n',
        'error': 'Ошибка',
        'success': 'Успех',
        'unknown_error': 'Неизвестная ошибка',
    }
}


# Global language setting
CURRENT_LANGUAGE = None


def get_language():
    """Get current language setting."""
    global CURRENT_LANGUAGE
    if CURRENT_LANGUAGE is not None:
        return CURRENT_LANGUAGE
    try:
        # Try to get system locale using setlocale
        current_locale = locale.setlocale(locale.LC_ALL, '')
        if current_locale and (current_locale.startswith('ru') or current_locale.startswith('uk') or current_locale.startswith('be')):
            return 'ru'
        return 'en'
    except:
        return 'en'


def set_language(lang):
    """Set the current language."""
    global CURRENT_LANGUAGE
    CURRENT_LANGUAGE = lang


def tr(key):
    """Get translation for a key."""
    lang = get_language()
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)


class ADBWorker(QThread):
    """Worker thread for ADB operations to prevent UI freezing."""
    finished = Signal(str)
    output = Signal(str)
    error = Signal(str)

    def __init__(self, command, args=None):
        super().__init__()
        self.command = command
        self.args = args or []

    def run(self):
        try:
            cmd = [self.command] + self.args
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate()
            if stdout:
                self.output.emit(stdout)
            if stderr:
                self.error.emit(stderr)
            self.finished.emit(f"Command completed with return code: {process.returncode}")
        except Exception as e:
            self.error.emit(f"Error: {str(e)}")


class ADBPairDialog(QDialog):
    """Dialog for ADB wireless pairing (Android 11+)."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setWindowTitle(tr('pairing_title'))
        self.setGeometry(100, 100, 600, 550)
        self.setup_ui()
    
    def get_adb_path(self):
        """Get the path to adb binary (local or system)."""
        if self.parent_window and hasattr(self.parent_window, 'get_adb_path'):
            return self.parent_window.get_adb_path()
        # Fallback: check local directory
        local_adb = Path(__file__).parent.resolve() / "adb"
        if local_adb.exists() and os.access(local_adb, os.X_OK):
            return str(local_adb)
        return "adb"
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QTextBrowser()
        instructions.setHtml(tr('pairing_instructions'))
        instructions.setMaximumHeight(220)
        layout.addWidget(instructions)
        
        # Pairing form
        form_group = QGroupBox(tr('pairing_info_group'))
        form_layout = QFormLayout(form_group)
        
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText(tr('ip_placeholder'))
        form_layout.addRow(tr('ip_address'), self.ip_input)
        
        self.pair_port_input = QLineEdit()
        self.pair_port_input.setPlaceholderText(tr('pairing_port_placeholder'))
        form_layout.addRow(tr('pairing_port'), self.pair_port_input)
        
        self.pair_code_input = QLineEdit()
        self.pair_code_input.setPlaceholderText(tr('pairing_code_placeholder'))
        self.pair_code_input.setMaxLength(6)
        form_layout.addRow(tr('pairing_code'), self.pair_code_input)
        
        self.connect_port_input = QLineEdit()
        self.connect_port_input.setPlaceholderText(tr('connect_port_placeholder'))
        form_layout.addRow(tr('connect_port'), self.connect_port_input)
        
        layout.addWidget(form_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.pair_btn = QPushButton(tr('pair_device'))
        self.pair_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.pair_btn.clicked.connect(self.pair_device)
        btn_layout.addWidget(self.pair_btn)
        
        self.connect_btn = QPushButton(tr('connect_after_pair'))
        self.connect_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.connect_btn.clicked.connect(self.connect_after_pair)
        btn_layout.addWidget(self.connect_btn)
        
        layout.addLayout(btn_layout)
        
        # Status
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(self.status_label)
    
    def pair_device(self):
        """Pair with the device."""
        ip = self.ip_input.text().strip()
        pair_port = self.pair_port_input.text().strip()
        pair_code = self.pair_code_input.text().strip()
        
        if not ip or not pair_port or not pair_code:
            QMessageBox.warning(self, tr('input_error'), tr('fill_all_fields'))
            return
        
        self.status_label.setText(tr('pairing'))
        self.status_label.setStyleSheet("color: #2196F3; font-weight: bold;")
        
        # Run adb pair command
        adb_path = self.get_adb_path()
        try:
            result = subprocess.run(
                [adb_path, "pair", f"{ip}:{pair_port}"],
                input=pair_code,
                capture_output=True,
                text=True
            )
            
            if "Successfully paired" in result.stdout or "Successfully paired" in result.stderr:
                self.status_label.setText(tr('paired_success_label'))
                self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
                QMessageBox.information(self, tr('success'), tr('paired_success'))
            else:
                error_msg = result.stderr or result.stdout or tr('unknown_error')
                self.status_label.setText(f"❌ {tr('failed_to_pair')} {error_msg}")
                self.status_label.setStyleSheet("color: #f44336; font-weight: bold;")
                QMessageBox.critical(self, tr('pairing_failed'), f"{tr('failed_to_pair')}{error_msg}")
        except Exception as e:
            self.status_label.setText(f"❌ {tr('error')}: {str(e)}")
            self.status_label.setStyleSheet("color: #f44336; font-weight: bold;")
            QMessageBox.critical(self, tr('error'), f"{tr('error')}: {str(e)}")
    
    def connect_after_pair(self):
        """Connect to the device after pairing."""
        ip = self.ip_input.text().strip()
        connect_port = self.connect_port_input.text().strip()
        
        if not ip or not connect_port:
            QMessageBox.warning(self, tr('input_error'), tr('fill_ip_connect'))
            return
        
        self.status_label.setText(tr('connecting_after_pair'))
        self.status_label.setStyleSheet("color: #2196F3; font-weight: bold;")
        
        # Run adb connect command
        adb_path = self.get_adb_path()
        try:
            result = subprocess.run(
                [adb_path, "connect", f"{ip}:{connect_port}"],
                capture_output=True,
                text=True
            )
            
            if "connected" in result.stdout.lower():
                self.status_label.setText(tr('connected_success'))
                self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
                QMessageBox.information(self, tr('success'), f"{tr('connected_to')}{ip}:{connect_port}!")
                self.accept()
            else:
                error_msg = result.stderr or result.stdout or tr('unknown_error')
                self.status_label.setText(f"❌ {tr('failed_to_connect')} {error_msg}")
                self.status_label.setStyleSheet("color: #f44336; font-weight: bold;")
                QMessageBox.critical(self, tr('connection_failed'), f"{tr('failed_to_connect')}{error_msg}")
        except Exception as e:
            self.status_label.setText(f"❌ {tr('error')}: {str(e)}")
            self.status_label.setStyleSheet("color: #f44336; font-weight: bold;")
            QMessageBox.critical(self, tr('error'), f"{tr('error')}: {str(e)}")


class ScrcpyGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_device = None
        self.workers = []
        self.pair_dialog = None
        self.scrcpy_process = None
        # Get the directory where the application is located
        self.app_dir = Path(__file__).parent.resolve()
        # Store translation keys for UI elements
        self.ui_keys = {}
        self.init_ui()
        self.refresh_devices()

    def init_ui(self):
        self.setWindowTitle(tr('title'))
        self.setGeometry(100, 100, 800, 650)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Title
        self.title_label = QLabel(tr('title'))
        self.title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui_keys['title_label'] = 'title'
        main_layout.addWidget(self.title_label)

        # Connection section
        self.connection_group = QGroupBox(tr('connection_group'))
        self.ui_keys['connection_group'] = 'connection_group'
        connection_layout = QVBoxLayout(self.connection_group)

        # Device input row
        input_layout = QHBoxLayout()
        self.device_label = QLabel(tr('device_label'))
        self.ui_keys['device_label'] = 'device_label'
        input_layout.addWidget(self.device_label)
        self.device_input = QLineEdit()
        self.device_input.setPlaceholderText(tr('device_placeholder'))
        self.device_input.setFont(QFont("Consolas", 11))
        input_layout.addWidget(self.device_input, 1)
        connection_layout.addLayout(input_layout)

        # Buttons row
        buttons_layout = QHBoxLayout()
        self.connect_btn = QPushButton(tr('connect_btn'))
        self.ui_keys['connect_btn'] = 'connect_btn'
        self.connect_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.connect_btn.clicked.connect(self.connect_device)
        buttons_layout.addWidget(self.connect_btn)

        self.disconnect_btn = QPushButton(tr('disconnect_btn'))
        self.ui_keys['disconnect_btn'] = 'disconnect_btn'
        self.disconnect_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.disconnect_btn.clicked.connect(self.disconnect_device)
        buttons_layout.addWidget(self.disconnect_btn)

        self.pair_btn = QPushButton(tr('pair_btn'))
        self.ui_keys['pair_btn'] = 'pair_btn'
        self.pair_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        self.pair_btn.clicked.connect(self.show_pair_dialog)
        buttons_layout.addWidget(self.pair_btn)

        self.refresh_btn = QPushButton(tr('refresh_btn'))
        self.ui_keys['refresh_btn'] = 'refresh_btn'
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        self.refresh_btn.clicked.connect(self.refresh_devices)
        buttons_layout.addWidget(self.refresh_btn)
        connection_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.connection_group)

        # Devices list section
        self.devices_group = QGroupBox(tr('devices_group'))
        self.ui_keys['devices_group'] = 'devices_group'
        devices_layout = QVBoxLayout(self.devices_group)

        devices_combo_layout = QHBoxLayout()
        self.lang_label = QLabel("Language:")
        devices_combo_layout.addWidget(self.lang_label)
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("English", "en")
        self.lang_combo.addItem("Русский", "ru")
        self.lang_combo.setCurrentIndex(0 if get_language() == 'en' else 1)
        self.lang_combo.currentTextChanged.connect(self.on_language_changed)
        devices_combo_layout.addWidget(self.lang_combo)
        devices_combo_layout.addStretch()
        devices_layout.addLayout(devices_combo_layout)

        self.devices_combo = QComboBox()
        self.devices_combo.setFont(QFont("Consolas", 10))
        self.devices_combo.currentTextChanged.connect(self.on_device_selected)
        devices_layout.addWidget(self.devices_combo)

        # Selected device info
        self.device_info_label = QLabel(tr('no_device'))
        self.device_info_label.setStyleSheet("color: #666; font-style: italic;")
        devices_layout.addWidget(self.device_info_label)
        main_layout.addWidget(self.devices_group)

        # Scrcpy section
        self.scrcpy_group = QGroupBox(tr('scrcpy_group'))
        self.ui_keys['scrcpy_group'] = 'scrcpy_group'
        scrcpy_layout = QVBoxLayout(self.scrcpy_group)

        # Scrcpy options
        options_layout = QHBoxLayout()
        self.bitrate_label = QLabel(tr('bitrate_label'))
        self.ui_keys['bitrate_label'] = 'bitrate_label'
        options_layout.addWidget(self.bitrate_label)
        self.bitrate_input = QLineEdit("8")
        self.bitrate_input.setFixedWidth(60)
        options_layout.addWidget(self.bitrate_input)

        self.max_size_label = QLabel(tr('max_size_label'))
        self.ui_keys['max_size_label'] = 'max_size_label'
        options_layout.addWidget(self.max_size_label)
        self.max_size_combo = QComboBox()
        self.max_size_combo.addItems([tr('no_limit'), "1024", "1280", "1920"])
        options_layout.addWidget(self.max_size_combo)

        options_layout.addStretch()
        scrcpy_layout.addLayout(options_layout)

        # Scrcpy buttons
        scrcpy_btn_layout = QHBoxLayout()
        self.start_scrcpy_btn = QPushButton(tr('start_scrcpy'))
        self.ui_keys['start_scrcpy_btn'] = 'start_scrcpy'
        self.start_scrcpy_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.start_scrcpy_btn.clicked.connect(self.start_scrcpy)
        scrcpy_btn_layout.addWidget(self.start_scrcpy_btn)

        self.stop_scrcpy_btn = QPushButton(tr('stop_scrcpy'))
        self.ui_keys['stop_scrcpy_btn'] = 'stop_scrcpy'
        self.stop_scrcpy_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF5722;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #E64A19;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.stop_scrcpy_btn.clicked.connect(self.stop_scrcpy)
        self.stop_scrcpy_btn.setEnabled(False)
        scrcpy_btn_layout.addWidget(self.stop_scrcpy_btn)
        scrcpy_layout.addLayout(scrcpy_btn_layout)
        main_layout.addWidget(self.scrcpy_group)

        # Log section
        self.log_group = QGroupBox(tr('log_group'))
        self.ui_keys['log_group'] = 'log_group'
        log_layout = QVBoxLayout(self.log_group)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 9))
        self.log_text.setMaximumHeight(120)
        log_layout.addWidget(self.log_text)

        # Clear log button
        self.clear_log_btn = QPushButton(tr('clear_log'))
        self.ui_keys['clear_log_btn'] = 'clear_log'
        self.clear_log_btn.setFixedWidth(100)
        self.clear_log_btn.clicked.connect(self.clear_log)
        log_layout.addWidget(self.clear_log_btn, 0, Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(self.log_group)

        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage(tr('ready'))

        # Check for scrcpy and adb on startup
        self.check_dependencies()

    def log(self, message, level="INFO"):
        """Add a message to the log."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}"
        self.log_text.append(log_message)
        self.statusBar.showMessage(message)

    def clear_log(self):
        """Clear the log."""
        self.log_text.clear()
        self.log(tr('log_cleared'))

    def get_adb_path(self):
        """Get the path to adb binary (local or system)."""
        # Check for local adb in the application directory
        local_adb = self.app_dir / "adb"
        if local_adb.exists() and os.access(local_adb, os.X_OK):
            return str(local_adb)
        
        # Check for adb.exe on Windows
        local_adb_exe = self.app_dir / "adb.exe"
        if local_adb_exe.exists():
            return str(local_adb_exe)
        
        # Fall back to system adb
        return "adb"

    def get_scrcpy_path(self):
        """Get the path to scrcpy binary (local or system)."""
        # Check for local scrcpy in the application directory
        local_scrcpy = self.app_dir / "scrcpy"
        if local_scrcpy.exists() and os.access(local_scrcpy, os.X_OK):
            return str(local_scrcpy)
        
        # Check for scrcpy.exe on Windows
        local_scrcpy_exe = self.app_dir / "scrcpy.exe"
        if local_scrcpy_exe.exists():
            return str(local_scrcpy_exe)
        
        # Fall back to system scrcpy
        return "scrcpy"

    def check_dependencies(self):
        """Check if adb and scrcpy are installed."""
        adb_path = self.get_adb_path()
        try:
            result = subprocess.run([adb_path, "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                if adb_path != "adb":
                    self.log(f"{tr('adb_installed')} ({adb_path})")
                else:
                    self.log(tr('adb_installed'))
            else:
                self.log(tr('adb_not_found'), "ERROR")
                QMessageBox.warning(self, tr('adb_not_found_title'), 
                    tr('adb_not_found'))
        except FileNotFoundError:
            self.log(tr('adb_not_found'), "ERROR")
            QMessageBox.warning(self, tr('adb_not_found_title'),
                tr('adb_not_found'))

        # Check for local or system scrcpy
        scrcpy_path = self.get_scrcpy_path()
        try:
            result = subprocess.run([scrcpy_path, "--version"], capture_output=True, text=True)
            if result.returncode == 0 or "scrcpy" in result.stderr.lower():
                if scrcpy_path != "scrcpy":
                    self.log(f"{tr('scrcpy_installed_local')}{scrcpy_path}")
                else:
                    self.log(tr('scrcpy_installed_system'))
            else:
                self.log(tr('scrcpy_not_found'), "WARNING")
        except FileNotFoundError:
            self.log(tr('scrcpy_not_found'), "WARNING")

    def refresh_devices(self):
        """Refresh the list of connected ADB devices."""
        adb_path = self.get_adb_path()
        try:
            result = subprocess.run([adb_path, "devices"], capture_output=True, text=True)
            lines = result.stdout.strip().split("\n")[1:]  # Skip header
            devices = []
            for line in lines:
                if line.strip() and "\t" in line:
                    parts = line.split("\t")
                    if len(parts) == 2 and parts[1] == "device":
                        devices.append(parts[0])

            current_text = self.devices_combo.currentText()
            self.devices_combo.clear()
            self.devices_combo.addItem("-- Select Device --" if get_language() == 'en' else "-- Выбрать устройство --")
            self.devices_combo.addItems(devices)

            if devices:
                self.log(f"{tr('devices_found')}{len(devices)}{tr('devices_found_suffix')}")
            else:
                self.log(tr('no_devices'))

            # Try to restore selection
            if current_text and current_text not in ["-- Select Device --", "-- Выбрать устройство --"] and current_text in devices:
                self.devices_combo.setCurrentText(current_text)

        except Exception as e:
            self.log(f"{tr('error_refresh')}{e}", "ERROR")

    def on_device_selected(self, device):
        """Handle device selection."""
        if device and device not in ["-- Select Device --", "-- Выбрать устройство --"]:
            self.current_device = device
            self.device_info_label.setText(f"{tr('selected_device')}{device}")
            self.device_info_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
            self.device_input.setText(device)
        else:
            self.current_device = None
            self.device_info_label.setText(tr('no_device'))
            self.device_info_label.setStyleSheet("color: #666; font-style: italic;")

    def run_adb_command(self, args, callback=None):
        """Run an ADB command in a separate thread."""
        adb_path = self.get_adb_path()
        worker = ADBWorker(adb_path, args)
        worker.finished.connect(lambda msg: self.log(msg))
        worker.output.connect(lambda msg: self.log(msg.strip()))
        worker.error.connect(lambda msg: self.log(msg.strip(), "ERROR"))
        if callback:
            worker.finished.connect(callback)
        self.workers.append(worker)
        worker.start()

    def connect_device(self):
        """Connect to a device via ADB over WiFi."""
        device = self.device_input.text().strip()
        if not device:
            QMessageBox.warning(self, tr('input_error'), tr('enter_ip_port'))
            return

        # Validate format
        if ":" not in device:
            QMessageBox.warning(self, tr('input_error'), tr('enter_ip_port_format'))
            return

        self.log(f"{tr('connecting')}{device}...")
        self.connect_btn.setEnabled(False)

        def on_finished():
            self.connect_btn.setEnabled(True)
            self.refresh_devices()

        self.run_adb_command(["connect", device], on_finished)

    def disconnect_device(self):
        """Disconnect from a device."""
        device = self.device_input.text().strip()
        if not device:
            QMessageBox.warning(self, tr('input_error'), tr('enter_ip_port'))
            return

        self.log(f"{tr('disconnecting')}{device}...")
        self.disconnect_btn.setEnabled(False)

        def on_finished():
            self.disconnect_btn.setEnabled(True)
            self.refresh_devices()

        self.run_adb_command(["disconnect", device], on_finished)

    def on_language_changed(self):
        """Handle language change - update UI language."""
        lang = self.lang_combo.currentData()
        set_language(lang)
        self.update_ui_texts()
    
    def update_ui_texts(self):
        """Update all UI text elements with current language."""
        # Update window title
        self.setWindowTitle(tr('title'))
        
        # Update title label
        if hasattr(self, 'title_label'):
            self.title_label.setText(tr('title'))
        
        # Update group boxes
        for widget_name, key in self.ui_keys.items():
            if hasattr(self, widget_name):
                widget = getattr(self, widget_name)
                if isinstance(widget, QGroupBox):
                    widget.setTitle(tr(key))
                elif isinstance(widget, QPushButton):
                    widget.setText(tr(key))
                elif isinstance(widget, QLabel):
                    widget.setText(tr(key))
        
        # Update lang label
        if hasattr(self, 'lang_label'):
            self.lang_label.setText("Language:" if get_language() == 'en' else "Язык:")
        
        # Update device info label
        if hasattr(self, 'device_info_label'):
            if self.current_device:
                self.device_info_label.setText(f"{tr('selected_device')}{self.current_device}")
            else:
                self.device_info_label.setText(tr('no_device'))
        
        # Update status bar
        self.statusBar.showMessage(tr('ready'))
        
        # Update max size combo
        if hasattr(self, 'max_size_combo'):
            self.max_size_combo.setItemText(0, tr('no_limit'))
        
        # Update device combo placeholder
        if hasattr(self, 'devices_combo'):
            current_device_text = self.devices_combo.currentText()
            placeholder = "-- Select Device --" if get_language() == 'en' else "-- Выбрать устройство --"
            if self.devices_combo.count() > 0:
                self.devices_combo.setItemText(0, placeholder)
                self.devices_combo.setCurrentText(current_device_text)
        
        self.log(f"Language changed to: {get_language()}")

    def show_pair_dialog(self):
        """Show the ADB pairing dialog."""
        if self.pair_dialog is None:
            self.pair_dialog = ADBPairDialog(self)
        self.pair_dialog.show()
        self.pair_dialog.raise_()
        self.pair_dialog.activateWindow()

    def start_scrcpy(self):
        """Start scrcpy for the selected device."""
        if not self.current_device:
            QMessageBox.warning(self, tr('no_device_title'), tr('select_device'))
            return

        # Get scrcpy path (local or system)
        scrcpy_path = self.get_scrcpy_path()

        # Build scrcpy command
        cmd = [scrcpy_path, "-s", self.current_device]

        # Add bitrate
        try:
            bitrate = int(self.bitrate_input.text().strip())
            cmd.extend(["-b", f"{bitrate}M"])
        except ValueError:
            pass

        # Add max size
        max_size = self.max_size_combo.currentText()
        if max_size != tr('no_limit'):
            cmd.extend(["-m", max_size])

        self.log(f"{tr('starting_scrcpy')}{self.current_device}...")
        self.log(f"{tr('command')}{' '.join(cmd)}")

        try:
            # Start scrcpy in a separate process
            self.scrcpy_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.start_scrcpy_btn.setEnabled(False)
            self.stop_scrcpy_btn.setEnabled(True)
            self.log(tr('scrcpy_started'))

            # Monitor the process
            QTimer.singleShot(1000, self.check_scrcpy_status)

        except FileNotFoundError:
            self.log(tr('scrcpy_not_found_error'), "ERROR")
            QMessageBox.critical(self, tr('scrcpy_not_found_title'),
                tr('scrcpy_not_found_error'))
        except Exception as e:
            self.log(f"{tr('error_starting')}{e}", "ERROR")

    def stop_scrcpy(self):
        """Stop the running scrcpy process."""
        if hasattr(self, 'scrcpy_process') and self.scrcpy_process.poll() is None:
            self.scrcpy_process.terminate()
            try:
                self.scrcpy_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.scrcpy_process.kill()
            self.log(tr('scrcpy_stopped'))
        self.start_scrcpy_btn.setEnabled(True)
        self.stop_scrcpy_btn.setEnabled(False)

    def check_scrcpy_status(self):
        """Check if scrcpy is still running."""
        if hasattr(self, 'scrcpy_process') and self.scrcpy_process is not None:
            if self.scrcpy_process.poll() is not None:
                # Process has ended
                self.start_scrcpy_btn.setEnabled(True)
                self.stop_scrcpy_btn.setEnabled(False)
                self.log(tr('scrcpy_ended'))
            else:
                # Still running, check again
                QTimer.singleShot(1000, self.check_scrcpy_status)

    def closeEvent(self, event):
        """Handle application close event - cleanup ADB and scrcpy."""
        # Stop scrcpy if running
        if hasattr(self, 'scrcpy_process') and self.scrcpy_process is not None:
            if self.scrcpy_process.poll() is None:
                self.log("Stopping scrcpy on exit...")
                self.scrcpy_process.terminate()
                try:
                    self.scrcpy_process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    self.scrcpy_process.kill()

        # Disconnect all ADB connections
        self.log("Disconnecting all ADB devices...")
        adb_path = self.get_adb_path()
        try:
            subprocess.run([adb_path, "disconnect"], capture_output=True, text=True, timeout=5)
        except:
            pass

        self.log("Application closed.")
        event.accept()


def main():
    app = QApplication(sys.argv)

    # Set application icon
    icon_path = Path(__file__).parent.resolve() / "icon.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    # Set application name
    app.setApplicationName("Scrcpy GUI")

    # Use system default style (no Fusion/dark theme)
    # app.setStyle("Fusion")  # Removed - use system style

    window = ScrcpyGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
# Copyright 2025 Dkmariolink (thedkmariolink@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Style Manager for EZ Streaming - Centralizes color definitions and QSS generation.
"""

class StyleManager:
    """Manages the application's styling, colors, and QSS generation."""

    def __init__(self):
        # --- Color Palette ---
        self.bg_color = "#1E1E1E"
        self.fg_color = "#FFFFFF"
        self.accent_color = "#9146FF" # Twitch purple
        self.button_color = "#772CE8" # Slightly darker purple for buttons
        self.disabled_bg_color = "#555555"
        self.disabled_fg_color = "#AAAAAA"
        self.input_bg_color = "#2E2E2E"
        self.border_color = "#444444"
        self.list_item_bg = "#2A2A2A"
        self.list_item_selected_bg = "#3D3D3D"
        self.list_item_hover_bg = "#333333"
        self.list_item_selected_active_bg = "#4D4D4D"
        self.tooltip_bg = "white"
        self.tooltip_fg = "black"
        self.tooltip_border = "#AAAAAA"

        # Status Colors
        self.ready_color = self.fg_color
        self.launching_color = self.accent_color
        self.launched_color = "#00C853" # Green
        self.error_color = "#FF5252"   # Red
        self.warning_color = "#FFC107" # Amber

    def get_main_stylesheet(self):
        """Returns the main application stylesheet."""
        return f"""
            QMainWindow, QWidget, QFrame {{ 
                background-color: {self.bg_color}; 
                color: {self.fg_color}; 
                font-family: 'Segoe UI', Arial, sans-serif; 
            }}
            QPushButton {{ 
                background-color: {self.button_color}; 
                color: {self.fg_color}; 
                border: none; 
                padding: 6px 12px; 
                border-radius: 4px; 
                font-weight: bold; 
                font-size: 10pt; 
            }}
            QPushButton:hover {{ 
                background-color: {self.accent_color}; 
            }}
            QPushButton:disabled {{ 
                background-color: {self.disabled_bg_color}; 
                color: {self.disabled_fg_color}; 
            }}
            QLabel {{ 
                font-size: 10pt; 
                background-color: transparent; /* Ensure labels have transparent background */
            }}
            QLineEdit, QComboBox {{ 
                background-color: {self.input_bg_color}; 
                color: {self.fg_color}; 
                border: 1px solid {self.border_color}; 
                padding: 5px 8px; 
                border-radius: 4px; 
                font-size: 10pt; 
                min-height: 24px; 
            }}
            QSpinBox {{ 
                font-size: 10pt; 
                min-height: 24px; 
                border: 1px solid {self.border_color}; 
                background-color: {self.input_bg_color}; 
                color: {self.fg_color}; /* Ensure text color is set */
                border-radius: 4px; 
                padding: 1px; 
            }} 
            QCheckBox {{ 
                font-size: 10pt; 
                background-color: transparent; /* Ensure checkbox has transparent background */
                color: {self.fg_color}; /* Ensure text color */
            }} 
            QCheckBox:disabled {{
                color: {self.disabled_fg_color};
            }}
            /* Hide default spin box buttons */
            QSpinBox::up-button {{ width: 0px; border: none; }}
            QSpinBox::down-button {{ width: 0px; border: none; }}
            /* Style custom arrow buttons */
            QPushButton#ArrowButton, QPushButton#ProfileUpArrow, QPushButton#ProfileDownArrow {{ 
                background-color: #3E3E3E; 
                color: white;
                border: 1px solid {self.border_color}; 
                padding: 1px 2px; 
                font-size: 7pt; 
                border-radius: 3px; 
                margin: 0px; 
            }}
            QPushButton#ArrowButton:hover, QPushButton#ProfileUpArrow:hover, QPushButton#ProfileDownArrow:hover {{ 
                background-color: #4E4E4E; 
                border: 1px solid {self.accent_color}; 
            }}
            QPushButton#ArrowButton:disabled, QPushButton#ProfileUpArrow:disabled, QPushButton#ProfileDownArrow:disabled {{ 
                background-color: {self.disabled_bg_color}; 
                color: {self.disabled_fg_color}; 
                border: 1px solid {self.border_color};
            }}
            /* Specific border removal/rounding for touching buttons */
            QPushButton#ProfileUpArrow {{ border-bottom-left-radius: 0px; border-bottom-right-radius: 0px; border-bottom: none; }} 
            QPushButton#ProfileDownArrow {{ border-top-left-radius: 0px; border-top-right-radius: 0px; border-top: none; }} 
            QPushButton#ProfileUpArrow:hover {{ border-bottom: none; }} 
            QPushButton#ProfileDownArrow:hover {{ border-top: none; }} 

            QComboBox::drop-down {{ 
                border: none; 
                background: {self.accent_color}; 
                width: 24px; 
                border-top-right-radius: 4px; /* Match main border radius */
                border-bottom-right-radius: 4px;
            }}
            QComboBox::down-arrow {{ 
                width: 12px; 
                height: 12px; 
                color: white; 
                image: url("data:image/svg+xml;charset=utf-8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12'><path fill='white' d='M0 3 L6 9 L12 3 Z'/></svg>"); 
                margin-right: 6px; 
            }}
            QComboBox QAbstractItemView {{ 
                background-color: {self.input_bg_color}; 
                color: {self.fg_color}; 
                selection-background-color: {self.accent_color}; 
                border: 1px solid {self.border_color}; /* Add border for consistency */
            }}
            QToolTip {{ 
                background-color: {self.tooltip_bg}; 
                color: {self.tooltip_fg}; 
                border: 1px solid {self.tooltip_border}; 
                padding: 4px; 
                font-size: 9pt; 
            }}
            QListWidget {{ 
                background-color: {self.bg_color}; 
                border: none; 
                outline: none; 
            }}
            QListWidget::item {{ 
                background-color: {self.list_item_bg}; 
                border-radius: 4px; 
                margin: 5px 0; 
                padding: 6px; 
                min-height: 40px; 
                color: {self.fg_color}; /* Ensure item text color */
            }}
            QListWidget::item:selected {{ 
                background-color: {self.list_item_selected_bg}; 
                border: 1px solid {self.accent_color}; 
                outline: none; 
            }}
            QListWidget::item:hover {{ 
                background-color: {self.list_item_hover_bg}; 
            }}
            QListWidget::item:selected:active {{ 
                background-color: {self.list_item_selected_active_bg}; 
                border: 1px solid {self.accent_color}; 
                outline: none; 
            }}
            QListWidget::item:focus {{ 
                outline: none; 
                border: 1px solid {self.accent_color}; 
            }}
            /* Remove focus rectangle */
            QWidget:focus {{ outline: none; }} 
        """

    def get_button_style(self, additional_style=""):
        """Returns the base QSS for QPushButton with optional additions."""
        return f"""
            QPushButton {{
                background-color: {self.button_color}; 
                color: {self.fg_color}; 
                border: none;
                padding: 6px 12px; 
                border-radius: 4px;
                font-weight: bold;
                font-size: 10pt;
            }}
            QPushButton:hover {{ background-color: {self.accent_color}; }}
            QPushButton:disabled {{ background-color: {self.disabled_bg_color}; color: {self.disabled_fg_color}; }}
            {additional_style}
        """

    def get_line_edit_style(self):
        """Returns the base QSS for QLineEdit."""
        return f"""
            QLineEdit {{
                background-color: {self.input_bg_color}; 
                color: {self.fg_color}; 
                border: 1px solid {self.border_color}; 
                padding: 5px 8px; 
                border-radius: 4px; 
                font-size: 10pt; 
                min-height: 24px;
            }}
        """
        
    def get_status_label_style(self, status_type="ready"):
        """Returns QSS for the status label based on status type."""
        color = self.ready_color
        if status_type == "launching":
            color = self.launching_color
        elif status_type == "launched":
            color = self.launched_color
        elif status_type == "error":
            color = self.error_color
        elif status_type == "warning":
            color = self.warning_color
            
        return f"background-color: transparent; color: {color}; border-radius: 4px;"

    def get_drag_handle_style(self):
        """Returns QSS for the drag handle label."""
        return f"background-color: transparent; color: {self.disabled_fg_color}; font-size: 18px; border-radius: 4px;"

    def get_checkbox_style(self, enabled=True):
        """Returns QSS for QCheckBox based on enabled state."""
        color = self.fg_color if enabled else self.disabled_fg_color
        return f"background-color: transparent; color: {color}; border-radius: 4px;"

# EZ Streaming
# Copyright (C) 2025 Dkmariolink <thedkmariolink@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""
Custom Exception Classes for EZ Streaming
"""

class AppError(Exception):
    """Base exception for application-specific errors."""
    pass

class ConfigError(AppError):
    """Exception raised for errors related to configuration loading or saving."""
    pass

class ProcessError(AppError):
    """Exception raised for errors related to launching or managing external processes."""
    pass

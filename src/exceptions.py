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

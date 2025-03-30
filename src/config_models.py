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
Configuration Model Classes for EZ Streaming
"""

from dataclasses import dataclass, field, asdict

@dataclass
class ProgramConfig:
    """Data class representing the configuration for a single program."""
    name: str = ""
    path: str = ""
    use_custom_delay: bool = False
    custom_delay_value: int = 0

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a ProgramConfig instance from a dictionary."""
        # Handle potential missing keys gracefully
        return cls(
            name=data.get("name", ""),
            path=data.get("path", ""),
            use_custom_delay=data.get("use_custom_delay", False),
            custom_delay_value=data.get("custom_delay_value", 0)
        )

    def to_dict(self) -> dict:
        """Converts the ProgramConfig instance to a dictionary."""
        return asdict(self)


@dataclass
class ProfileConfig:
    """Data class representing the configuration for a profile."""
    name: str
    launch_delay: int = 5
    programs: list[ProgramConfig] = field(default_factory=list)

    @classmethod
    def from_dict(cls, name: str, data: dict):
        """Creates a ProfileConfig instance from a dictionary."""
        programs_data = data.get("programs", [])
        programs = [ProgramConfig.from_dict(p_data) for p_data in programs_data if isinstance(p_data, dict)]
        
        # Ensure minimum number of program slots (e.g., 2)
        while len(programs) < 2:
            programs.append(ProgramConfig()) # Add empty program config

        return cls(
            name=name,
            launch_delay=data.get("launch_delay", 5),
            programs=programs
        )

    def to_dict(self) -> dict:
        """Converts the ProfileConfig instance to a dictionary suitable for JSON serialization."""
        return {
            "launch_delay": self.launch_delay,
            "programs": [p.to_dict() for p in self.programs]
        }

# EZ Streaming
# Copyright (C) 2025 Dkmariolink <thedkmariolink@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""
Resource Monitor for EZ Streaming - Monitors CPU, GPU, and Memory usage of processes
"""

import psutil
import os
import platform
from typing import Dict, Optional, Tuple

# Try to import GPU monitoring libraries
try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

try:
    # For NVIDIA GPUs
    import pynvml
    NVIDIA_AVAILABLE = True
except ImportError:
    NVIDIA_AVAILABLE = False


class ResourceMonitor:
    """Monitors system resources for running processes"""
    
    def __init__(self):
        self.system = platform.system()
        self._init_gpu_monitoring()
        
    def _init_gpu_monitoring(self):
        """Initialize GPU monitoring if available"""
        self.gpu_initialized = False
        
        if NVIDIA_AVAILABLE:
            try:
                pynvml.nvmlInit()
                self.gpu_count = pynvml.nvmlDeviceGetCount()
                self.gpu_initialized = True
            except:
                pass
    
    def get_process_by_path(self, exe_path: str) -> Optional[psutil.Process]:
        """Find a running process by its executable path"""
        if not exe_path:
            return None
            
        exe_name = os.path.basename(exe_path).lower()
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    # Check by exact path first, using normcase for case-insensitivity
                    if proc.info['exe'] and os.path.normcase(os.path.normpath(proc.info['exe'])) == os.path.normcase(os.path.normpath(exe_path)):
                        return proc
                    # Check by name as fallback
                    elif proc.info['name'] and proc.info['name'].lower() == exe_name:
                        # Verify it's the right process by checking if paths match, using normcase
                        if proc.exe() and os.path.normcase(os.path.normpath(proc.exe())) == os.path.normcase(os.path.normpath(exe_path)):
                            return proc
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except:
            pass
        
        return None
    
    def _get_gpu_usage_nvidia_smi(self, pid: int) -> float:
        """Get GPU usage using nvidia-smi command (most accurate for process-specific)"""
        try:
            import subprocess
            
            # First get the overall GPU usage
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            if result.returncode == 0:
                try:
                    overall_gpu = float(result.stdout.strip())
                    
                    # Try to get process-specific info
                    proc_result = subprocess.run(
                        ['nvidia-smi', '--query-compute-apps=pid,used_memory', '--format=csv,noheader,nounits'],
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                    
                    if proc_result.returncode == 0 and proc_result.stdout.strip():
                        # If our process is using GPU, return overall usage
                        # (process-specific GPU % is not available via nvidia-smi)
                        lines = proc_result.stdout.strip().split('\n')
                        for line in lines:
                            if str(pid) in line:
                                return overall_gpu
                    
                    # If process not found in GPU processes, return 0
                    return 0.0
                    
                except ValueError:
                    pass
        except Exception:
            pass
        
        return 0.0
    
    def get_process_resources(self, process: psutil.Process) -> Dict[str, float]:
        """
        Get resource usage for a process
        
        Returns:
            Dict with 'cpu', 'memory', and 'gpu' percentages
        """
        resources = {
            'cpu': 0.0,
            'memory': 0.0,
            'gpu': 0.0
        }
        
        if not process:
            return resources
        
        try:
            # CPU usage (percentage of total CPU)
            # Changed interval to None for non-blocking call
            cpu_percent = process.cpu_percent(interval=None)
            # Normalize to 0-100 range (psutil returns per-core percentage)
            cpu_count = psutil.cpu_count()
            resources['cpu'] = min(cpu_percent / cpu_count if cpu_count else cpu_percent, 100.0)
            
            # Memory usage (percentage of total RAM)
            memory_info = process.memory_info()
            total_memory = psutil.virtual_memory().total
            resources['memory'] = (memory_info.rss / total_memory) * 100.0
            
            # GPU usage - try multiple methods
            gpu_usage = 0.0
            
            # Removed initial call to _get_gpu_usage_nvidia_smi for performance.
            # Rely on pynvml and GPUtil first.
            if self.gpu_initialized and NVIDIA_AVAILABLE:
                gpu_usage = self._get_nvidia_gpu_usage(process.pid)
            
            if gpu_usage == 0.0: # If pynvml didn't work or wasn't available
                if GPU_AVAILABLE:
                    gpu_usage = self._get_gpu_usage_gputil()
                else:
                    gpu_usage = self._get_gpu_usage_windows()
            
            resources['gpu'] = gpu_usage
                
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
            
        return resources
    
    def _get_nvidia_gpu_usage(self, pid: int) -> float:
        """Get GPU usage for a specific process using NVIDIA tools"""
        try:
            # Get the default GPU (index 0)
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            
            # Get overall GPU utilization
            util = pynvml.nvmlDeviceGetUtilizationRates(handle)
            
            # Try to get process-specific usage
            try:
                processes = pynvml.nvmlDeviceGetComputeRunningProcesses(handle)
                for proc in processes:
                    if proc.pid == pid:
                        # Found our process - calculate percentage
                        mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                        return (proc.usedGpuMemory / mem_info.total) * 100.0
            except:
                pass
            
            # If we can't get process-specific, return overall GPU usage
            return float(util.gpu)
        except Exception as e:
            print(f"Error getting NVIDIA GPU usage: {e}")
            return 0.0
    
    def _get_gpu_usage_gputil(self) -> float:
        """Get GPU usage using GPUtil"""
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                return gpus[0].load * 100
        except:
            pass
        return 0.0
    
    def _get_gpu_usage_windows(self) -> float:
        """Get GPU usage using Windows Performance Counters"""
        if self.system != 'Windows':
            return 0.0
            
        try:
            # Try using Windows WMI
            import subprocess
            result = subprocess.run(
                ['wmic', 'path', 'Win32_VideoController', 'get', 'CurrentUsage'],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.strip() and not 'CurrentUsage' in line:
                        try:
                            return float(line.strip())
                        except:
                            pass
        except:
            pass
        
        return 0.0
    
    def get_resource_color(self, percentage: float, resource_type: str = 'cpu') -> str:
        """
        Get color based on resource usage percentage
        
        Returns:
            Hex color string (green/amber/red)
        """
        if resource_type == 'memory':
            # Memory thresholds are different
            if percentage < 60:
                return "#4CAF50"  # Green
            elif percentage < 85:
                return "#FFA726"  # Amber
            else:
                return "#EF5350"  # Red
        else:
            # CPU/GPU thresholds
            if percentage < 50:
                return "#4CAF50"  # Green
            elif percentage < 75:
                return "#FFA726"  # Amber
            else:
                return "#EF5350"  # Red
    
    def format_percentage(self, value: float) -> str:
        """Format percentage for display"""
        return f"{value:.1f}%"

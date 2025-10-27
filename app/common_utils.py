# -*- coding: utf-8 -*-
"""
通用工具模块 - 提供公共功能和工具
"""

import shutil
import subprocess
from typing import Dict, List, Tuple, Optional
from .logger_utils import log_info, log_success, log_warning, log_error


class ToolChecker:
    """工具检查器 - 提供通用的工具检查功能"""
    
    @staticmethod
    def check_command(command: str, version_arg: str = "--version", timeout: int = 10) -> bool:
        """检查命令是否可用
        
        Args:
            command: 命令名称
            version_arg: 版本参数
            timeout: 超时时间（秒）
            
        Returns:
            bool: 命令是否可用
        """
        try:
            result = subprocess.run(
                [command, version_arg],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            return False
    
    @staticmethod
    def check_tools_batch(tools: List[Tuple[str, str, str]], category_name: str) -> List[str]:
        """批量检查工具
        
        Args:
            tools: 工具列表 [(command, description, version_arg), ...]
            category_name: 分类名称
            
        Returns:
            List[str]: 缺失的工具列表
        """
        log_info(f"{category_name}:")
        missing_tools = []
        
        for tool_info in tools:
            if len(tool_info) == 2:
                command, description = tool_info
                version_arg = "--version"
            else:
                command, description, version_arg = tool_info
            
            if ToolChecker.check_command(command, version_arg):
                log_success(f"  ✅ {description} 已安装")
            else:
                log_warning(f"  ⚠️  {description} 未安装")
                missing_tools.append(command)
        
        log_info("")
        return missing_tools


class InstallationHelper:
    """安装帮助器 - 提供安装建议"""
    
    # 工具安装建议映射
    INSTALL_SUGGESTIONS = {
        'nuitka': 'pip install nuitka',
        'pyinstaller': 'pip install pyinstaller',
        'fpm': {
            'Linux': 'sudo apt install ruby-dev build-essential && sudo gem install fpm',
            'Darwin': 'brew install fpm',
            'Windows': 'Windows下建议使用WSL或Docker运行FPM'
        },
        'nfpm': '访问 https://nfpm.goreleaser.com/install/ 获取安装方法',
        'clang': {
            'Linux': 'sudo apt install clang',
            'Darwin': 'xcode-select --install 或 brew install clang',
            'Windows': '安装Visual Studio或MinGW'
        },
        'gcc': {
            'Linux': 'sudo apt install gcc',
            'Darwin': 'xcode-select --install 或 brew install gcc',
            'Windows': '安装MinGW或Visual Studio'
        },
        'dpkg-deb': {
            'deb系': 'sudo apt install dpkg-dev',
            'rpm系': 'sudo yum install dpkg-dev 或 sudo dnf install dpkg-dev',
            'arch系': 'sudo pacman -S dpkg',
            'default': '请根据发行版使用相应包管理器安装 dpkg-dev'
        },
        'rpmbuild': {
            'deb系': 'sudo apt install rpm',
            'rpm系': 'sudo yum install rpm-build 或 sudo dnf install rpm-build',
            'arch系': 'sudo pacman -S rpm-tools',
            'default': '请根据发行版使用相应包管理器安装 rpm-build'
        }
    }
    
    @staticmethod
    def get_install_suggestion(tool: str, platform: str = None, distro: str = None) -> str:
        """获取工具安装建议
        
        Args:
            tool: 工具名称
            platform: 平台名称 (Linux/Darwin/Windows)
            distro: Linux发行版类型 (deb系/rpm系/arch系)
            
        Returns:
            str: 安装建议
        """
        suggestion = InstallationHelper.INSTALL_SUGGESTIONS.get(tool)
        
        if not suggestion:
            return f"安装{tool}: 请查阅官方文档"
        
        if isinstance(suggestion, str):
            return f"安装{tool}: {suggestion}"
        
        # 处理平台特定建议
        if isinstance(suggestion, dict):
            if distro and distro in suggestion:
                return f"安装{tool}: {suggestion[distro]}"
            elif platform and platform in suggestion:
                return f"安装{tool}: {suggestion[platform]}"
            else:
                return f"安装{tool}: {suggestion.get('default', '请查阅官方文档')}"
        
        return f"安装{tool}: 请查阅官方文档"


class ConfigHelper:
    """配置帮助器 - 提供配置相关的通用功能"""
    
    @staticmethod
    def safe_getattr(obj, attr: str, default=None):
        """安全获取对象属性"""
        return getattr(obj, attr, default)
    
    @staticmethod
    def format_list_for_code(items: List[str], quote_char: str = '"') -> str:
        """格式化列表为代码字符串"""
        if not items:
            return "[]"
        items_str = ", ".join([f'{quote_char}{item}{quote_char}' for item in items])
        return f"[{items_str}]"
    
    @staticmethod
    def format_dict_for_code(data: Dict, indent: int = 4) -> str:
        """格式化字典为代码字符串"""
        if not data:
            return "{}"
        
        lines = ["{"]
        for key, value in data.items():
            if isinstance(value, list):
                value_str = ConfigHelper.format_list_for_code(value)
            elif isinstance(value, str):
                value_str = f'"{value}"'
            else:
                value_str = str(value)
            lines.append(f"{' ' * indent}'{key}': {value_str},")
        lines.append("}")
        
        return "\n".join(lines)


class PathHelper:
    """路径帮助器 - 提供路径相关的通用功能"""
    
    @staticmethod
    def find_executable_in_dirs(dirs: List[str], exclude_extensions: List[str] = None) -> Optional[str]:
        """在指定目录中查找可执行文件
        
        Args:
            dirs: 搜索目录列表
            exclude_extensions: 排除的文件扩展名
            
        Returns:
            Optional[str]: 找到的可执行文件路径，未找到返回None
        """
        from pathlib import Path
        import os
        
        if exclude_extensions is None:
            exclude_extensions = ['.spec', '.txt', '.log', '.exe']
        
        for build_dir in dirs:
            build_path = Path(build_dir)
            if build_path.exists():
                for file_path in build_path.rglob("*"):
                    if (file_path.is_file() and 
                        file_path.suffix not in exclude_extensions and
                        (os.access(file_path, os.X_OK) or file_path.suffix == '')):
                        return str(file_path)
        
        return None

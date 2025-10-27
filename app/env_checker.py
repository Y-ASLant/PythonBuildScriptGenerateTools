# -*- coding: utf-8 -*-
"""
环境检查模块 - 检查系统环境和所需的打包工具
"""

import sys
import platform
import shutil
from pathlib import Path
from .logger_utils import log_info, log_success, log_error, log_warning
from .common_utils import ToolChecker, InstallationHelper


class EnvironmentChecker:
    """环境检查器 - 检查系统环境和打包工具"""

    def __init__(self):
        self.system_info = {
            'platform': platform.system(),
            'architecture': platform.machine(),
            'python_version': platform.python_version(),
            'python_executable': sys.executable
        }

    def check_all(self):
        """检查所有环境和工具"""
        log_info("=" * 60)
        log_info("🔍 系统环境检查")
        log_info("=" * 60)
        
        # 检查系统信息
        self._check_system_info()
        
        # 检查Python环境
        self._check_python_environment()
        
        # 检查构建工具
        self._check_build_tools()
        
        # 检查打包工具
        self._check_package_tools()
        
        
        log_info("=" * 60)
        log_info("✅ 环境检查完成")
        log_info("=" * 60)

    def check_required_tools(self, required_tools):
        """检查指定的工具列表
        
        Args:
            required_tools (dict): 需要检查的工具配置
                {
                    'build_tools': ['nuitka', 'pyinstaller'],
                    'package_tools': ['nfpm', 'fpm'],
                    'system_tools': ['clang', 'gcc'],
                    'package_types': ['deb', 'rpm']
                }
        """
        log_info("=" * 60)
        log_info("🔍 针对性环境检查")
        log_info("=" * 60)
        
        # 检查系统信息（总是需要）
        self._check_system_info()
        
        # 检查Python环境（总是需要）
        self._check_python_environment()
        
        # 检查指定的构建工具
        if 'build_tools' in required_tools:
            self._check_specific_build_tools(required_tools['build_tools'])
        
        # 检查指定的打包工具
        if 'package_tools' in required_tools:
            self._check_specific_package_tools(required_tools['package_tools'])
        
        # 检查指定的系统工具
        if 'system_tools' in required_tools:
            self._check_specific_system_tools(required_tools['system_tools'])
        
        # 检查指定的包类型支持
        if 'package_types' in required_tools:
            self._check_package_type_support(required_tools['package_types'])
        
        log_info("=" * 60)
        log_info("✅ 针对性环境检查完成")
        log_info("=" * 60)

    def _check_system_info(self):
        """检查系统信息"""
        log_info("📋 系统信息:")
        
        # 显示基本系统信息
        platform_info = self.system_info['platform']
        
        # 如果是Linux，检测发行版类型
        if platform_info == 'Linux':
            distro_info = self._detect_linux_distro()
            log_info(f"  操作系统: {platform_info} ({distro_info})")
        else:
            log_info(f"  操作系统: {platform_info}")
            
        log_info(f"  架构: {self.system_info['architecture']}")
        log_info(f"  Python版本: {self.system_info['python_version']}")
        log_info(f"  Python路径: {self.system_info['python_executable']}")
        log_info("")

    def _detect_linux_distro(self):
        """检测Linux发行版类型"""
        try:
            # 尝试读取 /etc/os-release 文件
            if Path("/etc/os-release").exists():
                with open("/etc/os-release", "r") as f:
                    os_release = f.read()
                
                # 提取发行版信息
                distro_name = ""
                for line in os_release.split('\n'):
                    if line.startswith('NAME='):
                        distro_name = line.split('=')[1].strip('"').lower()
                        break
                
                # 根据发行版名称判断包管理器类型
                if any(x in distro_name for x in ['ubuntu', 'debian', 'mint', 'pop', 'elementary']):
                    return "deb系"
                elif any(x in distro_name for x in ['fedora', 'rhel', 'centos', 'rocky', 'alma', 'opensuse', 'suse']):
                    return "rpm系"
                elif 'arch' in distro_name or 'manjaro' in distro_name:
                    return "arch系"
                elif 'alpine' in distro_name:
                    return "apk系"
                else:
                    return "其他"
            
            # 备用检测方法：检查包管理器
            elif Path("/usr/bin/apt").exists() or Path("/usr/bin/dpkg").exists():
                return "deb系"
            elif Path("/usr/bin/yum").exists() or Path("/usr/bin/dnf").exists():
                return "rpm系"
            elif Path("/usr/bin/pacman").exists():
                return "arch系"
            elif Path("/sbin/apk").exists():
                return "apk系"
            else:
                return "其他"
                
        except Exception:
            return "检测失败"

    def _check_python_environment(self):
        """检查Python环境"""
        log_info("🐍 Python环境:")
        
        # 检查Python版本
        python_version = tuple(map(int, platform.python_version().split('.')))
        if python_version >= (3, 8):
            log_success(f"  ✅ Python {platform.python_version()} (支持)")
        else:
            log_warning(f"  ⚠️  Python {platform.python_version()} (建议使用3.8+)")
        
        # 检查包管理器
        self._check_package_managers()
        
        log_info("")

    def _check_package_managers(self):
        """检查Python包管理器"""
        # 检查现代包管理器
        modern_managers = [
            ("uv", "UV (现代包管理器)"),
            ("poetry", "Poetry"),
            ("pdm", "PDM"),
            ("pipenv", "Pipenv")
        ]
        
        found_modern_manager = False
        for manager, description in modern_managers:
            if shutil.which(manager):
                log_success(f"  ✅ {description} 已安装")
                found_modern_manager = True
        
        # 如果没有找到现代包管理器，再检查pip
        if not found_modern_manager:
            if shutil.which("pip"):
                log_success("  ✅ pip 已安装")
            else:
                log_warning("  ⚠️  未找到包管理器 (pip/uv/poetry等)")
        elif shutil.which("pip"):
            log_info("  📦 pip 也可用 (备用)")
        else:
            log_info("  📦 使用现代包管理器，无需pip")

    def _check_build_tools(self):
        """检查构建工具"""
        build_tools = [
            ("nuitka", "Nuitka编译器"),
            ("pyinstaller", "PyInstaller打包工具")
        ]
        
        ToolChecker.check_tools_batch(build_tools, "🔨 构建工具")

    def _check_package_tools(self):
        """检查打包工具"""
        package_tools = [
            ("fpm", "FPM (支持rpm、deb、pkg等格式)", "--version"),
            ("nfpm", "NFPM (现代包管理器)", "version")
        ]
        
        ToolChecker.check_tools_batch(package_tools, "📦 打包工具")

        # 根据系统检查特定打包工具
        if self.system_info['platform'] == 'Linux':
            self._check_linux_package_tools()
        elif self.system_info['platform'] == 'Darwin':
            self._check_macos_package_tools()
        elif self.system_info['platform'] == 'Windows':
            self._check_windows_package_tools()

    def _check_linux_package_tools(self):
        """检查Linux特定的打包工具"""
        distro_info = self._detect_linux_distro()
        
        linux_tools = [
            ("dpkg-deb", "DEB包构建工具"),
            ("rpmbuild", "RPM包构建工具")
        ]
        
        missing_tools = ToolChecker.check_tools_batch(linux_tools, "  🐧 Linux打包工具")
        
        # 为缺失的工具提供安装建议
        for tool in missing_tools:
            suggestion = InstallationHelper.get_install_suggestion(tool, distro=distro_info)
            log_info(f"      {suggestion}")

    def _check_macos_package_tools(self):
        """检查macOS特定的打包工具"""
        macos_tools = [
            ("pkgbuild", "pkgbuild (系统自带)"),
            ("productbuild", "productbuild (系统自带)")
        ]
        
        ToolChecker.check_tools_batch(macos_tools, "  🍎 macOS打包工具")

    def _check_windows_package_tools(self):
        """检查Windows特定的打包工具"""
        log_info("🪟 Windows打包工具:")
        
        # 检查NSIS
        nsis_paths = [
            "C:\\Program Files (x86)\\NSIS\\makensis.exe",
            "C:\\Program Files\\NSIS\\makensis.exe"
        ]
        
        nsis_found = False
        for nsis_path in nsis_paths:
            if Path(nsis_path).exists():
                log_success("    ✅ NSIS 已安装")
                nsis_found = True
                break
        
        if not nsis_found:
            log_warning("    ⚠️  NSIS 未安装")
            log_info("      下载地址: https://nsis.sourceforge.io/")
        
        # 检查Inno Setup
        inno_paths = [
            "C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe",
            "C:\\Program Files\\Inno Setup 6\\ISCC.exe"
        ]
        
        inno_found = False
        for inno_path in inno_paths:
            if Path(inno_path).exists():
                log_success("    ✅ Inno Setup 已安装")
                inno_found = True
                break
        
        if not inno_found:
            log_warning("    ⚠️  Inno Setup 未安装")
            log_info("      下载地址: https://jrsoftware.org/isinfo.php")



    def get_recommendations(self):
        """获取环境改进建议"""
        recommendations = []
        
        # 使用通用的安装建议生成器
        all_tools = ['nuitka', 'pyinstaller', 'fpm', 'nfpm']
        
        for tool in all_tools:
            if not ToolChecker.check_command(tool, "version" if tool == "nfpm" else "--version"):
                suggestion = InstallationHelper.get_install_suggestion(tool, self.system_info['platform'])
                recommendations.append(suggestion)
        
        # Linux特定工具
        if self.system_info['platform'] == 'Linux':
            distro_info = self._detect_linux_distro()
            linux_tools = ['dpkg-deb', 'rpmbuild']
            
            for tool in linux_tools:
                if not ToolChecker.check_command(tool):
                    suggestion = InstallationHelper.get_install_suggestion(tool, distro=distro_info)
                    recommendations.append(suggestion)
        
        
        return recommendations

    def _check_specific_build_tools(self, tools):
        """检查指定的构建工具"""
        tool_descriptions = {
            'nuitka': 'Nuitka编译器',
            'pyinstaller': 'PyInstaller打包工具'
        }
        
        tool_list = [(tool, tool_descriptions.get(tool, f"{tool}工具")) for tool in tools]
        ToolChecker.check_tools_batch(tool_list, "🔨 构建工具")

    def _check_specific_package_tools(self, tools):
        """检查指定的打包工具"""
        tool_descriptions = {
            'fpm': ('FPM (支持rpm、deb、pkg等格式)', '--version'),
            'nfpm': ('NFPM (现代包管理器)', 'version')
        }
        
        tool_list = []
        for tool in tools:
            if tool in tool_descriptions:
                desc, version_arg = tool_descriptions[tool]
                tool_list.append((tool, desc, version_arg))
        
        missing_tools = ToolChecker.check_tools_batch(tool_list, "📦 打包工具")
        
        # 为缺失的工具提供安装建议
        for tool in missing_tools:
            suggestion = InstallationHelper.get_install_suggestion(tool, self.system_info['platform'])
            log_info(f"    {suggestion}")

    def _check_specific_system_tools(self, tools):
        """检查指定的系统工具"""
        tool_descriptions = {
            'clang': 'Clang编译器',
            'gcc': 'GCC编译器',
            'make': 'Make构建工具',
            'cmake': 'CMake构建工具'
        }
        
        tool_list = [(tool, tool_descriptions.get(tool, f"{tool}工具")) for tool in tools]
        missing_tools = ToolChecker.check_tools_batch(tool_list, "⚙️  系统工具")
        
        # 为缺失的工具提供安装建议
        for tool in missing_tools:
            suggestion = InstallationHelper.get_install_suggestion(tool, self.system_info['platform'])
            log_info(f"    {suggestion}")

    def _check_package_type_support(self, package_types):
        """检查指定包类型的支持情况"""
        package_tools = {
            'deb': 'dpkg-deb',
            'rpm': 'rpmbuild'
        }
        
        tool_list = []
        for pkg_type in package_types:
            if pkg_type in package_tools:
                tool = package_tools[pkg_type]
                tool_list.append((tool, f"{pkg_type.upper()}包 支持"))
        
        if tool_list:
            missing_tools = ToolChecker.check_tools_batch(tool_list, "📋 包类型支持")
            
            # 为缺失的工具提供安装建议
            distro_info = self._detect_linux_distro()
            for tool in missing_tools:
                suggestion = InstallationHelper.get_install_suggestion(tool, distro=distro_info)
                log_info(f"    {suggestion}")

    def get_targeted_recommendations(self, required_tools):
        """获取针对指定工具的环境改进建议"""
        recommendations = []
        
        # 检查所有类型的工具
        all_tools = []
        
        # 收集所有需要检查的工具
        if 'build_tools' in required_tools:
            all_tools.extend(required_tools['build_tools'])
        
        if 'package_tools' in required_tools:
            all_tools.extend(required_tools['package_tools'])
        
        if 'system_tools' in required_tools:
            all_tools.extend(required_tools['system_tools'])
        
        # 检查包类型对应的工具
        if 'package_types' in required_tools:
            package_tools = {'deb': 'dpkg-deb', 'rpm': 'rpmbuild'}
            for pkg_type in required_tools['package_types']:
                if pkg_type in package_tools:
                    all_tools.append(package_tools[pkg_type])
        
        # 统一检查所有工具并生成建议
        distro_info = self._detect_linux_distro() if self.system_info['platform'] == 'Linux' else None
        
        for tool in all_tools:
            version_arg = "version" if tool == "nfpm" else "--version"
            if not ToolChecker.check_command(tool, version_arg):
                suggestion = InstallationHelper.get_install_suggestion(
                    tool, 
                    self.system_info['platform'], 
                    distro_info
                )
                recommendations.append(suggestion)
        
        return recommendations

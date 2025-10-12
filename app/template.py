# -*- coding: utf-8 -*-
"""
构建脚本模板 - 支持Nuitka和PyInstaller
"""

from .template_common import (
    COMMON_IMPORTS_AND_SETUP,
    COMMON_LOG_FUNCTIONS,
    COMMON_ENV_CHECK_FUNCTION,
    COMMON_COPY_FILES_FUNCTION,
    COMMON_MAIN_START,
    COMMON_MAIN_END
)

# Nuitka特定的工具检查函数
NUITKA_TOOL_CHECK = '''
def check_nuitka():
    """检查Nuitka是否已安装"""
    return check_tool_installed("Nuitka", "nuitka")

def check_build_dependencies():
    """检查构建依赖工具"""
    log_info("🔍 检查构建相关工具...")
    
    # 检查编译器
    compilers = ["clang", "gcc"]
    compiler_found = False
    for compiler in compilers:
        if check_tool_installed(compiler, silent=True):
            log_success(f"✅ {{compiler}} 编译器已安装")
            compiler_found = True
            break
    
    if not compiler_found:
        log_warning("⚠️  未找到C编译器 (clang/gcc)")
        log_info("💡 Linux: sudo apt install clang 或 sudo apt install gcc")
        log_info("💡 macOS: xcode-select --install")
    
    # 检查Linux包生成工具（如果需要）
    if "{linux_package_enabled}" == "True":
        log_info("🔍 检查Linux包生成工具...")
        
        # 检查nfpm
        if check_tool_installed("nfpm", silent=True):
            log_success("✅ nfpm 已安装")
        else:
            log_warning("⚠️  nfpm 未安装")
            log_info("💡 安装方法: https://nfpm.goreleaser.com/install/")
        
        # JSON模块检查（标准库，通常无需检查）
        try:
            import json
            log_success("✅ JSON 支持已就绪（标准库）")
        except ImportError:
            log_error("❌ JSON模块不可用")
        
        # 检查包类型支持
        package_types = {linux_package_types}
        for pkg_type in package_types:
            if pkg_type == "deb":
                if check_tool_installed("dpkg-deb", silent=True):
                    log_success("✅ DEB包支持已就绪")
                else:
                    log_warning("⚠️  dpkg-deb 未安装，DEB包生成可能失败")
            elif pkg_type == "rpm":
                if check_tool_installed("rpmbuild", silent=True):
                    log_success("✅ RPM包支持已就绪")
                else:
                    log_warning("⚠️  rpmbuild 未安装，RPM包生成可能失败")
    
    return True'''

# Nuitka特定的配置信息显示
NUITKA_CONFIG_INFO = '''    log_info("入口文件: {entry_name}")
    log_info("输出目录: {output_dir}")
    log_info("编译器: {compiler}")
    log_info("显示控制台: {console_display}")
    log_info("应用名称: {app_name}")
    log_info("=" * 60)
    
    # Nuitka编译参数
    args = [
    {args_str}
    ]
'''

# 组装完整的Nuitka模板
def _build_nuitka_template():
    return (
        COMMON_IMPORTS_AND_SETUP +
        COMMON_LOG_FUNCTIONS +
        COMMON_ENV_CHECK_FUNCTION +
        NUITKA_TOOL_CHECK +
        COMMON_COPY_FILES_FUNCTION +
        COMMON_MAIN_START +
        NUITKA_CONFIG_INFO +
        COMMON_MAIN_END
    )

BUILD_SCRIPT_TEMPLATE = _build_nuitka_template()


# PyInstaller特定的工具检查函数
PYINSTALLER_TOOL_CHECK = '''
def check_pyinstaller():
    """检查PyInstaller是否已安装"""
    return check_tool_installed("PyInstaller", "PyInstaller")

def check_build_dependencies():
    """检查构建依赖工具"""
    log_info("🔍 检查构建相关工具...")
    
    # 检查Linux包生成工具（如果需要）
    if "{linux_package_enabled}" == "True":
        log_info("🔍 检查Linux包生成工具...")
        
        # 检查nfpm
        if check_tool_installed("nfpm", silent=True):
            log_success("✅ nfpm 已安装")
        else:
            log_warning("⚠️  nfpm 未安装")
            log_info("💡 安装方法: https://nfpm.goreleaser.com/install/")
        
        # JSON模块检查（标准库，通常无需检查）
        try:
            import json
            log_success("✅ JSON 支持已就绪（标准库）")
        except ImportError:
            log_error("❌ JSON模块不可用（这不应该发生）")
        
        # 检查包类型支持
        package_types = {linux_package_types}
        for pkg_type in package_types:
            if pkg_type == "deb":
                if check_tool_installed("dpkg-deb", silent=True):
                    log_success("✅ DEB包支持已就绪")
                else:
                    log_warning("⚠️  dpkg-deb 未安装，DEB包生成可能失败")
            elif pkg_type == "rpm":
                if check_tool_installed("rpmbuild", silent=True):
                    log_success("✅ RPM包支持已就绪")
                else:
                    log_warning("⚠️  rpmbuild 未安装，RPM包生成可能失败")
    
    return True'''

# PyInstaller特定的配置信息显示
PYINSTALLER_CONFIG_INFO = '''    log_info("入口文件: {entry_name}")
    log_info("输出目录: {output_dir}")
    log_info("应用名称: {app_name}")
    log_info("单文件模式: {onefile}")
    log_info("显示控制台: {console_display}")
    log_info("公司名称: {company_name}")
    log_info("文件版本: {file_version}")
    log_info("=" * 60)
    
    # PyInstaller编译参数
    args = [
    {args_str}
    ]
'''

# 组装完整的PyInstaller模板
def _build_pyinstaller_template():
    return (
        COMMON_IMPORTS_AND_SETUP +
        COMMON_LOG_FUNCTIONS +
        COMMON_ENV_CHECK_FUNCTION +
        PYINSTALLER_TOOL_CHECK +
        COMMON_COPY_FILES_FUNCTION +
        COMMON_MAIN_START +
        PYINSTALLER_CONFIG_INFO +
        COMMON_MAIN_END
    )

PYINSTALLER_BUILD_SCRIPT_TEMPLATE = _build_pyinstaller_template()

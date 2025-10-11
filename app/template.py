# -*- coding: utf-8 -*-
"""
构建脚本模板 - 支持Nuitka和PyInstaller
"""

BUILD_SCRIPT_TEMPLATE = '''# -*- coding: utf-8 -*-
"""
Nuitka构建脚本
自动生成于 {entry_name} 项目
"""

import os
import sys
from pathlib import Path
from shutil import copy, copytree, rmtree
from datetime import datetime


def log_message(level, message):
    """输出日志信息"""
    colors = {{'INFO': '\\033[94m', 'SUCCESS': '\\033[92m', 'ERROR': '\\033[91m', 'WARNING': '\\033[93m'}}
    color = colors.get(level, '\\033[0m')
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{{timestamp}} | {{color}}{{level:<7}}\\033[0m | {{message}}")

def log_info(message): log_message('INFO', message)
def log_success(message): log_message('SUCCESS', message)  
def log_error(message): log_message('ERROR', message)
def log_warning(message): log_message('WARNING', message)


def check_nuitka():
    """检查Nuitka是否已安装"""
    try:
        import nuitka
        log_success("✅ Nuitka已安装")
        return True
    except ImportError:
        log_error("❌ Nuitka未安装！")
        log_info("📦 请运行: pip install nuitka")
        return False


def main():
    """主构建函数"""
    # 检查Nuitka依赖
    log_info("🔍 检查构建工具依赖...")
    if not check_nuitka():
        sys.exit(1)
    
    # 记录开始时间
    start_time = datetime.now()
    
    log_info("=" * 60)
    log_info("🚀 Nuitka 构建脚本")
    log_info("=" * 60)
    log_info("入口文件: {entry_name}")
    log_info("输出目录: {output_dir}")
    log_info("编译器: {compiler}")
    log_info("显示控制台: {console_display}")
    log_info("应用名称: {app_name}")
    log_info("=" * 60)
    
    # Nuitka编译参数
    args = [
    {args_str}
    ]
    
    log_info("开始Nuitka编译...")
    log_info("执行命令: " + " ".join(args))
    
    # 执行Nuitka编译
    result = os.system(" ".join(args))
    
    if result != 0:
        log_error(f"❌ 编译失败！错误代码: {{result}}")
        sys.exit(1)
    
    log_success("✅ Nuitka编译完成！")
    
    # 复制额外文件和目录
    copy_additional_files()
    
    # 计算总耗时
    end_time = datetime.now()
    duration = end_time - start_time
    total_seconds = int(duration.total_seconds())
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    
    log_success("🎉 构建完成！")
    log_info("输出位置: {output_dir}")
    log_info(f"⏱️  总耗时: {{minutes}}分{{seconds}}秒")


def copy_additional_files():
    """复制额外的文件和目录到构建输出目录"""
    from distutils.sysconfig import get_python_lib
    
    build_output_dir = Path("{output_dir}")
    
    if not build_output_dir.exists():
        log_warning(f"⚠️  构建输出目录不存在: {{build_output_dir}}")
        return
    
    log_info("📁 复制额外文件和目录...")
    
    # 需要复制的目录列表
    copy_dirs = [
{copy_dirs_str}
    ]
    
    for dir_name in copy_dirs:
        src_dir = Path(dir_name)
        if src_dir.exists() and src_dir.is_dir():
            dest_dir = build_output_dir / dir_name
            
            try:
                if dest_dir.exists():
                    rmtree(dest_dir)
                
                copytree(src_dir, dest_dir)
                log_success(f"✅ 已复制目录: {{src_dir}} -> {{dest_dir}}")
            except Exception as e:
                log_error(f"❌ 复制目录 {{src_dir}} 失败: {{e}}")
        else:
            log_warning(f"⚠️  目录不存在，跳过: {{src_dir}}")
    
    # 复制site-packages（如果需要）
    copied_site_packages = []  # 在这里添加需要复制的site-packages
    
    if copied_site_packages:
        site_packages = Path(get_python_lib())
        log_info("📦 复制site-packages...")
        
        for pkg_name in copied_site_packages:
            src = site_packages / pkg_name
            dest = build_output_dir / src.name
            
            log_info(f"复制site-packages {{src}} 到 {{dest}}")
            
            try:
                if src.is_file():
                    copy(src, dest)
                else:
                    copytree(src, dest)
                log_success(f"✅ 已复制: {{src}}")
            except (FileNotFoundError, PermissionError, OSError) as e:
                log_error(f"❌ 复制 {{src}} 失败: {{e}}")
    
    # 复制标准库文件（如果需要）
    copied_standard_packages = []  # 在这里添加需要复制的标准库文件
    
    if copied_standard_packages:
        site_packages = Path(get_python_lib())
        log_info("📚 复制标准库文件...")
        
        for file_name in copied_standard_packages:
            src = site_packages.parent / file_name
            dest = build_output_dir / src.name
            
            log_info(f"复制标准库 {{src}} 到 {{dest}}")
            
            try:
                if src.is_file():
                    copy(src, dest)
                else:
                    copytree(src, dest)
                log_success(f"✅ 已复制: {{src}}")
            except (FileNotFoundError, PermissionError, OSError) as e:
                log_error(f"❌ 复制 {{src}} 失败: {{e}}")


if __name__ == "__main__":
    main()
'''


PYINSTALLER_BUILD_SCRIPT_TEMPLATE = '''# -*- coding: utf-8 -*-
"""
PyInstaller构建脚本
自动生成于 {entry_name} 项目
"""

import os
import sys
from pathlib import Path
from shutil import copy, copytree, rmtree
from datetime import datetime


def log_message(level, message):
    """输出日志信息"""
    colors = {{'INFO': '\\033[94m', 'SUCCESS': '\\033[92m', 'ERROR': '\\033[91m', 'WARNING': '\\033[93m'}}
    color = colors.get(level, '\\033[0m')
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{{timestamp}} | {{color}}{{level:<7}}\\033[0m | {{message}}")

def log_info(message): log_message('INFO', message)
def log_success(message): log_message('SUCCESS', message)  
def log_error(message): log_message('ERROR', message)
def log_warning(message): log_message('WARNING', message)


def check_pyinstaller():
    """检查PyInstaller是否已安装"""
    try:
        import PyInstaller
        log_success("✅ PyInstaller已安装")
        return True
    except ImportError:
        log_error("❌ PyInstaller未安装！")
        log_info("📦 请运行: pip install pyinstaller")
        return False


def main():
    """主构建函数"""
    # 检查PyInstaller依赖
    log_info("🔍 检查构建工具依赖...")
    if not check_pyinstaller():
        sys.exit(1)
    
    # 记录开始时间
    start_time = datetime.now()
    
    log_info("=" * 60)
    log_info("🚀 PyInstaller 构建脚本")
    log_info("=" * 60)
    log_info("入口文件: {entry_name}")
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
    
    log_info("开始PyInstaller编译...")
    log_info("执行命令: " + " ".join(args))
    
    # 执行PyInstaller编译
    result = os.system(" ".join(args))
    
    if result != 0:
        log_error(f"❌ 编译失败！错误代码: {{result}}")
        sys.exit(1)
    
    log_success("✅ PyInstaller编译完成！")
    
    # 复制额外文件和目录
    copy_additional_files()
    
    # 计算总耗时
    end_time = datetime.now()
    duration = end_time - start_time
    total_seconds = int(duration.total_seconds())
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    
    log_success("🎉 构建完成！")
    log_info("输出位置: {output_dir}")
    log_info(f"⏱️  总耗时: {{minutes}}分{{seconds}}秒")


def copy_additional_files():
    """复制额外的文件和目录到构建输出目录"""
    build_output_dir = Path("{output_dir}")
    
    if not build_output_dir.exists():
        log_warning(f"⚠️  构建输出目录不存在: {{build_output_dir}}")
        return
    
    log_info("📁 复制额外文件和目录...")
    
    # 需要复制的目录列表
    copy_dirs = [
{copy_dirs_str}
    ]
    
    for dir_name in copy_dirs:
        src_dir = Path(dir_name)
        if src_dir.exists() and src_dir.is_dir():
            dest_dir = build_output_dir / dir_name
            
            try:
                if dest_dir.exists():
                    rmtree(dest_dir)
                
                copytree(src_dir, dest_dir)
                log_success(f"✅ 已复制目录: {{src_dir}} -> {{dest_dir}}")
            except Exception as e:
                log_error(f"❌ 复制目录 {{src_dir}} 失败: {{e}}")
        else:
            log_warning(f"⚠️  目录不存在，跳过: {{src_dir}}")


if __name__ == "__main__":
    main()
'''

# -*- coding: utf-8 -*-
"""
Nuitka构建脚本模板
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


# ANSI颜色代码
class Colors:
    BLUE = '\\033[94m'      # 蓝色 - INFO
    GREEN = '\\033[92m'     # 绿色 - SUCCESS  
    RED = '\\033[91m'       # 红色 - ERROR
    YELLOW = '\\033[93m'    # 黄色 - WARNING
    RESET = '\\033[0m'      # 重置颜色


def log_info(message):
    """输出信息日志"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{{timestamp}} | {{Colors.BLUE}}INFO   {{Colors.RESET}} | {{message}}")


def log_success(message):
    """输出成功日志"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{{timestamp}} | {{Colors.GREEN}}SUCCESS{{Colors.RESET}} | {{message}}")


def log_error(message):
    """输出错误日志"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{{timestamp}} | {{Colors.RED}}ERROR  {{Colors.RESET}} | {{message}}")


def log_warning(message):
    """输出警告日志"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{{timestamp}} | {{Colors.YELLOW}}WARNING{{Colors.RESET}} | {{message}}")


def main():
    """主构建函数"""
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

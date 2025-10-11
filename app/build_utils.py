# -*- coding: utf-8 -*-
"""
构建工具模块 - 提供构建脚本的通用工具函数
"""

import subprocess
import sys
from datetime import datetime


# ANSI颜色代码
class Colors:
    BLUE = '\033[94m'      # 蓝色 - INFO
    GREEN = '\033[92m'     # 绿色 - SUCCESS  
    RED = '\033[91m'       # 红色 - ERROR
    YELLOW = '\033[93m'    # 黄色 - WARNING
    RESET = '\033[0m'      # 重置颜色


def log_info(message):
    """输出信息日志"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{timestamp} | {Colors.BLUE}INFO   {Colors.RESET} | {message}")


def log_success(message):
    """输出成功日志"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{timestamp} | {Colors.GREEN}SUCCESS{Colors.RESET} | {message}")


def log_error(message):
    """输出错误日志"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{timestamp} | {Colors.RED}ERROR  {Colors.RESET} | {message}")


def log_warning(message):
    """输出警告日志"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{timestamp} | {Colors.YELLOW}WARNING{Colors.RESET} | {message}")


def check_dependency(tool_name):
    """检查构建工具是否已安装"""
    try:
        result = subprocess.run([tool_name, "--version"], 
                              capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        return False


def install_dependency(tool_name):
    """安装构建工具依赖"""
    log_info(f"🔧 开始安装 {tool_name}...")
    
    try:
        # 使用pip安装
        result = subprocess.run([sys.executable, "-m", "pip", "install", tool_name], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            log_success(f"✅ {tool_name} 安装成功！")
            return True
        else:
            log_error(f"❌ {tool_name} 安装失败: {result.stderr}")
            return False
    except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
        log_error(f"❌ 安装 {tool_name} 时发生错误: {e}")
        return False


def check_and_install_dependency(tool_name):
    """检查并根据用户选择安装依赖"""
    if check_dependency(tool_name):
        log_success(f"✅ {tool_name} 已安装")
        return True
    
    log_warning(f"⚠️  {tool_name} 未安装")
    
    # 询问用户是否安装
    while True:
        choice = input(f"是否在当前环境安装 {tool_name}? (y/n): ").strip().lower()
        if choice in ['y', 'yes', '是']:
            return install_dependency(tool_name)
        elif choice in ['n', 'no', '否']:
            log_error(f"❌ 无法继续构建，{tool_name} 未安装")
            return False
        else:
            log_warning("⚠️  请输入 y 或 n")

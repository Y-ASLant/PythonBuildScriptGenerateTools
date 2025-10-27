# -*- coding: utf-8 -*-
"""
日志工具模块 - 提供统一的日志输出功能
"""

from datetime import datetime


# ANSI颜色代码
class Colors:
    BLUE = "\033[94m"  # 蓝色 - INFO
    GREEN = "\033[92m"  # 绿色 - SUCCESS
    RED = "\033[91m"  # 红色 - ERROR
    YELLOW = "\033[93m"  # 黄色 - WARNING
    RESET = "\033[0m"  # 重置颜色


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

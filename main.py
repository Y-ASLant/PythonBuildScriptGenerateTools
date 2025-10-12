# -*- coding: utf-8 -*-

"""
Python打包脚本生成器CLI程序入口
用于交互式生成Nuitka和PyInstaller编译脚本
"""

import argparse
import sys
from app.builder import NuitkaScriptBuilder


def create_parser():
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        prog="PythonBuildScriptGenerator",
        description="交互式Python打包脚本生成器 - 同时支持Nuitka和PyInstaller\n - 支持rpm、deb包生成 \n - 支持exe包生成\n - 支持pkg包生成",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="PythonBuildScriptGenerator 1.0.0"
    )
    
    parser.add_argument(
        "--check-env",
        action="store_true",
        help="检查系统环境和所需的打包工具"
    )
    
    return parser


def main():
    """主函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    # 如果是环境检查模式
    if args.check_env:
        from app.env_checker import EnvironmentChecker
        checker = EnvironmentChecker()
        checker.check_all()
        
        # 显示建议
        recommendations = checker.get_recommendations()
        if recommendations:
            from app.logger_utils import log_info, log_warning
            log_info("💡 改进建议:")
            for rec in recommendations:
                log_warning(f"  • {rec}")
        return
    
    # 启动构建器
    builder = NuitkaScriptBuilder()
    builder.run()


if __name__ == "__main__":
    main()

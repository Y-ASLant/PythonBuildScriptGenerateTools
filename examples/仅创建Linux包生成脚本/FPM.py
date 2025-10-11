#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Linux包生成脚本
自动生成的独立打包脚本
"""

import sys
import os
from pathlib import Path

# 添加app目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.package_generators import create_linux_packages
from app.logger_utils import log_info, log_success, log_error

def main():
    """主函数"""
    try:
        log_info(" Linux包生成脚本")
        log_info("=" * 60)
        
        # 查找可执行文件
        build_dirs = ["build", "dist"]
        exe_file = None
        
        for build_dir in build_dirs:
            build_path = Path(build_dir)
            if build_path.exists():
                for file_path in build_path.rglob("*"):
                    if file_path.is_file() and file_path.suffix not in ['.spec', '.txt', '.log', '.exe']:
                        if os.access(file_path, os.X_OK) or file_path.suffix == '':
                            exe_file = str(file_path)
                            break
                if exe_file:
                    break
        
        if not exe_file:
            log_error(" 未找到可执行文件")
            log_info(" 请确保在 build/ 或 dist/ 目录中有可执行文件")
            return False
        
        log_info(f" 找到可执行文件: {{exe_file}}")
        
        # 生成Linux包
        success = create_linux_packages(exe_file)
        
        if success:
            log_success(" Linux包生成完成！")
        else:
            log_error(" Linux包生成失败")
            
        return success
        
    except KeyboardInterrupt:
        log_info(" 用户取消操作")
        return False
    except Exception as e:
        log_error(f" 生成Linux包时发生错误: {{e}}")
        return False
    finally:
        input("按下任意键退出...")

if __name__ == "__main__":
    main()

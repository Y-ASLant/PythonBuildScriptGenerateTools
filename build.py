# -*- coding: utf-8 -*-
"""
Nuitka构建脚本
自动生成于 main.py 项目
完全独立，无外部依赖
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime
def log_message(level, message, end='\n'):
    """输出日志信息"""
    colors = {'INFO': '\033[94m', 'SUCCESS': '\033[92m', 'ERROR': '\033[91m', 'WARNING': '\033[93m'}
    color = colors.get(level, '\033[0m')
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{timestamp} | {color}{level:<7}\033[0m | {message}", end=end)

def log_info(message, end='\n'): log_message('INFO', message, end)
def log_success(message, end='\n'): log_message('SUCCESS', message, end)  
def log_error(message, end='\n'): log_message('ERROR', message, end)
def log_warning(message, end='\n'): log_message('WARNING', message, end)


def check_tool_installed(tool_name, import_name=None, silent=False):
    """检查工具是否已安装"""
    if import_name:
        try:
            __import__(import_name)
            if not silent:
                log_success(f"✅ Nuitka已安装")
            return True
        except ImportError:
            if not silent:
                log_error(f"❌ Nuitka未安装！")
                log_info(f"📦 请运行: pip install {tool_name.lower()}")
            return False
    else:
        if shutil.which(tool_name.lower()):
            if not silent:
                log_success(f"✅ Nuitka已安装")
            return True
        else:
            if not silent:
                log_error(f"❌ Nuitka未安装！")
            return False


def find_executable_in_dirs(dirs, exclude_extensions=None):
    """在指定目录中查找可执行文件"""
    if exclude_extensions is None:
        exclude_extensions = ['.spec', '.txt', '.log', '.exe', '.toc', '.pyz', '.pkg', '.so', '.dll', '.dylib']
    
    for build_dir in dirs:
        build_path = Path(build_dir)
        if build_path.exists():
            # 优先查找直接在目录下的可执行文件（单文件模式）
            for file_path in build_path.iterdir():
                if (file_path.is_file() and 
                    file_path.suffix not in exclude_extensions and
                    file_path.name not in ['base_library.zip', 'python312.dll'] and
                    not file_path.name.startswith('_') and
                    (os.access(file_path, os.X_OK) or file_path.suffix == '')):
                    return str(file_path)
            
            # 查找子目录中的可执行文件（目录模式）
            for subdir in build_path.iterdir():
                if subdir.is_dir():
                    for file_path in subdir.iterdir():
                        if (file_path.is_file() and 
                            file_path.suffix not in exclude_extensions and
                            file_path.name not in ['base_library.zip', 'python312.dll'] and
                            not file_path.name.startswith('_') and
                            (os.access(file_path, os.X_OK) or file_path.suffix == '')):
                            return str(file_path)
    
    return None
def check_environment():
    """检查系统环境和构建工具"""
    log_info("🔍 是否进行环境检查？(Y/n): ", end="")
    try:
        user_input = input().strip().lower()
        if user_input == '' or user_input == 'y' or user_input == 'yes':
            log_info("开始基础环境检查...")
            
            # 检查Python版本
            import platform
            python_version = tuple(map(int, platform.python_version().split('.')))
            if python_version >= (3, 8):
                log_success(f"✅ Python {platform.python_version()} (支持)")
            else:
                log_warning(f"⚠️  Python {platform.python_version()} (建议使用3.8+)")
            
            # 检查包管理器
            modern_managers = ["uv", "poetry", "pdm", "pipenv"]
            found_manager = False
            for manager in modern_managers:
                if shutil.which(manager):
                    log_success(f"✅ {manager.title()} 包管理器已安装")
                    found_manager = True
                    break
            
            if not found_manager and shutil.which("pip"):
                log_success("✅ pip 已安装")
            elif not found_manager:
                log_warning("⚠️  未找到包管理器 (pip/uv/poetry等)")
            
            log_success("✅ 基础环境检查完成")
            return True
        else:
            log_info("跳过环境检查")
            return True
    except KeyboardInterrupt:
        log_info("\n用户中断操作")
        return False
    except Exception as e:
        log_error(f"环境检查过程中发生错误: {e}")
        return True
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
            log_success(f"✅ {compiler} 编译器已安装")
            compiler_found = True
            break
    
    if not compiler_found:
        log_warning("⚠️  未找到C编译器 (clang/gcc)")
        log_info("💡 Linux: sudo apt install clang 或 sudo apt install gcc")
        log_info("💡 macOS: xcode-select --install")
    
    # 检查Linux包生成工具（如果需要）
    if "False" == "True":
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
        package_types = ['deb']
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
    
    return True
def copy_additional_files():
    """复制额外的文件和目录到构建输出目录"""
    build_output_dir = Path("build")
    
    if not build_output_dir.exists():
        log_warning(f"⚠️  构建输出目录不存在: {build_output_dir}")
        return
    
    log_info("📁 复制额外文件和目录...")
    
    # 需要复制的目录列表
    copy_dirs = [

    ]
    
    for dir_name in copy_dirs:
        src_dir = Path(dir_name)
        if src_dir.exists() and src_dir.is_dir():
            dest_dir = build_output_dir / dir_name
            
            try:
                if dest_dir.exists():
                    shutil.rmtree(dest_dir)
                
                shutil.copytree(src_dir, dest_dir)
                log_success(f"✅ 已复制目录: {src_dir} -> {dest_dir}")
            except Exception as e:
                log_error(f"❌ 复制目录 {src_dir} 失败: {e}")
        else:
            log_warning(f"⚠️  目录不存在，跳过: {src_dir}")


def main():
    """主构建函数"""
    # 环境检查
    if not check_environment():
        sys.exit(1)
    
    # 检查Nuitka依赖
    log_info("🔍 检查构建工具依赖...")
    if not check_nuitka():
        sys.exit(1)
    
    # 检查构建依赖工具
    if not check_build_dependencies():
        sys.exit(1)
    
    # 记录开始时间
    start_time = datetime.now()
    
    log_info("=" * 60)
    log_info("🚀 Nuitka 构建脚本")
    log_info("=" * 60)
    log_info("入口文件: main.py")
    log_info("输出目录: build")
    log_info("编译器: mingw64")
    log_info("显示控制台: 是")
    log_info("应用名称: PythonBuildScriptGenerate")
    log_info("=" * 60)
    
    # Nuitka编译参数
    args = [
        "nuitka",    "--standalone",    "--onefile",    "--assume-yes-for-downloads",    "--remove-output",    "--mingw64",    "--quiet",    "--windows-company-name=ASLant",    "--windows-file-version=1.0.0",    "--output-dir=build",    "--output-filename=PythonBuildScriptGenerate",    "--jobs=12",    "--windows-icon-from-ico=app.ico",    "--linux-icon=app.ico",    "--nofollow-import-to=nuitka",    "--nofollow-import-to=pyinstaller",    "--nofollow-import-to=pyinstaller-hooks-contrib",    "main.py",
    ]
    
    log_info("开始Nuitka编译...")
    log_info("执行命令: " + " ".join(args))
    
    # 执行Nuitka编译
    result = os.system(" ".join(args))
    
    if result != 0:
        log_error(f"❌ 编译失败！错误代码: {result}")
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
    log_info("输出位置: build")
    log_info(f"⏱️  总耗时: {minutes}分{seconds}秒")
    
    # 清理临时构建目录和生成的.spec文件
    temp_dir = Path("build_temp")
    if temp_dir.exists():
        try:
            shutil.rmtree(temp_dir)
            log_success("✅ 已清理临时构建目录")
        except Exception as e:
            log_warning(f"⚠️  清理临时目录失败: {e}")
    
    # 清理PyInstaller生成的.spec文件
    spec_file = Path("PythonBuildScriptGenerate.spec")
    if spec_file.exists():
        try:
            spec_file.unlink()
            log_success("✅ 已清理.spec文件")
        except Exception as e:
            log_warning(f"⚠️  清理.spec文件失败: {e}")
    
    # Linux包生成（如果启用）
        # Linux包生成已禁用


if __name__ == "__main__":
    main()
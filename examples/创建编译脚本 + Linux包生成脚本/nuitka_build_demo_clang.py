# -*- coding: utf-8 -*-
"""
Nuitka构建脚本
自动生成于 main.py 项目
"""

import os
import sys
from pathlib import Path
from shutil import copy, copytree, rmtree
from datetime import datetime


def log_message(level, message):
    """输出日志信息"""
    colors = {'INFO': '\033[94m', 'SUCCESS': '\033[92m', 'ERROR': '\033[91m', 'WARNING': '\033[93m'}
    color = colors.get(level, '\033[0m')
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{timestamp} | {color}{level:<7}\033[0m | {message}")

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
    log_info("入口文件: main.py")
    log_info("输出目录: build")
    log_info("编译器: clang")
    log_info("显示控制台: 是")
    log_info("应用名称: PythonBuildScriptGenerate")
    log_info("=" * 60)
    
    # Nuitka编译参数
    args = [
        "nuitka",    "--standalone",    "--onefile",    "--assume-yes-for-downloads",    "--remove-output",    "--clang",    "--quiet",    "--output-dir=build",    "--output-filename=PythonBuildScriptGenerate",    "--jobs=8",    "--windows-icon-from-ico=app.ico",    "--linux-icon=app.ico",    "main.py",
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
    
    # Linux包生成（如果启用）
    
    # 生成Linux安装包
    generate_linux_packages("nfpm", ["deb", "rpm"])


def generate_linux_packages(tool, package_types):
    """生成Linux安装包"""
    import subprocess
    from pathlib import Path
    
    log_info("📦 开始生成Linux安装包...")
    
    # 查找可执行文件
    dist_dir = Path("dist")
    exe_files = []
    
    # 递归查找可执行文件
    for file_path in dist_dir.rglob("*"):
        if file_path.is_file() and file_path.suffix not in ['.spec', '.txt', '.log', '.exe']:
            if os.access(file_path, os.X_OK) or file_path.suffix == '':
                exe_files.append(file_path)
    
    if not exe_files:
        log_error("❌ 未找到可执行文件，跳过Linux包生成")
        return
    
    exe_file = exe_files[0]
    log_info(f"📁 使用可执行文件: {exe_file}")
    
    # 应用信息
    app_name = "PythonBuildScriptGenerate".lower().replace('_', '-')
    version = "1.0.0"
    description = "PythonBuildScriptGenerate - 自动生成的Linux安装包"
    maintainer = "Auto Generated <auto@example.com>"
    
    # 检查选择的工具是否可用
    if tool == "nfpm":
        if check_nfpm_installation():
            generate_nfpm_packages(exe_file, app_name, version, description, maintainer, package_types)
        else:
            log_warning("⚠️  NFPM不可用，尝试使用FPM...")
            if check_fpm_installation():
                generate_fpm_packages(exe_file, app_name, version, description, maintainer, package_types)
            else:
                log_error("❌ 没有可用的打包工具，跳过Linux包生成")
    else:
        if check_fpm_installation():
            generate_fpm_packages(exe_file, app_name, version, description, maintainer, package_types)
        else:
            log_warning("⚠️  FPM不可用，尝试使用NFPM...")
            if check_nfpm_installation():
                generate_nfpm_packages(exe_file, app_name, version, description, maintainer, package_types)
            else:
                log_error("❌ 没有可用的打包工具，跳过Linux包生成")


def check_nfpm_installation():
    """检查NFPM是否已安装"""
    import subprocess
    try:
        result = subprocess.run(["nfpm", "version"], capture_output=True, text=True, check=True)
        log_success("✅ NFPM已安装")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        log_error("❌ NFPM未安装或不可用！")
        log_info("💡 安装方法:")
        log_info("   方法1(多平台支持): go install github.com/goreleaser/nfpm/v2/cmd/nfpm@latest")
        log_info("   方法2(仅Windows): choco install nfpm (Windows)")
        log_info("   方法3(多平台支持): 下载二进制文件 https://github.com/goreleaser/nfpm/releases，手动安装")
        return False


def check_fpm_installation():
    """检查FPM是否已安装"""
    import subprocess
    try:
        result = subprocess.run(["fpm", "--version"], capture_output=True, text=True, check=True)
        log_success("✅ FPM已安装")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        log_error("❌ FPM未安装或不可用！")
        log_info("💡 安装方法:")
        log_info("   Ubuntu/Debian: sudo apt-get install ruby ruby-dev rubygems build-essential && sudo gem install --no-document fpm")
        log_info("   CentOS/RHEL: sudo yum install ruby ruby-devel rubygems rpm-build && sudo gem install --no-document fpm")
        return False


def generate_nfpm_packages(exe_file, app_name, version, description, maintainer, package_types):
    """使用NFPM生成包"""
    import subprocess
    from pathlib import Path
    
    # 创建NFPM配置文件内容
    config_content = f"""name: {app_name}
arch: amd64
platform: linux
version: {version}
section: utils
priority: optional
maintainer: {maintainer}
description: {description}
vendor: {maintainer.split('<')[0].strip() if '<' in maintainer else maintainer}
homepage: https://example.com
license: MIT

contents:
  - src: {str(exe_file).replace(chr(92), '/')}
    dst: /usr/local/bin/{app_name}
    file_info:
      mode: 0755

overrides:
  deb:
    depends:
      - libc6
  rpm:
    depends:
      - glibc
"""
    
    config_file = "nfpm.yaml"
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    log_info(f"📝 NFPM配置文件已生成: {config_file}")
    
    # 生成包
    for package_type in package_types:
        try:
            cmd = ["nfpm", "package", "--packager", package_type, "--config", config_file]
            log_info(f"🔧 生成{package_type.upper()}包...")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                log_success(f"✅ {package_type.upper()}包生成成功")
                package_files = list(Path(".").glob(f"{app_name}*.{package_type}"))
                for package_file in package_files:
                    log_success(f"📦 生成的包: {package_file}")
            else:
                log_error(f"❌ {package_type.upper()}包生成失败: {result.stderr}")
        except Exception as e:
            log_error(f"❌ 生成{package_type.upper()}包时发生错误: {e}")
    
    # 清理配置文件
    try:
        Path(config_file).unlink()
    except:
        pass


def generate_fpm_packages(exe_file, app_name, version, description, maintainer, package_types):
    """使用FPM生成包"""
    import subprocess
    from pathlib import Path
    
    for package_type in package_types:
        try:
            exe_path = str(exe_file).replace(chr(92), '/')
            cmd = [
                "fpm", "-s", "dir", "-t", package_type, "-n", app_name, "-v", version,
                "--description", description, "--maintainer", maintainer,
                "--license", "MIT", "--force", f"{exe_path}=/usr/local/bin/{app_name}"
            ]
            
            if package_type == "deb":
                cmd.extend(["--architecture", "amd64"])
            elif package_type == "rpm":
                cmd.extend(["--architecture", "x86_64"])
            
            log_info(f"🔧 生成{package_type.upper()}包...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                log_success(f"✅ {package_type.upper()}包生成成功")
                if package_type == "deb":
                    package_files = list(Path(".").glob(f"{app_name}*.deb"))
                elif package_type == "rpm":
                    package_files = list(Path(".").glob(f"{app_name}*.rpm"))
                
                for package_file in package_files:
                    log_success(f"📦 生成的包: {package_file}")
            else:
                log_error(f"❌ {package_type.upper()}包生成失败: {result.stderr}")
        except Exception as e:
            log_error(f"❌ 生成{package_type.upper()}包时发生错误: {e}")


def copy_additional_files():
    """复制额外的文件和目录到构建输出目录"""
    from distutils.sysconfig import get_python_lib
    
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
                    rmtree(dest_dir)
                
                copytree(src_dir, dest_dir)
                log_success(f"✅ 已复制目录: {src_dir} -> {dest_dir}")
            except Exception as e:
                log_error(f"❌ 复制目录 {src_dir} 失败: {e}")
        else:
            log_warning(f"⚠️  目录不存在，跳过: {src_dir}")
    
    # 复制site-packages（如果需要）
    copied_site_packages = []  # 在这里添加需要复制的site-packages
    
    if copied_site_packages:
        site_packages = Path(get_python_lib())
        log_info("📦 复制site-packages...")
        
        for pkg_name in copied_site_packages:
            src = site_packages / pkg_name
            dest = build_output_dir / src.name
            
            log_info(f"复制site-packages {src} 到 {dest}")
            
            try:
                if src.is_file():
                    copy(src, dest)
                else:
                    copytree(src, dest)
                log_success(f"✅ 已复制: {src}")
            except (FileNotFoundError, PermissionError, OSError) as e:
                log_error(f"❌ 复制 {src} 失败: {e}")
    
    # 复制标准库文件（如果需要）
    copied_standard_packages = []  # 在这里添加需要复制的标准库文件
    
    if copied_standard_packages:
        site_packages = Path(get_python_lib())
        log_info("📚 复制标准库文件...")
        
        for file_name in copied_standard_packages:
            src = site_packages.parent / file_name
            dest = build_output_dir / src.name
            
            log_info(f"复制标准库 {src} 到 {dest}")
            
            try:
                if src.is_file():
                    copy(src, dest)
                else:
                    copytree(src, dest)
                log_success(f"✅ 已复制: {src}")
            except (FileNotFoundError, PermissionError, OSError) as e:
                log_error(f"❌ 复制 {src} 失败: {e}")


if __name__ == "__main__":
    main()

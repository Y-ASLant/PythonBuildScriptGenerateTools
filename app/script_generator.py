# -*- coding: utf-8 -*-
"""
脚本生成模块 - 处理Nuitka和PyInstaller参数和脚本生成
"""

import sys
from pathlib import Path
from typing import List
from .template import BUILD_SCRIPT_TEMPLATE, PYINSTALLER_BUILD_SCRIPT_TEMPLATE
from .version_info_template import VERSION_INFO_TEMPLATE


class ScriptGenerator:
    """脚本生成器 - 负责生成Nuitka和PyInstaller参数和Python构建脚本"""

    def generate_nuitka_args(self, config) -> List[str]:
        """生成Nuitka编译参数列表"""
        if not config.entry_file:
            raise ValueError("入口文件未设置")

        args = ["nuitka"]

        # 基本选项
        if config.standalone:
            args.append("--standalone")

        # 单文件模式
        if config.onefile:
            args.append("--onefile")

        args.append("--assume-yes-for-downloads")

        # 移除构建文件
        if config.remove_output:
            args.append("--remove-output")

        # 编译器选择（仅在Windows上应用Windows特定编译器）
        if sys.platform.startswith("win"):
            if config.compiler == "mingw64":
                args.append("--mingw64")
            elif config.compiler == "msvc":
                args.append("--msvc=latest")
            elif config.compiler == "clang":
                args.append("--clang")
        else:
            # 在非Windows系统上，只有clang是通用的
            if config.compiler == "clang":
                args.append("--clang")

        # 进度显示和静默模式
        if config.quiet_mode:
            args.append("--quiet")
        else:
            # 进度条控制
            if config.show_progressbar:
                args.append("--show-progress")
            else:
                args.append("--no-progressbar")
            args.append("--show-memory")

        # 控制台窗口
        if not config.show_console:
            args.append("--windows-disable-console")

        # Windows特定选项
        if sys.platform.startswith("win"):
            if config.company_name:
                args.append(f"--windows-company-name={config.company_name}")
            if config.file_version:
                args.append(f"--windows-file-version={config.file_version}")
            if config.uac_admin:
                args.append("--windows-uac-admin")

        # 输出设置
        if config.output_dir:
            args.append(f"--output-dir={config.output_dir}")
        if config.app_name:
            args.append(f"--output-filename={config.app_name}")

        # 编译线程数
        args.append(f"--jobs={config.jobs}")

        # 图标文件
        if config.icon_file:
            args.append(f"--windows-icon-from-ico={config.icon_file}")
            args.append(f"--linux-icon={config.icon_file}")

        # 插件
        for plugin in config.enable_plugins:
            args.append(f"--enable-plugin={plugin}")

        # 排除包导入
        for package in config.exclude_packages:
            args.append(f"--nofollow-import-to={package}")

        # 入口文件（必须是最后一个参数）
        entry_relative = Path(config.entry_file).relative_to(Path(config.project_dir))
        args.append(str(entry_relative))

        return args

    def generate_pyinstaller_args(self, config) -> List[str]:
        """生成PyInstaller编译参数列表"""
        if not config.entry_file:
            raise ValueError("入口文件未设置")

        args = ["pyinstaller"]

        # 基本选项
        if config.onefile:
            args.append("--onefile")
        else:
            args.append("--onedir")

        # 控制台窗口
        if not config.show_console:
            args.append("--windowed")
        else:
            args.append("--console")

        # 输出目录和工作目录
        if config.output_dir:
            args.append("--distpath=dist")
            args.append(f"--workpath={config.output_dir}")

        # 应用名称
        if config.app_name:
            args.append(f"--name={config.app_name}")

        # 图标文件
        if config.icon_file:
            args.append(f"--icon={config.icon_file}")

        # 隐藏导入
        for hidden_import in config.hidden_imports:
            args.append(f"--hidden-import={hidden_import}")

        # 收集所有子模块
        for collect_pkg in config.collect_all:
            args.append(f"--collect-all={collect_pkg}")

        # 添加数据文件
        for data_path in config.add_data:
            args.append(f"--add-data={data_path}")

        # 排除包
        for package in config.exclude_packages:
            args.append(f"--exclude-module={package}")

        # UPX压缩
        if config.upx_dir:
            if config.upx_dir == "auto":
                args.append("--upx-dir=")
            else:
                args.append(f"--upx-dir={config.upx_dir}")

        # 调试模式
        if config.debug:
            args.append("--debug=all")

        # 清理临时文件
        if config.clean:
            args.append("--clean")

        # 静默模式
        if config.quiet_mode:
            args.append("--log-level=WARN")

        # 入口文件（必须是最后一个参数）
        entry_relative = Path(config.entry_file).relative_to(Path(config.project_dir))
        args.append(str(entry_relative))

        return args

    def generate_build_args(self, config) -> List[str]:
        """根据构建工具生成相应的参数"""
        if config.build_tool == "nuitka":
            return self.generate_nuitka_args(config)
        elif config.build_tool == "pyinstaller":
            return self.generate_pyinstaller_args(config)
        else:
            raise ValueError(f"不支持的构建工具: {config.build_tool}")

    def generate_python_script(self, args: List[str], config) -> str:
        """生成Python构建脚本"""
        # 格式化参数列表
        args_list = [f'    "{arg}",' for arg in args]
        args_str = "".join(args_list)

        # 格式化复制目录列表
        copy_dirs_str = ""
        if config.copy_dirs:
            dirs_list = [f'    "{d}",' for d in config.copy_dirs]
            copy_dirs_str = "".join(dirs_list)

        # 生成Linux包生成代码
        linux_package_code = self._generate_linux_package_code(config)

        entry_name = Path(config.entry_file).name

        # 根据构建工具选择模板
        if config.build_tool == "nuitka":
            template = BUILD_SCRIPT_TEMPLATE
            script_content = template.format(
                entry_name=entry_name,
                output_dir=config.output_dir,
                compiler=config.compiler,
                console_display="是" if config.show_console else "否",
                app_name=config.app_name,
                args_str=args_str,
                copy_dirs_str=copy_dirs_str,
                linux_package_code=linux_package_code,
            )
        elif config.build_tool == "pyinstaller":
            template = PYINSTALLER_BUILD_SCRIPT_TEMPLATE
            script_content = template.format(
                entry_name=entry_name,
                output_dir=config.output_dir,
                onefile="是" if config.onefile else "否",
                console_display="是" if config.show_console else "否",
                app_name=config.app_name,
                company_name=config.company_name or "Unknown Company",
                file_version=config.file_version,
                args_str=args_str,
                copy_dirs_str=copy_dirs_str,
                linux_package_code=linux_package_code,
            )
        else:
            raise ValueError(f"不支持的构建工具: {config.build_tool}")

        return script_content

    def _generate_linux_package_code(self, config) -> str:
        """生成Linux包生成代码"""
        if not config.generate_linux_packages:
            return ""
        
        # 生成包类型列表
        package_types_str = ", ".join([f'"{pkg}"' for pkg in config.linux_package_types])
        
        # 使用字符串拼接而不是f-string来避免嵌套问题
        code = f'''
    # 生成Linux安装包
    generate_linux_packages("{config.linux_packaging_tool}", [{package_types_str}])


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
    log_info(f"📁 使用可执行文件: {{exe_file}}")
    
    # 应用信息
    app_name = "{config.app_name}".lower().replace('_', '-')
    version = "1.0.0"
    description = "{config.app_name} - 自动生成的Linux安装包"
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
    config_content = f"""name: {{app_name}}
arch: amd64
platform: linux
version: {{version}}
section: utils
priority: optional
maintainer: {{maintainer}}
description: {{description}}
vendor: {{maintainer.split('<')[0].strip() if '<' in maintainer else maintainer}}
homepage: https://example.com
license: MIT

contents:
  - src: {{str(exe_file).replace(chr(92), '/')}}
    dst: /usr/local/bin/{{app_name}}
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
    
    log_info(f"📝 NFPM配置文件已生成: {{config_file}}")
    
    # 生成包
    for package_type in package_types:
        try:
            cmd = ["nfpm", "package", "--packager", package_type, "--config", config_file]
            log_info(f"🔧 生成{{package_type.upper()}}包...")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                log_success(f"✅ {{package_type.upper()}}包生成成功")
                package_files = list(Path(".").glob(f"{{app_name}}*.{{package_type}}"))
                for package_file in package_files:
                    log_success(f"📦 生成的包: {{package_file}}")
            else:
                log_error(f"❌ {{package_type.upper()}}包生成失败: {{result.stderr}}")
        except Exception as e:
            log_error(f"❌ 生成{{package_type.upper()}}包时发生错误: {{e}}")
    
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
                "--license", "MIT", "--force", f"{{exe_path}}=/usr/local/bin/{{app_name}}"
            ]
            
            if package_type == "deb":
                cmd.extend(["--architecture", "amd64"])
            elif package_type == "rpm":
                cmd.extend(["--architecture", "x86_64"])
            
            log_info(f"🔧 生成{{package_type.upper()}}包...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                log_success(f"✅ {{package_type.upper()}}包生成成功")
                if package_type == "deb":
                    package_files = list(Path(".").glob(f"{{app_name}}*.deb"))
                elif package_type == "rpm":
                    package_files = list(Path(".").glob(f"{{app_name}}*.rpm"))
                
                for package_file in package_files:
                    log_success(f"📦 生成的包: {{package_file}}")
            else:
                log_error(f"❌ {{package_type.upper()}}包生成失败: {{result.stderr}}")
        except Exception as e:
            log_error(f"❌ 生成{{package_type.upper()}}包时发生错误: {{e}}")'''
        
        return code

    def generate_version_info_file(self, config) -> str:
        """生成PyInstaller版本信息文件内容"""
        # 解析版本号为元组格式
        version_parts = config.file_version.split(".")
        while len(version_parts) < 4:
            version_parts.append("0")
        version_tuple = ", ".join(version_parts[:4])

        # 生成版本信息文件内容
        version_content = VERSION_INFO_TEMPLATE.format(
            file_version_tuple=version_tuple,
            product_version_tuple=version_tuple,
            company_name=config.company_name or "Unknown Company",
            file_description=f"{config.app_name} Application"
            if config.app_name
            else "Python Application",
            file_version=config.file_version,
            internal_name=config.app_name or "app",
            copyright=f"Copyright (C) {config.company_name}"
            if config.company_name
            else "Copyright (C) Unknown",
            original_filename=f"{config.app_name}.exe"
            if config.app_name
            else "app.exe",
            product_name=config.app_name or "Python Application",
            product_version=config.file_version,
        )

        return version_content

    def save_version_info_file(self, config) -> bool:
        """保存PyInstaller版本信息文件"""
        if config.build_tool != "pyinstaller" or not sys.platform.startswith("win"):
            return True

        if not (config.company_name or config.file_version):
            return True

        try:
            from loguru import logger

            version_content = self.generate_version_info_file(config)
            version_filename = f"{config.app_name or 'app'}_version.txt"
            version_path = Path(config.project_dir) / version_filename

            with open(version_path, "w", encoding="utf-8") as f:
                f.write(version_content)

            logger.success(f"✅ 版本信息文件已保存到: {version_path.absolute()}")
            return True
        except (OSError, IOError) as e:
            logger.error(f"❌ 保存版本信息文件失败: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ 生成版本信息文件时发生未知错误: {e}")
            return False

    def save_script(self, script_content: str, config, filename: str = None) -> bool:
        """保存脚本到文件"""
        try:
            from loguru import logger

            # 使用传入的文件名或默认的脚本文件名
            script_filename = filename or config.script_filename
            script_path = Path(config.project_dir) / script_filename
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(script_content)
            logger.success(f"✅ 脚本已保存到: {script_path.absolute()}")
            return True
        except (OSError, IOError, PermissionError) as e:
            logger.error(f"❌ 保存脚本失败: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ 保存脚本时发生未知错误: {e}")
            return False

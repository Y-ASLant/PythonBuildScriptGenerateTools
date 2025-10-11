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

        # 输出目录
        if config.output_dir:
            args.append(f"--distpath={config.output_dir}")

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
            )
        else:
            raise ValueError(f"不支持的构建工具: {config.build_tool}")

        return script_content

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

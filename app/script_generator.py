# -*- coding: utf-8 -*-
"""
脚本生成模块 - 处理Nuitka参数和脚本生成
"""

import sys
from pathlib import Path
from typing import List
from .template import BUILD_SCRIPT_TEMPLATE


class ScriptGenerator:
    """脚本生成器 - 负责生成Nuitka参数和Python构建脚本"""

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

        # 使用模板生成脚本
        script_content = BUILD_SCRIPT_TEMPLATE.format(
            entry_name=entry_name,
            output_dir=config.output_dir,
            compiler=config.compiler,
            console_display="是" if config.show_console else "否",
            app_name=config.app_name,
            args_str=args_str,
            copy_dirs_str=copy_dirs_str,
        )

        return script_content

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
        except Exception as e:
            logger.error(f"❌ 保存脚本失败: {e}")
            return False

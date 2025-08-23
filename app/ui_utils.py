# -*- coding: utf-8 -*-
"""
UI工具模块 - 处理横幅显示和摘要显示
"""

import sys
import shutil
from loguru import logger


class UIUtils:
    """UI工具类 - 负责界面显示相关功能"""

    @staticmethod
    def display_banner():
        """显示程序横幅"""
        terminal_width = shutil.get_terminal_size().columns
        title = "Nuitka打包脚本生成器@ASLant"

        # 计算实际显示宽度（中文字符占2个字符宽度）
        display_width = 0
        for char in title:
            if ord(char) > 127:
                display_width += 2
            else:
                display_width += 1

        # 计算左侧填充
        padding = (terminal_width - display_width) // 2
        centered_title = " " * padding + title

        print("=" * terminal_width)
        print()
        print(centered_title)
        print()
        print("=" * terminal_width)

    @staticmethod
    def display_summary(config):
        """显示配置摘要"""
        logger.info("" + "=" * 60)
        logger.info("📋 配置摘要")
        logger.info("=" * 60)
        logger.info(f"项目目录: {config.project_dir}")
        logger.info(f"入口文件: {config.entry_file}")
        logger.info(f"图标文件: {config.icon_file or '未设置'}")
        logger.info(f"编译器: {config.compiler}")
        logger.info(f"显示控制台: {'是' if config.show_console else '否'}")
        logger.info(f"应用名称: {config.app_name}")
        logger.info(f"输出目录: {config.output_dir}")
        logger.info(f"独立打包: {'是' if config.standalone else '否'}")
        logger.info(f"单文件模式: {'是' if config.onefile else '否'}")
        if sys.platform.startswith("win"):
            logger.info(f"管理员权限: {'是' if config.uac_admin else '否'}")
        logger.info(
            f"启用插件: {', '.join(config.enable_plugins) if config.enable_plugins else '无'}"
        )
        logger.info(f"公司名称: {config.company_name or '未设置'}")
        logger.info(f"文件版本: {config.file_version}")
        logger.info(f"编译线程: {config.jobs}")
        logger.info(f"静默模式: {'是' if config.quiet_mode else '否'}")
        logger.info(f"显示进度条: {'是' if config.show_progressbar else '否'}")
        logger.info(f"移除构建文件: {'是' if config.remove_output else '否'}")
        logger.info(
            f"复制目录: {', '.join(config.copy_dirs) if config.copy_dirs else '无'}"
        )
        logger.info(f"脚本文件名: {config.script_filename}")
        logger.info("=" * 60)

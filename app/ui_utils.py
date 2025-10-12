# -*- coding: utf-8 -*-
"""
UI工具模块 - 处理横幅显示和摘要显示
"""

import sys
import shutil
from loguru import logger
from .tool_analyzer import ToolRequirementAnalyzer


class UIUtils:
    """UI工具类 - 负责界面显示相关功能"""

    @staticmethod
    def display_banner():
        """显示程序横幅"""
        terminal_width = shutil.get_terminal_size().columns
        title = "交互式 Python打包脚本生成器@ASLant"
        help_tip = "💡 在任何输入提示处输入 ? 可查看详细帮助"

        # 计算标题实际显示宽度（中文字符占2个字符宽度）
        title_display_width = 0
        for char in title:
            if ord(char) > 127:
                title_display_width += 2
            else:
                title_display_width += 1

        # 计算帮助提示实际显示宽度
        help_display_width = 0
        for char in help_tip:
            if ord(char) > 127:
                help_display_width += 2
            else:
                help_display_width += 1

        # 计算左侧填充
        title_padding = (terminal_width - title_display_width) // 2
        help_padding = (terminal_width - help_display_width) // 2
        
        centered_title = " " * title_padding + title
        centered_help = " " * help_padding + help_tip

        print("=" * terminal_width)
        print()
        print(centered_title)
        print()
        print(centered_help)
        print()
        print("=" * terminal_width)

    @staticmethod
    def display_summary(config):
        """显示配置摘要"""
        logger.info("" + "=" * 60)
        logger.info("📋 配置摘要")
        logger.info("=" * 60)
        logger.info(f"构建工具: {config.build_tool.upper()}")
        logger.info(f"项目目录: {config.project_dir}")
        logger.info(f"入口文件: {config.entry_file}")
        logger.info(f"图标文件: {config.icon_file or '未设置'}")
        
        # 仅Nuitka显示编译器信息
        if config.build_tool == "nuitka":
            logger.info(f"编译器: {config.compiler}")
        
        logger.info(f"显示控制台: {'是' if config.show_console else '否'}")
        logger.info(f"应用名称: {config.app_name}")
        logger.info(f"输出目录: {config.output_dir}")
        
        if config.build_tool == "nuitka":
            logger.info(f"独立打包: {'是' if config.standalone else '否'}")
        
        logger.info(f"单文件模式: {'是' if config.onefile else '否'}")
        
        if sys.platform.startswith("win"):
            logger.info(f"管理员权限: {'是' if config.uac_admin else '否'}")
        
        # 显示工具特定配置
        if config.build_tool == "nuitka":
            logger.info(
                f"启用插件: {', '.join(config.enable_plugins) if config.enable_plugins else '无'}"
            )
        elif config.build_tool == "pyinstaller":
            logger.info(
                f"隐藏导入: {', '.join(config.hidden_imports) if config.hidden_imports else '无'}"
            )
            logger.info(
                f"收集子模块: {', '.join(config.collect_all) if config.collect_all else '无'}"
            )
            logger.info(
                f"数据文件: {', '.join(config.add_data) if config.add_data else '无'}"
            )
            if config.upx_dir:
                logger.info(f"UPX压缩: {'自动检测' if config.upx_dir == 'auto' else config.upx_dir}")
            logger.info(f"调试模式: {'是' if config.debug else '否'}")
            logger.info(f"清理临时文件: {'是' if config.clean else '否'}")
        
        logger.info(f"公司名称: {config.company_name or '未设置'}")
        logger.info(f"文件版本: {config.file_version}")
        logger.info(f"编译线程: {config.jobs}")
        logger.info(f"静默模式: {'是' if config.quiet_mode else '否'}")
        logger.info(f"显示进度条: {'是' if config.show_progressbar else '否'}")
        
        if config.build_tool == "nuitka":
            logger.info(f"移除构建文件: {'是' if config.remove_output else '否'}")
        
        logger.info(
            f"复制目录: {', '.join(config.copy_dirs) if config.copy_dirs else '无'}"
        )
        logger.info(f"脚本文件名: {config.script_filename}")
        
        # 显示工具需求
        analyzer = ToolRequirementAnalyzer()
        requirements_summary = analyzer.get_requirements_summary(config)
        logger.info(f"工具需求: {requirements_summary}")
        
        logger.info("=" * 60)

# -*- coding: utf-8 -*-
"""
Nuitka脚本构建器核心类
"""

import sys
from loguru import logger
from .config_collector import ConfigCollector
from .script_generator import ScriptGenerator
from .ui_utils import UIUtils

# 配置loguru只显示时间，并启用彩色显示
logger.remove()
logger.add(
    sys.stderr,
    format="{time:HH:mm:ss} | <level>{level: <7}</level> | {message}",
    colorize=True,
    level="DEBUG",
)

# 添加自定义颜色配置，INFO级别显示为蓝色
logger.level("INFO", color="<blue>")


class NuitkaScriptBuilder:
    """Nuitka脚本构建器，作为协调器"""

    def __init__(self):
        self.config_collector = ConfigCollector()
        self.script_generator = ScriptGenerator()
        self.ui_utils = UIUtils()

    def display_banner(self):
        """显示程序横幅"""
        self.ui_utils.display_banner()

    def run(self):
        """运行CLI程序"""
        try:
            self.display_banner()

            # 收集所有配置
            self.config_collector.collect_all_config()

            # 显示配置摘要
            self.ui_utils.display_summary(self.config_collector)

            # 生成参数
            args = self.script_generator.generate_build_args(self.config_collector)
            tool_name = (
                "Nuitka"
                if self.config_collector.build_tool == "nuitka"
                else "PyInstaller"
            )
            logger.info(f"🔧 生成的{tool_name}参数:")
            logger.info(" ".join(args))

            # 生成Python脚本
            python_script = self.script_generator.generate_python_script(
                args, self.config_collector
            )

            # 保存脚本
            logger.info("💾 保存脚本...")

            # PyInstaller不需要额外的版本信息文件

            if self.script_generator.save_script(python_script, self.config_collector):
                logger.success("🎉 脚本生成完成！")
                logger.info(
                    f"运行 python {self.config_collector.script_filename} 开始编译"
                )

            # 暂停等待用户按键
            input("按下任意键退出...")

        except KeyboardInterrupt:
            logger.info("👋 程序已取消")
            sys.exit(0)
        except Exception as e:
            logger.error(f"❌ 发生错误: {e}")
            sys.exit(1)

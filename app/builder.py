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

    def _select_mode(self):
        """选择运行模式"""
        from .input_handlers import InputHandlers

        mode = InputHandlers.get_choice_input(
            "🎯 请选择运行模式",
            {
                "1": "完整模式 - 创建编译脚本 + Linux包生成脚本 (推荐)",
                "2": "编译模式 - 仅创建编译脚本",
                "3": "打包模式 - 仅创建Linux包生成脚本",
            },
            "1",
            help_text="完整模式：一键完成编译和Linux包生成；编译模式：只生成编译脚本；打包模式：只生成Linux包脚本（需要已有可执行文件）",
        )

        mode_map = {"1": "full", "2": "compile", "3": "package"}
        selected_mode = mode_map[mode]

        if selected_mode == "full":
            logger.success("✅ 选择完整模式 - 编译 + Linux包生成")
        elif selected_mode == "compile":
            logger.success("✅ 选择编译模式 - 仅编译脚本")
        else:
            logger.success("✅ 选择打包模式 - 仅Linux包生成")

        return selected_mode

    def _generate_full_script(self):
        """生成完整脚本（编译 + Linux包生成）"""
        # 生成参数
        args = self.script_generator.generate_build_args(self.config_collector)
        tool_name = (
            "Nuitka" if self.config_collector.build_tool == "nuitka" else "PyInstaller"
        )
        logger.info(f"🔧 生成的{tool_name}参数:")
        logger.info(" ".join(args))

        # 生成Python脚本
        python_script = self.script_generator.generate_python_script(
            args, self.config_collector
        )

        # 保存脚本
        logger.info("💾 保存脚本...")
        if self.script_generator.save_script(python_script, self.config_collector):
            logger.success("🎉 完整脚本生成完成！")
            logger.info(
                f"运行 python {self.config_collector.script_filename} 开始编译和打包"
            )

    def _generate_compile_script(self):
        """生成编译脚本（仅编译，不包含Linux包生成）"""
        # 临时禁用Linux包生成
        original_generate_linux_packages = self.config_collector.generate_linux_packages
        self.config_collector.generate_linux_packages = False

        # 生成参数
        args = self.script_generator.generate_build_args(self.config_collector)
        tool_name = (
            "Nuitka" if self.config_collector.build_tool == "nuitka" else "PyInstaller"
        )
        logger.info(f" 生成的{tool_name}参数:")
        logger.info(" ".join(args))

        # 生成Python脚本
        python_script = self.script_generator.generate_python_script(
            args, self.config_collector
        )

        # 恢复原设置
        self.config_collector.generate_linux_packages = original_generate_linux_packages

        # 保存脚本
        logger.info(" 保存脚本...")
        if self.script_generator.save_script(python_script, self.config_collector):
            logger.success(" 编译脚本生成完成！")
            logger.info(f"运行 python {self.config_collector.script_filename} 开始编译")

    def _generate_package_script(self):
        """生成Linux包生成脚本"""
        logger.info("💾 生成Linux包生成脚本...")
        
        # 获取配置参数
        config = self.config_collector
        
        # 创建使用预配置参数的Linux包生成脚本
        package_script_content = f'''
# -*- coding: utf-8 -*-
"""
Linux包生成脚本
自动生成的独立打包脚本
使用预配置参数，无需重新输入
"""

import sys
import os
from pathlib import Path

# 添加app目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.package_generators import LinuxPackageGenerator
from app.logger_utils import log_info, log_success, log_error

def main():
    """主函数"""
    try:
        log_info("📦 Linux包生成脚本")
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
            log_error("❌ 未找到可执行文件")
            log_info("📝 请确保在 build/ 或 dist/ 目录中有可执行文件")
            return False
        
        log_info(f"📁 找到可执行文件: {{exe_file}}")
        
        # 使用预配置参数创建生成器
        generator = LinuxPackageGenerator()
        
        # 设置预配置参数
        generator.app_name = "{config.app_name}"
        generator.version = "{config.file_version}"
        generator.description = "{getattr(config, 'description', config.app_name + ' application')}"
        generator.maintainer = "{getattr(config, 'company_name', 'Unknown')} <unknown@example.com>"
        generator.url = "{getattr(config, 'url', '')}"
        generator.license = "MIT"
        generator.executable_path = exe_file
        generator.install_path = "{getattr(config, 'package_install_path', '/usr/local/bin')}"
        generator.packaging_tool = "{config.linux_packaging_tool}"
        generator.package_types = {config.linux_package_types}
        
        # 设置扩展参数
        generator.architecture = "{getattr(config, 'package_architecture', 'amd64')}"
        generator.depends = {getattr(config, 'package_depends', [])}
        generator.desktop_file = "{getattr(config, 'package_desktop_name', '')}"
        generator.create_service = {getattr(config, 'package_create_service', False)}
        generator.service_name = "{getattr(config, 'package_service_name', '')}"
        generator.output_dir = "{getattr(config, 'package_output_dir', 'output_pkg')}"
        
        log_info("🚀 使用预配置参数开始打包...")
        log_info(f"📝 应用名称: {{generator.app_name}}")
        log_info(f"💻 目标架构: {{generator.architecture}}")
        log_info(f"📁 安装路径: {{generator.install_path}}")
        log_info(f"📦 包类型: {{', '.join(generator.package_types)}}")
        log_info(f"📂 输出目录: {{generator.output_dir}}")
        
        # 生成包
        success = generator.generate_packages()
        
        if success:
            log_success("🎉 Linux包生成完成！")
            log_info(f"📦 包文件已保存在: {{generator.output_dir}}/")
        else:
            log_error("❌ Linux包生成失败")
            
        return success
        
    except KeyboardInterrupt:
        log_info("👋 用户取消操作")
        return False
    except Exception as e:
        log_error(f"❌ 生成Linux包时发生错误: {{e}}")
        return False
    finally:
        input("按下任意键退出...")

if __name__ == "__main__":
    main()
'''

        # 保存脚本
        script_filename = "create_packages.py"
        try:
            with open(script_filename, "w", encoding="utf-8") as f:
                f.write(package_script_content)
            logger.success(" Linux包生成脚本已保存！")
            logger.info(f"运行 python {script_filename} 开始生成Linux包")
        except Exception as e:
            logger.error(f" 保存脚本失败: {e}")

    def run(self):
        """运行CLI程序"""
        try:
            self.display_banner()

            # 选择运行模式
            mode = self._select_mode()

            # 收集所有配置
            self.config_collector.collect_all_config(mode)

            # 显示配置摘要
            self.ui_utils.display_summary(self.config_collector)

            if mode == "package":
                # 打包模式：生成独立的Linux包生成脚本
                self._generate_package_script()
            elif mode == "compile":
                # 编译模式：生成编译脚本（不包含Linux包生成）
                self._generate_compile_script()
            else:
                # 完整模式：生成包含Linux包生成的编译脚本
                self._generate_full_script()

            # 暂停等待用户按键
            input("按下任意键退出...")

        except KeyboardInterrupt:
            logger.info("👋 程序已取消")
            sys.exit(0)
        except Exception as e:
            logger.error(f"❌ 发生错误: {e}")
            sys.exit(1)

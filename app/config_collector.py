# -*- coding: utf-8 -*-
"""
配置收集模块 - 处理所有用户输入收集
"""

import sys
from pathlib import Path
from typing import Optional
from loguru import logger
from .interactive_menu import InteractiveMenu
from .plugins import get_plugin_list
from .config_validators import ConfigValidators
from .input_handlers import InputHandlers


class ConfigCollector:
    """配置收集器 - 负责收集所有用户配置"""

    def __init__(self):
        self.project_dir: str = "."
        self.entry_file: Optional[str] = None
        self.icon_file: Optional[str] = None
        self.compiler: str = "mingw64"
        self.show_console: bool = False
        self.output_dir: str = "dist"
        self.app_name: Optional[str] = None
        self.enable_plugins: list = []
        self.exclude_packages: list = []
        self.copy_dirs: list = []
        self.company_name: str = ""
        self.file_version: str = "1.0.0"
        self.jobs: int = 4
        self.standalone: bool = True
        self.onefile: bool = False
        self.uac_admin: bool = False
        self.script_filename: str = "build.py"
        self.quiet_mode: bool = False
        self.show_progressbar: bool = True
        self.remove_output: bool = False

    def get_project_dir(self):
        """获取项目根目录"""
        while True:
            project_dir = InputHandlers.get_text_input("📂 请输入项目根目录", ".")

            is_valid, result = ConfigValidators.validate_project_dir(project_dir)
            if is_valid:
                self.project_dir = result
                logger.success(f"✅ 项目目录: {self.project_dir}")
                break
            else:
                logger.error(f"❌ {result}")

    def get_entry_file(self):
        """获取入口文件"""
        while True:
            entry = InputHandlers.get_text_input(
                "📁 请输入Python入口文件路径 (相对于项目目录)", required=True
            )

            is_valid, result = ConfigValidators.validate_entry_file(
                entry, self.project_dir
            )
            if is_valid:
                self.entry_file = result
                logger.success(f"✅ 入口文件: {self.entry_file}")
                break
            else:
                logger.error(f"❌ {result}")

    def get_icon_file(self):
        """获取图标文件"""
        icon = InputHandlers.get_text_input(
            "🎨 请输入图标文件路径 (仅支持.ico格式，可选，直接回车跳过)"
        )

        is_valid, result = ConfigValidators.validate_icon_file(icon, self.project_dir)
        if is_valid:
            self.icon_file = result
            if result:
                logger.success(f"✅ 图标文件: {self.icon_file}")
            else:
                logger.info("⏭️  跳过图标设置")
        else:
            logger.warning(f"⚠️  {result}，将跳过")
            self.icon_file = None

    def get_compiler_settings(self):
        """获取编译器设置"""
        choices = {
            "1": "MinGW64 (Windows)",
            "2": "MSVC (Windows)",
            "3": "Clang (Linux、Windows、macOS)",
        }

        choice = InputHandlers.get_choice_input("🔧 请选择编译器", choices, "1")

        compiler_map = {"1": "mingw64", "2": "msvc", "3": "clang"}
        self.compiler = compiler_map[choice]
        logger.success(f"✅ 编译器: {self.compiler}")

    def get_console_settings(self):
        """获取控制台显示设置"""
        self.show_console = InputHandlers.get_yes_no_input(
            "🖥️  是否显示控制台窗口?", "y"
        )
        if self.show_console:
            logger.success("✅ 将显示控制台窗口")
        else:
            logger.success("✅ 将隐藏控制台窗口")

    def get_app_name(self):
        """获取应用名称"""
        if self.entry_file:
            default_name = Path(self.entry_file).stem
            self.app_name = InputHandlers.get_text_input(
                "📝 请输入应用名称", default_name
            )
            # 确保应用名称不包含文件扩展名
            if self.app_name.endswith(".py"):
                self.app_name = self.app_name[:-3]
            logger.success(f"✅ 应用名称: {self.app_name}")

    def get_additional_settings(self):
        """获取其他设置"""
        # 输出目录
        self.output_dir = InputHandlers.get_text_input("📂 请输入输出目录", "build")

        # 是否独立打包
        self.standalone = InputHandlers.get_yes_no_input(
            "📦 是否创建独立可执行文件?", "y"
        )
        if self.standalone:
            logger.success("✅ 将创建独立可执行文件")
        else:
            logger.success("✅ 将创建依赖系统Python的可执行文件")

        # 是否单文件模式
        if self.standalone:
            self.onefile = InputHandlers.get_yes_no_input("📄 是否启用单文件模式?", "y")
            if self.onefile:
                logger.success("✅ 将创建单个可执行文件")
            else:
                logger.success("✅ 将创建文件夹形式的可执行文件")

        # 公司名称
        self.company_name = InputHandlers.get_text_input("🏢 请输入公司名称 (可选)","ASLant")

        # 文件版本
        self.file_version = InputHandlers.get_text_input("🔢 请输入文件版本", "1.0.0")

        # 编译线程数
        self.jobs = InputHandlers.get_integer_input("⚡ 请输入编译线程数", 4, 1)

        # 静默模式
        self.quiet_mode = InputHandlers.get_yes_no_input(
            "🔇 是否启用静默模式(减少输出信息)?", "y"
        )
        if self.quiet_mode:
            logger.success("✅ 将启用静默模式")
        else:
            logger.success("✅ 将显示详细输出信息")

        # 进度条显示
        self.show_progressbar = InputHandlers.get_yes_no_input(
            "📊 是否显示进度条?", "y"
        )
        if self.show_progressbar:
            logger.success("✅ 将显示进度条")
        else:
            logger.success("✅ 将隐藏进度条")

        # 移除构建文件
        self.remove_output = InputHandlers.get_yes_no_input(
            "🗑️  是否移除编译后的构建文件?", "y"
        )
        if self.remove_output:
            logger.success("✅ 将移除编译后的构建文件")
        else:
            logger.success("✅ 保留编译后的构建文件")

        # Windows UAC管理员权限
        if sys.platform.startswith("win"):
            self.uac_admin = InputHandlers.get_yes_no_input(
                "🔐 是否需要管理员权限(UAC)?", "n"
            )
            if self.uac_admin:
                logger.success("✅ 将请求管理员权限")
            else:
                logger.success("✅ 不请求管理员权限")

        # 插件选择
        self.get_plugin_settings()

        # 包排除选择
        self.get_exclude_packages_settings()

        # 需要复制的目录
        logger.info("📁 需要复制到输出目录的文件夹 (可选，多个用逗号分隔):")
        self.copy_dirs = InputHandlers.get_list_input("例如: assets,models,libs")

    def get_script_filename(self):
        """获取脚本文件名"""
        filename = InputHandlers.get_text_input(
            "📄 请输入脚本文件名", self.script_filename
        )
        self.script_filename = ConfigValidators.validate_script_filename(filename)
        logger.success(f"✅ 脚本文件名: {self.script_filename}")

    def get_plugin_settings(self):
        """获取插件设置"""
        enable_plugins = InputHandlers.get_yes_no_input("🔌 是否启用额外插件?", "n")

        if enable_plugins:
            self._get_plugins_interactive()
        else:
            logger.info("⏭️  跳过插件选择")
            self.enable_plugins = []

    def _get_plugins_interactive(self):
        """交互式界面选择插件"""
        menu = InteractiveMenu()

        # 从plugins模块获取插件列表
        plugin_items = get_plugin_list()

        # 显示交互式菜单
        try:
            selected_keys = menu.show_menu("🔌 选择需要启用的插件", plugin_items)

            if selected_keys:
                # 处理自定义插件输入
                final_plugins = []
                for plugin_key in selected_keys:
                    if plugin_key == "__custom__":
                        # 自定义插件输入
                        custom_plugins = self._get_custom_plugins()
                        final_plugins.extend(custom_plugins)
                    else:
                        final_plugins.append(plugin_key)

                self.enable_plugins = final_plugins
                logger.success(f"✅ 已选择插件: {', '.join(final_plugins)}")
            else:
                logger.info("⏭️  跳过插件选择")
                self.enable_plugins = []
        except Exception as e:
            logger.error(f"❌ 交互式菜单出错: {e}")
            logger.info("⏭️  跳过插件选择")
            self.enable_plugins = []

    def _get_custom_plugins(self):
        """获取自定义插件输入"""
        custom_plugins = []
        logger.info("🔧 自定义插件输入")
        logger.info("请输入自定义插件名称，多个插件用逗号分隔")
        logger.info("例如: numpy,scipy,requests")

        while True:
            custom_input = input("🔌 请输入插件名称 (直接回车跳过): ").strip()
            if not custom_input:
                break

            # 解析输入的插件名称
            plugin_names = [
                name.strip() for name in custom_input.split(",") if name.strip()
            ]

            if plugin_names:
                for plugin_name in plugin_names:
                    # 简单验证插件名称格式
                    if plugin_name.replace("-", "").replace("_", "").isalnum():
                        custom_plugins.append(plugin_name)
                        logger.success(f"✅ 添加自定义插件: {plugin_name}")
                    else:
                        logger.warning(f"⚠️  跳过无效插件名: {plugin_name}")
                break
            else:
                logger.warning("⚠️  请输入有效的插件名称")

        return custom_plugins

    def get_exclude_packages_settings(self):
        """获取包排除设置"""
        exclude_packages = InputHandlers.get_yes_no_input(
            "🚫 是否排除某些包的导入?", "n"
        )

        if exclude_packages:
            self._get_exclude_packages_interactive()
        else:
            logger.info("⏭️  跳过包排除设置")
            self.exclude_packages = []

    def _get_installed_packages(self):
        """获取当前环境已安装的包列表"""
        try:
            from importlib import metadata

            installed_packages = []

            for dist in metadata.distributions():
                package_name = dist.metadata["Name"].lower()
                version = dist.version
                installed_packages.append((package_name, f"{package_name} ({version})"))

            # 按包名排序
            installed_packages.sort(key=lambda x: x[0])
            return installed_packages

        except Exception as e:
            logger.warning(f"⚠️  获取已安装包列表失败: {e}")
            return []

    def _get_exclude_packages_interactive(self):
        """交互式界面选择要排除的包"""
        menu = InteractiveMenu()

        # 获取已安装的包列表
        logger.info("📦 正在获取当前环境已安装的包...")
        installed_packages = self._get_installed_packages()

        if not installed_packages:
            logger.warning("⚠️  未找到已安装的包，使用手动输入模式")
            self._get_exclude_packages_manual()
            return

        # 添加手动输入选项
        package_items = installed_packages + [("__manual__", "🔧 手动输入包名")]

        # 显示交互式菜单
        try:
            selected_keys = menu.show_menu("🚫 选择要排除导入的包", package_items)

            if selected_keys:
                # 处理选择结果
                final_excludes = []
                for package_key in selected_keys:
                    if package_key == "__manual__":
                        # 手动输入包名
                        manual_excludes = self._get_exclude_packages_manual()
                        final_excludes.extend(manual_excludes)
                    else:
                        final_excludes.append(package_key)

                self.exclude_packages = final_excludes
                logger.success(f"✅ 已选择排除包: {', '.join(final_excludes)}")
            else:
                logger.info("⏭️  跳过包排除设置")
                self.exclude_packages = []
        except Exception as e:
            logger.error(f"❌ 交互式菜单出错: {e}")
            logger.info("⏭️  跳过包排除设置")
            self.exclude_packages = []

    def _get_exclude_packages_manual(self):
        """手动输入要排除的包名"""
        manual_excludes = []
        logger.info("🔧 手动输入包排除")
        logger.info("请输入要排除的包名，多个包用逗号分隔")
        logger.info("例如: numpy,pandas,matplotlib")

        while True:
            exclude_input = input("🚫 请输入包名 (直接回车跳过): ").strip()
            if not exclude_input:
                break

            # 解析输入的包名
            package_names = [
                name.strip() for name in exclude_input.split(",") if name.strip()
            ]

            if package_names:
                for package_name in package_names:
                    # 简单验证包名格式
                    if (
                        package_name.replace("-", "")
                        .replace("_", "")
                        .replace(".", "")
                        .isalnum()
                    ):
                        manual_excludes.append(package_name)
                        logger.success(f"✅ 添加排除包: {package_name}")
                    else:
                        logger.warning(f"⚠️  跳过无效包名: {package_name}")
                break
            else:
                logger.warning("⚠️  请输入有效的包名")

        return manual_excludes

    def collect_all_config(self):
        """收集所有配置"""
        self.get_project_dir()
        self.get_entry_file()
        self.get_app_name()
        self.get_icon_file()
        self.get_compiler_settings()
        self.get_console_settings()
        self.get_additional_settings()
        self.get_script_filename()

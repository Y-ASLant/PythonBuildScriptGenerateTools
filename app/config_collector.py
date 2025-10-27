# -*- coding: utf-8 -*-
"""
配置收集模块 - 处理所有用户输入收集
"""

import sys
from pathlib import Path
from typing import Optional
from .logger_utils import log_info, log_success, log_error, log_warning
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
        self.build_tool: str = "nuitka"  # nuitka 或 pyinstaller
        self.compiler: str = "mingw64"  # 仅Nuitka使用
        self.show_console: bool = False
        self.output_dir: str = "build"
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
        # PyInstaller特有选项
        self.add_data: list = []  # 添加数据文件
        self.hidden_imports: list = []  # 隐藏导入
        self.collect_all: list = []  # 收集所有子模块
        self.upx_dir: Optional[str] = None  # UPX压缩工具路径
        self.debug: bool = False  # 调试模式
        self.clean: bool = True  # 清理临时文件
        # Linux包生成选项
        self.generate_linux_packages: bool = False  # 是否生成Linux包
        self.linux_packaging_tool: str = "nfpm"  # nfpm 或 fpm
        self.linux_package_types: list = ["deb"]  # 包类型
        
        # 扩展打包配置
        self.package_architecture: str = "amd64"  # 目标架构
        self.package_install_path: str = "/usr/local/bin"  # 安装路径
        self.package_depends: list = []  # 依赖包
        self.package_desktop_name: str = ""  # 桌面显示名称
        self.package_create_service: bool = False  # 是否创建服务
        self.package_service_name: str = ""  # 服务名称
        self.package_output_dir: str = "output_pkg"  # 输出目录

    def get_project_dir(self):
        """获取项目根目录"""
        while True:
            project_dir = InputHandlers.get_text_input(
                "📂 请输入项目根目录",
                default=".",
                help_text="请输入需要打包的Python项目的根目录路径。这是包含您的Python代码和相关文件的主目录。可以是绝对路径或相对路径，默认为当前目录(.)",
            )

            is_valid, result = ConfigValidators.validate_project_dir(project_dir)
            if is_valid:
                self.project_dir = result
                log_success(f"✅ 项目目录: {self.project_dir}")
                break
            else:
                log_error(f"❌ {result}")

    def get_entry_file(self):
        """获取入口文件"""
        while True:
            entry = InputHandlers.get_text_input(
                "📁 请输入Python入口文件路径 (相对于项目目录)",
                default="main.py",
                required=True,
                help_text="请输入您的Python程序的主入口文件路径。这是程序启动时执行的.py文件，通常包含main()函数或程序的主要逻辑。路径相对于项目根目录",
            )

            is_valid, result = ConfigValidators.validate_entry_file(
                entry, self.project_dir
            )
            if is_valid:
                self.entry_file = result
                log_success(f"✅ 入口文件: {self.entry_file}")
                break
            else:
                log_error(f"❌ {result}")

    def get_icon_file(self):
        """获取图标文件"""
        icon = InputHandlers.get_text_input(
            "🎨 请输入图标文件路径 (仅支持.ico格式，可选项，直接回车跳过)",
            default="app.ico",
            help_text="请输入应用程序图标文件的路径。图标将显示在可执行文件上，仅支持.ico格式。路径相对于项目根目录。如果不需要图标，直接回车跳过",
        )

        is_valid, result = ConfigValidators.validate_icon_file(icon, self.project_dir)
        if is_valid:
            self.icon_file = result
            if result:
                log_success(f"✅ 图标文件: {self.icon_file}")
            else:
                log_info("⏭️  跳过图标设置")
        else:
            log_warning(f"⚠️  {result}，将跳过")
            self.icon_file = None

    def get_build_tool_settings(self):
        """获取构建工具设置"""
        choices = {
            "1": "Nuitka (打包速度慢、性能好、体积小)",
            "2": "PyInstaller (体积较大、兼容性好、打包速度极快)",
        }

        choice = InputHandlers.get_choice_input(
            "🛠️  请选择构建工具",
            choices,
            "1",
            help_text="选择用于打包Python程序的工具。Nuitka：编译为机器码，性能好但打包慢；PyInstaller：打包快速，兼容性好但体积较大",
        )

        tool_map = {"1": "nuitka", "2": "pyinstaller"}
        self.build_tool = tool_map[choice]
        log_success(f"✅ 构建工具: {self.build_tool}")

    def get_compiler_settings(self):
        """获取编译器设置（仅Nuitka使用）"""
        if self.build_tool != "nuitka":
            return

        choices = {
            "1": "MinGW64 (Windows)",
            "2": "MSVC (Windows)",
            "3": "Clang (Linux、Windows、macOS)",
        }

        choice = InputHandlers.get_choice_input(
            "🔧 请选择编译器",
            choices,
            "3",
            help_text="选择Nuitka使用的C++编译器。MinGW64：Windows上的GCC；MSVC：微软Visual Studio编译器；Clang：跨平台编译器，推荐选择",
        )

        compiler_map = {"1": "mingw64", "2": "msvc", "3": "clang"}
        self.compiler = compiler_map[choice]
        log_success(f"✅ 编译器: {self.compiler}")

    def get_console_settings(self):
        """获取控制台显示设置"""
        self.show_console = InputHandlers.get_yes_no_input(
            "🖥️  是否显示控制台窗口?",
            "y",
            help_text="选择是否在运行程序时显示控制台窗口。选择'是'：可以看到程序的输出信息和错误；选择'否'：程序将在后台运行，适合GUI应用",
        )
        if self.show_console:
            log_success("✅ 将显示控制台窗口")
        else:
            log_success("✅ 将隐藏控制台窗口")

    def get_app_name(self):
        """获取应用名称"""
        if self.entry_file:
            default_name = Path(self.entry_file).stem
            self.app_name = InputHandlers.get_text_input(
                "📝 请输入应用名称",
                default=default_name,
                help_text="请输入打包后可执行文件的名称。这将是最终生成的.exe文件的名称（Windows）或可执行文件名称（Linux/macOS）。默认使用入口文件的名称",
            )
            # 确保应用名称不包含文件扩展名
            if self.app_name.endswith(".py"):
                self.app_name = self.app_name[:-3]
            log_success(f"✅ 应用名称: {self.app_name}")

    def get_additional_settings(self):
        """获取其他设置"""
        # 输出目录
        self.output_dir = InputHandlers.get_text_input(
            "📂 请输入输出目录",
            "build",
            help_text="请输入打包后文件的输出目录。所有生成的可执行文件和相关文件将保存在此目录中。相对于项目根目录",
        )

        if self.build_tool == "nuitka":
            self.get_nuitka_specific_settings()
        else:
            self.get_pyinstaller_specific_settings()

        # 通用设置
        self.get_common_settings()

    def get_nuitka_specific_settings(self):
        """获取Nuitka特有设置"""
        # 是否独立打包
        self.standalone = InputHandlers.get_yes_no_input(
            "📦 是否创建独立可执行文件?",
            "y",
            help_text="选择是否创建独立的可执行文件。选择'是'：打包所有依赖，可在没有Python环境的机器上运行；选择'否'：需要目标机器已安装Python",
        )
        self._log_boolean_choice(
            self.standalone, "将创建独立可执行文件", "将创建依赖系统Python的可执行文件"
        )

        # 是否单文件模式
        if self.standalone:
            self.onefile = InputHandlers.get_yes_no_input(
                "📄 是否启用单文件模式?",
                "y",
                help_text="选择是否将所有文件打包成单个可执行文件。选择'是'：生成单个.exe文件，便于分发；选择'否'：生成文件夹，启动速度更快",
            )
            self._log_boolean_choice(
                self.onefile, "将创建单个可执行文件", "将创建文件夹形式的可执行文件"
            )

        # 编译线程数
        self.jobs = InputHandlers.get_integer_input(
            "⚡ 请输入编译线程数",
            4,
            1,
            help_text="设置编译时使用的并行线程数。更多线程可以加快编译速度，但会消耗更多CPU和内存。建议设置为CPU核心数",
        )

        # 进度条显示
        self.show_progressbar = InputHandlers.get_yes_no_input(
            "📊 是否显示进度条?",
            "y",
            help_text="选择是否在编译过程中显示进度条。显示进度条可以了解编译进度，但在某些环境下可能影响性能",
        )
        self._log_boolean_choice(self.show_progressbar, "将显示进度条", "将隐藏进度条")

        # 移除构建文件
        self.remove_output = InputHandlers.get_yes_no_input(
            "🗑️  是否移除编译后的构建文件?",
            "y",
            help_text="选择是否在编译完成后删除中间构建文件。选择'是'：节省磁盘空间；选择'否'：保留文件便于调试",
        )
        self._log_boolean_choice(
            self.remove_output, "将移除编译后的构建文件", "保留编译后的构建文件"
        )

        # 插件选择
        self.get_plugin_settings()

    def get_pyinstaller_specific_settings(self):
        """获取PyInstaller特有设置"""
        # 是否单文件模式
        self.onefile = InputHandlers.get_yes_no_input(
            "📄 是否启用单文件模式?",
            "y",
            help_text="选择是否将所有文件打包成单个可执行文件。选择'是'：生成单个.exe文件，便于分发；选择'否'：生成文件夹，启动速度更快",
        )
        self._log_boolean_choice(
            self.onefile, "将创建单个可执行文件", "将创建文件夹形式的可执行文件"
        )

        # PyInstaller特有设置
        self.get_pyinstaller_settings()

    def get_common_settings(self):
        """获取通用设置"""
        # 公司名称
        self.company_name = InputHandlers.get_text_input(
            "🏢 请输入公司名称 (可选)",
            "ASLant",
            help_text="请输入软件开发公司或组织的名称。这将显示在可执行文件的属性信息中，可选项",
        )

        # 文件版本
        self.file_version = InputHandlers.get_text_input(
            "🔢 请输入文件版本",
            "1.0.0",
            help_text="请输入软件的版本号，格式为 x.y.z (如 1.0.0)。这将显示在可执行文件的属性信息中",
        )

        # 静默模式
        self.quiet_mode = InputHandlers.get_yes_no_input(
            "🔇 是否启用静默模式(减少输出信息)?",
            "y",
            help_text="选择是否启用静默模式。选择'是'：减少编译过程中的输出信息，界面更简洁；选择'否'：显示详细的编译信息",
        )
        self._log_boolean_choice(
            self.quiet_mode, "将启用静默模式", "将显示详细输出信息"
        )

        # Windows UAC管理员权限
        if sys.platform.startswith("win"):
            self.uac_admin = InputHandlers.get_yes_no_input(
                "🔐 是否需要管理员权限(UAC)?",
                "n",
                help_text="选择程序是否需要管理员权限运行。选择'是'：程序启动时会弹出UAC提示；选择'否'：程序以普通用户权限运行",
            )
            self._log_boolean_choice(
                self.uac_admin, "将请求管理员权限", "不请求管理员权限"
            )

        # 包排除选择
        self.get_exclude_packages_settings()

        # 需要复制的目录
        log_info("📁 需要复制到输出目录的文件夹 (可选，多个用逗号分隔):")
        self.copy_dirs = InputHandlers.get_list_input(
            "例如: assets,models,libs",
            help_text="请输入需要复制到输出目录的文件夹名称，多个文件夹用逗号分隔。这些文件夹将被完整复制到可执行文件旁边",
        )

    def get_script_filename(self):
        """获取脚本文件名"""
        filename = InputHandlers.get_text_input(
            "📄 请输入脚本文件名",
            self.script_filename,
            help_text="请输入生成的打包脚本的文件名。这个脚本包含了所有打包配置，可以重复运行来打包程序",
        )
        self.script_filename = ConfigValidators.validate_script_filename(filename)
        log_success(f"✅ 脚本文件名: {self.script_filename}")

    def get_plugin_settings(self):
        """获取插件设置"""
        enable_plugins = InputHandlers.get_yes_no_input("🔌 是否启用额外插件?", "n")

        if enable_plugins:
            self._get_plugins_interactive()
        else:
            log_info("⏭️  跳过插件选择")
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
                log_success(f"✅ 已选择插件: {', '.join(final_plugins)}")
            else:
                log_info("⏭️  跳过插件选择")
                self.enable_plugins = []
        except Exception as e:
            log_error(f"❌ 交互式菜单出错: {e}")
            log_info("⏭️  跳过插件选择")
            self.enable_plugins = []

    def _get_custom_plugins(self):
        """获取自定义插件输入"""
        custom_plugins = []
        log_info("🔧 自定义插件输入")
        log_info("请输入自定义插件名称，多个插件用逗号分隔")
        log_info("例如: numpy,scipy,requests")

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
                        log_success(f"✅ 添加自定义插件: {plugin_name}")
                    else:
                        log_warning(f"⚠️  跳过无效插件名: {plugin_name}")
                break
            else:
                log_warning("⚠️  请输入有效的插件名称")

        return custom_plugins

    def get_exclude_packages_settings(self):
        """获取包排除设置"""
        exclude_packages = InputHandlers.get_yes_no_input(
            "🚫 是否排除某些包的导入?", "n"
        )

        if exclude_packages:
            self._get_exclude_packages_interactive()
        else:
            log_info("⏭️  跳过包排除设置")
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
            log_warning(f"⚠️  获取已安装包列表失败: {e}")
            return []

    def _get_exclude_packages_interactive(self):
        """交互式界面选择要排除的包"""
        menu = InteractiveMenu()

        # 获取已安装的包列表
        log_info("📦 正在获取当前环境已安装的包...")
        installed_packages = self._get_installed_packages()

        if not installed_packages:
            log_warning("⚠️  未找到已安装的包，使用手动输入模式")
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
                log_success(f"✅ 已选择排除包: {', '.join(final_excludes)}")
            else:
                log_info("⏭️  跳过包排除设置")
                self.exclude_packages = []
        except Exception as e:
            log_error(f"❌ 交互式菜单出错: {e}")
            log_info("⏭️  跳过包排除设置")
            self.exclude_packages = []

    def _get_exclude_packages_manual(self):
        """手动输入要排除的包名"""
        manual_excludes = []
        log_info("🔧 手动输入包排除")
        log_info("请输入要排除的包名，多个包用逗号分隔")
        log_info("例如: numpy,pandas,matplotlib")

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
                        log_success(f"✅ 添加排除包: {package_name}")
                    else:
                        log_warning(f"⚠️  跳过无效包名: {package_name}")
                break
            else:
                log_warning("⚠️  请输入有效的包名")

        return manual_excludes

    def get_pyinstaller_settings(self):
        """获取PyInstaller特有设置"""
        log_info("🔧 PyInstaller特有配置")

        # 隐藏导入
        hidden_imports = InputHandlers.get_yes_no_input(
            "📦 是否需要添加隐藏导入?",
            "n",
            help_text="添加PyInstaller无法自动检测到的模块。如果程序运行时提示缺少某些模块，可以在这里手动指定导入",
        )
        if hidden_imports:
            log_info("请输入需要隐藏导入的模块，多个用逗号分隔")
            log_info("例如: numpy,pandas,requests")
            self.hidden_imports = InputHandlers.get_list_input(
                "隐藏导入模块",
                help_text="请输入需要隐藏导入的模块名称，多个模块用逗号分隔。例如：numpy,pandas,requests",
            )
            if self.hidden_imports:
                log_success(f"✅ 隐藏导入: {', '.join(self.hidden_imports)}")

        # 收集所有子模块
        collect_all = InputHandlers.get_yes_no_input(
            "📚 是否收集某些包的所有子模块?",
            "n",
            help_text="强制收集指定包的所有子模块。适用于动态导入的模块，如tkinter、PIL等大型包，确保所有子模块都被包含",
        )
        if collect_all:
            log_info("请输入需要收集所有子模块的包，多个用逗号分隔")
            log_info("例如: tkinter,PIL,matplotlib")
            self.collect_all = InputHandlers.get_list_input(
                "收集子模块的包",
                help_text="请输入需要收集所有子模块的包名称，多个包用逗号分隔。例如：tkinter,PIL,matplotlib",
            )
            if self.collect_all:
                log_success(f"✅ 收集子模块: {', '.join(self.collect_all)}")

        # 添加数据文件
        add_data = InputHandlers.get_yes_no_input(
            "📁 是否需要添加数据文件?",
            "n",
            help_text="添加程序需要的数据文件（如配置文件、图片、文档等）到打包中。格式：源路径;目标路径，多个文件用逗号分隔",
        )
        if add_data:
            log_info("请输入数据文件路径，格式: 源路径;目标路径")
            log_info("例如: data/config.ini;data")
            log_info(
                "💡 多个数据文件需要使用逗号隔开，如: data/config.ini;data,assets/logo.png;assets"
            )
            while True:
                data_path = input("📁 数据文件路径 (直接回车结束): ").strip()
                if not data_path:
                    break

                # 支持逗号分隔的多个数据文件
                data_paths = [path.strip() for path in data_path.split(",")]
                for single_path in data_paths:
                    if ";" in single_path:
                        self.add_data.append(single_path)
                        log_success(f"✅ 添加数据文件: {single_path}")
                    else:
                        log_warning(
                            f"⚠️  格式错误: {single_path}，请使用 源路径;目标路径 格式"
                        )

        # UPX压缩
        upx_compress = InputHandlers.get_yes_no_input(
            "🗜️  是否启用UPX压缩?",
            "n",
            help_text="使用UPX工具压缩可执行文件以减小体积。需要系统中安装UPX工具。压缩后文件更小但启动可能稍慢",
        )
        if upx_compress:
            upx_path = InputHandlers.get_text_input(
                "请输入UPX工具路径 (可选，留空自动检测)",
                help_text="请输入UPX压缩工具的完整路径。如果UPX已添加到系统PATH环境变量，可以留空自动检测",
            )
            if upx_path:
                self.upx_dir = upx_path
                log_success(f"✅ UPX路径: {self.upx_dir}")
            else:
                self.upx_dir = "auto"
                log_success("✅ 将自动检测UPX路径")

        # 调试模式
        self.debug = InputHandlers.get_yes_no_input(
            "🐛 是否启用调试模式?",
            "n",
            help_text="启用调试模式会输出详细的编译信息，便于排查问题。通常在遇到编译错误时启用",
        )
        self._log_boolean_choice(self.debug, "将启用调试模式", "将禁用调试模式")

        # 清理临时文件
        self.clean = InputHandlers.get_yes_no_input(
            "🧹 是否清理构建临时文件?",
            "y",
            help_text="选择是否在打包完成后清理临时构建文件。选择'是'：节省磁盘空间；选择'否'：保留文件便于调试",
        )
        self._log_boolean_choice(self.clean, "将清理临时文件", "将保留临时文件")

    def _log_boolean_choice(
        self, condition: bool, true_message: str, false_message: str
    ):
        """记录布尔选择的结果"""
        if condition:
            log_success(f"✅ {true_message}")
        else:
            log_success(f"✅ {false_message}")

    def collect_all_config(self, mode="full"):
        """收集所有配置"""
        if mode in ["full", "compile"]:
            # 编译相关配置
            self.get_project_dir()
            self.get_entry_file()
            self.get_app_name()
            self.get_icon_file()
            self.get_build_tool_settings()
            self.get_compiler_settings()
            self.get_console_settings()
            self.get_additional_settings()
            self.get_script_filename()

        if mode in ["full", "package"]:
            # Linux包生成配置
            if mode == "package":
                # 打包模式下，需要基本信息和脚本名称
                self.get_app_name_for_package()
                self.script_filename = "create_packages.py"  # 打包模式默认脚本名
                self.get_script_filename()  # 添加脚本名称设置
            self.get_linux_package_settings(mode == "package")

    def get_linux_package_settings(self, force_enable=False):
        """获取Linux包生成设置"""
        if force_enable:
            # 打包模式下强制启用
            self.generate_linux_packages = True
            log_success("✅ 打包模式 - 自动启用Linux包生成")
        else:
            self.generate_linux_packages = InputHandlers.get_yes_no_input(
                "📦 是否在编译完成后自动生成Linux安装包",
                "n",
                help_text="选择是否在编译完成后自动生成deb/rpm安装包。这样可以一键完成从源码到安装包的整个流程",
            )

        if self.generate_linux_packages:
            # 选择打包工具
            tool_choice = InputHandlers.get_choice_input(
                "🛠️ 请选择Linux包生成工具",
                {
                    "1": "NFPM (推荐，跨平台支持Windows/macOS/Linux，Go语言高性能)",
                    "2": "FPM (Windows上支持有限，不建议在Windows下使用该工具打包)",
                },
                "1",
                help_text="NFPM是Go编写的现代化打包工具，支持在Windows、macOS、Linux上运行，性能更好，无依赖；FPM是Ruby编写的传统工具，功能全面但需要Ruby环境，在Windows上可能遇到兼容性问题",
            )

            self.linux_packaging_tool = "nfpm" if tool_choice == "1" else "fpm"

            # 选择包类型
            deb_choice = InputHandlers.get_yes_no_input(
                "📦 是否生成 DEB 包 (Debian/Ubuntu)",
                "y",
                help_text="DEB包适用于Debian、Ubuntu等基于Debian的Linux发行版",
            )

            rpm_choice = InputHandlers.get_yes_no_input(
                "📦 是否生成 RPM 包 (RedHat/CentOS/Fedora)",
                "y",
                help_text="RPM包适用于RedHat、CentOS、Fedora等基于RedHat的Linux发行版",
            )

            self.linux_package_types = []
            if deb_choice:
                self.linux_package_types.append("deb")
            if rpm_choice:
                self.linux_package_types.append("rpm")

            if not self.linux_package_types:
                self.linux_package_types = ["deb"]  # 默认生成DEB包
            
            # 扩展配置选项
            self._collect_extended_package_config()

    def get_app_name_for_package(self):
        """获取打包用的应用名称"""
        self.app_name = InputHandlers.get_text_input(
            "📝 请输入应用名称",
            default="app",
            help_text="请输入要打包的应用程序名称，这将作为包名。建议使用小写字母和连字符",
        )
        log_success(f"✅ 应用名称: {self.app_name}")
    
    def _collect_extended_package_config(self):
        """收集扩展打包配置（简化版）"""
        log_info("🔧 扩展配置选项")
        
        # 架构选择
        arch_choice = InputHandlers.get_choice_input(
            "💻 请选择目标架构",
            {
                "1": "amd64 (64位 Intel/AMD)",
                "2": "arm64 (64位 ARM)",
                "3": "all (架构无关)"
            },
            "1",
            help_text="选择包的目标架构。amd64适用于大多数桌面和服务器；arm64适用于ARM处理器；all适用于纯脚本程序"
        )
        
        arch_map = {"1": "amd64", "2": "arm64", "3": "all"}
        self.package_architecture = arch_map[arch_choice]
        log_success(f"✅ 目标架构: {self.package_architecture}")
        
        # 输出目录设置
        self.package_output_dir = InputHandlers.get_text_input(
            "📁 请输入输出目录",
            default="output_pkg",
            help_text="请输入生成的RPM/DEB包文件的输出目录名称"
        )
        log_success(f"✅ 输出目录: {self.package_output_dir}")
        
        # 安装路径自定义
        custom_path = InputHandlers.get_yes_no_input(
            "📁 是否自定义安装路径?",
            "n",
            help_text="默认安装到 /usr/local/bin，您可以选择自定义路径"
        )
        
        if custom_path:
            self.package_install_path = InputHandlers.get_text_input(
                "请输入安装路径",
                default="/usr/local/bin",
                help_text="请输入可执行文件的安装路径"
            )
        else:
            self.package_install_path = "/usr/local/bin"
        log_success(f"✅ 安装路径: {self.package_install_path}")
        
        # 依赖包设置
        add_depends = InputHandlers.get_yes_no_input(
            "📦 是否添加运行时依赖包?",
            "n",
            help_text="添加程序运行所需的系统包依赖。例如：python3, libssl1.1等"
        )
        
        if add_depends:
            log_info("请输入依赖包名称，多个包用逗号分隔")
            log_info("例如: python3,libssl1.1,libc6")
            self.package_depends = InputHandlers.get_list_input(
                "依赖包",
                help_text="请输入程序运行所需的系统包，多个包用逗号分隔"
            )
            if self.package_depends:
                log_success(f"✅ 依赖包: {', '.join(self.package_depends)}")
        else:
            self.package_depends = []
        
        # 桌面文件
        add_desktop = InputHandlers.get_yes_no_input(
            "🖥️ 是否创建桌面快捷方式?",
            "n",
            help_text="为GUI应用创建桌面快捷方式，会在应用程序菜单中显示"
        )
        
        if add_desktop:
            self.package_desktop_name = InputHandlers.get_text_input(
                "请输入应用显示名称",
                default=self.app_name.title(),
                help_text="在桌面和应用程序菜单中显示的名称"
            )
            log_success(f"✅ 将创建桌面快捷方式: {self.package_desktop_name}")
        else:
            self.package_desktop_name = ""
        
        # 系统服务
        add_service = InputHandlers.get_yes_no_input(
            "⚙️ 是否创建系统服务?",
            "n",
            help_text="为后台服务程序创建systemd服务，可以开机自启动"
        )
        
        if add_service:
            self.package_create_service = True
            self.package_service_name = InputHandlers.get_text_input(
                "请输入服务名称",
                default=self.app_name,
                help_text="systemd服务的名称，建议使用应用名称"
            )
            log_success(f"✅ 将创建系统服务: {self.package_service_name}")
        else:
            self.package_create_service = False
            self.package_service_name = ""

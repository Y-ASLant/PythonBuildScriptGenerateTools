# -*- coding: utf-8 -*-
"""
Linux包生成器模块 - 支持生成deb和rpm安装包
"""

import os
import subprocess
from pathlib import Path
from .logger_utils import log_info, log_success, log_error, log_warning
from .input_handlers import InputHandlers


class LinuxPackageGenerator:
    """Linux包生成器 - 支持FPM和NFPM两种工具"""

    def __init__(self):
        self.app_name = ""
        self.version = "1.0.0"
        self.description = ""
        self.maintainer = ""
        self.url = ""
        self.license = "MIT"
        self.executable_path = ""
        self.install_path = "/usr/local/bin"
        self.package_types = []
        self.packaging_tool = "nfpm"  # 默认使用NFPM
        self.nfpm_path = "nfpm"  # NFPM可执行文件路径

    def collect_package_info(self, executable_path: str):
        """收集打包信息"""
        self.executable_path = executable_path

        log_info("📦 Linux包生成配置")

        # 选择打包工具
        self._select_packaging_tool()

        # 应用名称
        default_name = Path(executable_path).stem.lower().replace("_", "-")
        self.app_name = InputHandlers.get_text_input(
            "📝 请输入应用名称",
            default=default_name,
            help_text="请输入应用程序的名称，这将作为包名和可执行文件名。建议使用小写字母和连字符",
        )

        # 规范化应用名称
        self.app_name = self._normalize_app_name(self.app_name)

        # 版本号
        self.version = InputHandlers.get_text_input(
            "🔢 请输入版本号",
            default="1.0.0",
            help_text="请输入应用程序的版本号，格式为 x.y.z (如 1.0.0)",
        )

        # 描述
        self.description = InputHandlers.get_text_input(
            "📄 请输入应用描述",
            help_text="请输入应用程序的简短描述，这将显示在包管理器中",
        )

        # 维护者信息
        self.maintainer = InputHandlers.get_text_input(
            "👤 请输入维护者信息",
            default="Your Name <your.email@example.com>",
            help_text="请输入维护者的姓名和邮箱，格式：姓名 <邮箱>",
        )

        # 项目URL
        self.url = InputHandlers.get_text_input(
            "🌐 请输入项目URL (可选)",
            help_text="请输入项目的官方网站或代码仓库地址，可选项",
        )

        # 许可证
        self.license = InputHandlers.get_text_input(
            "📜 请输入许可证",
            default="MIT",
            help_text="请输入软件许可证类型，如 MIT、GPL、Apache-2.0 等",
        )

        # 安装路径
        self.install_path = InputHandlers.get_text_input(
            "📁 请输入安装路径",
            default="/usr/local/bin",
            help_text="请输入可执行文件的安装路径，默认为 /usr/local/bin",
        )

        # 包类型选择
        self._select_package_types()

    def _select_packaging_tool(self):
        """选择打包工具"""
        tool_choice = InputHandlers.get_choice_input(
            "🛠️ 请选择包生成工具",
            {
                "1": "NFPM (推荐，跨平台支持Windows/macOS/Linux，Go语言高性能)",
                "2": "FPM (Windows上支持有限，不建议在Windows下使用该工具打包)",
            },
            "1",
            help_text="NFPM是Go编写的现代化打包工具，支持在Windows、macOS、Linux上运行，性能更好，无依赖；FPM是Ruby编写的传统工具，功能全面但需要Ruby环境，在Windows上可能遇到兼容性问题",
        )

        if tool_choice == "1":
            self.packaging_tool = "nfpm"
            log_success("✅ 选择了 NFPM 打包工具")
        else:
            self.packaging_tool = "fpm"
            log_success("✅ 选择了 FPM 打包工具")

    def _normalize_app_name(self, name: str) -> str:
        """规范化应用名称，确保符合包命名规范"""
        # 转换为小写
        name = name.lower()

        # 替换不允许的字符
        import re

        name = re.sub(r"[^a-z0-9\-\.]", "-", name)

        # 移除连续的连字符
        name = re.sub(r"-+", "-", name)

        # 移除开头和结尾的连字符
        name = name.strip("-")

        # 确保不为空
        if not name:
            name = "app"

        log_info(f"📝 规范化后的应用名称: {name}")
        return name

    def _select_package_types(self):
        """选择要生成的包类型"""
        log_info("📦 选择要生成的包类型:")

        deb_choice = InputHandlers.get_yes_no_input(
            "📦 是否生成 DEB 包 (Debian/Ubuntu)?",
            "y",
            help_text="DEB包适用于Debian、Ubuntu等基于Debian的Linux发行版",
        )

        if deb_choice:
            self.package_types.append("deb")

        rpm_choice = InputHandlers.get_yes_no_input(
            "📦 是否生成 RPM 包 (RedHat/CentOS/Fedora)?",
            "y",
            help_text="RPM包适用于RedHat、CentOS、Fedora等基于RedHat的Linux发行版",
        )

        if rpm_choice:
            self.package_types.append("rpm")

        if not self.package_types:
            log_warning("⚠️  未选择任何包类型，将默认生成DEB包")
            self.package_types.append("deb")

    def check_tool_installation(self):
        """检查选择的打包工具是否已安装"""
        if self.packaging_tool == "nfpm":
            return self._check_nfpm_installation()
        else:
            return self._check_fpm_installation()

    def _check_nfpm_installation(self):
        """检查NFPM是否已安装"""
        # 首先尝试直接命令
        try:
            subprocess.run(
                ["nfpm", "version"], capture_output=True, text=True, check=True
            )
            log_success("✅ NFPM已安装并在PATH中")
            self.nfpm_path = "nfpm"
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        # 尝试查找NFPM的完整路径
        nfpm_path = self._find_nfpm_path()
        if nfpm_path:
            try:
                subprocess.run(
                    [nfpm_path, "version"], capture_output=True, text=True, check=True
                )
                log_success(f"✅ NFPM已安装: {nfpm_path}")
                self.nfpm_path = nfpm_path
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass

        log_error("❌ NFPM未安装或不可用")
        log_info("请安装NFPM:")
        log_info(
            "方法1: curl -sfL https://install.goreleaser.com/github.com/goreleaser/nfpm.sh | sh"
        )
        log_info("方法2: go install github.com/goreleaser/nfpm/v2/cmd/nfpm@latest")
        log_info("方法3: 下载二进制文件 https://github.com/goreleaser/nfpm/releases")
        log_info("如果已安装，请添加到PATH或重新加载shell配置")
        return False

    def _find_nfpm_path(self):
        """查找NFPM的完整路径"""
        import os

        # 常见的Go安装路径
        possible_paths = [
            "~/go/bin/nfpm",
            "/usr/local/go/bin/nfpm",
            "$HOME/go/bin/nfpm",
        ]

        # 获取GOPATH
        try:
            result = subprocess.run(
                ["go", "env", "GOPATH"], capture_output=True, text=True, check=True
            )
            gopath = result.stdout.strip()
            if gopath:
                possible_paths.insert(0, f"{gopath}/bin/nfpm")
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        # 检查每个可能的路径
        for path_str in possible_paths:
            expanded_path = os.path.expanduser(os.path.expandvars(path_str))
            if Path(expanded_path).exists() and os.access(expanded_path, os.X_OK):
                return expanded_path

        return None

    def _check_fpm_installation(self):
        """检查FPM是否已安装"""
        try:
            subprocess.run(
                ["fpm", "--version"], capture_output=True, text=True, check=True
            )
            log_success("✅ FPM已安装")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            log_error("❌ FPM未安装")
            log_info("请安装FPM:")
            log_info(
                "Ubuntu/Debian: sudo apt-get install ruby ruby-dev rubygems build-essential && sudo gem install --no-document fpm"
            )
            log_info(
                "CentOS/RHEL: sudo yum install ruby ruby-devel rubygems rpm-build && sudo gem install --no-document fpm"
            )
            return False

    def generate_packages(self):
        """生成Linux包"""
        if not self.check_tool_installation():
            return False

        # 验证可执行文件
        if not self._validate_executable():
            return False

        success = True

        if self.packaging_tool == "nfpm":
            success = self._generate_with_nfpm()
        else:
            success = self._generate_with_fpm()

        return success

    def _validate_executable(self):
        """验证可执行文件"""
        if not os.path.exists(self.executable_path):
            log_error(f"❌ 可执行文件不存在: {self.executable_path}")
            return False

        # 检查文件大小
        file_size = os.path.getsize(self.executable_path)
        if file_size == 0:
            log_error(f"❌ 可执行文件为空: {self.executable_path}")
            return False

        log_info(f"📁 可执行文件验证通过: {self.executable_path} ({file_size} bytes)")

        # 如果是Windows可执行文件，给出警告
        if self.executable_path.endswith(".exe"):
            log_warning("⚠️  这是Windows可执行文件，在Linux上需要Wine才能运行")

        return True

    def _generate_with_nfpm(self):
        """使用NFPM生成包"""
        log_info("🔧 使用NFPM生成包...")

        # 生成NFPM配置文件
        config_file = self._create_nfpm_config()

        success = True
        for package_type in self.package_types:
            try:
                self._generate_nfpm_package(package_type, config_file)
                log_success(f"✅ {package_type.upper()}包生成成功")
            except Exception as e:
                log_error(f"❌ {package_type.upper()}包生成失败: {e}")
                success = False

        # 清理配置文件
        if Path(config_file).exists():
            Path(config_file).unlink()

        return success

    def _generate_with_fpm(self):
        """使用FPM生成包（精简版）"""
        log_info("🔧 使用FPM生成包...")

        success = True
        for package_type in self.package_types:
            try:
                self._generate_fpm_package(package_type)
                log_success(f"✅ {package_type.upper()}包生成成功")
            except Exception as e:
                log_error(f"❌ {package_type.upper()}包生成失败: {e}")
                success = False

        return success

    def _cleanup_existing_packages(self, package_type: str):
        """清理已存在的包文件"""
        if package_type == "deb":
            # DEB包会被自动转换为小写名称
            lowercase_name = self.app_name.lower()
            pattern = f"{lowercase_name}*.deb"
        elif package_type == "rpm":
            pattern = f"{self.app_name}*.rpm"
        else:
            return

        # 查找并删除已存在的包文件
        existing_files = list(Path(".").glob(pattern))
        for file_path in existing_files:
            try:
                file_path.unlink()
                log_info(f"🗑️  删除已存在的包文件: {file_path}")
            except Exception as e:
                log_warning(f"⚠️  无法删除文件 {file_path}: {e}")

    def _create_nfpm_config(self):
        """创建NFPM配置文件"""
        config_file = "nfpm.yaml"

        # 将Windows路径转换为Unix格式
        unix_path = str(Path(self.executable_path)).replace("\\", "/")

        config_content = f"""name: {self.app_name}
arch: amd64
platform: linux
version: {self.version}
section: utils
priority: optional
maintainer: {self.maintainer}
description: {self.description.strip()}
vendor: {self.maintainer.split("<")[0].strip() if "<" in self.maintainer else self.maintainer}
homepage: {self.url or "https://example.com"}
license: {self.license}

contents:
  - src: {unix_path}
    dst: {self.install_path}/{self.app_name}
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

        with open(config_file, "w", encoding="utf-8") as f:
            f.write(config_content)

        log_info(f"📝 NFPM配置文件已生成: {config_file}")
        return config_file

    def _generate_nfpm_package(self, package_type: str, config_file: str):
        """使用NFPM生成指定类型的包"""
        # 清理已存在的包文件
        self._cleanup_existing_packages(package_type)

        cmd = [
            self.nfpm_path,
            "package",
            "--packager",
            package_type,
            "--config",
            config_file,
        ]

        log_info(f"🔧 生成{package_type.upper()}包...")
        log_info(f"执行命令: {' '.join(cmd)}")

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            log_info("📋 NFPM输出:")
            if result.stdout:
                log_info(result.stdout)

            # 查找生成的包文件
            package_files = list(Path(".").glob(f"{self.app_name}*.{package_type}"))
            for package_file in package_files:
                log_success(f"📦 生成的包: {package_file}")
        else:
            error_msg = f"NFPM命令执行失败 (返回码: {result.returncode})"
            if result.stderr:
                error_msg += f"\n错误输出: {result.stderr}"
            if result.stdout:
                error_msg += f"\n标准输出: {result.stdout}"
            raise Exception(error_msg)

    def _generate_fpm_package(self, package_type: str):
        """使用FPM生成指定类型的包（精简版）"""
        # 清理已存在的包文件
        self._cleanup_existing_packages(package_type)

        # 将Windows路径转换为Unix格式
        unix_path = str(Path(self.executable_path)).replace("\\", "/")

        # 构建精简的FPM命令
        cmd = [
            "fpm",
            "-s",
            "dir",
            "-t",
            package_type,
            "-n",
            self.app_name,
            "-v",
            self.version,
            "--description",
            self.description.strip(),
            "--maintainer",
            self.maintainer,
            "--license",
            self.license,
            "--force",
            f"{unix_path}={self.install_path}/{self.app_name}",
        ]

        # 添加架构参数
        if package_type == "deb":
            cmd.extend(["--architecture", "amd64"])
        elif package_type == "rpm":
            cmd.extend(["--architecture", "x86_64"])

        # 添加可选URL
        if self.url:
            cmd.extend(["--url", self.url])

        log_info(f"🔧 生成{package_type.upper()}包...")
        log_info(f"执行命令: {' '.join(cmd)}")

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            log_info("📋 FPM输出:")
            if result.stdout:
                log_info(result.stdout)

            # 查找生成的包文件
            package_files = []
            if package_type == "deb":
                package_files = list(Path(".").glob(f"{self.app_name}*.deb"))
            elif package_type == "rpm":
                package_files = list(Path(".").glob(f"{self.app_name}*.rpm"))

            for package_file in package_files:
                log_success(f"📦 生成的包: {package_file}")
        else:
            error_msg = f"FPM命令执行失败 (返回码: {result.returncode})"
            if result.stderr:
                error_msg += f"\n错误输出: {result.stderr}"
            if result.stdout:
                error_msg += f"\n标准输出: {result.stdout}"
            raise Exception(error_msg)


def create_linux_packages(executable_path: str):
    """创建Linux安装包的主函数"""
    generator = LinuxPackageGenerator()

    try:
        # 收集打包信息
        generator.collect_package_info(executable_path)

        # 生成包
        if generator.generate_packages():
            log_success("🎉 Linux包生成完成！")
            log_info("📦 生成的文件:")
            log_info("- *.deb 或 *.rpm 包文件")
            log_info("💡 安装方法:")
            log_info("- DEB包: sudo apt install -fy ./包文件名.deb")
            log_info(
                "- RPM包: sudo rpm -i 包文件名.rpm 或 sudo dnf install 包文件名.rpm"
            )
            return True
        else:
            log_error("❌ Linux包生成失败")
            return False

    except KeyboardInterrupt:
        log_info("👋 用户取消操作")
        return False
    except Exception as e:
        log_error(f"❌ 生成Linux包时发生错误: {e}")
        return False

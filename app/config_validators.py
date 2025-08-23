# -*- coding: utf-8 -*-
"""
配置验证模块 - 提供配置项验证功能
"""

from pathlib import Path
from loguru import logger


class ConfigValidators:
    """配置验证器集合"""

    @staticmethod
    def validate_project_dir(project_dir: str) -> tuple[bool, str]:
        """验证项目目录"""
        if not project_dir:
            return False, "项目目录不能为空"

        project_path = Path(project_dir)
        if not project_path.exists():
            return False, f"目录不存在: {project_dir}"

        if not project_path.is_dir():
            return False, f"路径不是目录: {project_dir}"

        return True, str(project_path.resolve())

    @staticmethod
    def validate_entry_file(entry_file: str, project_dir: str) -> tuple[bool, str]:
        """验证入口文件"""
        if not entry_file:
            return False, "入口文件不能为空"

        # 如果是绝对路径，直接使用；否则相对于项目目录
        if Path(entry_file).is_absolute():
            entry_path = Path(entry_file)
        else:
            entry_path = Path(project_dir) / entry_file

        if not entry_path.exists():
            return False, f"文件不存在: {entry_path}"

        if not entry_path.suffix == ".py":
            return False, "请输入有效的Python文件(.py)"

        return True, str(entry_path.absolute())

    @staticmethod
    def validate_icon_file(icon_file: str, project_dir: str) -> tuple[bool, str]:
        """验证图标文件"""
        if not icon_file:
            return True, None  # 图标文件是可选的

        # 如果是绝对路径，直接使用；否则相对于项目目录
        if Path(icon_file).is_absolute():
            icon_path = Path(icon_file)
        else:
            icon_path = Path(project_dir) / icon_file

        if not icon_path.exists():
            return False, f"图标文件不存在: {icon_path}"

        if icon_path.suffix.lower() != ".ico":
            if icon_path.suffix.lower() in [".png", ".jpg", ".jpeg"]:
                logger.warning("⚠️  Nuitka只支持.ico格式图标，请转换后重新输入")
            return False, "仅支持.ico格式图标"

        # 保存相对于项目目录的路径
        try:
            relative_path = icon_path.relative_to(Path(project_dir))
            return True, str(relative_path)
        except ValueError:
            # 如果无法转换为相对路径，使用绝对路径
            return True, str(icon_path)

    @staticmethod
    def validate_compiler(compiler: str) -> bool:
        """验证编译器选择"""
        valid_compilers = ["mingw64", "msvc", "clang"]
        return compiler in valid_compilers

    @staticmethod
    def validate_jobs(jobs_str: str) -> tuple[bool, int]:
        """验证编译线程数"""
        if not jobs_str:
            return True, 4  # 默认值

        try:
            jobs = int(jobs_str)
            if jobs > 0:
                return True, jobs
            else:
                return False, 0
        except ValueError:
            return False, 0

    @staticmethod
    def validate_version(version: str) -> bool:
        """验证版本号格式"""
        if not version:
            return True  # 版本号是可选的

        # 简单的版本号格式验证 (x.y.z)
        parts = version.split(".")
        if len(parts) != 3:
            return False

        try:
            for part in parts:
                int(part)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_script_filename(filename: str) -> str:
        """验证并格式化脚本文件名"""
        if not filename:
            return "build.py"

        # 确保文件名以.py结尾
        if not filename.endswith(".py"):
            filename += ".py"

        return filename

    @staticmethod
    def validate_package_names(packages_str: str) -> list[str]:
        """验证并解析包名列表"""
        if not packages_str:
            return []

        valid_packages = []
        package_names = [
            name.strip() for name in packages_str.split(",") if name.strip()
        ]

        for package_name in package_names:
            # 简单验证包名格式
            if (
                package_name.replace("-", "")
                .replace("_", "")
                .replace(".", "")
                .isalnum()
            ):
                valid_packages.append(package_name)
            else:
                logger.warning(f"⚠️  跳过无效包名: {package_name}")

        return valid_packages

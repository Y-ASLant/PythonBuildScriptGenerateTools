# -*- coding: utf-8 -*-
"""
工具需求分析器 - 根据构建配置分析需要的工具
"""

import sys
from typing import Dict, List


class ToolRequirementAnalyzer:
    """工具需求分析器 - 根据配置分析需要哪些工具"""

    def __init__(self):
        pass

    def analyze_requirements(self, config) -> Dict[str, List[str]]:
        """分析配置并返回需要的工具列表
        
        Args:
            config: 构建配置对象
            
        Returns:
            Dict[str, List[str]]: 工具需求字典
                {
                    'build_tools': ['nuitka', 'pyinstaller'],
                    'package_tools': ['nfpm', 'fpm'],
                    'system_tools': ['clang', 'gcc'],
                    'package_types': ['deb', 'rpm']
                }
        """
        requirements = {
            'build_tools': [],
            'package_tools': [],
            'system_tools': [],
            'package_types': []
        }

        # 分析构建工具需求
        self._analyze_build_tools(config, requirements)
        
        # 分析系统工具需求
        self._analyze_system_tools(config, requirements)
        
        # 分析打包工具需求
        self._analyze_package_tools(config, requirements)
        
        # 分析包类型需求
        self._analyze_package_types(config, requirements)

        return requirements

    def _analyze_build_tools(self, config, requirements):
        """分析构建工具需求"""
        if hasattr(config, 'build_tool'):
            if config.build_tool == 'nuitka':
                requirements['build_tools'].append('nuitka')
            elif config.build_tool == 'pyinstaller':
                requirements['build_tools'].append('pyinstaller')

    def _analyze_system_tools(self, config, requirements):
        """分析系统工具需求"""
        if hasattr(config, 'compiler'):
            # 只检查跨平台的编译器
            if config.compiler == 'clang':
                requirements['system_tools'].append('clang')
            elif config.compiler == 'gcc':
                requirements['system_tools'].append('gcc')
            # Windows特定编译器（mingw64, msvc）不需要额外检查，由系统处理

    def _analyze_package_tools(self, config, requirements):
        """分析打包工具需求"""
        # 检查是否启用Linux包生成
        if hasattr(config, 'generate_linux_packages') and config.generate_linux_packages:
            if hasattr(config, 'linux_packaging_tool'):
                if config.linux_packaging_tool == 'fpm':
                    requirements['package_tools'].append('fpm')
                elif config.linux_packaging_tool == 'nfpm':
                    requirements['package_tools'].append('nfpm')

    def _analyze_package_types(self, config, requirements):
        """分析包类型需求"""
        # 检查是否启用Linux包生成
        if hasattr(config, 'generate_linux_packages') and config.generate_linux_packages:
            if hasattr(config, 'linux_package_types'):
                for pkg_type in config.linux_package_types:
                    if pkg_type in ['deb', 'rpm']:
                        requirements['package_types'].append(pkg_type)

    def generate_requirements_code(self, config) -> str:
        """生成工具需求代码字符串，用于插入到构建脚本中"""
        requirements = self.analyze_requirements(config)
        
        # 过滤空列表
        filtered_requirements = {k: v for k, v in requirements.items() if v}
        
        if not filtered_requirements:
            return "required_tools = {}"
        
        # 生成代码字符串
        lines = ["required_tools = {"]
        for key, values in filtered_requirements.items():
            values_str = ", ".join([f"'{v}'" for v in values])
            lines.append(f"    '{key}': [{values_str}],")
        lines.append("}")
        
        return "\n            ".join(lines)

    def get_requirements_summary(self, config) -> str:
        """获取工具需求摘要，用于显示给用户"""
        requirements = self.analyze_requirements(config)
        
        summary_lines = []
        
        if requirements['build_tools']:
            tools = ", ".join(requirements['build_tools'])
            summary_lines.append(f"构建工具: {tools}")
        
        if requirements['system_tools']:
            tools = ", ".join(requirements['system_tools'])
            summary_lines.append(f"系统工具: {tools}")
            
        if requirements['package_tools']:
            tools = ", ".join(requirements['package_tools'])
            summary_lines.append(f"打包工具: {tools}")
            
        if requirements['package_types']:
            types = ", ".join([t.upper() for t in requirements['package_types']])
            summary_lines.append(f"包类型: {types}")
        
        if not summary_lines:
            return "无额外工具需求"
        
        return " | ".join(summary_lines)

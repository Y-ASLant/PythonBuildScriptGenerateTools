# -*- coding: utf-8 -*-
"""
Nuitka插件配置模块
基于官方 nuitka --plugin-list 输出
"""

# 官方Nuitka插件列表
NUITKA_PLUGINS = [
    # GUI框架插件
    ("pyqt5", "PyQt5 GUI框架"),
    ("pyqt6", "PyQt6 GUI框架"),
    ("pyside2", "PySide2 GUI框架"),
    ("pyside6", "PySide6 GUI框架"),
    ("tk-inter", "Python Tkinter GUI支持"),
    ("kivy", "Kivy跨平台GUI框架"),
    # 科学计算和数据处理
    ("matplotlib", "Matplotlib绘图库"),
    ("multiprocessing", "Python多进程模块支持"),
    # 网络和异步
    ("eventlet", "Eventlet异步网络库"),
    ("gevent", "Gevent异步网络库"),
    # Web相关
    ("pywebview", "PyWebView Web视图组件"),
    ("playwright", "Playwright浏览器自动化"),
    # 机器学习和AI
    ("spacy", "SpaCy自然语言处理"),
    ("transformers", "Transformers机器学习库"),
    # 3D和游戏
    ("glfw", "OpenGL和GLFW支持"),
    # 系统和工具
    ("upx", "UPX二进制压缩"),
    ("delvewheel", "Delvewheel包支持"),
    # 兼容性插件
    ("dill-compat", "Dill和CloudPickle兼容性"),
    ("enum-compat", "Python2 enum包兼容性"),
    ("pbr-compat", "PBR包兼容性"),
    ("pkg-resources", "pkg_resources支持"),
    # 其他工具
    ("pmw-freezer", "Pmw包支持"),
    ("pylint-warnings", "PyLint/PyDev标记支持"),
    # 自定义插件选项
    ("__custom__", "🔧 自定义插件 (手动输入插件名)"),
]


def get_plugin_list():
    """获取插件列表"""
    return NUITKA_PLUGINS.copy()


def get_plugin_names():
    """获取所有插件名称列表"""
    return [plugin[0] for plugin in NUITKA_PLUGINS]


def get_plugin_description(plugin_name):
    """根据插件名称获取描述"""
    for name, desc in NUITKA_PLUGINS:
        if name == plugin_name:
            return desc
    return None


def is_valid_plugin(plugin_name):
    """检查插件名称是否有效"""
    return plugin_name in get_plugin_names()

# -*- coding: utf-8 -*-

"""
Nuitka打包脚本生成器CLI程序入口
用于交互式生成Nuitka编译脚本
"""

from app.builder import NuitkaScriptBuilder


def main():
    """主函数"""
    builder = NuitkaScriptBuilder()
    builder.run()


if __name__ == "__main__":
    main()

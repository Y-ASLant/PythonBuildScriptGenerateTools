# -*- coding: utf-8 -*-
"""
输入处理模块 - 提供统一的用户输入处理功能
"""

from loguru import logger


class InputHandlers:
    """用户输入处理器集合"""

    @staticmethod
    def get_yes_no_input(prompt: str, default: str = "n") -> bool:
        """获取是/否输入"""
        while True:
            response = input(f"{prompt} (y/n, 默认{default}): ").strip().lower()
            if not response:
                response = default

            if response in ["y", "yes", "是"]:
                return True
            elif response in ["n", "no", "否"]:
                return False
            else:
                logger.error("❌ 请输入 y 或 n")

    @staticmethod
    def get_choice_input(prompt: str, choices: dict, default: str = None) -> str:
        """获取选择输入"""
        # 显示选项
        for key, desc in choices.items():
            logger.info(f"{key}. {desc}")

        while True:
            choice = input(f"{prompt} (默认{default}): ").strip()
            if not choice and default:
                choice = default

            if choice in choices:
                return choice
            else:
                valid_choices = ", ".join(choices.keys())
                logger.error(f"❌ 请输入有效选项 ({valid_choices})")

    @staticmethod
    def get_text_input(prompt: str, default: str = None, required: bool = False) -> str:
        """获取文本输入"""
        while True:
            if default:
                text = input(f"{prompt} (默认: {default}): ").strip()
                if not text:
                    text = default
            else:
                text = input(f"{prompt}: ").strip()

            if required and not text:
                logger.error("❌ 此项不能为空")
                continue

            return text

    @staticmethod
    def get_integer_input(
        prompt: str, default: int = None, min_value: int = None
    ) -> int:
        """获取整数输入"""
        while True:
            if default is not None:
                value_str = input(f"{prompt} (默认: {default}): ").strip()
                if not value_str:
                    return default
            else:
                value_str = input(f"{prompt}: ").strip()

            try:
                value = int(value_str)
                if min_value is not None and value < min_value:
                    logger.error(f"❌ 请输入大于等于{min_value}的数字")
                    continue
                return value
            except ValueError:
                logger.error("❌ 请输入有效的数字")

    @staticmethod
    def get_list_input(prompt: str, separator: str = ",") -> list[str]:
        """获取列表输入"""
        text = input(f"{prompt}: ").strip()
        if not text:
            return []

        return [item.strip() for item in text.split(separator) if item.strip()]

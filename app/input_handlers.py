# -*- coding: utf-8 -*-
"""
输入处理模块 - 提供统一的用户输入处理功能
"""

from .logger_utils import log_info, log_error


class InputHandlers:
    """用户输入处理器集合"""

    @staticmethod
    def get_yes_no_input(prompt: str, default: str = "n", help_text: str = None) -> bool:
        """获取是/否输入"""
        while True:
            display_prompt = f"{prompt} (y/n, 默认{default})"
            
            response = input(f"{display_prompt}: ").strip().lower()
            
            # 处理帮助请求（支持中英文问号）
            if response in ["?", "？"] and help_text:
                log_info(f"💡 {help_text}")
                continue
            
            if not response:
                response = default

            if response in ["y", "yes", "是"]:
                return True
            elif response in ["n", "no", "否"]:
                return False
            else:
                log_error("❌ 请输入 y 或 n")

    @staticmethod
    def get_choice_input(prompt: str, choices: dict, default: str = None, help_text: str = None) -> str:
        """获取选择输入"""
        # 显示选项
        for key, desc in choices.items():
            log_info(f"{key}. {desc}")

        while True:
            display_prompt = f"{prompt} (默认{default})"
            
            choice = input(f"{display_prompt}: ").strip()
            
            # 处理帮助请求（支持中英文问号）
            if choice in ["?", "？"] and help_text:
                log_info(f"💡 {help_text}")
                continue
            
            if not choice and default:
                choice = default

            if choice in choices:
                return choice
            else:
                valid_choices = ", ".join(choices.keys())
                log_error(f"❌ 请输入有效选项 ({valid_choices})")

    @staticmethod
    def get_text_input(prompt: str, default: str = None, required: bool = False, help_text: str = None) -> str:
        """获取文本输入"""
        while True:
            if default:
                display_prompt = f"{prompt} (默认: {default})"
            else:
                display_prompt = prompt
            
            text = input(f"{display_prompt}: ").strip()
            
            # 处理帮助请求（支持中英文问号）
            if text in ["?", "？"] and help_text:
                log_info(f"💡 {help_text}")
                continue
            
            if not text and default:
                text = default

            if required and not text:
                log_error("❌ 此项不能为空")
                continue

            return text

    @staticmethod
    def get_integer_input(
        prompt: str, default: int = None, min_value: int = None, help_text: str = None
    ) -> int:
        """获取整数输入"""
        while True:
            if default is not None:
                display_prompt = f"{prompt} (默认: {default})"
            else:
                display_prompt = prompt
            
            value_str = input(f"{display_prompt}: ").strip()
            
            # 处理帮助请求（支持中英文问号）
            if value_str in ["?", "？"] and help_text:
                log_info(f"💡 {help_text}")
                continue
            
            if not value_str and default is not None:
                return default

            try:
                value = int(value_str)
                if min_value is not None and value < min_value:
                    log_error(f"❌ 请输入大于等于{min_value}的数字")
                    continue
                return value
            except ValueError:
                log_error("❌ 请输入有效的数字")

    @staticmethod
    def get_list_input(prompt: str, separator: str = ",", help_text: str = None) -> list[str]:
        """获取列表输入"""
        while True:
            display_prompt = prompt
            
            text = input(f"{display_prompt}: ").strip()
            
            # 处理帮助请求（支持中英文问号）
            if text in ["?", "？"] and help_text:
                log_info(f"💡 {help_text}")
                continue
            
            if not text:
                return []

            return [item.strip() for item in text.split(separator) if item.strip()]

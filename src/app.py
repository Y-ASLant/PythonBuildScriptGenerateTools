"""
主应用类
"""

import asyncio
from pathlib import Path
from typing import Literal
from textual.app import App
from textual.binding import Binding
from textual import events

from src.screens.welcome_screen import WelcomeScreen
from src.utils import load_config, save_config


SeverityLevel = Literal["information", "warning", "error"]


class PyBuildTUI(App):
    """Python 构建脚本生成器 TUI 应用"""

    TITLE = "Python Build Script Generator"
    SUB_TITLE = "跨平台Python编译脚本生成器"

    ENABLE_COMMAND_PALETTE = False

    # 通知配置
    NOTIFICATION_TIMEOUT = 1.5  # 通知显示时长（秒）

    # Toast 通知样式：定位到右上角
    CSS = """
    ToastRack {
        dock: top;
        width: auto;
        height: auto;
    }

    Button,
    Link,
    ListItem,
    Select,
    SelectionList,
    Switch,
    Tab {
        pointer: pointer;
    }

    Input,
    MarkdownViewer {
        pointer: text;
    }
    """

    # 主题映射表：键位 -> 主题名
    THEME_MAP = {
        "f1": "textual-dark",
        "f2": "gruvbox",
        "f3": "dracula",
        "f4": "monokai",
        "f5": "flexoki",
        "f6": "tokyo-night",
        "f7": "catppuccin-latte",
        "f8": "textual-light",
    }

    BINDINGS = [
        Binding("ctrl+c", "quit", "退出", priority=True),
        Binding("ctrl+p", "noop", show=False, priority=True),
    ] + [
        Binding(key, f"set_theme('{theme}')", theme, priority=True)
        for key, theme in THEME_MAP.items()
    ]

    def __init__(self):
        super().__init__()

        # 项目配置
        self.project_dir: Path | None = None  # 选中的项目目录
        self.build_mode: str | None = None  # 构建模式: simple, full, expert

        # 加载配置
        self.config = load_config()
        self.initial_theme = self.config["theme"]

    def on_mount(self) -> None:
        """应用启动时调用"""
        # 设置启动主题
        self.theme = self.initial_theme
        self.push_screen(WelcomeScreen())

    def notify(
        self,
        message: str,
        *,
        title: str = "",
        severity: SeverityLevel = "information",
        timeout: float | None = None,
        markup: bool = True,
    ) -> None:
        """重写 notify 方法以设置自定义显示时长"""
        # 使用自定义超时时间，如果未指定则使用默认值
        if timeout is None:
            timeout = self.NOTIFICATION_TIMEOUT

        # 调用父类的 notify 方法
        super().notify(
            message, title=title, severity=severity, timeout=timeout, markup=markup
        )

    # 主题切换
    def action_set_theme(self, theme: str) -> None:
        """统一主题切换动作"""
        self.theme = theme
        try:
            self.notify(f"已切换主题: {theme}", severity="information")
        except Exception:
            pass
        # 异步保存配置，不阻塞 UI
        asyncio.create_task(self._async_save_theme_to_config(theme))

    def on_key(self, event: events.Key) -> None:
        """全局按键处理：F1..F8 切换主题"""
        theme = self.THEME_MAP.get(event.key)
        if theme:
            self.action_set_theme(theme)
            event.stop()

    def action_noop(self) -> None:
        """空动作：用于屏蔽默认 Ctrl+P 行为"""
        return

    async def _async_save_theme_to_config(self, theme: str) -> None:
        """异步将主题写入配置文件"""
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None, lambda: save_config({**self.config, "theme": theme})
            )
        except Exception:
            pass

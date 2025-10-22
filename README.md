# Python 构建脚本生成器-待重构（使用TUI）

智能化 Python 打包工具，支持 Nuitka 和 PyInstaller，一键生成**完全独立**的构建脚本。

> 🎯 **核心优势**: 生成的 `build.py` 脚本完全独立，可在任何设备上直接运行，无需依赖本项目！

## ✨ 核心特性

- **📦 完全独立** - 生成的脚本零依赖，可在任何设备运行
- **🔍 智能检查** - 自动检测环境和工具依赖，确保构建成功
- **🚀 双引擎支持** - Nuitka (性能优先) / PyInstaller (兼容性优先)
- **💡 智能帮助** - 任意位置输入 `?` 获取详细说明
- **🔧 多编译器** - MinGW64、MSVC、Clang 全支持
- **📦 Linux 打包** - 自动生成 DEB/RPM 安装包 (NFPM/FPM)
- **🧹 自动清理** - 构建完成后清理临时文件

## 🚀 快速开始

### 安装依赖
```bash
# 推荐使用 uv (更快更现代)
uv venv

# 或使用传统 pip
pip install -r requirements.txt
```

### 运行程序
```bash
# 1. 启动交互式配置
uv run main.py

# 2. 执行生成的构建脚本 (完全独立!)
uv run build.py  # 推荐使用 uv
# 或 python build.py  # 可在任何设备运行
```

## 📋 使用流程

1. **选择模式** - 完整模式 / 编译模式 / 打包模式
2. **配置参数** - 构建工具、入口文件、输出设置
3. **选择插件** - 14种常用插件 (PyQt、NumPy、Pandas等)
4. **生成脚本** - 自动生成 `build.py` 构建脚本
5. **执行构建** - 运行脚本完成打包

### 💡 智能帮助
任何输入提示处输入 `?` 获取详细说明：
```bash
📂 请输入项目根目录 (默认: .): ?
💡 请输入需要打包的Python项目的根目录路径...
```

### 📦 Linux 包生成
支持 NFPM (推荐) 和 FPM 两种工具：
```bash
# 安装 NFPM (推荐)(支持Windows/MacOS/Debian系/Redhat系基于Go语言)
go install github.com/goreleaser/nfpm/v2/cmd/nfpm@latest

# 或安装 FPM(主要支持Linux/MacOS，Windows支持有限，基于Ruby语言)
sudo gem install fpm
```

## 🔌 支持插件（Nuitka）

**GUI 框架**: PyQt5/6, PySide2/6, Tkinter  
**科学计算**: NumPy, SciPy, Pandas, Matplotlib  
**其他库**: Pillow, Requests, SQLAlchemy, Multiprocessing

## 📝 生成脚本示例

**🎯 独立脚本优势**：
- **零依赖运行** - 只需 Python 标准库，无需安装本项目
- **跨设备部署** - 可复制到服务器、CI/CD、其他开发环境
- **智能环境检查** - 自动检测工具依赖，确保打包顺利进行
- **完整功能** - 包含环境检查、构建、清理、Linux打包全流程
- **自包含逻辑** - 所有必要代码都内嵌在生成的脚本中

### Nuitka 参数示例
```python
args = ["nuitka", "--standalone", "--onefile", "--mingw64", 
        "--output-dir=dist", "--enable-plugin=pyqt5", "main.py"]
```

### PyInstaller 参数示例  
```python
args = ["pyinstaller", "--onefile", "--windowed", "--name=app",
        "--icon=app.ico", "--add-data=data;data", "main.py"]
```

## ❓ 常见问题

**Q: 不知道选项含义？**  
A: 任意输入提示处输入 `?` 查看详细说明

**Q: 编译失败找不到编译器？**  
A: 确保已安装 MinGW64/MSVC/Clang 编译器

**Q: 生成的文件很大？**  
A: 独立打包包含 Python 运行时，可使用 UPX 压缩

**Q: 运行时缺少模块？**  
A: 检查插件设置或添加隐藏导入

**Q: Linux 包生成失败？**  
A: 先安装 NFPM 或 FPM 打包工具

**Q: 在新设备上运行 build.py 有什么保障？**  
A: 脚本内置环境检查，会自动检测所需工具并给出安装建议

## 📄 许可证

MIT License © 2025 ASLant

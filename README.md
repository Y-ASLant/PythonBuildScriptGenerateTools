# 交互式 Python打包脚本生成器

一个功能强大的交互式CLI程序，支持Nuitka和PyInstaller两种打包工具，提供完整的帮助系统，简化Python应用程序的打包过程。

## 功能特性

- 🚀 **交互式界面** - 友好的命令行交互体验，支持键盘导航
- ❓ **完整帮助系统** - 在任何输入提示处输入 `?` 可查看详细帮助，支持中英文问号
- 🛠️ **双工具支持** - 支持Nuitka和PyInstaller两种打包工具
- 📁 **智能文件选择** - 自动验证入口文件和图标文件
- 🔧 **多编译器支持** - Nuitka支持MinGW64、MSVC、Clang
- 🖥️ **控制台选项** - 可选择是否显示控制台窗口
- 📦 **打包模式** - 支持独立打包和单文件打包
- 🎨 **图标支持** - 支持ICO格式图标文件
- 🔌 **插件系统** - 支持14种常用插件选择（PyQt5/6、PySide2/6等）
- 📝 **Python脚本生成** - 生成完整的Python构建脚本
- 📁 **文件复制功能** - 自动复制资源目录和UI文件
- ⚡ **多线程编译** - 可配置编译线程数
- 🏢 **企业级选项** - 支持公司名称和版本信息
- 🎯 **交互式菜单** - 支持上下键导航、空格选择的多选菜单
- 🎨 **彩色界面** - 支持ANSI颜色显示，增强用户体验
- 📦 **双工具Linux包生成** - 支持NFPM和FPM两种工具，生成 deb/rpm 安装包
- ⏸️ **用户友好** - 程序结束前暂停，方便查看结果

## 安装要求

```bash
# 使用uv安装依赖（推荐）
uv sync

# 或使用pip安装
pip install nuitka>=2.7.12 pyinstaller>=6.15.0 setuptools>=80.9.0 loguru>=0.7.3
```

## 使用方法

### 1. 运行CLI程序

```bash
# 使用uv运行（推荐）
uv run main.py

# 或直接运行
python main.py
```

### 2. 使用帮助系统

程序启动后会显示帮助提示：
```
========================================================================================================================

                                      Python打包脚本生成器@ASLant

                                      💡 在任何输入提示处输入 ? 可查看详细帮助

========================================================================================================================
```

在任何输入提示处输入 `?` 或 `？` 可查看该选项的详细说明，例如：
```bash
📂 请输入项目根目录 (默认: .): ?
💡 请输入需要打包的Python项目的根目录路径。这是包含您的Python代码和相关文件的主目录。可以是绝对路径或相对路径，默认为当前目录(.)
```

### 3. 按提示输入配置信息

程序会依次询问以下配置：

- **构建工具**: 选择Nuitka或PyInstaller
- **入口文件**: Python主程序文件路径
- **应用名称**: 生成的可执行文件名称
- **图标文件**: 应用程序图标（支持.ico格式）
- **编译器**: 选择编译器（MinGW64/MSVC/Clang，仅Nuitka）
- **控制台**: 是否显示控制台窗口
- **输出目录**: 编译输出目录
- **打包模式**: 独立打包或单文件打包
- **单文件模式**: 是否启用单文件模式
- **公司名称**: 可执行文件的公司信息（可选）
- **文件版本**: 可执行文件版本号
- **编译线程**: 并行编译的线程数（仅Nuitka）
- **插件选择**: 使用交互式菜单选择插件
- **复制目录**: 需要复制到输出目录的资源文件夹
- **PyInstaller特有选项**: 数据文件、隐藏导入、UPX压缩等

### 4. 生成Python构建脚本

程序会自动生成 `build.py` 脚本文件，包含完整的构建逻辑和文件复制功能，支持Nuitka和PyInstaller两种工具。

### 5. 执行编译

运行生成的Python脚本：

```bash
# 使用uv运行（推荐）
uv run build.py

# 或直接运行
python build.py
```

### 6. 生成Linux安装包（可选）

如果需要将可执行文件打包成 deb 或 rpm 安装包：

```bash
# 方法1：完整模式（推荐）- 一键完成编译和Linux包生成
uv run main.py
# 选择 "1. 完整模式" 并启用Linux包生成

# 方法2：打包模式 - 仅为已有可执行文件生成Linux包
uv run main.py  
# 选择 "3. 打包模式"
```

**支持双打包工具**：
- **NFPM**（推荐，默认）：跨平台支持Windows/macOS/Linux，高性能，Go编写，无依赖
- **FPM**：功能全面，成熟稳定，Ruby编写，但在Windows上支持有限

**安装打包工具**：

**NFPM 安装**（推荐）：
```bash
# 跨平台 - 方法2：使用Go安装
go install github.com/goreleaser/nfpm/v2/cmd/nfpm@latest

# Linux/macOS - 方法1：使用安装脚本
curl -sfL https://install.goreleaser.com/github.com/goreleaser/nfpm.sh | sh

# Windows - 方法3：使用Chocolatey
choco install nfpm

# 跨平台 - 方法4：下载预编译二进制文件
# 访问 https://github.com/goreleaser/nfpm/releases
# 下载对应平台的可执行文件（Windows: nfpm.exe）
```

**FPM 安装**：
```bash
# Ubuntu/Debian
sudo apt-get install ruby ruby-dev rubygems build-essential
sudo gem install --no-document fpm

# CentOS/RHEL/Fedora
sudo yum install ruby ruby-devel rubygems rpm-build
sudo gem install --no-document fpm
```

## 插件支持

程序支持14种常用插件，分为三个类别：

### 📱 GUI框架插件
- **PyQt5** - PyQt5 GUI框架 (推荐)
- **PyQt6** - PyQt6 GUI框架
- **PySide2** - PySide2 GUI框架
- **PySide6** - PySide6 GUI框架 (推荐)
- **tk-inter** - Tkinter GUI支持

### 🔬 科学计算库
- **numpy** - NumPy数值计算库
- **scipy** - SciPy科学计算库
- **pandas** - Pandas数据分析库
- **matplotlib** - Matplotlib绘图库

### 🛠️ 其他常用库
- **pillow** - Pillow图像处理库
- **requests** - Requests HTTP库
- **sqlalchemy** - SQLAlchemy数据库ORM
- **multiprocessing** - 多进程支持
- **eventlet** - Eventlet异步网络库

## 示例

运行程序的完整示例：

1. 运行 `uv run main.py` 或 `python main.py`
2. 选择运行模式：
   - `1` - 完整模式（编译 + Linux包生成，推荐）
   - `2` - 编译模式（仅生成编译脚本）
   - `3` - 打包模式（仅生成Linux包脚本）
3. 查看帮助提示，了解可以使用 `?` 获取帮助
4. 选择构建工具: `1` (Nuitka) 或 `2` (PyInstaller)
5. 输入入口文件: `main.py`（如不确定可输入 `?` 查看帮助）
6. 选择是否启用额外插件: `y`
7. 使用交互式菜单选择插件（上下键导航，空格选择，回车确认）
8. 按提示完成其他配置（任何不清楚的选项都可以输入 `?` 查看详细说明）
9. 运行生成的 `uv run build.py` 或 `python build.py`
10. （可选）如果选择了完整模式并启用Linux包生成，会自动生成 deb/rpm 安装包

## 生成的Python脚本示例

生成的`build.py`脚本包含：
- 完整的构建参数配置（Nuitka或PyInstaller）
- 自动文件和目录复制功能
- 错误处理和进度显示
- UI文件(.ui)自动复制
- 资源目录批量复制
- 版本信息文件生成（PyInstaller）

### Nuitka示例
```python
args = [
    "nuitka",
    "--standalone",
    "--onefile",
    "--assume-yes-for-downloads",
    "--mingw64",
    "--show-progress",
    "--show-memory",
    "--windows-company-name=aslant.top",
    "--windows-file-version=1.0.0",
    "--output-dir=dist",
    "--output-filename=main",
    "--jobs=4",
    "--windows-icon-from-ico=app.ico",
    "--enable-plugin=pyqt5",
    "main.py",
]
```

### PyInstaller示例
```python
args = [
    "pyinstaller",
    "--onefile",
    "--windowed",
    "--name=main",
    "--distpath=dist",
    "--workpath=build",
    "--icon=app.ico",
    "--version-file=version_info.txt",
    "--add-data=data;data",
    "--hidden-import=requests",
    "main.py",
]
```

## 支持的配置选项

### 通用选项
| 选项 | 描述 | 默认值 | 适用工具 |
|------|------|--------|----------|
| 构建工具 | 选择Nuitka或PyInstaller | Nuitka | 通用 |
| 入口文件 | Python主程序文件 | 必填 | 通用 |
| 应用名称 | 可执行文件名称 | 入口文件名 | 通用 |
| 图标文件 | 应用程序图标（.ico格式） | 无 | 通用 |
| 显示控制台 | 是否显示控制台 | 是 | 通用 |
| 输出目录 | 编译输出目录 | dist | 通用 |
| 独立打包 | 是否创建独立可执行文件 | 是 | 通用 |
| 单文件模式 | 是否启用单文件模式 | 是 | 通用 |
| 启用插件 | 是否启用额外插件 | 否 | 通用 |
| 公司名称 | 可执行文件公司信息 | 无 | 通用 |
| 文件版本 | 可执行文件版本 | 1.0.0 | 通用 |
| 复制目录 | 需要复制的资源目录 | 无 | 通用 |

### Nuitka专用选项
| 选项 | 描述 | 默认值 |
|------|------|--------|
| 编译器 | 编译器选择（MinGW64/MSVC/Clang） | MinGW64 |
| 编译线程 | 并行编译线程数 | 4 |
| 显示进度条 | 是否显示编译进度 | 是 |
| 移除构建文件 | 编译后是否清理临时文件 | 是 |

### PyInstaller专用选项
| 选项 | 描述 | 默认值 |
|------|------|--------|
| 数据文件 | 添加数据文件到打包 | 无 |
| 隐藏导入 | 指定隐藏的导入模块 | 无 |
| 收集所有子模块 | 收集指定包的所有子模块 | 无 |
| UPX压缩 | UPX压缩工具路径 | 无 |
| 调试模式 | 启用调试信息 | 否 |
| 清理临时文件 | 构建后清理临时文件 | 是 |

## 注意事项

### 通用注意事项
1. **帮助系统**: 在任何输入提示处输入 `?` 或 `？` 可查看详细帮助说明
2. **构建工具选择**: Nuitka性能更好但编译时间长，PyInstaller兼容性更好打包速度非常快
3. **依赖处理**: 两种工具都会自动处理大部分Python依赖
4. **插件支持**: 可选择启用14种常用插件，包括GUI框架和科学计算库
5. **文件路径**: 支持相对路径和绝对路径
6. **图标格式**: 支持ICO格式图标文件
7. **资源复制**: 自动复制指定目录和.ui文件到输出目录
8. **交互式菜单**: 支持键盘导航，在不支持的终端会自动降级到文本输入
9. **用户体验**: 程序完成后会暂停，按任意键退出

### Nuitka特有注意事项
1. **编译器要求**: 确保系统已安装选择的编译器（MinGW64/MSVC/Clang）
2. **多线程编译**: 根据CPU核心数调整编译线程数以提高速度
3. **内存使用**: 编译过程可能消耗大量内存，建议关闭不必要程序

### PyInstaller特有注意事项
1. **版本信息**: 自动生成Windows版本信息文件，解决exe文件属性显示问题
2. **UPX压缩**: 可选择UPX压缩减小文件大小，需要单独安装UPX工具
3. **隐藏导入**: 对于动态导入的模块，需要手动指定隐藏导入

## 故障排除

### 常见问题

**Q: 不知道某个选项的含义怎么办？**
A: 在任何输入提示处输入 `?` 或 `？` 可查看该选项的详细说明和使用建议

**Q: 编译失败，提示找不到编译器（Nuitka）**
A: 确保已安装MinGW64、MSVC或Clang编译器

**Q: 生成的exe文件很大**
A: 这是正常的，独立打包会包含Python运行时。可尝试UPX压缩（PyInstaller）

**Q: 程序运行时缺少模块**
A: Nuitka检查插件设置；PyInstaller添加隐藏导入或使用--collect-all参数

**Q: 资源文件找不到**
A: 确保在配置时正确指定了需要复制的目录或数据文件

**Q: 编译速度慢（Nuitka）**
A: 可以增加编译线程数，但不要超过CPU核心数

**Q: PyInstaller打包的exe没有版本信息**
A: 程序会自动生成version_info.txt文件解决此问题

**Q: 交互式菜单不工作**
A: 程序会自动降级到文本输入模式，功能不受影响

**Q: 选择工具的建议**
A: 追求性能选Nuitka，追求兼容性和快速打包选PyInstaller

**Q: 帮助功能不工作**
A: 确保输入的是英文问号 `?` 或中文问号 `？`，程序支持两种问号

**Q: Linux包生成失败，提示FPM未安装**
A: 需要先安装FPM工具，参考安装命令：Ubuntu/Debian系统安装ruby和gem，然后gem install fpm

**Q: 生成的deb/rpm包无法安装**
A: 检查包的依赖关系，确保目标系统满足运行时依赖；检查安装路径权限

**Q: 如何自定义Linux包的安装路径**
A: 在Linux包生成过程中会询问安装路径，默认为/usr/local/bin，可以修改为其他路径

**Q: deb包安装时提示"missing final newline"错误**
A: 这是包描述格式问题，运行 `python fix_linux_packages.py` 重新生成正确格式的包

**Q: Windows可执行文件能在Linux上运行吗？**
A: 不能直接运行。需要在Linux环境下重新编译，或者安装Wine来运行Windows程序

## 许可证

MIT License

Copyright (c) 2025 ASLant

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

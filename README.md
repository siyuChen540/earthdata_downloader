# 🌐 **Earthdata Downloader**

![License](https://img.shields.io/github/license/SiyuChen540/earthdata_downloader)
![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
![Downloads](https://img.shields.io/github/downloads/SiyuChen540/earthdata_downloader/total)
![Build Status](https://img.shields.io/github/actions/workflow/status/SiyuChen540/earthdata_downloader/ci.yml?branch=main)

## 📢 介绍

**Earthdata Downloader** 是一个强大且易于使用的 Python 脚本，用于从 [NASA Earthdata](https://earthdata.nasa.gov/) 自动化下载海量数据。无论您是科学研究人员、数据分析师还是地理信息系统（GIS）爱好者，这个工具都能极大地简化您的数据获取流程。

## 🚀 特性

- **自动认证与重定向处理**：智能处理登录后的网页跳转，确保稳定下载。
- **断点续传与重试机制**：在网络不稳定或下载失败时自动重试，确保数据完整性。
- **高效的进度显示**：集成 `tqdm` 进度条，实时展示下载进度。
- **灵活的命令行接口**：通过 `argparse` 提供丰富的命令行选项，满足多样化需求。
- **详细的日志记录**：记录下载过程中的所有重要信息，便于排查问题。
- **Pythonic 代码结构**：遵循最佳实践，代码清晰易读，易于维护和扩展。

## 📁 目录

- [📢 介绍](#-介绍)
- [🚀 特性](#-特性)
- [📁 目录](#-目录)
- [🛠️ 安装](#️-安装)
- [⚙️ 使用方法](#️-使用方法)
  - [基本用法](#基本用法)
  - [示例](#示例)
- [🔧 依赖](#-依赖)
- [🤝 贡献](#-贡献)
- [📜 许可证](#-许可证)
- [📫 联系我们](#-联系我们)

## 🛠️ 安装

确保您的系统已安装 [Python 3.10](https://www.python.org/downloads/) 及以上版本。

1. **克隆仓库**

   ```bash
   git clone [https://github.com/yourusername/earthdata-downloader.git](https://github.com/siyuChen540/earthdata_downloader)
   cd earthdata-downloader
   ```
2. **创建虚拟环境（可选但推荐）**
   ```bash
   conda create --name downloader_env python==3.12.0
   conda activate downloader_env
   ```
3. **安装依赖**
## ⚙️ 使用方法
### 基本用法
运行脚本并提供必要的参数：
```bash
python downloader.py --save-dir <保存目录> \
                    --username <你的用户名> \
                    --password <你的密码> \
                    --txt-dir <下载链接文件路径>
```
### 参数说明
<ul>
  <li><code>--save-dir</code>：指定下载文件的保存目录。</li>
  <li><code>--username</code>：您的 Earthdata 用户名。</li>
  <li><code>--password</code>：您的 Earthdata 密码。</li>
  <li><code>--txt-dir</code>：包含下载链接的文本文件路径。文件中每行一个 URL。</li>
</ul>

### 实例
```ruby
https://example.com/data/file1.nc
https://example.com/data/file2.nc
https://example.com/data/file3.nc
```
运行以下命令开始下载：
```bash
python downloader.py --save-dir ./downloads \
                    --username myEarthdataUser \
                    --password mySecurePassword \
                    --txt-dir ./urls.txt
```

## 🔧 依赖
本项目依赖以下 Python 库：
- [requests](https://pypi.org/project/requests/)
- [pandas](https://pypi.org/project/pandas/)
- [tqdm](https://pypi.org/project/tqdm/)
- [logging](https://docs.python.org/3/library/logging.html)

您可以通过以下命令安装所有依赖：
```bash
pip install -r requirements.txt
```

## 🤝 贡献
欢迎贡献！请遵循以下步骤：
**1. Fork 本仓库**
**2. 创建特性分支**
```bash
git checkout -b feature/YourFeature
```
**3. 提交更改**
```bash
git commit -m "Add some feature"
```
**4. 推送到分支**
```bash
git push origin feature/YourFeature
```
**5. 创建 Pull Request**

确保您的代码遵循 [PEP 8](https://pep8.org/) 规范，并包含适当的测试和文档。

## 📜 许可证
此项目采用 MIT 许可证。

## 📫 联系我们
如果您有任何问题或建议，欢迎通过以下方式联系我：
- 邮箱: chensy57@mail2.sysu.edu.cn
- GitHub: [SiyuChen540](https://github.com/SiyuChen540)

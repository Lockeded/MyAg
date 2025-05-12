# MyAg：好玩的命令行助手 🤖

 `MyAg` 灵感来自`jyy`老师的 [操作系统原理](https://www.bilibili.com/video/BV1XZAbeqEyt)，他在终端上输入 `ag` 就能把一个大模型叫出来问问题，这让我感觉很有趣，于是我动手实现了一个自己的`ag`命令—— `MyAg`。
 
 这是一个在`Linux`平台，基于 [智谱清言](https://open.bigmodel.cn/) 提供的 `GLM-4-Flash` 免费模型的命令行助手，具备**上下文记忆**能力，支持**附加文件**辅助对话，为日常开发、学习与工作提供帮助，同时挺好玩的。

## ✨ 主要功能

- 📜 支持上下文对话
- 📎 支持附加文件参与推理
- 🧠 自动保存历史记录
- ⚡ 流式输出体验，丝滑

## 📦 下载

点击右侧 👉 [Release](https://github.com/Lockeded/MyAg/releases/download/Linux/ag) 下载 `ag` 可执行文件。

## 🔧 安装方式（推荐）

将 `ag` 放入你的系统 `$PATH` 路径中，例如：

```bash
chmod +x ag  # 添加可执行权限
sudo mv ag /usr/local/bin/ag  # 移动到 PATH 中
```

之后你就可以在任意位置使用，像这样：

```bash
locked@Locked:~$ ag
👇💬~
👴:
```
支持附加文件对话：
```bash
ag --file main.py
```

## 🔐 API Key 设置

`MyAg` 使用的是智谱 API 服务，需要你提前设置环境变量：

```bash
export ZHIPU_API_KEY=你的-api-key
```
建议写入 `~/.bashrc` 或 `~/.zshrc`：

```bash
echo 'export ZHIPU_API_KEY=你的-key' >> ~/.bashrc
source ~/.bashrc
```

## 📁 项目结构

```
MyAg/
├── ag.py # 程序入口，启动助手
├── chat.py # 对话逻辑实现
├── requirements.txt # 依赖列表
├── README.md
├── history/ # 存储上下文
```
## 🚀 从源码安装

```bash
git clone https://github.com/Lockeded/MyAg.git
cd MyAg
pip install -r requirements.txt
python ag.py
```

## 🧠 使用别的模型

`MyAg`  默认使用的是智谱的免费模型 GLM-4-Flash，已支持流式输出与上下文记忆。

如果你想接入其他模型，也可以修改 `chat.py` 中的大模型接入逻辑，应该会很简单。

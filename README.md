# 🦜✨ LangChain-Book

## 环境安装

### 安装 JupyterLab

要安装 JupyterLab，你可以使用 Python 的包管理器 pip。在你的命令行中运行以下命令：

```bash
pip install jupyterlab
```

如果你正在使用一个特定的 Python 虚拟环境，或者你想要为一个特定的 Python 项目安装 JupyterLab，你应该在那个环境中运行这个命令。

如果你正在使用 Poetry 来管理你的 Python 项目，你可以使用以下命令来安装 JupyterLab：

```bash
poetry add jupyterlab
```

安装完成后，你可以通过在命令行中运行 `jupyter lab` 来启动 JupyterLab。

### 在 JupyterLab 中使用专门的 ipykernel

要在 Poetry 环境中创建一个 JupyterLab 可用的 kernel，你需要先确保你已经安装了 `ipykernel` 包。你可以使用以下命令在你的 Poetry 环境中安装 `ipykernel`：

```bash
poetry add ipykernel
```

然后，你可以使用以下命令在你的 Poetry 环境中创建一个新的 Jupyter kernel：

```bash
poetry run python -m ipykernel install --user --name=langchain_book_kernel
```

在这个命令中，`langchain_book_kernel` 是你的新 kernel 的名称，你可以根据你的需要更改它。

现在，当你启动 JupyterLab 时，你应该能在 kernel 列表中看到你的新 kernel。你可以通过选择这个新 kernel 来在你的 Poetry 环境中运行 Jupyter notebook。
<h2 style="text-align:left"><b>基于Python的Ftp文件共享服务器</b></h2>

### 一、项目概述
本项目旨在使用Python语言搭建一个简单的Ftp文件共享服务器，实现文件的上传、下载以及基本的文件管理功能，方便用户在局域网或特定网络环境下进行文件的共享与交互。

### 二、项目特点
- **简单易用**：通过简洁的Python代码实现核心功能，易于理解和部署，即使对于初学者也能快速上手。
- **跨平台支持**：依托Python的跨平台特性，该服务器可以在多种操作系统（如Windows、Linux、macOS）上运行，满足不同用户的需求。
- **灵活定制**：代码结构清晰，方便开发者根据具体需求对服务器的功能进行扩展和定制，例如添加用户认证、权限管理等高级功能。

### 三、技术栈
- **编程语言**：Python
- **相关库**：[Pillow、pypiwin32、pyinstaller、nuitkapystray]

### 四、安装与部署

#### **（一）环境要求**
- Python 3.8版本

#### **（二）安装步骤**
1. ##### **克隆本项目仓库到本地**：
```bash
git clone https://github.com/dcyyd/ftp-server-based-on-python-master.git
```
2. ##### **进入项目目录**：
```bash
cd ftp-server-based-on-python-master
```
3. ##### **安装所需的**Python库：
```bash
pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com [依赖库列表]
```

#### **（三）启动服务器**
在完成上述安装步骤后，通过以下命令启动Ftp文件共享服务器：
```python
python ftpServer.py
```

### 五、使用方法

#### **（一）连接到服务器**
使用任何标准的Ftp客户端工具（如FileZilla、WinSCP等），按照以下配置连接到本服务器：
- **主机**：[服务器给的IP地址或域名，默认一般是127.0.0.1或localhost]
- **端口**：[服务器监听的Ftp端口，默认一般是21，若你有修改请注明]
- **用户名**：[如果有设置用户名，填写此处，若未设置可留空或使用默认值]
- **密码**：[如果有设置密码，填写此处，若未设置可留空或使用默认值]

#### **（二）文件操作**

连接成功后，即可在Ftp客户端中进行常规的文件操作，包括但不限于：
- **上传文件**：将本地文件上传到服务器指定的目录下。
- **下载文件**：从服务器下载文件到本地计算机。
- **浏览文件**：查看服务器上已有的文件和目录结构。

### 六、项目结构
#### **（一）本项目大致结构说明：**

```
ftp-server-based-on-python-master/
|-- __pycache__/
|   |-- （这里存放着一些编译后的Python字节码文件）
|-- mypyftpdlib/
|   |-- （该文件夹是 `mypyftpdlib` 库的相关文件，包含其模块、类定义等）
|--.gitignore	用于指定哪些文件或文件夹不需要被Git版本控制系统跟踪。
|-- FtpServer.json	用于配置FTP服务器相关设置的文件。
|-- LICENSE	项目的开源许可证文件。
|-- README.md	项目介绍文件
|-- Settings.py	存放项目的各种设置参数的Python模块。
|-- ftpServer.py	项目的主程序文件。
|-- ftpServers.ico	图标文件
|-- preview.png		项目预览图片
|-- requirements.txt	记录项目所依赖的外部库及其版本信息
```

#### **（二）项目效果图：**

<img src="https://img.picui.cn/free/2024/11/02/672621f3d6f33.png" alt="preview.png" title="preview.png" />

### 七、贡献指南

本项目欢迎大家的贡献！如果你有兴趣参与项目的改进、添加新功能或修复漏洞等，可以按照以下步骤进行：

#### **（一）Fork本项目**
在GitHub上点击项目页面的 `Fork` 按钮，将项目复制到你自己的仓库中。

#### **（二）创建分支**
在你Fork后的仓库中，创建一个新的分支用于开发，分支名称建议采用有意义的格式，如 `feature/user-login` 表示添加用户登录功能的分支。

#### **（三）提交代码**
在新分支上进行代码的修改和开发，完成后提交你的代码到该分支，并确保提交信息清晰明了，描述了所做的更改内容。

#### **（四）创建Pull Request**
回到项目的原始仓库页面，点击 `Pull Request` 按钮，填写相关信息并提交你的Pull Request，等待项目维护者的审核和合并。

### 八、常见问题解答

#### **（一）无法连接到服务器**
- 检查服务器是否已成功启动，查看启动脚本的输出是否有报错信息。
- 确认客户端配置的IP地址、端口、用户名和密码等信息是否正确。
- 确保服务器所在的网络环境允许Ftp连接，可能需要检查防火墙设置等。

#### **（二）文件上传/下载失败**
- 检查服务器的磁盘空间是否充足，可能是因为磁盘已满导致无法写入或读取文件。
- 查看服务器日志（如果有设置日志记录功能），以确定是否存在其他导致文件操作失败的原因，如权限问题等。

#### **（三）遇到其他问题**
- 如果遇到其他未在上述常见问题中提及的问题，可以在项目的GitHub issues页面上提交问题描述或用以下联系方式联系我，我们会尽快回复并帮助你解决。
### 九、联系我
如果你想与我联系，可以通过以下方式：
- webcat：dugu0528
- Phone：15139448615
- Email：dcyyd_kcug@yeah.net
- GitHub：https://github.io/dcyyd
### 十、许可证
本项目采用： **MIT开源协议** 进行授权，详情请查看项目根目录下的 `LICENSE` 文件。

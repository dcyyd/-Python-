import socket, sys, os, queue, time, base64, threading, ctypes, webbrowser, pystray

import tkinter
from tkinter import ttk, scrolledtext, filedialog

from mypyftpdlib.authorizers import DummyAuthorizer
from mypyftpdlib.handlers import FTPHandler
from mypyftpdlib.servers import ThreadedFTPServer

import Settings
from PIL import ImageTk, Image
from io import BytesIO

import win32clipboard
import win32con

# pip install Pillow pypiwin32 pyinstaller nuitka pystray

# 打包 单文件 隐藏终端窗口 pyinstaller.exe -F -w .\ftpServer.py -i .\ftpServers.ico nuitka --standalone --onefile
# --enable-plugin=tk-inter --windows-disable-console .\ftpServer.py --windows-icon-from-ico=.\ftpServers.ico
"""
import base64
with open(r"ftpServers.ico", "rb") as f:
    iconStr = base64.b64encode(f.read())
    print(iconStr)
"""


iconStr = ("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")

appName = "FTP Server"
appLabel = "FTP文件服务器"
appVersion = "v1.0.1"
appAuthor = "Dou ChangYou"
githubLink = "https://github.com/dcyyd/python_ftp_servers"
windowsTitle = appLabel + " " + appVersion + " By " + appAuthor
tipsTitle = ("若用户名空白则默认匿名访问(anonymous)。\n"
             "若中文乱码则需更换编码方式，再重启服务。\n"
             "请设置完后再开启服务。\n"
             "以下为本机所有IP地址，右键可复制。\n")

logMsg = queue.Queue()
logThreadrunning = True

permReadOnly = "elr"
permReadWrite = "elradfmwMT"

isSupportdIPv6 = False
isIPv4ThreadRunning = False
isIPv6ThreadRunning = False

settings = Settings.Settings()


def updateSettingVars():
    global settings
    global directoryCombobox
    global userNameVar
    global userPasswordVar
    global IPv4PortVar
    global IPv6PortVar
    global isReadOnlyVar
    global isGBKVar
    global isAutoStartServerVar

    settings.directoryList = list(directoryCombobox["value"])
    if len(settings.directoryList) > 0:
        directory = directoryCombobox.get()
        if directory in settings.directoryList:
            settings.directoryList.remove(directory)
            settings.directoryList.insert(0, directory)
    else:
        settings.directoryList = [settings.appDirectory]

    directoryCombobox["value"] = tuple(settings.directoryList)
    directoryCombobox.current(0)

    settings.userName = userNameVar.get()
    settings.userPassword = userPasswordVar.get()
    settings.isGBK = isGBKVar.get()
    settings.isReadOnly = isReadOnlyVar.get()
    settings.isAutoStartServer = isAutoStartServerVar.get()

    try:
        IPv4PortInt = int(IPv4PortVar.get())
        if 0 < IPv4PortInt and IPv4PortInt < 65536:
            settings.IPv4Port = IPv4PortInt
        else:
            raise
    except:
        print(
            f"\n\n!!! 当前 IPv4 设置端口：{IPv4PortVar.get()} 错误，正常范围: 1 ~ 65535，已重设为: 21\n\n"
        )
        settings.IPv4Port = 21
        IPv4PortVar.set("21")

    try:
        IPv6PortInt = int(IPv6PortVar.get())
        if 0 < IPv6PortInt and IPv6PortInt < 65536:
            settings.IPv6Port = IPv6PortInt
        else:
            raise
    except:
        print(
            f"\n\n!!! 当前 IPv6 设置端口：{IPv6PortVar.get()} 错误，正常范围: 1 ~ 65535，已重设为: 21\n\n"
        )
        settings.IPv6Port = 21
        IPv6PortVar.set("21")


class myStdout:  # 重定向输出
    def __init__(self):
        sys.stdout = self
        sys.stderr = self

    def write(self, info):
        logMsg.put(info)


def set_clipboard(data):
    win32clipboard.OpenClipboard()
    win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, data)
    win32clipboard.CloseClipboard()


def ip_into_int(ip_str):
    parts = ip_str.split(".")
    ip_int = (
            (int(parts[0]) << 24)
            + (int(parts[1]) << 16)
            + (int(parts[2]) << 8)
            + int(parts[3])
    )
    return ip_int


def is_internal_ip(ip_str):
    ip_int = ip_into_int(ip_str)
    net_A = ip_into_int("10.255.255.255") >> 24
    net_B = ip_into_int("172.31.255.255") >> 20
    net_C = ip_into_int("192.168.255.255") >> 16
    net_ISP = ip_into_int("100.127.255.255") >> 22
    net_DHCP = ip_into_int("169.254.255.255") >> 16
    return (
            ip_int >> 24 == net_A
            or ip_int >> 20 == net_B
            or ip_int >> 16 == net_C
            or ip_int >> 22 == net_ISP
            or ip_int >> 16 == net_DHCP
    )


def startServer():
    global serverThreadV4
    global serverThreadV6
    global isSupportdIPv6
    global isIPv4ThreadRunning
    global isIPv6ThreadRunning
    global tipsTextWidget
    global tipsTextWidgetRightClickMenu

    if isIPv4ThreadRunning:
        print("[FTP IPv4]正在运行")
        return
    if isIPv6ThreadRunning:
        print("[FTP IPv6]正在运行")
        return

    updateSettingVars()

    if not os.path.exists(settings.directoryList[0]):
        print(
            f"路径: [ {settings.directoryList[0]} ]异常！请检查路径是否正确或者有没有读取权限。"
        )
        return

    if len(settings.userName) > 0 and len(settings.userPassword) == 0:
        print(f"\n\n!!! 请设置密码再启动服务 !!!")
        return

    settings.save()

    tipsStr, ipList = getTipsAnd_IP_Info()

    tipsTextWidget.configure(state="normal")
    tipsTextWidget.delete("0.0", tkinter.END)
    tipsTextWidget.insert(tkinter.INSERT, tipsStr)
    tipsTextWidget.configure(state="disable")

    tipsTextWidgetRightClickMenu.delete(0, len(ipList))
    for ip in ipList:
        tipsTextWidgetRightClickMenu.add_command(
            label="复制 " + ip, command=lambda ip=ip: set_clipboard(ip)
        )

    try:
        serverThreadV4 = threading.Thread(target=serverThreadFunV4)
        serverThreadV4.start()

        if isSupportdIPv6:
            serverThreadV6 = threading.Thread(target=serverThreadFunV6)
            serverThreadV6.start()
    except:
        print("Error: 无法启动线程")

    print(
        "\n用户名: {}\n密码: {}\n权限: {}\n编码: {}\n目录: {}\n".format(
            (
                settings.userName
                if len(settings.userName) > 0
                else "匿名访问(anonymous)"
            ),
            settings.userPassword,
            ("只读" if settings.isReadOnly else "读写"),
            ("GBK" if settings.isGBK else "UTF-8"),
            settings.directoryList[0],
        )
    )


def serverThreadFunV4():
    global serverV4
    global isIPv4ThreadRunning

    print("[FTP IPv4]开启中...")
    authorizer = DummyAuthorizer()

    if len(settings.userName) > 0:
        authorizer.add_user(
            settings.userName,
            settings.userPassword,
            settings.directoryList[0],
            perm=permReadOnly if settings.isReadOnly else permReadWrite,
        )
    else:
        authorizer.add_anonymous(
            settings.directoryList[0],
            perm=permReadOnly if settings.isReadOnly else permReadWrite,
        )

    handler = FTPHandler
    handler.authorizer = authorizer
    handler.encoding = "gbk" if settings.isGBK else "utf8"
    serverV4 = ThreadedFTPServer(("0.0.0.0", settings.IPv4Port), handler)
    print("[FTP IPv4]开始运行")
    isIPv4ThreadRunning = True
    serverV4.serve_forever()
    isIPv4ThreadRunning = False
    print("已停止[FTP IPv4]")


def serverThreadFunV6():
    global serverV6
    global isIPv6ThreadRunning

    print("[FTP IPv6]开启中...")
    authorizer = DummyAuthorizer()

    if len(settings.userName) > 0:
        authorizer.add_user(
            settings.userName,
            settings.userPassword,
            settings.directoryList[0],
            perm=permReadOnly if settings.isReadOnly else permReadWrite,
        )
    else:
        authorizer.add_anonymous(
            settings.directoryList[0],
            perm=permReadOnly if settings.isReadOnly else permReadWrite,
        )

    handler = FTPHandler
    handler.authorizer = authorizer
    handler.encoding = "gbk" if settings.isGBK else "utf8"
    serverV6 = ThreadedFTPServer(("::", settings.IPv6Port), handler)
    print("[FTP IPv6]开始运行")
    isIPv6ThreadRunning = True
    serverV6.serve_forever()
    isIPv6ThreadRunning = False
    print("已停止[FTP IPv6]")


def closeServer():
    global serverV4
    global serverV6
    global serverThreadV4
    global serverThreadV6
    global isIPv4ThreadRunning
    global isIPv6ThreadRunning
    global isSupportdIPv6

    if isIPv4ThreadRunning:
        print("[FTP IPv4]正在停止...")
        serverV4.close_all()
        serverThreadV4.join()
        print("[FTP IPv4]服务线程已退出\n")
    else:
        print("当前没有[FTP IPv4]服务")

    if isSupportdIPv6:
        if isIPv6ThreadRunning:
            print("[FTP IPv6]正在停止...")
            serverV6.close_all()
            serverThreadV6.join()
            print("[FTP IPv6]服务线程已退出\n")
        else:
            print("当前没有[FTP IPv6]服务")


def pickDirectory():
    global directoryCombobox
    global settings

    directory = filedialog.askdirectory()
    if len(directory) == 0:
        return

    if os.path.exists(directory):
        if directory in settings.directoryList:
            settings.directoryList.remove(directory)
            settings.directoryList.insert(0, directory)
        else:
            settings.directoryList.insert(0, directory)
            while len(settings.directoryList) > 20:
                settings.directoryList.pop()

        directoryCombobox["value"] = tuple(settings.directoryList)
        directoryCombobox.current(0)
    else:
        print(f"路径不存在或无访问权限：{directory}")


def openGithub():
    webbrowser.open(githubLink)


def show_window():
    global window
    window.deiconify()


def hide_window():
    global window
    window.withdraw()


def handleExit(icon: pystray._base.Icon):
    global window
    global logThreadrunning
    global logThread

    icon.stop()
    print("等待日志线程退出...")
    logThreadrunning = False
    logThread.join()

    updateSettingVars()
    settings.save()

    closeServer()
    window.destroy()
    exit(0)


def logThreadFun():
    global logThreadrunning
    global loggingWidget
    cnt = 0
    while logThreadrunning:
        if logMsg.empty():
            time.sleep(0.1)
            continue

        cnt += 1
        if cnt > 100:
            cnt = 0
            loggingWidget.delete(0.0, tkinter.END)

        logInfo = ""
        while not logMsg.empty():
            logInfo += logMsg.get()

        loggingWidget.insert("end", logInfo)
        loggingWidget.see(tkinter.END)


def getTipsAnd_IP_Info():
    global isSupportdIPv6
    global tipsTitle

    addrs = socket.getaddrinfo(socket.gethostname(), None)

    IPv4IPstr = ""
    IPv6IPstr = ""
    IPv4List = []
    IPv6List = []
    for item in addrs:
        ipStr = item[4][0]
        if ":" in ipStr:  # IPv6
            isSupportdIPv6 = True
            fullLink = (
                    "ftp://["
                    + ipStr
                    + "]"
                    + ("" if settings.IPv6Port == 21 else (":" + str(settings.IPv6Port)))
            )
            IPv6List.append(fullLink)
            if ipStr[:4] == "fe80":
                IPv6IPstr += "\n[IPv6 局域网] " + fullLink
            elif ipStr[:4] == "240e":
                IPv6IPstr += "\n[IPv6 电信公网] " + fullLink
            elif ipStr[:4] == "2408":
                IPv6IPstr += "\n[IPv6 联通公网] " + fullLink
            elif ipStr[:4] == "2409":
                IPv6IPstr += "\n[IPv6 移动/铁通网] " + fullLink
            else:
                IPv6IPstr += "\n[IPv6 公网] " + fullLink
        else:  # IPv4
            fullLink = (
                    "ftp://"
                    + ipStr
                    + ("" if settings.IPv4Port == 21 else (":" + str(settings.IPv4Port)))
            )
            IPv4List.append(fullLink)
            if is_internal_ip(ipStr):
                if ipStr[:3] == "10." or ipStr[:3] == "100":
                    IPv4IPstr += "\n[IPv4 局域网] " + fullLink
                else:
                    IPv4IPstr += "\n[IPv4 局域网] " + fullLink
            else:
                IPv4IPstr += "\n[IPv4 公网] " + fullLink

    ipList = IPv4List + IPv6List
    tipsStr = tipsTitle + IPv4IPstr + IPv6IPstr
    return tipsStr, ipList


def main():
    global window
    global loggingWidget
    global logThread
    global tipsTextWidget
    global tipsTextWidgetRightClickMenu
    global directoryCombobox

    global userNameVar
    global userPasswordVar
    global IPv4PortVar
    global IPv6PortVar
    global isReadOnlyVar
    global isGBKVar
    global isAutoStartServerVar

    # 告诉操作系统使用程序自身的dpi适配
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

    ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)

    def scale(n: int) -> int:
        return int(n * ScaleFactor / 100)

    mystd = myStdout()  # 实例化重定向类

    settings.load()

    strayMenu = (
        pystray.MenuItem("显示", show_window, default=True),
        pystray.MenuItem("退出", handleExit),
    )
    strayImage = Image.open(BytesIO(base64.b64decode(iconStr)))
    strayIcon = pystray.Icon("icon", strayImage, "FTP服务器", strayMenu)

    logThread = threading.Thread(target=logThreadFun)
    logThread.start()

    window = tkinter.Tk()  # 实例化tk对象
    window.title(windowsTitle)
    icon_img = ImageTk.PhotoImage(data=base64.b64decode(iconStr))
    window.tk.call("wm", "iconphoto", window._w, icon_img)

    window.resizable(0, 0)  # 固定窗口
    window.protocol("WM_DELETE_WINDOW", hide_window)

    winWidht = 600
    winHeight = 500
    window.geometry(str(scale(winWidht)) + "x" + str(scale(winHeight)))

    startButton = ttk.Button(window, text="开启", command=startServer)
    startButton.place(x=scale(10), y=scale(10), width=scale(60), height=scale(25))
    ttk.Button(window, text="停止", command=closeServer).place(
        x=scale(80), y=scale(10), width=scale(60), height=scale(25)
    )

    ttk.Button(window, text="设置目录", command=pickDirectory).place(
        x=scale(150), y=scale(10), width=scale(70), height=scale(25)
    )

    directoryCombobox = ttk.Combobox(window, state="readonly")
    directoryCombobox.place(
        x=scale(230), y=scale(10), width=scale(280), height=scale(25)
    )

    ttk.Button(window, text="关于/更新", command=openGithub).place(
        x=scale(520), y=scale(10), width=scale(70), height=scale(25)
    )

    ttk.Label(window, text="用户名").place(
        x=scale(10), y=scale(40), width=scale(50), height=scale(25)
    )
    userNameVar = tkinter.StringVar()
    ttk.Entry(window, textvariable=userNameVar, width=scale(12)).place(
        x=scale(60), y=scale(40), width=scale(100), height=scale(25)
    )

    ttk.Label(window, text="密码").place(
        x=scale(10), y=scale(70), width=scale(40), height=scale(25)
    )
    userPasswordVar = tkinter.StringVar()
    ttk.Entry(window, textvariable=userPasswordVar, width=scale(12)).place(
        x=scale(60), y=scale(70), width=scale(100), height=scale(25)
    )

    ttk.Label(window, text="IPv4端口").place(
        x=scale(180), y=scale(40), width=scale(80), height=scale(25)
    )
    IPv4PortVar = tkinter.StringVar()
    ttk.Entry(window, textvariable=IPv4PortVar, width=scale(8)).place(
        x=scale(240), y=scale(40), width=scale(60), height=scale(25)
    )

    ttk.Label(window, text="IPv6端口").place(
        x=scale(180), y=scale(70), width=scale(80), height=scale(25)
    )
    IPv6PortVar = tkinter.StringVar()
    ttk.Entry(window, textvariable=IPv6PortVar, width=scale(8)).place(
        x=scale(240), y=scale(70), width=scale(60), height=scale(25)
    )

    isGBKVar = tkinter.BooleanVar()
    ttk.Radiobutton(window, text="UTF-8 编码", variable=isGBKVar, value=False).place(
        x=scale(310), y=scale(40), width=scale(100), height=scale(25)
    )
    ttk.Radiobutton(window, text="GBK 编码", variable=isGBKVar, value=True).place(
        x=scale(310), y=scale(70), width=scale(100), height=scale(25)
    )

    isReadOnlyVar = tkinter.BooleanVar()
    ttk.Radiobutton(window, text="读写", variable=isReadOnlyVar, value=False).place(
        x=scale(400), y=scale(40), width=scale(100), height=scale(25)
    )
    ttk.Radiobutton(window, text="只读", variable=isReadOnlyVar, value=True).place(
        x=scale(400), y=scale(70), width=scale(100), height=scale(25)
    )

    isAutoStartServerVar = tkinter.BooleanVar()
    ttk.Checkbutton(
        window,
        text="下次自启动服务\n并隐藏窗口",
        variable=isAutoStartServerVar,
        onvalue=True,
        offvalue=False,
    ).place(x=scale(460), y=scale(40), width=scale(160), height=scale(50))

    tipsStr, ipList = getTipsAnd_IP_Info()

    tipsTextWidget = scrolledtext.ScrolledText(window, bg="#dddddd", wrap=tkinter.CHAR)
    tipsTextWidget.insert(tkinter.INSERT, tipsStr)
    tipsTextWidget.configure(state="disable")
    tipsTextWidget.place(x=scale(10), y=scale(100), width=scale(580), height=scale(150))

    tipsTextWidgetRightClickMenu = tkinter.Menu(window, tearoff=False)
    for ip in ipList:
        tipsTextWidgetRightClickMenu.add_command(
            label="复制 " + ip, command=lambda ip=ip: set_clipboard(ip)
        )

    def popup(event: tkinter.Event):
        tipsTextWidgetRightClickMenu.post(
            event.x_root, event.y_root
        )  # post在指定的位置显示弹出菜单

    tipsTextWidget.bind("<Button-3>", popup)  # 绑定鼠标右键,执行popup函数

    loggingWidget = scrolledtext.ScrolledText(window, bg="#dddddd", wrap=tkinter.CHAR)
    loggingWidget.place(x=scale(10), y=scale(260), width=scale(580), height=scale(230))

    # 设置程序缩放
    window.tk.call("tk", "scaling", ScaleFactor / 75)

    directoryCombobox["value"] = tuple(settings.directoryList)
    directoryCombobox.current(0)

    userNameVar.set(settings.userName)
    userPasswordVar.set(settings.userPassword)
    IPv4PortVar.set(str(settings.IPv4Port))
    IPv6PortVar.set(str(settings.IPv6Port))
    isGBKVar.set(settings.isGBK)
    isReadOnlyVar.set(settings.isReadOnly)
    isAutoStartServerVar.set(settings.isAutoStartServer)

    threading.Thread(target=strayIcon.run, daemon=True).start()

    if settings.isAutoStartServer:
        startButton.invoke()
        window.withdraw()

    window.mainloop()


if __name__ == "__main__":
    main()

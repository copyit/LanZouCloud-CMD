import os
from time import sleep

import readline
import requests

from lanzou.api import LanZouCloud
from lanzou.cmder import version, config


def error(msg, end='\n'):
    print(f"\033[1;31mError : {msg}\033[0m", end=end)


def info(msg, end='\n'):
    print(f"\033[1;34mInfo : {msg}\033[0m", end=end)


def clear_screen():
    """清空屏幕"""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def why_error(code):
    """错误原因"""
    if code == LanZouCloud.URL_INVALID:
        return '分享链接无效'
    elif code == LanZouCloud.LACK_PASSWORD:
        return '缺少提取码'
    elif code == LanZouCloud.PASSWORD_ERROR:
        return '提取码错误'
    elif code == LanZouCloud.FILE_CANCELLED:
        return '分享链接已失效'
    elif code == LanZouCloud.ZIP_ERROR:
        return '解压过程异常'
    elif code == LanZouCloud.NETWORK_ERROR:
        return '网络连接异常'
    elif code == LanZouCloud.CAPTCHA_ERROR:
        return '验证码错误'
    elif code == LanZouCloud.OFFICIAL_LIMITED:
        return '操作被官方限制'
    else:
        return '未知错误'


def ignore_limit():
    return os.path.exists(".ignore_limit")


def set_console_style():
    """设置命令行窗口样式"""
    if os.name != 'nt':
        return None
    # os.system('mode 120, 40')
    os.system(f'title 蓝奏云 CMD 控制台 {version}')


def text_align(text, length) -> str:
    """中英混合字符串对齐"""
    text_len = len(text)
    for char in text:
        if u'\u4e00' <= char <= u'\u9fff':
            text_len += 1
    space = length - text_len
    return text + ' ' * space


def set_completer(choice_list, *, cmd_list=None, condition=None):
    """设置自动补全"""
    if condition is None:
        condition = lambda typed, choice: choice.startswith(typed)  # 默认筛选条件：选项以键入字符开头

    def completer(typed, rank):
        tab_list = []  # TAB 补全的选项列表
        if cmd_list is not None and not typed:  # 内置命令提示
            return cmd_list[rank]

        for choice in choice_list:
            if condition(typed, choice):
                tab_list.append(choice)
        return tab_list[rank]

    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)


def print_logo():
    """输出logo"""
    clear_screen()
    ext_msg = "Unlimited " if ignore_limit() else ""
    logo_str = f"""
        _                  ______            _____ _                 _ 
       | |                |___  /           /  __ \ |               | |
       | |     __ _ _ __     / /  ___  _   _| /  \/ | ___  _   _  __| |
       | |    / _  |  _ \   / /  / _ \| | | | |   | |/ _ \| | | |/ _  |
       | |___| (_| | | | | / /__| (_) | |_| | \__/\ | (_) | |_| | (_| |
       \_____/\____|_| |_|\_____/\___/ \____|\____/_|\___/ \____|\____|
      --------------------------------------------------------------------
      Github: https://github.com/zaxtyson/LanZouCloud-CMD ({ext_msg}Version: {version})
      --------------------------------------------------------------------
    """
    print(logo_str)


def print_help():
    clear_screen()
    help_text = f"""
    • CMD 版蓝奏云控制台 v{version}
    
    命令帮助 :
    help        显示本信息
    update      检查更新
    rmode       屏幕阅读器模式
    refresh     刷新当前目录
    xghost      清理"幽灵"文件夹
    login       使用 Cookie 登录网盘
    logout      注销当前账号
    jobs        查看后台任务列表   
    jobs <ID>   查看 ID 对应任务的详情(失败原因)
    ls          列出文件(夹)
    cd          切换工作目录
    cdrec       进入回收站
    rm          删除网盘文件(夹)
    rename      重命名文件(夹)
    desc        修改文件(夹)描述
    mv          移动文件(夹)
    mkdir       创建新文件夹(最大深度 4)
    share       显示文件(夹)分享信息
    export      导出文件夹下的文件信息到文件
    clear       清空屏幕
    clean       清空回收站
    upload      上传文件(夹), 大文件上传功能已关闭
    down        下载文件(夹), 支持 URL, 支持递归下载
    passwd      设置文件(夹)提取码
    setpath     设置文件下载路径
    setsize     设置单文件大小限制
    setpasswd   设置文件(夹)默认提取码
    setdelay    设置上传大文件数据块的延时
    bye         退出本程序
    
    更详细的介绍请参考本项目的 Github 主页:
    https://github.com/zaxtyson/LanZouCloud-CMD   
    如有 Bug 反馈或建议请在 GitHub 提 Issue 或者
    发送邮件至 : zaxtyson@foxmail.com
    感谢您的使用 (●'◡'●)
    """
    print(help_text)


def check_update():
    """检查更新"""
    clear_screen()
    print("正在检测更新...")
    api = "https://api.github.com/repos/zaxtyson/LanZouCloud-CMD/releases/latest"
    try:
        resp = requests.get(api, timeout=3).json()
        tag_name, msg = resp['tag_name'], resp['body']
        update_url = resp['assets'][0]['browser_download_url']
        ver = version.split('.')
        ver2 = tag_name.replace('v', '').split('.')
        local_version = int(ver[0]) * 100 + int(ver[1]) * 10 + int(ver[2])
        remote_version = int(ver2[0]) * 100 + int(ver2[1]) * 10 + int(ver2[2])
        if remote_version > local_version:
            "\033[1;34mInfo : {msg}\033[0m"
            print(f"\n程序可以更新 v{version} -> \033[1;32m{tag_name}\033[0m")
            print(f"\n# 更新说明\n\n{msg}")
            print(f"\n# Windows 更新\n")
            print(f"蓝奏云: https://zaxtyson.lanzouf.com/b0f14h1od")
            print(f"Github: {update_url}")
            print("\n# Linux 更新\n")
            print("git pull --rebase")
        else:
            print("\n(*/ω＼*) 暂无新版本发布~")
            print("但项目可能已经更新，建议去项目主页看看")
            print("如有 Bug 或建议,请提 Issue 或发邮件反馈\n")
            print("Email: zaxtyson@foxmail.com")
            print("Github: https://github.com/zaxtyson/LanZouCloud-CMD")
            print()
    except (requests.RequestException, AttributeError, KeyError):
        error("检查更新时发生异常")
        sleep(2)
        return
    except TimeoutError:
        error("检查更新超时, 请稍后重试")
        sleep(2)
        return


def show_tips_first():
    """第一次启动时的提醒"""
    if not config.cookie:
        info(f"下载文件保存路径为: {config.save_path}")
        info("使用 setpath 命令可修改保存路径")
        info("其它帮助信息请使用 help 命令查看\n")

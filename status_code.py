import argparse
import requests
import warnings
from termcolor import colored

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# 状态码说明和颜色配置
status_codes_explanation = {
    200: "可访问",
    301: "永久重定向",
    302: "临时重定向",
    400: "请求错误",
    401: "未授权",
    403: "无权限",
    404: "未找到",
    500: "服务器错误",
    503: "服务不可用",
}

status_colors = {
    200: "green",
    301: "blue",
    302: "blue",
    400: "yellow",
    401: "yellow",
    403: "yellow",
    404: "yellow",
    500: "red",
    503: "red",
}


def check_url(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=4, verify=False)
        status_code = response.status_code
        explanation = status_codes_explanation.get(status_code, "未知状态码")
        color = status_colors.get(status_code, "magenta")

        # 打印结果
        output = colored(f"[{status_code}] {explanation} {url}", color)
        print(output)

        # 保存到对应的文件
        filename = f"{status_code}.txt"
        with open(filename, "a") as file:
            file.write(url + "\n")

    except requests.exceptions.Timeout:
        print(colored(f"[Error] 请求超时 {url}", "red"))
    except requests.exceptions.ConnectionError:
        print(colored(f"[Error] 连接错误 {url}", "red"))
    except requests.exceptions.RequestException as e:
        print(colored(f"[Error] 请求异常 {url} [异常消息] {e}", "red"))


def main():
    parser = argparse.ArgumentParser(description='URL状态码检查工具')
    parser.add_argument("-l", "--list", type=str, help="包含网站列表的文件")
    parser.add_argument("-u", "--url", type=str, nargs='+', help="一个或多个网站URL")
    args = parser.parse_args()

    # 处理单个或多个URL
    if args.url:
        for url in args.url:
            check_url(url)

    # 处理文件中的URL列表
    if args.list:
        try:
            with open(args.list, "r") as file:
                urls = [line.strip() for line in file if line.strip()]
                for url in urls:
                    check_url(url)
        except FileNotFoundError:
            print(colored(f"文件 {args.list} 未找到。", "red"))

    print("检查完成")


if __name__ == "__main__":
    main()

import tkinter as tk
from PIL import Image, ImageTk
import os
import platform
import sys

# 全局变量
no_count = 0
font_size = 12
jian_size = 12
countdown = None
root = None
auto_close_countdown = None


def resource_path(relative_path):
    """获取资源文件的绝对路径，兼容打包后的环境"""
    if hasattr(sys, '_MEIPASS'):  # 打包后运行
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)  # 开发环境


def choose_yes():
    global countdown, auto_close_countdown
    if no_count:
        root.after_cancel(countdown)
    result_label.config(text="真乖，恭喜你获得了一个小奖励")
    # 延迟5秒后执行下一步操作
    root.after(3000, lambda: perform_next_step(True))
    # 恢复不是按钮状态
    no_button.config(state=tk.NORMAL)


def choose_no():
    global no_count, auto_close_countdown
    if no_count:
        root.after_cancel(no_count)
    result_label.config(text="你完蛋了，kuromi将代表正义的狸老师惩罚你")
    # 延迟5秒后执行下一步操作
    root.after(3000, lambda: perform_next_step(False))
    # 恢复不是按钮状态
    no_button.config(state=tk.NORMAL)


def perform_next_step(is_yes):
    global countdown, auto_close_countdown
    warning_label.config(text="")
    countdown_label.config(text="")
    if is_yes:
        show_image_jiangli()
        auto_close_countdown = root.after(5000, root.destroy)
    else:
        show_image_kuromi()
        auto_close_countdown = root.after(10000, root.destroy)
    # 绑定鼠标右键事件以结束程序
    root.bind("<Button-1>", lambda event: root.destroy())


def show_image_jiangli():
    global countdown, auto_close_countdown
    # 创建新窗口显示图片
    image_window = tk.Toplevel(root)
    image_window.title("警告")
    image_window.attributes('-topmost', True)
    image_window.overrideredirect(True)

    try:
        # 使用 resource_path() 函数获取图片路径
        image_path = resource_path("jiangli.jpg")
        image = Image.open(image_path)

        # 获取图片边缘颜色（这里简单获取左上角像素颜色作为代表）
        edge_color = image.getpixel((0, 0))
        # 将边缘颜色转换为十六进制格式
        edge_color_hex = '#{:02x}{:02x}{:02x}'.format(*edge_color)

        # 设置窗口背景颜色为图片边缘颜色
        image_window.configure(bg=edge_color_hex)

        # 缩小图像
        new_width = int(image.width * 0.5)
        new_height = int(image.height * 0.5)
        image = image.resize((new_width, new_height), Image.ANTIALIAS)

        photo = ImageTk.PhotoImage(image)

        # 获取屏幕宽度和高度
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # 设置窗口大小为整个屏幕
        image_window.geometry(f"{screen_width}x{screen_height}+0+0")

        # 添加与图片边缘颜色相同的边框
        border_width = 0
        border_color = edge_color_hex
        image_label = tk.Label(image_window, image=photo, borderwidth=border_width, relief="solid", bg=border_color)
        image_label.image = photo  # 防止图片被垃圾回收
        # 使用 pack 布局管理器的 anchor 选项将图像上下居中
        image_label.pack(side=tk.TOP, anchor=tk.CENTER)

        # 绑定鼠标右键事件以关闭图片窗口
        image_window.bind("<Button-2>", lambda event: image_window.destroy())
        # 绑定鼠标右键事件以结束程序
        root.bind("<Button-1>", lambda event: root.destroy())
        # 启动 15 秒后自动关闭程序的倒计时
        auto_close_countdown = root.after(10000, root.destroy)
    except FileNotFoundError:
        tk.messagebox.showerror("错误", "未找到图片文件，请检查路径。")


def show_image_kuromi():
    global countdown, auto_close_countdown
    # 创建新窗口显示图片
    image_window = tk.Toplevel(root)
    image_window.title("警告")
    image_window.attributes('-topmost', True)
    image_window.overrideredirect(True)
    image_window.configure(bg="black")  # 设置窗口背景颜色为黑色

    try:
        # 使用 resource_path() 函数获取图片路径
        image_path = resource_path("kuromi.jpg")
        image = Image.open(image_path)

        # 缩小图像，这里将图像缩小为原来的 0.5 倍，你可以根据需要调整缩放比例
        new_width = int(image.width * 0.5)
        new_height = int(image.height * 0.5)
        image = image.resize((new_width, new_height), Image.ANTIALIAS)

        photo = ImageTk.PhotoImage(image)

        # 获取屏幕宽度和高度
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # 设置窗口大小为整个屏幕
        image_window.geometry(f"{screen_width}x{screen_height}+0+0")

        # 添加黑色边框
        image_label = tk.Label(image_window, image=photo, borderwidth=5, relief="solid", bg="black")
        image_label.image = photo  # 防止图片被垃圾回收
        # 使用 pack 布局管理器的 anchor 选项将图像上下居中
        image_label.pack(side=tk.TOP, anchor=tk.CENTER)

        # 绑定鼠标右键事件以关闭图片窗口
        image_window.bind("<Button-2>", lambda event: image_window.destroy())
        # 绑定鼠标右键事件以结束程序
        root.bind("<Button-1>", lambda event: root.destroy())
        # 启动 15 秒后自动关闭程序的倒计时
        auto_close_countdown = root.after(10000, root.destroy)
    except FileNotFoundError:
        tk.messagebox.showerror("错误", "未找到图片文件，请检查路径。")


def lock_interface():
    # 屏蔽鼠标左键和键盘事件
    root.bind("<Button-1>", lambda event: "break")
    root.bind_all("<Key>", lambda event: "break")


# 创建主窗口
root = tk.Tk()
root.title("如果熬夜了你会")
# 窗口置顶
root.attributes('-topmost', True)
# 去除边框和标题栏
root.overrideredirect(True)
# 最大化窗口
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
# 创建问题标签
question_label = tk.Label(root, text="如果你今天熬夜了你会（跪着选，不要皮，乖乖的有奖励！）", font=("Arial", 16))
question_label.pack(pady=20)

# 创建“是”按钮
yes_button = tk.Button(root, text="对不起daddy我错了，请狠狠惩罚我吧", font=("Arial", font_size), command=choose_yes)
yes_button.pack(pady=10)

# 创建“不是”按钮
no_button = tk.Button(root, text="狗叫什么，你眼睛长痔疮了，我这叫按摩眼睛不叫熬夜", font=("Arial", jian_size), command=choose_no)
no_button.pack(pady=20)

# 创建结果标签
result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack(pady=40)
# 创建警告标签
warning_label = tk.Label(root, text="", font=("Arial", 14))
warning_label.pack(pady=10)
# 创建倒计时标签
countdown_label = tk.Label(root, text="", font=("Arial", 14))
countdown_label.pack(pady=10)
# 创建数字标签
count_label = tk.Label(root, text="", font=("Arial", 30))
count_label.pack(pady=10)
# 锁定界面
lock_interface()
# 运行主循环
root.mainloop()
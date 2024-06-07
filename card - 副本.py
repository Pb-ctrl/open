import tkinter as tk
from tkinter import ttk
import os
import threading
import pyperclip
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# 全局变量
prices = {}
file_path = "C:\\Users\\31716\\Documents\\gift_card\\price_list\\prices.md"

# 读取价格数据
def read_prices():
    global prices
    try:
        with open(file_path, "r") as f:
            for line in f:
                if '=' in line:
                    value, price = line.strip().split('=')
                    prices[int(value[:-2])] = float(price)
    except FileNotFoundError:
        with open(file_path, "w") as f:
            for option in options:
                f.write(f"{option}TL=0.0\n")
        read_prices()

# 覆盖520数值
def update_price_in_file(new_price):
    lines = []
    with open(file_path, "r") as f:
        for line in f:
            if line.startswith(f"520TL="):
                lines.append(f"520TL={new_price}\n")
            else:
                lines.append(line)
    with open(file_path, "w") as f:
        f.writelines(lines)

# 覆盖当前选项面值数据
def update_price_in_file1(value, new_price):
    lines = []
    with open(file_path, "r") as f:
        for line in f:
            if line.startswith(f"{value}TL="):
                lines.append(f"{value}TL={new_price}\n")
            else:
                lines.append(line)
    with open(file_path, "w") as f:
        f.writelines(lines)

# 保存价格数据
def save_prices():
    with open(file_path, "w") as f:
        for value, price in prices.items():
            f.write(f"{value}TL={price}\n")

# 更新成本单价
def update_price(value, new_price):
    prices[value] = new_price
    save_prices()

# 计算总价格
def calculate_price(event=None):
    def task():
        value = card_value.get()
        qty = quantity.get()
        if value in prices:
            unit_price = prices[value]
            total_price = unit_price * qty
            result_text = f"{total_price:.3f}"
            result_text1 = f"总共: {total_price:.2f}元"
            result_text2 = f"总共: {total_price:.2f} USDT"           
            if value==520:
                # print("1111")
                result_label.config(text=result_text1)
            else:
                result_label.config(text=result_text2)
            pyperclip.copy(result_text)  # 复制结果到剪贴板
            # if current_unit_price!=prices[value]:
            save_results(total_price)
        else:
            result_label.config(text="未找到选定面值的价格")
    threading.Thread(target=task).start()

# 计算闲鱼售卖单价
def calculate_original_price():
    def task():
        value = card_value.get()
        rate = exchange_rate.get()
        if value in prices:
            unit_price = prices[value]
            original_price = unit_price * rate
            result_text = f"{original_price:.3f}"
            result_text1 = f"成本价: {original_price:.2f} 元"
            result_label.config(text=result_text1)
            pyperclip.copy(result_text)  # 复制结果到剪贴板
            # if current_unit_price!=prices[value]:
            save_original_price(original_price)
            update_price_in_file(result_text)
    threading.Thread(target=task).start()

# current_unit_price=total_value.get() / quantity.get()

# 计算买入时单价成本
def calculate_current_unit_price():
    def task():
        value = card_value.get() #礼品卡面值
        total_value_in_usdt = total_value.get() #总价
        qty = quantity.get() #数量
        if qty > 0:
            current_unit_price = total_value_in_usdt / qty #买入时的单价成本
            result_text = f"{current_unit_price:.3f}"
            result_text1 = f"现在单价: {current_unit_price:.2f} USDT"
            result_label.config(text=result_text1)
            pyperclip.copy(result_text)  # 复制结果到剪贴板
            # if current_unit_price!=prices[value]:
            save_current_unit_price(current_unit_price)
            # if current_unit_price < prices[value]:          
            update_price_in_file1(value, result_text)
    threading.Thread(target=task).start()
# 假设 value 是一个全局变量，存储上次保存的结果
previous_results = {
    "save_results": None,
    "save_original_price": None,
    "save_current_unit_price": None
}

# 保存计算结果
def save_results(total_price):
    def task():
        result_text = f"礼品卡面值: **{card_value.get()} TL**, 购买数量: **{quantity.get()}**, 总价格: =={total_price:.2f}==**USDT**\n"
        if previous_results["save_results"] != result_text:
            with open("C:\\Users\\31716\\Documents\\gift_card\\log\\result.md", "a") as f:
                f.write(result_text)
            previous_results["save_results"] = result_text
    threading.Thread(target=task).start()

# 保存成本价结果
def save_original_price(original_price):
    def task():
        result_text = f"礼品卡面值: **{card_value.get()} TL**, 汇率: **{exchange_rate.get()}**, 成本价: =={original_price:.2f}==**元**\n"
        if previous_results["save_original_price"] != result_text:
            with open("C:\\Users\\31716\\Documents\\gift_card\\log\\result.md", "a") as f:
                f.write(result_text)
            previous_results["save_original_price"] = result_text
    threading.Thread(target=task).start()

# 保存现在单价结果
def save_current_unit_price(current_unit_price):
    def task():
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        result_text = f" \n \n面值: **{card_value.get()} TL**, 时间：**{timestamp}**, 单价成本: =={current_unit_price:.2f}==**USDT**\n \n"
        if previous_results["save_current_unit_price"] != result_text:
            with open("C:\\Users\\31716\\Documents\\gift_card\\log\\result.md", "a") as f:
                f.write(result_text)
            previous_results["save_current_unit_price"] = result_text
    threading.Thread(target=task).start()

# 查看日志
def view_results():
    os.system('start typora "C:\\Users\\31716\\Documents\\gift_card\\log\\result.md"')

# 礼品卡价格数据
def view_cost():
    os.system('start typora "C:\\Users\\31716\\Documents\\gift_card\\price_list\\prices.md"')

# 监控文件变化
class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == file_path:
            read_prices()

observer = Observer()
event_handler = FileChangeHandler()
observer.schedule(event_handler, path=os.path.dirname(file_path), recursive=False)
observer.start()

# 创建主窗口
root = tk.Tk()
root.title("礼品卡价格计算器")
root.geometry("400x400")

# 下拉栏选项
options = [25, 50, 100, 500, 1000, 520]

# 变量
card_value = tk.IntVar()
quantity = tk.IntVar(value=5)
exchange_rate = tk.DoubleVar(value=7.26)
total_value = tk.DoubleVar(value=3.36)

# 创建并放置组件
ttk.Label(root, text="礼品卡面值 (TL):").grid(column=0, row=0, padx=0, pady=0)
ttk.Label(root, text="购买数量:").grid(column=0, row=1, padx=10, pady=0)
ttk.Label(root, text="汇率:").grid(column=0, row=7, padx=0, pady=0)
ttk.Label(root, text="支付时页面价格 (USDT):").grid(column=0, row=5, padx=10, pady=0)

card_value_menu = ttk.Combobox(root, textvariable=card_value)
card_value_menu['values'] = options
card_value_menu.grid(column=1, row=0, padx=0, pady=0)
card_value_menu.current(0)

quantity_entry = ttk.Entry(root, textvariable=quantity)
quantity_entry.grid(column=1, row=1, padx=5, pady=5)

exchange_rate_entry = ttk.Entry(root, textvariable=exchange_rate)
exchange_rate_entry.grid(column=1, row=7, padx=0, pady=0)

total_value_entry = ttk.Entry(root, textvariable=total_value)
total_value_entry.grid(column=1, row=5, padx=0, pady=0)

# 按钮
calculate_button = ttk.Button(root, text="1总价格 (Enter)", command=calculate_price)
calculate_button.grid(column=0, row=3, padx=10, pady=1)

original_price_button = ttk.Button(root, text="3闲鱼售卖单价", command=calculate_original_price)
original_price_button.grid(column=1, row=3, padx=10, pady=1)

current_unit_price_button = ttk.Button(root, text="2买入时单价成本", command=calculate_current_unit_price)
current_unit_price_button.grid(column=0, row=6, padx=10, pady=0)

view_results_button = ttk.Button(root, text="查看日志", command=view_results)
view_results_button.grid(column=1, row=4, padx=10, pady=10)

view_cost_button = ttk.Button(root, text="礼品卡价格数据", command=view_cost)
view_cost_button.grid(column=0, row=4, padx=10, pady=10)

# 显示结果的标签
result_label = ttk.Label(root, text="总价格 (USDT): ")
result_label.grid(column=1, row=6, padx=10, pady=10)

# 绑定Enter键
root.bind('<Return>', calculate_price)

# 调整布局使窗口可调整大小
for i in range(7):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

# 读取价格数据
read_prices()

root.mainloop()

# 停止观察者
observer.stop()
observer.join()
try:
    import pyperclip
except ImportError:
    os.system('pip install pyperclip')
    import pyperclip

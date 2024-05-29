import tkinter as tk
from tkinter import messagebox

# 定义文件路径
file_path = "C:\\Users\\31716\\Documents\\gift_card\\prices.txt"
result_file_path = "C:\\Users\\31716\\Documents\\gift_card\\result.txt"

# 尝试打开文件并读取价格数据
prices = {}
try:
    with open(file_path, 'r') as file:
        for line in file:
            # 跳过空行和注释行
            if '=' in line:
                var_name, var_value = line.split('=')
                prices[var_name.strip()] = float(var_value.strip())
except FileNotFoundError:
    messagebox.showerror("错误", "无法找到价格文件")
    prices = None
except ValueError:
    messagebox.showerror("错误", "价格文件包含无效数据")
    prices = None

# 如果成功读取价格，则将其分配给相应的变量
if prices:
    price25 = prices.get('25TL', 0.0)
    price50 = prices.get('50TL', 0.0)
    price100 = prices.get('100TL', 0.0)
    price250 = prices.get('250TL', 0.0)
    price500 = prices.get('500TL', 0.0)
    price1000 = prices.get('1000TL', 0.0)
else:
    price25 = price50 = price100 = price250 = price500 = price1000 = 0.0

# 创建主窗口
root = tk.Tk()
root.title("Gift Card Price Calculator")

# 允许窗口拖动的功能
def start_move(event):
    root.x = event.x
    root.y = event.y

def stop_move(event):
    root.x = None
    root.y = None

def on_move(event):
    if root.x is not None and root.y is not None:
        delta_x = event.x - root.x
        delta_y = event.y - root.y
        new_x = root.winfo_x() + delta_x
        new_y = root.winfo_y() + delta_y
        root.geometry(f"+{new_x}+{new_y}")

root.bind("<Button-1>", start_move)
root.bind("<ButtonRelease-1>", stop_move)
root.bind("<B1-Motion>", on_move)

# 创建选择框标签和下拉菜单
tk.Label(root, text="请选择礼品卡金额:").pack()
options = ["25TL", "50TL", "100TL", "250TL", "500TL", "1000TL"]
variable = tk.StringVar(root)
variable.set(options[0])  # 默认选择第一个选项
option_menu = tk.OptionMenu(root, variable, *options)
option_menu.pack()

# 创建数量输入框标签和输入框
tk.Label(root, text="请输入购买数量:").pack()
num_entry = tk.Entry(root)
num_entry.pack()

# 创建汇率输入框标签和输入框
tk.Label(root, text="请输入汇率:").pack()
exchange_rate_entry = tk.Entry(root)
exchange_rate_entry.pack()
exchange_rate_entry.insert(0, "7.24")  # 设置默认值为7.24

# 计算价格的函数
def calculate_price():
    try:
        amount = variable.get()
        quantity = int(num_entry.get())
        
        if amount == "25TL":
            price = price25
        elif amount == "50TL":
            price = price50
        elif amount == "100TL":
            price = price100
        elif amount == "250TL":
            price = price250
        elif amount == "500TL":
            price = price500
        elif amount == "1000TL":
            price = price1000
        else:
            raise ValueError("无效的金额选择")
        
        total_price = price * quantity
        with open(result_file_path, 'a') as result_file:
            result_file.write(f"选择了 {amount}，购买数量为：{quantity} 个，总价为: {total_price:.3f} USDT\n")
        messagebox.showinfo("计算结果", f"选择了 {amount}，购买数量为：{quantity} 个，总价为: {total_price:.3f} USDT")
    except ValueError:
        messagebox.showerror("错误", "无效的输入，请输入正确的数字")

# 计算当前单价的函数
def calculate_unit_price():
    try:
        amount = variable.get()
        exchange_rate = float(exchange_rate_entry.get())
        
        if amount == "25TL":
            unit_price = float(price25) * exchange_rate
        elif amount == "50TL":
            unit_price = float(price50) * exchange_rate
        elif amount == "100TL":
            unit_price = float(price100) * exchange_rate
        elif amount == "250TL":
            unit_price = float(price250) * exchange_rate
        elif amount == "500TL":
            unit_price = float(price500) * exchange_rate
        elif amount == "1000TL":
            unit_price = float(price1000) * exchange_rate
        else:
            raise ValueError("无效的金额选择")
        
        with open(result_file_path, 'a') as result_file:
            result_file.write(f"当前单价: {unit_price:.3f} CNY\n")
        messagebox.showinfo("当前单价计算结果", f"当前单价: {unit_price:.3f} CNY")
    except ValueError:
        messagebox.showerror("错误", "无效的输入，请输入正确的数字")

# 创建计算价格按钮
calculate_button = tk.Button(root, text="计算价格", command=calculate_price)
calculate_button.pack()

# 创建计算当前单价按钮
calculate_unit_price_button = tk.Button(root, text="计算当前单价", command=calculate_unit_price)
calculate_unit_price_button.pack()

# 显示价格和结果的功能保持不变
def show_prices():
    price_window = tk.Toplevel(root)
    price_window.title("价格列表(UNiT：USDT)")
    
    tk.Label(price_window, text="25TL:").grid(row=0, column=0)
    price25_entry = tk.Entry(price_window)
    price25_entry.grid(row=0, column=1)
    price25_entry.insert(0, price25)
    
    tk.Label(price_window, text="50TL:").grid(row=1, column=0)
    price50_entry = tk.Entry(price_window)
    price50_entry.grid(row=1, column=1)
    price50_entry.insert(0, price50)
    
    tk.Label(price_window, text="100TL:").grid(row=2, column=0)
    price100_entry = tk.Entry(price_window)
    price100_entry.grid(row=2, column=1)
    price100_entry.insert(0, price100)
    
    tk.Label(price_window, text="250TL:").grid(row=3, column=0)
    price250_entry = tk.Entry(price_window)
    price250_entry.grid(row=3, column=1)
    price250_entry.insert(0, price250)
    
    tk.Label(price_window, text="500TL:").grid(row=4, column=0)
    price500_entry = tk.Entry(price_window)
    price500_entry.grid(row=4, column=1)
    price500_entry.insert(0, price500)
    
    tk.Label(price_window, text="1000TL:").grid(row=5, column=0)
    price1000_entry = tk.Entry(price_window)
    price1000_entry.grid(row=5, column=1)
    price1000_entry.insert(0, price1000)
    
    def save_prices():
        try:
            new_prices = {
                'price25': float(price25_entry.get()),
                'price50': float(price50_entry.get()),
                'price100': float(price100_entry.get()),
                'price250': float(price250_entry.get()),
                'price500': float(price500_entry.get()),
                'price1000': float(price1000_entry.get()),
            }
            with open(file_path, 'w') as file:
                for key, value in new_prices.items():
                    file.write(f"{key}={value}\n")
            messagebox.showinfo("成功", "价格已更新")
            price_window.destroy()
        except ValueError:
            messagebox.showerror("错误", "无效的输入，价格必须是数字")
        except IOError:
            messagebox.showerror("错误", f"无法写入价格文件：{file_path}")
    
    tk.Button(price_window, text="保存", command=save_prices).grid(row=6, columnspan=2)

def show_results():
    try:
        with open(result_file_path, 'r') as result_file:
            results = result_file.read()
    except FileNotFoundError:
        messagebox.showerror("错误", "无法找到结果文件")
        results = ""
    except IOError:
        messagebox.showerror("错误", f"无法读取结果文件：{result_file_path}")
        results = ""
    
    messagebox.showinfo("结果信息", results)

# 创建显示价格按钮
show_prices_button = tk.Button(root, text="显示价格", command=show_prices)
show_prices_button.pack()

# 创建显示结果按钮
show_results_button = tk.Button(root, text="显示结果", command=show_results)
show_results_button.pack()

# 运行主循环
root.mainloop()

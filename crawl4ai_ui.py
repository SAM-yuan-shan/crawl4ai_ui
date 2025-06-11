"""
Crawl4AI 图形用户界面
===================

功能完整的网页爬取工具界面，适合小白用户使用

主要功能：
1. 基础网页爬取
2. 智能内容过滤
3. PDF导出
4. 网页截图
5. 信息提取
6. 批量处理

作者: Claude
版本: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import asyncio
import threading
import queue
import json
import os
from pathlib import Path
from datetime import datetime
import webbrowser
import nest_asyncio

# 应用nest_asyncio支持
nest_asyncio.apply()

# 导入Crawl4AI相关模块
try:
    from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
    from crawl4ai.content_filter_strategy import PruningContentFilter, BM25ContentFilter
    from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
    import base64
    CRAWL4AI_AVAILABLE = True
except ImportError as e:
    CRAWL4AI_AVAILABLE = False
    IMPORT_ERROR = str(e)

class Crawl4AI_GUI:
    """Crawl4AI 图形用户界面类"""
    
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.setup_ui()
        self.setup_output_queue()
        
        # 检查依赖
        if not CRAWL4AI_AVAILABLE:
            self.show_dependency_error()
    
    def setup_window(self):
        """设置主窗口"""
        self.root.title("Crawl4AI 网页爬取工具 v1.0.0")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # 设置图标（如果有的话）
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
    
    def setup_variables(self):
        """设置变量"""
        # 基础设置
        self.url_var = tk.StringVar(value="https://www.anthropic.com")
        self.output_dir_var = tk.StringVar(value="outputs")
        
        # 浏览器设置
        self.browser_type_var = tk.StringVar(value="chromium")
        self.headless_var = tk.BooleanVar(value=True)
        self.viewport_width_var = tk.IntVar(value=1280)
        self.viewport_height_var = tk.IntVar(value=720)
        
        # 过滤设置
        self.filter_type_var = tk.StringVar(value="none")
        self.keywords_var = tk.StringVar()
        
        # 导出设置
        self.export_markdown_var = tk.BooleanVar(value=True)
        self.export_pdf_var = tk.BooleanVar(value=False)
        self.export_screenshot_var = tk.BooleanVar(value=False)
        self.export_info_var = tk.BooleanVar(value=False)
        
        # 状态变量
        self.is_running = False
        
    def setup_ui(self):
        """设置用户界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(7, weight=1)
        
        # 创建各个区域
        self.create_header(main_frame)
        self.create_url_section(main_frame)
        self.create_browser_section(main_frame)
        self.create_filter_section(main_frame)
        self.create_export_section(main_frame)
        self.create_batch_section(main_frame)
        self.create_control_section(main_frame)
        self.create_output_section(main_frame)
        self.create_status_section(main_frame)
    
    def create_header(self, parent):
        """创建标题区域"""
        header_frame = ttk.LabelFrame(parent, text="🌐 Crawl4AI 网页爬取工具", padding="10")
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 主标题
        title_label = ttk.Label(header_frame, text="智能网页内容抓取与处理工具", 
                               font=("Microsoft YaHei", 14, "bold"))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # 功能介绍
        desc_label = ttk.Label(header_frame, 
                              text="支持内容过滤、PDF导出、截图、批量处理等功能，适合内容采集、数据分析使用",
                              font=("Microsoft YaHei", 9))
        desc_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # 帮助按钮
        help_btn = ttk.Button(header_frame, text="📖 使用说明", command=self.show_help)
        help_btn.grid(row=0, column=1, rowspan=2, sticky=tk.E)
        
        header_frame.columnconfigure(0, weight=1)
    
    def create_url_section(self, parent):
        """创建URL输入区域"""
        url_frame = ttk.LabelFrame(parent, text="🎯 目标网址", padding="10")
        url_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # URL输入
        ttk.Label(url_frame, text="网址:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=50)
        url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # 预设URL按钮
        preset_frame = ttk.Frame(url_frame)
        preset_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Label(preset_frame, text="快速选择:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        preset_urls = [
            ("Anthropic", "https://www.anthropic.com"),
            ("OpenAI", "https://openai.com"),
            ("百度", "https://www.baidu.com"),
            ("GitHub", "https://github.com")
        ]
        
        for i, (name, url) in enumerate(preset_urls):
            btn = ttk.Button(preset_frame, text=name, 
                           command=lambda u=url: self.url_var.set(u))
            btn.grid(row=0, column=i+1, padx=(0, 5))
        
        # 输出目录
        ttk.Label(url_frame, text="输出目录:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        output_entry = ttk.Entry(url_frame, textvariable=self.output_dir_var, width=40)
        output_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(0, 10), pady=(10, 0))
        
        browse_btn = ttk.Button(url_frame, text="浏览", command=self.browse_output_dir)
        browse_btn.grid(row=2, column=2, pady=(10, 0))
        
        url_frame.columnconfigure(1, weight=1)
    
    def create_browser_section(self, parent):
        """创建浏览器配置区域"""
        browser_frame = ttk.LabelFrame(parent, text="🌍 浏览器设置", padding="10")
        browser_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N), pady=(0, 10), padx=(0, 5))
        
        # 浏览器类型
        ttk.Label(browser_frame, text="浏览器类型:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        browser_combo = ttk.Combobox(browser_frame, textvariable=self.browser_type_var,
                                    values=["chromium", "firefox", "webkit"], state="readonly")
        browser_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # 无头模式
        headless_check = ttk.Checkbutton(browser_frame, text="无头模式（后台运行）", 
                                        variable=self.headless_var)
        headless_check.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        # 窗口大小
        ttk.Label(browser_frame, text="窗口宽度:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        width_spin = ttk.Spinbox(browser_frame, from_=800, to=1920, 
                               textvariable=self.viewport_width_var, width=10)
        width_spin.grid(row=2, column=1, sticky=tk.W, pady=(0, 5))
        
        ttk.Label(browser_frame, text="窗口高度:").grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        height_spin = ttk.Spinbox(browser_frame, from_=600, to=1080, 
                                textvariable=self.viewport_height_var, width=10)
        height_spin.grid(row=3, column=1, sticky=tk.W, pady=(0, 5))
        
        browser_frame.columnconfigure(1, weight=1)
    
    def create_filter_section(self, parent):
        """创建内容过滤区域"""
        filter_frame = ttk.LabelFrame(parent, text="🔍 内容过滤", padding="10")
        filter_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N), pady=(0, 10), padx=(5, 0))
        
        # 过滤类型
        ttk.Label(filter_frame, text="过滤模式:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_type_var,
                                   values=["none", "pruning", "bm25"], state="readonly")
        filter_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        filter_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        # 过滤说明
        self.filter_info_label = ttk.Label(filter_frame, text="无过滤：保留原始内容", 
                                          foreground="gray", font=("Microsoft YaHei", 8))
        self.filter_info_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        # 关键词输入（BM25专用）
        ttk.Label(filter_frame, text="关键词:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.keywords_entry = ttk.Entry(filter_frame, textvariable=self.keywords_var, 
                                       state="disabled")
        self.keywords_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # 关键词说明
        keywords_info = ttk.Label(filter_frame, text="用空格分隔多个关键词", 
                                 foreground="gray", font=("Microsoft YaHei", 8))
        keywords_info.grid(row=3, column=0, columnspan=2, sticky=tk.W)
        
        filter_frame.columnconfigure(1, weight=1)
    
    def create_export_section(self, parent):
        """创建导出选项区域"""
        export_frame = ttk.LabelFrame(parent, text="📥 导出选项", padding="10")
        export_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 导出选项
        export_options = [
            (self.export_markdown_var, "📄 Markdown文档", "导出为Markdown格式文本"),
            (self.export_pdf_var, "📑 PDF文档", "导出为PDF格式（需要较长时间）"),
            (self.export_screenshot_var, "📸 网页截图", "保存完整网页截图（文件较大）"),
            (self.export_info_var, "ℹ️ 页面信息", "提取页面元数据和统计信息")
        ]
        
        for i, (var, text, desc) in enumerate(export_options):
            row = i // 2
            col = i % 2
            
            frame = ttk.Frame(export_frame)
            frame.grid(row=row, column=col, sticky=(tk.W, tk.E), padx=(0, 20), pady=(0, 5))
            
            check = ttk.Checkbutton(frame, text=text, variable=var)
            check.grid(row=0, column=0, sticky=tk.W)
            
            desc_label = ttk.Label(frame, text=desc, foreground="gray", 
                                  font=("Microsoft YaHei", 8))
            desc_label.grid(row=1, column=0, sticky=tk.W)
        
        export_frame.columnconfigure(0, weight=1)
        export_frame.columnconfigure(1, weight=1)
    
    def create_batch_section(self, parent):
        """创建批量处理区域"""
        batch_frame = ttk.LabelFrame(parent, text="📋 批量处理", padding="10")
        batch_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 批量URL输入
        ttk.Label(batch_frame, text="批量URL（每行一个）:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.batch_text = scrolledtext.ScrolledText(batch_frame, height=4, width=50)
        self.batch_text.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # 批量操作按钮
        batch_btn_frame = ttk.Frame(batch_frame)
        batch_btn_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
        ttk.Button(batch_btn_frame, text="📂 从文件加载", 
                  command=self.load_urls_from_file).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(batch_btn_frame, text="💾 保存到文件", 
                  command=self.save_urls_to_file).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(batch_btn_frame, text="🗑️ 清空", 
                  command=self.clear_batch_urls).grid(row=0, column=2)
        
        batch_frame.columnconfigure(1, weight=1)
    
    def create_control_section(self, parent):
        """创建控制按钮区域"""
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 主要操作按钮
        self.start_btn = ttk.Button(control_frame, text="🚀 开始爬取", 
                                   command=self.start_crawling, style="Accent.TButton")
        self.start_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_btn = ttk.Button(control_frame, text="⏹️ 停止", 
                                  command=self.stop_crawling, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=(0, 10))
        
        # 其他功能按钮
        ttk.Button(control_frame, text="🗂️ 打开输出目录", 
                  command=self.open_output_dir).grid(row=0, column=2, padx=(0, 10))
        ttk.Button(control_frame, text="🧹 清理输出", 
                  command=self.clean_output).grid(row=0, column=3, padx=(0, 10))
        ttk.Button(control_frame, text="⚙️ 重置配置", 
                  command=self.reset_config).grid(row=0, column=4)
    
    def create_output_section(self, parent):
        """创建输出日志区域"""
        output_frame = ttk.LabelFrame(parent, text="📋 运行日志", padding="10")
        output_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 日志显示区域
        self.output_text = scrolledtext.ScrolledText(output_frame, height=15, 
                                                    font=("Consolas", 9))
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 日志控制按钮
        log_btn_frame = ttk.Frame(output_frame)
        log_btn_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(log_btn_frame, text="🗑️ 清空日志", 
                  command=self.clear_log).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(log_btn_frame, text="💾 保存日志", 
                  command=self.save_log).grid(row=0, column=1)
        
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
    
    def create_status_section(self, parent):
        """创建状态栏"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # 状态标签
        self.status_label = ttk.Label(status_frame, text="就绪", relief="sunken", padding="5")
        self.status_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # 进度条
        self.progress_bar = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress_bar.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        status_frame.columnconfigure(0, weight=1)
        status_frame.columnconfigure(1, weight=2)
    
    def setup_output_queue(self):
        """设置输出队列"""
        self.output_queue = queue.Queue()
        self.check_queue()
    
    def check_queue(self):
        """检查输出队列"""
        try:
            while True:
                message = self.output_queue.get_nowait()
                self.log_message(message)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_queue)
    
    def log_message(self, message):
        """记录日志消息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.output_text.insert(tk.END, formatted_message)
        self.output_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_status(self, status):
        """更新状态"""
        self.status_label.config(text=status)
        self.root.update_idletasks()
    
    # 事件处理方法
    def on_filter_change(self, event=None):
        """过滤类型改变时的处理"""
        filter_type = self.filter_type_var.get()
        
        if filter_type == "none":
            self.filter_info_label.config(text="无过滤：保留原始内容")
            self.keywords_entry.config(state="disabled")
        elif filter_type == "pruning":
            self.filter_info_label.config(text="智能修剪：自动移除导航、页脚等噪音内容")
            self.keywords_entry.config(state="disabled")
        elif filter_type == "bm25":
            self.filter_info_label.config(text="关键词过滤：基于BM25算法提取相关内容")
            self.keywords_entry.config(state="normal")
    
    def browse_output_dir(self):
        """浏览输出目录"""
        directory = filedialog.askdirectory(initialdir=self.output_dir_var.get())
        if directory:
            self.output_dir_var.set(directory)
    
    def load_urls_from_file(self):
        """从文件加载URL"""
        file_path = filedialog.askopenfilename(
            title="选择URL文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    urls = f.read()
                self.batch_text.delete('1.0', tk.END)
                self.batch_text.insert('1.0', urls)
                self.log_message(f"已从文件加载URL: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"加载文件失败: {str(e)}")
    
    def save_urls_to_file(self):
        """保存URL到文件"""
        file_path = filedialog.asksaveasfilename(
            title="保存URL文件",
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                urls = self.batch_text.get('1.0', tk.END).strip()
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(urls)
                self.log_message(f"已保存URL到文件: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存文件失败: {str(e)}")
    
    def clear_batch_urls(self):
        """清空批量URL"""
        self.batch_text.delete('1.0', tk.END)
    
    def open_output_dir(self):
        """打开输出目录"""
        output_dir = self.output_dir_var.get()
        if os.path.exists(output_dir):
            if os.name == 'nt':  # Windows
                os.startfile(output_dir)
            else:  # macOS and Linux
                webbrowser.open(f'file://{os.path.abspath(output_dir)}')
        else:
            messagebox.showwarning("警告", "输出目录不存在")
    
    def clean_output(self):
        """清理输出目录"""
        if messagebox.askyesno("确认", "确定要清理输出目录中的所有文件吗？\n此操作不可恢复！"):
            try:
                output_dir = Path(self.output_dir_var.get())
                if output_dir.exists():
                    import shutil
                    shutil.rmtree(output_dir)
                    output_dir.mkdir()
                    self.log_message("输出目录已清理")
                else:
                    self.log_message("输出目录不存在，无需清理")
            except Exception as e:
                messagebox.showerror("错误", f"清理失败: {str(e)}")
    
    def reset_config(self):
        """重置配置"""
        if messagebox.askyesno("确认", "确定要重置所有配置到默认值吗？"):
            self.setup_variables()
            self.log_message("配置已重置为默认值")
    
    def clear_log(self):
        """清空日志"""
        self.output_text.delete('1.0', tk.END)
    
    def save_log(self):
        """保存日志"""
        file_path = filedialog.asksaveasfilename(
            title="保存日志文件",
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                log_content = self.output_text.get('1.0', tk.END)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(log_content)
                self.log_message(f"日志已保存到: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存日志失败: {str(e)}")
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
Crawl4AI 网页爬取工具使用说明
============================

🎯 基本功能：
1. 输入要爬取的网址
2. 选择浏览器设置和过滤选项
3. 选择导出格式
4. 点击"开始爬取"

🌍 浏览器设置：
- Chromium: 推荐选择，兼容性最好
- Firefox: 适合某些特殊网站
- Webkit: 轻量级选择
- 无头模式: 后台运行，不显示浏览器窗口

🔍 内容过滤：
- 无过滤: 保留网页原始内容
- 智能修剪: 自动移除导航、广告等噪音
- 关键词过滤: 只保留包含指定关键词的内容

📥 导出选项：
- Markdown: 文本格式，体积小
- PDF: 文档格式，适合保存
- 截图: 图片格式，保留视觉效果
- 信息: JSON格式，包含元数据

📋 批量处理：
- 每行输入一个网址
- 支持从文件加载和保存URL列表
- 会按顺序依次处理所有网址

⚠️ 注意事项：
- 首次运行可能需要下载浏览器组件
- PDF和截图文件较大，注意存储空间
- 某些网站可能有反爬虫机制
- 网络连接问题可能导致爬取失败

💡 小贴士：
- 建议先用单个网址测试
- 复杂网站推荐使用智能修剪
- 批量处理时建议关闭截图功能
"""
        
        help_window = tk.Toplevel(self.root)
        help_window.title("使用说明")
        help_window.geometry("600x500")
        help_window.configure(bg='#f0f0f0')
        
        text_widget = scrolledtext.ScrolledText(help_window, font=("Microsoft YaHei", 10))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert('1.0', help_text)
        text_widget.config(state='disabled')
    
    def show_dependency_error(self):
        """显示依赖错误信息"""
        error_text = f"""
依赖库缺失错误
=============

错误信息: {IMPORT_ERROR}

解决方案:
1. 安装Crawl4AI: pip install crawl4ai
2. 安装其他依赖: pip install nest-asyncio
3. 重新启动程序

详细安装说明请参考项目文档。
"""
        
        messagebox.showerror("依赖错误", error_text)
        
        # 禁用相关功能
        self.start_btn.config(state="disabled")
    
    def start_crawling(self):
        """开始爬取"""
        if not CRAWL4AI_AVAILABLE:
            self.show_dependency_error()
            return
        
        if self.is_running:
            messagebox.showwarning("警告", "爬取任务正在运行中...")
            return
        
        # 验证输入
        url = self.url_var.get().strip()
        batch_urls = self.batch_text.get('1.0', tk.END).strip().split('\n')
        batch_urls = [u.strip() for u in batch_urls if u.strip()]
        
        if not url and not batch_urls:
            messagebox.showerror("错误", "请输入至少一个有效的网址")
            return
        
        # 检查导出选项
        if not any([self.export_markdown_var.get(), self.export_pdf_var.get(),
                   self.export_screenshot_var.get(), self.export_info_var.get()]):
            if not messagebox.askyesno("确认", "没有选择任何导出选项，是否继续？\n将只在日志中显示结果"):
                return
        
        # 检查关键词过滤
        if self.filter_type_var.get() == "bm25" and not self.keywords_var.get().strip():
            messagebox.showerror("错误", "使用关键词过滤时必须输入关键词")
            return
        
        # 准备URL列表
        urls_to_process = []
        if url:
            urls_to_process.append(url)
        urls_to_process.extend(batch_urls)
        
        # 启动爬取任务
        self.is_running = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.progress_bar.start()
        
        # 在新线程中运行异步任务
        threading.Thread(target=self.run_crawling_task, 
                        args=(urls_to_process,), daemon=True).start()
    
    def run_crawling_task(self, urls):
        """运行爬取任务"""
        try:
            # 创建新的事件循环
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # 运行异步爬取
            loop.run_until_complete(self.async_crawl_urls(urls))
            
        except Exception as e:
            self.output_queue.put(f"❌ 爬取任务异常: {str(e)}")
        finally:
            # 恢复UI状态
            self.root.after(0, self.crawling_finished)
    
    async def async_crawl_urls(self, urls):
        """异步爬取URL列表"""
        self.output_queue.put(f"🚀 开始爬取 {len(urls)} 个网址...")
        
        # 创建输出目录
        output_dir = Path(self.output_dir_var.get())
        output_dir.mkdir(exist_ok=True)
        
        # 创建子目录
        if self.export_markdown_var.get():
            (output_dir / "markdown").mkdir(exist_ok=True)
        if self.export_pdf_var.get():
            (output_dir / "pdf").mkdir(exist_ok=True)
        if self.export_screenshot_var.get():
            (output_dir / "screenshots").mkdir(exist_ok=True)
        if self.export_info_var.get():
            (output_dir / "info").mkdir(exist_ok=True)
        
        # 配置浏览器
        browser_config = BrowserConfig(
            browser_type=self.browser_type_var.get(),
            headless=self.headless_var.get(),
            viewport_width=self.viewport_width_var.get(),
            viewport_height=self.viewport_height_var.get()
        )
        
        # 配置内容过滤
        content_filter = None
        if self.filter_type_var.get() == "pruning":
            content_filter = PruningContentFilter()
        elif self.filter_type_var.get() == "bm25":
            keywords = self.keywords_var.get().strip()
            content_filter = BM25ContentFilter(user_query=keywords)
        
        # 配置爬虫运行参数
        run_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            content_filter=content_filter,
            pdf=self.export_pdf_var.get(),
            screenshot=self.export_screenshot_var.get(),
            markdown_generator=DefaultMarkdownGenerator(
                options={"ignore_links": True, "ignore_images": True}
            ) if content_filter else None
        )
        
        # 统计信息
        success_count = 0
        total_count = len(urls)
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            for i, url in enumerate(urls, 1):
                if not self.is_running:  # 检查是否被停止
                    self.output_queue.put("⏹️ 爬取已停止")
                    break
                
                self.output_queue.put(f"\n📄 [{i}/{total_count}] 处理: {url}")
                self.root.after(0, lambda: self.update_status(f"处理 {i}/{total_count}: {url[:50]}..."))
                
                try:
                    result = await crawler.arun(url=url, config=run_config)
                    
                    if result.success:
                        success_count += 1
                        self.output_queue.put(f"✅ 爬取成功")
                        
                        # 生成文件名前缀
                        safe_url = url.replace("https://", "").replace("http://", "").replace("/", "_")
                        if len(safe_url) > 50:
                            safe_url = safe_url[:50]
                        filename_prefix = f"{i:03d}_{safe_url}"
                        
                        # 保存Markdown
                        if self.export_markdown_var.get():
                            md_file = output_dir / "markdown" / f"{filename_prefix}.md"
                            with open(md_file, 'w', encoding='utf-8') as f:
                                f.write(result.markdown)
                            self.output_queue.put(f"   📄 Markdown已保存: {md_file.name}")
                        
                        # 保存PDF
                        if self.export_pdf_var.get() and result.pdf:
                            pdf_file = output_dir / "pdf" / f"{filename_prefix}.pdf"
                            with open(pdf_file, 'wb') as f:
                                f.write(result.pdf)
                            self.output_queue.put(f"   📑 PDF已保存: {pdf_file.name} ({len(result.pdf)/1024:.1f}KB)")
                        
                        # 保存截图
                        if self.export_screenshot_var.get() and result.screenshot:
                            try:
                                screenshot_data = base64.b64decode(result.screenshot)
                                screenshot_file = output_dir / "screenshots" / f"{filename_prefix}.png"
                                with open(screenshot_file, 'wb') as f:
                                    f.write(screenshot_data)
                                self.output_queue.put(f"   📸 截图已保存: {screenshot_file.name} ({len(screenshot_data)/1024/1024:.1f}MB)")
                            except Exception as e:
                                self.output_queue.put(f"   ❌ 截图保存失败: {str(e)}")
                        
                        # 保存信息
                        if self.export_info_var.get():
                            info = {
                                "url": result.url,
                                "title": getattr(result, 'title', 'N/A'),
                                "content_length": len(result.markdown),
                                "word_count": len(result.markdown.split()),
                                "links": {
                                    "internal": len(result.links.get('internal', [])),
                                    "external": len(result.links.get('external', []))
                                } if result.links else {"internal": 0, "external": 0},
                                "images": len(result.media.get('images', [])) if result.media else 0,
                                "extract_time": datetime.now().isoformat()
                            }
                            
                            info_file = output_dir / "info" / f"{filename_prefix}_info.json"
                            with open(info_file, 'w', encoding='utf-8') as f:
                                json.dump(info, f, ensure_ascii=False, indent=2)
                            self.output_queue.put(f"   ℹ️ 信息已保存: {info_file.name}")
                        
                        # 显示内容统计
                        self.output_queue.put(f"   📊 内容长度: {len(result.markdown)} 字符")
                        
                    else:
                        self.output_queue.put(f"❌ 爬取失败: {result.error_message}")
                        
                except Exception as e:
                    self.output_queue.put(f"❌ 处理异常: {str(e)}")
        
        # 完成总结
        self.output_queue.put(f"\n🎉 爬取完成！")
        self.output_queue.put(f"   总计: {total_count} 个网址")
        self.output_queue.put(f"   成功: {success_count} 个")
        self.output_queue.put(f"   失败: {total_count - success_count} 个")
        self.output_queue.put(f"   输出目录: {output_dir}")
    
    def stop_crawling(self):
        """停止爬取"""
        if messagebox.askyesno("确认", "确定要停止当前的爬取任务吗？"):
            self.is_running = False
            self.output_queue.put("⏹️ 正在停止爬取任务...")
    
    def crawling_finished(self):
        """爬取完成后的UI更新"""
        self.is_running = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.progress_bar.stop()
        self.update_status("就绪")

def main():
    """主函数"""
    # 创建主窗口
    root = tk.Tk()
    
    # 设置主题样式
    style = ttk.Style()
    if "vista" in style.theme_names():
        style.theme_use("vista")
    elif "clam" in style.theme_names():
        style.theme_use("clam")
    
    # 创建应用实例
    app = Crawl4AI_GUI(root)
    
    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    main() 
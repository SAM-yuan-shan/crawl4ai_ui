#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境测试脚本
检查运行Crawl4AI UI所需的所有依赖
"""

import sys
import os

def test_python_version():
    """测试Python版本"""
    print(f"Python版本: {sys.version}")
    if sys.version_info >= (3, 7):
        print("✅ Python版本符合要求 (>=3.7)")
        return True
    else:
        print("❌ Python版本过低，需要3.7或更高版本")
        return False

def test_basic_modules():
    """测试基础模块"""
    modules = [
        ('sys', '系统模块'),
        ('os', '操作系统模块'),
        ('json', 'JSON处理'),
        ('pathlib', '路径处理'),
        ('datetime', '日期时间'),
        ('threading', '线程'),
        ('queue', '队列'),
        ('asyncio', '异步IO'),
    ]
    
    success = True
    for module_name, desc in modules:
        try:
            __import__(module_name)
            print(f"✅ {desc} ({module_name}) - 可用")
        except ImportError as e:
            print(f"❌ {desc} ({module_name}) - 不可用: {e}")
            success = False
    
    return success

def test_ui_modules():
    """测试UI相关模块"""
    try:
        import tkinter
        import tkinter.ttk
        import tkinter.filedialog
        import tkinter.messagebox
        import tkinter.scrolledtext
        print("✅ Tkinter UI库 - 完全可用")
        
        # 测试创建简单窗口
        root = tkinter.Tk()
        root.withdraw()  # 隐藏窗口
        root.destroy()   # 销毁窗口
        print("✅ Tkinter窗口创建 - 测试通过")
        return True
        
    except ImportError as e:
        print(f"❌ Tkinter UI库 - 不可用: {e}")
        print("解决方案:")
        print("  Windows: 重新安装Python，确保选中tkinter组件")
        print("  Ubuntu/Debian: sudo apt-get install python3-tk")
        print("  CentOS/RHEL: sudo yum install tkinter")
        return False
    except Exception as e:
        print(f"❌ Tkinter窗口创建失败: {e}")
        return False

def test_crawl4ai_modules():
    """测试Crawl4AI相关模块"""
    modules = [
        ('nest_asyncio', 'Nest Asyncio支持'),
        ('crawl4ai', 'Crawl4AI主模块'),
    ]
    
    success = True
    for module_name, desc in modules:
        try:
            if module_name == 'nest_asyncio':
                import nest_asyncio
                nest_asyncio.apply()
                print(f"✅ {desc} - 已安装并应用")
            elif module_name == 'crawl4ai':
                from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
                from crawl4ai.content_filter_strategy import PruningContentFilter, BM25ContentFilter
                print(f"✅ {desc} - 完全可用")
            else:
                __import__(module_name)
                print(f"✅ {desc} - 可用")
        except ImportError as e:
            print(f"❌ {desc} - 未安装: {e}")
            if module_name == 'nest_asyncio':
                print("   安装命令: pip install nest-asyncio")
            elif module_name == 'crawl4ai':
                print("   安装命令: pip install crawl4ai")
            success = False
        except Exception as e:
            print(f"⚠️ {desc} - 安装但有问题: {e}")
    
    return success

def test_file_structure():
    """测试文件结构"""
    required_files = [
        'crawl4ai_ui.py',
        'start_ui.py',
        'requirements.txt',
        'UI使用指南.md'
    ]
    
    success = True
    print("\n文件结构检查:")
    for file_name in required_files:
        if os.path.exists(file_name):
            size = os.path.getsize(file_name)
            print(f"✅ {file_name} - 存在 ({size} bytes)")
        else:
            print(f"❌ {file_name} - 缺失")
            success = False
    
    return success

def main():
    """主测试函数"""
    print("="*60)
    print("  Crawl4AI UI 环境测试")
    print("="*60)
    
    tests = [
        ("Python版本", test_python_version),
        ("基础模块", test_basic_modules),
        ("UI模块", test_ui_modules),
        ("Crawl4AI模块", test_crawl4ai_modules),
        ("文件结构", test_file_structure),
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        print(f"\n📋 测试: {test_name}")
        print("-" * 40)
        result = test_func()
        all_passed = all_passed and result
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 所有测试通过！可以运行UI界面")
        print("启动命令: python start_ui.py")
    else:
        print("❌ 部分测试失败，请根据上面的提示解决问题")
        print("或者先安装依赖: pip install -r requirements.txt")
    print("="*60)

if __name__ == "__main__":
    main() 
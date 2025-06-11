#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crawl4AI UI 启动器
================

简单的启动脚本，自动检查依赖并启动图形界面

使用方法：
    python start_ui.py
    或者
    双击运行此文件
"""

import sys
import subprocess
import os

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 7):
        print("❌ 错误: 需要Python 3.7或更高版本")
        print(f"   当前版本: {sys.version}")
        input("按回车键退出...")
        sys.exit(1)
    else:
        print(f"✅ Python版本检查通过: {sys.version.split()[0]}")

def check_and_install_dependencies():
    """检查并安装依赖"""
    required_packages = [
        'crawl4ai',
        'nest-asyncio',
        'tkinter'  # 通常内置，但仍然检查
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'tkinter':
                import tkinter
            elif package == 'crawl4ai':
                import crawl4ai
            elif package == 'nest-asyncio':
                import nest_asyncio
            print(f"✅ {package} 已安装")
        except ImportError:
            print(f"❌ {package} 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n🔧 需要安装以下依赖包: {', '.join(missing_packages)}")
        
        # 对于tkinter的特殊处理
        if 'tkinter' in missing_packages:
            print("⚠️  tkinter通常是Python内置模块")
            print("   如果缺失，请安装: sudo apt-get install python3-tk (Ubuntu/Debian)")
            print("   或者重新安装Python时选择包含tkinter")
        
        # 询问是否自动安装
        while True:
            choice = input("\n是否自动安装缺失的依赖？(y/n): ").lower().strip()
            if choice in ['y', 'yes', '是', '']:
                break
            elif choice in ['n', 'no', '否']:
                print("请手动安装依赖后重新运行")
                input("按回车键退出...")
                sys.exit(1)
            else:
                print("请输入 y 或 n")
        
        # 安装依赖
        for package in missing_packages:
            if package == 'tkinter':
                continue  # 跳过tkinter，需要系统级安装
            
            print(f"\n📦 正在安装 {package}...")
            try:
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', package
                ])
                print(f"✅ {package} 安装成功")
            except subprocess.CalledProcessError:
                print(f"❌ {package} 安装失败")
                print("请尝试手动安装:")
                print(f"   pip install {package}")
                input("按回车键退出...")
                sys.exit(1)
        
        print("\n🎉 所有依赖安装完成！")

def start_ui():
    """启动UI界面"""
    print("\n🚀 启动Crawl4AI图形界面...")
    
    try:
        # 导入并运行UI
        from crawl4ai_ui import main
        main()
    except ImportError as e:
        print(f"❌ 导入UI模块失败: {e}")
        print("请确保 crawl4ai_ui.py 文件在同一目录下")
        input("按回车键退出...")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 启动UI失败: {e}")
        input("按回车键退出...")
        sys.exit(1)

def main():
    """主函数"""
    print("=" * 50)
    print("  🌐 Crawl4AI 网页爬取工具")
    print("  版本: 1.0.0")
    print("  启动器正在初始化...")
    print("=" * 50)
    
    try:
        # 1. 检查Python版本
        print("\n📋 步骤1: 检查Python版本")
        check_python_version()
        
        # 2. 检查依赖
        print("\n📋 步骤2: 检查依赖包")
        check_and_install_dependencies()
        
        # 3. 启动UI
        print("\n📋 步骤3: 启动图形界面")
        start_ui()
        
    except KeyboardInterrupt:
        print("\n\n⏹️ 用户取消操作")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        input("按回车键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main() 
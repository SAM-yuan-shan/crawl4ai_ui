#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Crawl4AI 基础测试脚本
按照教程逐步测试各项功能
"""

import asyncio
import os
import nest_asyncio
from playwright.async_api import async_playwright

# 允许在Jupyter中使用异步操作
nest_asyncio.apply()

# 设置输出路径
OUTPUT_PATH = 'outputs/markdown/'

def output_md(base_filename, md_str):
    """保存markdown内容到文件"""
    # 创建输出目录
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    
    # 生成带长度的文件名
    length = len(md_str)
    name, ext = os.path.splitext(base_filename)
    filename = f"{name}({length}){ext}"
    
    # 完整路径
    full_path = os.path.join(OUTPUT_PATH, filename)
    
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(md_str)
    
    print(f"已保存到: {full_path}")
    return full_path

def check_version():
    """检查Crawl4AI版本"""
    try:
        import crawl4ai
        version = crawl4ai.__version__.__version__
        print(f"✅ Crawl4AI版本: {version}")
        return True
    except Exception as e:
        print(f"❌ Crawl4AI版本检查失败: {e}")
        return False

async def test_browser():
    """测试浏览器功能"""
    try:
        print("🔧 测试浏览器功能...")
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto('https://example.com')
            title = await page.title()
            print(f"✅ 浏览器测试成功! 标题: {title}")
            await browser.close()
        return True
    except Exception as e:
        print(f"❌ 浏览器测试失败: {e}")
        return False

async def test_basic_crawl(output_filename):
    """基础爬虫测试"""
    try:
        print("🕷️ 开始基础爬虫测试...")
        
        from crawl4ai import AsyncWebCrawler
        
        # 创建爬虫对象，自动管理资源
        async with AsyncWebCrawler() as crawler:
            # 访问指定网址并等待响应
            result = await crawler.arun("https://www.anthropic.com/news/agent-capabilities-api")
            
            # 打印抓取结果
            print(f"✅ 抓取成功! Markdown长度: {len(result.markdown)}")
            print("📝 前300字符预览:")
            print(result.markdown[:300])
            print("..." if len(result.markdown) > 300 else "")
            
            # 保存到.md文件
            saved_path = output_md(output_filename, result.markdown)
            print(f"💾 已保存到: {saved_path}")
            
        return True
        
    except Exception as e:
        print(f"❌ 基础爬虫测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """主函数"""
    print("🚀 开始Crawl4AI测试...")
    print("=" * 50)
    
    # 1. 检查版本
    if not check_version():
        return
        
    # 2. 测试浏览器
    if not await test_browser():
        return
        
    # 3. 测试基础爬虫
    if not await test_basic_crawl('1_1_Basic.md'):
        return
        
    print("=" * 50)
    print("🎉 所有测试通过!")

if __name__ == "__main__":
    asyncio.run(main()) 
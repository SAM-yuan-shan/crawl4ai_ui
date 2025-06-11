#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修复版Crawl4AI扩展功能测试脚本
"""

import asyncio
import os
import base64
import nest_asyncio

nest_asyncio.apply()

OUTPUT_PATH = 'outputs/'

def create_directories():
    """创建必要的目录"""
    dirs = ['outputs/markdown', 'outputs/pdf', 'outputs/screenshots']
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)

async def test_pdf_export():
    """测试PDF导出功能"""
    try:
        print("📄 测试PDF导出功能...")
        
        from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig
        
        # 浏览器配置
        browser_config = BrowserConfig(
            headless=True,
            viewport_width=1280,
            viewport_height=720,
            user_agent='Chrome/114.0.0.0',
        )
        
        # 爬虫运行配置，只启用PDF
        run_config = CrawlerRunConfig(
            pdf=True,      # 生成PDF
        )
        
        # 创建爬虫并执行
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(
                url="https://www.anthropic.com/news/agent-capabilities-api",
                config=run_config,
            )
            
            # 保存PDF
            if result.pdf:
                pdf_path = os.path.join(OUTPUT_PATH, 'pdf', 'test_page.pdf')
                with open(pdf_path, 'wb') as f:
                    f.write(result.pdf)
                print(f"✅ PDF已保存到: {pdf_path} ({len(result.pdf)} 字节)")
            else:
                print("⚠️ 未生成PDF")
            
        return True
        
    except Exception as e:
        print(f"❌ PDF导出测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_screenshot():
    """测试截图功能"""
    try:
        print("📷 测试截图功能...")
        
        from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig
        
        # 浏览器配置
        browser_config = BrowserConfig(
            headless=True,
            viewport_width=1280,
            viewport_height=720,
            user_agent='Chrome/114.0.0.0',
        )
        
        # 爬虫运行配置，只启用截图
        run_config = CrawlerRunConfig(
            screenshot=True,  # 生成截图
        )
        
        # 创建爬虫并执行
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(
                url="https://www.anthropic.com/news/agent-capabilities-api",
                config=run_config,
            )
            
            # 保存截图
            if result.screenshot:
                screenshot_path = os.path.join(OUTPUT_PATH, 'screenshots', 'test_page.png')
                
                # 检查截图数据类型并适当处理
                if isinstance(result.screenshot, str):
                    # 如果是base64字符串，需要解码
                    try:
                        screenshot_data = base64.b64decode(result.screenshot)
                        print("截图数据为base64格式，已解码")
                    except:
                        # 如果不是base64，可能是其他字符串格式
                        screenshot_data = result.screenshot.encode('utf-8')
                        print("截图数据为字符串格式，已编码")
                else:
                    # 如果已经是字节数据
                    screenshot_data = result.screenshot
                    print("截图数据为字节格式")
                
                with open(screenshot_path, 'wb') as f:
                    f.write(screenshot_data)
                print(f"✅ 截图已保存到: {screenshot_path} ({len(screenshot_data)} 字节)")
            else:
                print("⚠️ 未生成截图")
            
        return True
        
    except Exception as e:
        print(f"❌ 截图测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_basic_info():
    """测试基本信息提取"""
    try:
        print("ℹ️ 测试基本信息提取...")
        
        from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig
        
        # 浏览器配置
        browser_config = BrowserConfig(
            headless=True,
            viewport_width=1280,
            viewport_height=720,
            user_agent='Chrome/114.0.0.0',
        )
        
        # 创建爬虫并执行
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(
                url="https://www.anthropic.com/news/agent-capabilities-api",
            )
            
            print("📊 页面基本信息:")
            print(f"  - URL: {result.url}")
            print(f"  - 状态码: {result.status_code}")
            print(f"  - Markdown长度: {len(result.markdown)}")
            
            # 检查是否有链接信息
            if hasattr(result, 'links') and result.links:
                internal_count = len(result.links.get('internal', []))
                external_count = len(result.links.get('external', []))
                print(f"  - 内部链接: {internal_count}")
                print(f"  - 外部链接: {external_count}")
            
            # 检查是否有媒体信息
            if hasattr(result, 'media') and result.media:
                print("  - 媒体信息:")
                for media_type, items in result.media.items():
                    if isinstance(items, list):
                        print(f"    - {media_type}: {len(items)}个")
            
            # 保存基本信息
            info_text = f"""页面信息报告
=============

URL: {result.url}
状态码: {result.status_code}
Markdown长度: {len(result.markdown)}

内容预览 (前500字符):
{result.markdown[:500]}
"""
            
            info_path = os.path.join(OUTPUT_PATH, 'page_info.txt')
            with open(info_path, 'w', encoding='utf-8') as f:
                f.write(info_text)
            print(f"💾 页面信息已保存到: {info_path}")
            
        return True
        
    except Exception as e:
        print(f"❌ 基本信息提取测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """主函数"""
    print("🚀 开始Crawl4AI扩展功能测试...")
    print("=" * 60)
    
    # 创建目录
    create_directories()
    
    # 1. 测试PDF导出
    if not await test_pdf_export():
        return
        
    print("-" * 60)
    
    # 2. 测试截图
    if not await test_screenshot():
        return
        
    print("-" * 60)
    
    # 3. 测试基本信息提取
    if not await test_basic_info():
        return
        
    print("=" * 60)
    print("🎉 扩展功能测试完成!")
    
    # 显示生成的文件
    print("\n📁 生成的文件:")
    for root, dirs, files in os.walk(OUTPUT_PATH):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            print(f"  - {file_path} ({file_size} 字节)")

if __name__ == "__main__":
    asyncio.run(main()) 
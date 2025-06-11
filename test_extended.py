#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Crawl4AI 扩展功能测试脚本
测试PDF导出、截图、链接提取、图片信息提取等扩展功能
"""

import asyncio
import os
import nest_asyncio

nest_asyncio.apply()

OUTPUT_PATH = 'outputs/'

def create_directories():
    """创建必要的目录"""
    dirs = ['outputs/markdown', 'outputs/pdf', 'outputs/screenshots']
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)

async def test_pdf_and_screenshot():
    """测试PDF导出和截图功能"""
    try:
        print("📄 测试PDF导出和截图功能...")
        
        from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig
        
        # 浏览器配置
        browser_config = BrowserConfig(
            headless=True,
            viewport_width=1280,
            viewport_height=720,
            user_agent='Chrome/114.0.0.0',
        )
        
        # 爬虫运行配置，启用PDF和截图
        run_config = CrawlerRunConfig(
            pdf=True,      # 生成PDF
            screenshot=True,  # 生成截图
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
                print(f"✅ PDF已保存到: {pdf_path}")
            
            # 保存截图
            if result.screenshot:
                screenshot_path = os.path.join(OUTPUT_PATH, 'screenshots', 'test_page.png')
                with open(screenshot_path, 'wb') as f:
                    f.write(result.screenshot)
                print(f"✅ 截图已保存到: {screenshot_path}")
            
        return True
        
    except Exception as e:
        print(f"❌ PDF和截图测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_links_extraction():
    """测试链接提取功能"""
    try:
        print("🔗 测试链接提取功能...")
        
        from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig
        
        # 浏览器配置
        browser_config = BrowserConfig(
            headless=True,
            viewport_width=1280,
            viewport_height=720,
            user_agent='Chrome/114.0.0.0',
        )
        
        # 爬虫运行配置
        run_config = CrawlerRunConfig(
            # 这些参数不会影响链接收集，链接会自动存储到result.links
            exclude_external_links=False,  # 不排除外部链接
            exclude_social_media_links=False,  # 不排除社交媒体链接
        )
        
        # 创建爬虫并执行
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(
                url="https://www.anthropic.com/news/agent-capabilities-api",
                config=run_config,
            )
            
            # 分析链接
            if hasattr(result, 'links') and result.links:
                internal_links = result.links.get('internal', [])
                external_links = result.links.get('external', [])
                
                print(f"✅ 内部链接数量: {len(internal_links)}")
                print(f"✅ 外部链接数量: {len(external_links)}")
                
                # 显示前几个内部链接示例
                print("📍 内部链接示例 (前5个):")
                for i, link in enumerate(internal_links[:5]):
                    print(f"  {i+1}. 文字: '{link.get('text', '')[:50]}' -> URL: {link.get('href', '')}")
                
                # 显示前几个外部链接示例
                if external_links:
                    print("🌐 外部链接示例 (前5个):")
                    for i, link in enumerate(external_links[:5]):
                        print(f"  {i+1}. 文字: '{link.get('text', '')[:50]}' -> URL: {link.get('href', '')}")
                
                # 保存链接信息到文件
                links_info = f"内部链接数量: {len(internal_links)}\n外部链接数量: {len(external_links)}\n\n"
                links_info += "=== 内部链接 ===\n"
                for link in internal_links:
                    links_info += f"文字: {link.get('text', '')}\nURL: {link.get('href', '')}\n\n"
                
                if external_links:
                    links_info += "\n=== 外部链接 ===\n"
                    for link in external_links:
                        links_info += f"文字: {link.get('text', '')}\nURL: {link.get('href', '')}\n\n"
                
                links_path = os.path.join(OUTPUT_PATH, 'links_info.txt')
                with open(links_path, 'w', encoding='utf-8') as f:
                    f.write(links_info)
                print(f"💾 链接信息已保存到: {links_path}")
                
            else:
                print("⚠️ 未找到链接信息")
                
        return True
        
    except Exception as e:
        print(f"❌ 链接提取测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_images_extraction():
    """测试图片信息提取功能"""
    try:
        print("🖼️ 测试图片信息提取功能...")
        
        from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig
        
        # 浏览器配置
        browser_config = BrowserConfig(
            headless=True,
            viewport_width=1280,
            viewport_height=720,
            user_agent='Chrome/114.0.0.0',
        )
        
        # 爬虫运行配置
        run_config = CrawlerRunConfig()
        
        # 创建爬虫并执行
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(
                url="https://www.anthropic.com/news/agent-capabilities-api",
                config=run_config,
            )
            
            # 分析图片信息
            if hasattr(result, 'media') and result.media and 'images' in result.media:
                images = result.media['images']
                print(f"✅ 找到图片数量: {len(images)}")
                
                # 显示图片信息
                print("🖼️ 图片信息:")
                for i, img in enumerate(images[:5]):  # 只显示前5个
                    print(f"  {i+1}. URL: {img.get('src', 'N/A')}")
                    print(f"     Alt: {img.get('alt', 'N/A')}")
                    print(f"     描述: {img.get('desc', 'N/A')}")
                    print()
                
                # 保存图片信息到文件
                images_info = f"图片总数: {len(images)}\n\n"
                for i, img in enumerate(images):
                    images_info += f"=== 图片 {i+1} ===\n"
                    images_info += f"URL: {img.get('src', 'N/A')}\n"
                    images_info += f"Alt文本: {img.get('alt', 'N/A')}\n"
                    images_info += f"描述: {img.get('desc', 'N/A')}\n\n"
                
                images_path = os.path.join(OUTPUT_PATH, 'images_info.txt')
                with open(images_path, 'w', encoding='utf-8') as f:
                    f.write(images_info)
                print(f"💾 图片信息已保存到: {images_path}")
                
            else:
                print("⚠️ 未找到图片信息")
                
        return True
        
    except Exception as e:
        print(f"❌ 图片信息提取测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_comprehensive_extraction():
    """综合测试：同时提取多种信息"""
    try:
        print("🔍 综合测试：同时提取多种信息...")
        
        from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig
        from crawl4ai.content_filter_strategy import PruningContentFilter
        from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
        
        # 浏览器配置
        browser_config = BrowserConfig(
            headless=True,
            viewport_width=1280,
            viewport_height=720,
            user_agent='Chrome/114.0.0.0',
        )
        
        # 高级配置：同时启用多种功能
        run_config = CrawlerRunConfig(
            markdown_generator=DefaultMarkdownGenerator(
                content_filter=PruningContentFilter(threshold=0.8),
                options={
                    "ignore_links": False,  # 保留链接以便分析
                    "ignore_images": False,  # 保留图片以便分析
                }
            ),
            pdf=True,
            screenshot=True,
        )
        
        # 创建爬虫并执行
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(
                url="https://www.anthropic.com/news/agent-capabilities-api",
                config=run_config,
            )
            
            print("📊 综合分析结果:")
            print(f"  - Markdown长度: {len(result.markdown.fit_markdown if hasattr(result.markdown, 'fit_markdown') else result.markdown)}")
            print(f"  - PDF大小: {len(result.pdf) if result.pdf else 0} 字节")
            print(f"  - 截图大小: {len(result.screenshot) if result.screenshot else 0} 字节")
            
            # 保存综合结果
            if hasattr(result.markdown, 'fit_markdown'):
                markdown_content = result.markdown.fit_markdown
            else:
                markdown_content = result.markdown
                
            md_path = os.path.join(OUTPUT_PATH, 'markdown', 'comprehensive_test.md')
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"  - Markdown已保存到: {md_path}")
            
            if result.pdf:
                pdf_path = os.path.join(OUTPUT_PATH, 'pdf', 'comprehensive_test.pdf')
                with open(pdf_path, 'wb') as f:
                    f.write(result.pdf)
                print(f"  - PDF已保存到: {pdf_path}")
            
            if result.screenshot:
                screenshot_path = os.path.join(OUTPUT_PATH, 'screenshots', 'comprehensive_test.png')
                with open(screenshot_path, 'wb') as f:
                    f.write(result.screenshot)
                print(f"  - 截图已保存到: {screenshot_path}")
            
        return True
        
    except Exception as e:
        print(f"❌ 综合测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """主函数"""
    print("🚀 开始Crawl4AI扩展功能测试...")
    print("=" * 60)
    
    # 创建目录
    create_directories()
    
    # 1. 测试PDF和截图
    if not await test_pdf_and_screenshot():
        return
        
    print("-" * 60)
    
    # 2. 测试链接提取
    if not await test_links_extraction():
        return
        
    print("-" * 60)
    
    # 3. 测试图片信息提取
    if not await test_images_extraction():
        return
        
    print("-" * 60)
    
    # 4. 综合测试
    if not await test_comprehensive_extraction():
        return
        
    print("=" * 60)
    print("🎉 所有扩展功能测试通过!")

if __name__ == "__main__":
    asyncio.run(main()) 
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Crawl4AI 高级测试脚本
测试浏览器配置、内容过滤、markdown生成器等高级功能
"""

import asyncio
import os
import nest_asyncio

# 允许在Jupyter中使用异步操作
nest_asyncio.apply()

# 设置输出路径
OUTPUT_PATH = 'outputs/markdown/'

def output_md(base_filename, md_str):
    """保存markdown内容到文件"""
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    
    length = len(md_str)
    name, ext = os.path.splitext(base_filename)
    filename = f"{name}({length}){ext}"
    
    full_path = os.path.join(OUTPUT_PATH, filename)
    
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(md_str)
    
    print(f"已保存到: {full_path}")
    return full_path

async def test_browser_config(output_filename):
    """测试浏览器配置功能"""
    try:
        print("🔧 测试浏览器配置...")
        
        from crawl4ai import AsyncWebCrawler, BrowserConfig
        
        # 配置浏览器参数
        browser_config = BrowserConfig(
            headless=True,  # 无头模式，不显示浏览器窗口
            viewport_width=1280,   # 窗口宽度
            viewport_height=720,   # 窗口高度
            user_agent='Chrome/114.0.0.0',  # 浏览器标识
            text_mode=True, # 禁用图片加载，可能会加速仅文本的爬取
        )
        
        # 创建异步网页爬虫，自动管理资源
        async with AsyncWebCrawler(config=browser_config) as crawler:
            # 执行网页爬取
            result = await crawler.arun(
                url="https://www.anthropic.com/news/agent-capabilities-api",  # 目标网址
            )
            
            # 显示爬取结果
            print(f"✅ 浏览器配置测试成功! Markdown长度: {len(result.markdown)}")
            print("📝 前300字符预览:")
            print(result.markdown[:300])
            
            output_md(output_filename, result.markdown)
            
        return True
        
    except Exception as e:
        print(f"❌ 浏览器配置测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_crawler_run_config(output_filename):
    """测试爬虫运行配置"""
    try:
        print("⚙️ 测试爬虫运行配置...")
        
        from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
        from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
        
        # 配置浏览器参数
        browser_config = BrowserConfig(
            headless=True,
            viewport_width=1280,
            viewport_height=720,
            user_agent='Chrome/114.0.0.0',
            text_mode=True,
        )
        
        # 配置爬虫运行参数
        run_config = CrawlerRunConfig(
            cache_mode=CacheMode.DISABLED,  # 禁用缓存，获取最新内容
            markdown_generator=DefaultMarkdownGenerator(),
        )
        
        # 创建异步网页爬虫，自动管理资源
        async with AsyncWebCrawler(config=browser_config) as crawler:
            # 执行网页爬取
            result = await crawler.arun(
                url="https://www.anthropic.com/news/agent-capabilities-api",
                config=run_config,
            )
            
            print(f"✅ 运行配置测试成功! Markdown长度: {len(result.markdown)}")
            output_md(output_filename, result.markdown)
            
        return True
        
    except Exception as e:
        print(f"❌ 运行配置测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_content_filter_pruning(output_filename):
    """测试PruningContentFilter内容过滤"""
    try:
        print("🔍 测试PruningContentFilter内容过滤...")
        
        from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, BrowserConfig
        from crawl4ai.content_filter_strategy import PruningContentFilter
        from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
        
        # 浏览器配置
        browser_config = BrowserConfig(
            headless=True,
            viewport_width=1280,
            viewport_height=720,
            user_agent='Chrome/114.0.0.0',
            text_mode=True,
        )
        
        # 爬虫运行配置
        run_config = CrawlerRunConfig(
            cache_mode=CacheMode.DISABLED,
            markdown_generator=DefaultMarkdownGenerator(
                content_filter=PruningContentFilter(
                    threshold=0.76,  # 过滤阈值
                    threshold_type="fixed",  # 固定阈值
                ),
            ),
        )
        
        # 创建爬虫并执行
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(
                url="https://www.anthropic.com/news/agent-capabilities-api",
                config=run_config,
            )
            
            # 保存原始内容
            print(f"原始Markdown长度: {len(result.markdown.raw_markdown)}")
            output_md(output_filename.replace('.md', '_raw.md'), result.markdown.raw_markdown)
            
            # 保存过滤后内容
            print(f"✅ 过滤后Markdown长度: {len(result.markdown.fit_markdown)}")
            output_md(output_filename.replace('.md', '_fit.md'), result.markdown.fit_markdown)
            
        return True
        
    except Exception as e:
        print(f"❌ 内容过滤测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_content_filter_with_options(output_filename):
    """测试带Options的内容过滤"""
    try:
        print("📝 测试内容过滤 + Options...")
        
        from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, BrowserConfig
        from crawl4ai.content_filter_strategy import PruningContentFilter
        from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
        
        # 浏览器配置
        browser_config = BrowserConfig(
            headless=True,
            viewport_width=1280,
            viewport_height=720,
            user_agent='Chrome/114.0.0.0',
            text_mode=True,
        )
        
        # 爬虫运行配置
        run_config = CrawlerRunConfig(
            cache_mode=CacheMode.DISABLED,
            markdown_generator=DefaultMarkdownGenerator(
                content_filter=PruningContentFilter(
                    threshold=0.76,
                    threshold_type="dynamic",  # 动态阈值
                ),
                options={
                    "ignore_links": True,     # 移除超链接
                    "ignore_images": True,    # 移除图片引用
                }
            ),
        )
        
        # 创建爬虫并执行
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(
                url="https://www.anthropic.com/news/agent-capabilities-api",
                config=run_config,
            )
            
            # 保存原始内容
            print(f"原始Markdown长度: {len(result.markdown.raw_markdown)}")
            output_md(output_filename.replace('.md', '_raw.md'), result.markdown.raw_markdown)
            
            # 保存过滤后内容
            print(f"✅ 过滤后Markdown长度: {len(result.markdown.fit_markdown)}")
            output_md(output_filename.replace('.md', '_fit.md'), result.markdown.fit_markdown)
            
        return True
        
    except Exception as e:
        print(f"❌ Options测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_bm25_content_filter(output_filename):
    """测试BM25内容过滤"""
    try:
        print("🔤 测试BM25内容过滤...")
        
        from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, BrowserConfig
        from crawl4ai.content_filter_strategy import BM25ContentFilter
        from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
        
        # 浏览器配置
        browser_config = BrowserConfig(
            headless=True,
            viewport_width=1280,
            viewport_height=720,
            user_agent='Chrome/114.0.0.0',
            text_mode=True,
        )
        
        # 爬虫运行配置
        run_config = CrawlerRunConfig(
            cache_mode=CacheMode.DISABLED,
            markdown_generator=DefaultMarkdownGenerator(
                content_filter=BM25ContentFilter(
                    user_query="ANTHROPIC API",  # 关键词查询
                    threshold=1.2,  # BM25阈值
                ),
                options={
                    "ignore_links": True,
                    "ignore_images": True,
                }
            ),
        )
        
        # 创建爬虫并执行
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(
                url="https://www.anthropic.com/news/agent-capabilities-api",
                config=run_config,
            )
            
            # 保存原始内容
            print(f"原始Markdown长度: {len(result.markdown.raw_markdown)}")
            output_md(output_filename.replace('.md', '_raw.md'), result.markdown.raw_markdown)
            
            # 保存过滤后内容
            print(f"✅ BM25过滤后Markdown长度: {len(result.markdown.fit_markdown)}")
            output_md(output_filename.replace('.md', '_fit.md'), result.markdown.fit_markdown)
            
        return True
        
    except Exception as e:
        print(f"❌ BM25过滤测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """主函数"""
    print("🚀 开始Crawl4AI高级功能测试...")
    print("=" * 60)
    
    # 1. 测试浏览器配置
    if not await test_browser_config('2_1_BrowserConfig.md'):
        return
        
    print("-" * 60)
    
    # 2. 测试爬虫运行配置
    if not await test_crawler_run_config('2_2_0_RunConfig.md'):
        return
        
    print("-" * 60)
    
    # 3. 测试内容过滤 - Pruning
    if not await test_content_filter_pruning('2_2_1_ContentFilterPruning.md'):
        return
        
    print("-" * 60)
    
    # 4. 测试内容过滤 + Options
    if not await test_content_filter_with_options('2_2_2_ContentFilterPruning_Options.md'):
        return
        
    print("-" * 60)
    
    # 5. 测试BM25内容过滤
    if not await test_bm25_content_filter('2_2_3_BM25ContentFilter.md'):
        return
        
    print("=" * 60)
    print("🎉 所有高级功能测试通过!")

if __name__ == "__main__":
    asyncio.run(main()) 
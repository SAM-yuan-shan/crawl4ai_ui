#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修复版BM25内容过滤测试
"""

import asyncio
import os
import nest_asyncio

nest_asyncio.apply()

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

async def test_bm25_content_filter_fixed():
    """测试修复版BM25内容过滤"""
    try:
        print("🔤 测试修复版BM25内容过滤...")
        
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
        
        # 先检查BM25ContentFilter的正确参数
        print("检查BM25ContentFilter参数...")
        try:
            # 尝试不同的参数组合
            content_filter = BM25ContentFilter(
                user_query="ANTHROPIC API"
            )
            print("✅ BM25ContentFilter创建成功")
        except Exception as e:
            print(f"尝试其他参数: {e}")
            try:
                content_filter = BM25ContentFilter(
                    query="ANTHROPIC API"
                )
                print("✅ BM25ContentFilter创建成功 (使用query参数)")
            except Exception as e2:
                print(f"再次尝试: {e2}")
                content_filter = BM25ContentFilter()
                print("✅ BM25ContentFilter创建成功 (使用默认参数)")
        
        # 爬虫运行配置
        run_config = CrawlerRunConfig(
            cache_mode=CacheMode.DISABLED,
            markdown_generator=DefaultMarkdownGenerator(
                content_filter=content_filter,
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
            output_md('2_2_3_BM25ContentFilter_raw.md', result.markdown.raw_markdown)
            
            # 保存过滤后内容
            print(f"✅ BM25过滤后Markdown长度: {len(result.markdown.fit_markdown)}")
            output_md('2_2_3_BM25ContentFilter_fit.md', result.markdown.fit_markdown)
            
        return True
        
    except Exception as e:
        print(f"❌ BM25过滤测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    await test_bm25_content_filter_fixed()

if __name__ == "__main__":
    asyncio.run(main()) 
"""
Crawl4AI 实用工具脚本
提供简单易用的接口来执行常见的爬取任务
"""

import asyncio
import nest_asyncio
import argparse
import json
import os
from pathlib import Path
from datetime import datetime
import base64

# 应用nest_asyncio以支持在已有事件循环中运行
nest_asyncio.apply()

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter, BM25ContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

class CrawlUtility:
    """Crawl4AI 实用工具类"""
    
    def __init__(self, output_dir="outputs"):
        """初始化工具"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    async def simple_crawl(self, url, output_file=None):
        """简单爬取网页内容"""
        print(f"🌐 开始爬取: {url}")
        
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)
            
            if result.success:
                print(f"✅ 爬取成功，内容长度: {len(result.markdown)} 字符")
                
                # 保存到文件
                if output_file:
                    output_path = self.output_dir / output_file
                else:
                    filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
                    output_path = self.output_dir / f"{filename}.md"
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(result.markdown)
                
                print(f"📁 已保存到: {output_path}")
                return result.markdown
            else:
                print(f"❌ 爬取失败: {result.error_message}")
                return None
                
    async def clean_crawl(self, url, keywords=None, output_file=None):
        """爬取并清洗网页内容"""
        print(f"🧹 开始清洗爬取: {url}")
        
        # 选择过滤策略
        if keywords:
            content_filter = BM25ContentFilter(user_query=keywords)
            print(f"🔍 使用关键词过滤: {keywords}")
        else:
            content_filter = PruningContentFilter()
            print("🔧 使用智能内容修剪")
        
        run_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            content_filter=content_filter,
            markdown_generator=DefaultMarkdownGenerator(
                options={"ignore_links": True, "ignore_images": True}
            )
        )
        
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url, config=run_config)
            
            if result.success:
                print(f"✅ 清洗完成，内容长度: {len(result.markdown)} 字符")
                
                # 保存到文件
                if output_file:
                    output_path = self.output_dir / output_file
                else:
                    filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
                    suffix = f"_filtered_{keywords}" if keywords else "_cleaned"
                    output_path = self.output_dir / f"{filename}{suffix}.md"
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(result.markdown)
                
                print(f"📁 已保存到: {output_path}")
                return result.markdown
            else:
                print(f"❌ 清洗失败: {result.error_message}")
                return None
                
    async def pdf_export(self, url, output_file=None):
        """导出网页为PDF"""
        print(f"📄 开始PDF导出: {url}")
        
        run_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            pdf=True
        )
        
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url, config=run_config)
            
            if result.success and result.pdf:
                print(f"✅ PDF生成成功，大小: {len(result.pdf) / 1024:.1f} KB")
                
                # 保存PDF
                if output_file:
                    output_path = self.output_dir / output_file
                else:
                    filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
                    output_path = self.output_dir / f"{filename}.pdf"
                
                with open(output_path, 'wb') as f:
                    f.write(result.pdf)
                
                print(f"📁 已保存到: {output_path}")
                return str(output_path)
            else:
                print(f"❌ PDF导出失败: {result.error_message if not result.success else 'PDF生成失败'}")
                return None
                
    async def screenshot(self, url, output_file=None):
        """截取网页截图"""
        print(f"📸 开始截图: {url}")
        
        run_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            screenshot=True
        )
        
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url, config=run_config)
            
            if result.success and result.screenshot:
                try:
                    # 解码base64截图
                    screenshot_data = base64.b64decode(result.screenshot)
                    print(f"✅ 截图成功，大小: {len(screenshot_data) / 1024 / 1024:.1f} MB")
                    
                    # 保存截图
                    if output_file:
                        output_path = self.output_dir / output_file
                    else:
                        filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
                        output_path = self.output_dir / f"{filename}.png"
                    
                    with open(output_path, 'wb') as f:
                        f.write(screenshot_data)
                    
                    print(f"📁 已保存到: {output_path}")
                    return str(output_path)
                except Exception as e:
                    print(f"❌ 截图处理失败: {str(e)}")
                    return None
            else:
                print(f"❌ 截图失败: {result.error_message if not result.success else '截图生成失败'}")
                return None
                
    async def extract_info(self, url, output_file=None):
        """提取网页信息"""
        print(f"ℹ️ 开始信息提取: {url}")
        
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)
            
            if result.success:
                # 提取信息
                info = {
                    "url": result.url,
                    "title": getattr(result, 'title', 'N/A'),
                    "content_length": len(result.markdown),
                    "word_count": len(result.markdown.split()),
                    "links": {
                        "internal": len(result.links.get('internal', [])),
                        "external": len(result.links.get('external', []))
                    },
                    "images": len(result.media.get('images', [])) if result.media else 0,
                    "extract_time": datetime.now().isoformat()
                }
                
                print(f"✅ 信息提取完成")
                print(f"   标题: {info['title']}")
                print(f"   内容长度: {info['content_length']} 字符")
                print(f"   内部链接: {info['links']['internal']} 个")
                print(f"   外部链接: {info['links']['external']} 个")
                print(f"   图片: {info['images']} 个")
                
                # 保存信息
                if output_file:
                    output_path = self.output_dir / output_file
                else:
                    filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
                    output_path = self.output_dir / f"{filename}_info.json"
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(info, f, ensure_ascii=False, indent=2)
                
                print(f"📁 已保存到: {output_path}")
                return info
            else:
                print(f"❌ 信息提取失败: {result.error_message}")
                return None
                
    async def batch_crawl(self, urls, output_dir=None):
        """批量爬取多个URL"""
        print(f"🔄 开始批量爬取 {len(urls)} 个URL")
        
        if output_dir:
            batch_output_dir = Path(output_dir)
        else:
            batch_output_dir = self.output_dir / f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        batch_output_dir.mkdir(exist_ok=True)
        
        results = []
        
        async with AsyncWebCrawler() as crawler:
            for i, url in enumerate(urls, 1):
                print(f"  📄 [{i}/{len(urls)}] {url}")
                
                try:
                    result = await crawler.arun(url=url)
                    
                    if result.success:
                        # 生成文件名
                        filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
                        output_file = batch_output_dir / f"{i:03d}_{filename}.md"
                        
                        # 保存内容
                        with open(output_file, 'w', encoding='utf-8') as f:
                            f.write(result.markdown)
                        
                        results.append({
                            "url": url,
                            "success": True,
                            "file": str(output_file),
                            "length": len(result.markdown)
                        })
                        
                        print(f"     ✅ 成功，{len(result.markdown)} 字符")
                    else:
                        results.append({
                            "url": url,
                            "success": False,
                            "error": result.error_message
                        })
                        print(f"     ❌ 失败: {result.error_message}")
                        
                except Exception as e:
                    results.append({
                        "url": url,
                        "success": False,
                        "error": str(e)
                    })
                    print(f"     ❌ 异常: {str(e)}")
        
        # 保存批量结果报告
        report_file = batch_output_dir / "batch_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                "total_urls": len(urls),
                "successful": sum(1 for r in results if r["success"]),
                "failed": sum(1 for r in results if not r["success"]),
                "results": results,
                "created_at": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
        
        successful = sum(1 for r in results if r["success"])
        print(f"🎉 批量爬取完成: {successful}/{len(urls)} 成功")
        print(f"📁 结果保存在: {batch_output_dir}")
        
        return results

def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="Crawl4AI 实用工具")
    parser.add_argument("command", choices=["simple", "clean", "pdf", "screenshot", "info", "batch"], 
                        help="执行的命令")
    parser.add_argument("url", nargs="?", help="目标URL（batch模式下为文件路径）")
    parser.add_argument("-o", "--output", help="输出文件名")
    parser.add_argument("-k", "--keywords", help="关键词过滤（仅clean模式）")
    parser.add_argument("--output-dir", default="outputs", help="输出目录")
    
    args = parser.parse_args()
    
    # 创建工具实例
    utility = CrawlUtility(args.output_dir)
    
    async def run_command():
        if args.command == "simple":
            if not args.url:
                print("❌ 请提供URL")
                return
            await utility.simple_crawl(args.url, args.output)
            
        elif args.command == "clean":
            if not args.url:
                print("❌ 请提供URL")
                return
            await utility.clean_crawl(args.url, args.keywords, args.output)
            
        elif args.command == "pdf":
            if not args.url:
                print("❌ 请提供URL")
                return
            await utility.pdf_export(args.url, args.output)
            
        elif args.command == "screenshot":
            if not args.url:
                print("❌ 请提供URL")
                return
            await utility.screenshot(args.url, args.output)
            
        elif args.command == "info":
            if not args.url:
                print("❌ 请提供URL")
                return
            await utility.extract_info(args.url, args.output)
            
        elif args.command == "batch":
            if not args.url:
                print("❌ 请提供URL列表文件路径")
                return
            
            # 读取URL列表
            try:
                with open(args.url, 'r', encoding='utf-8') as f:
                    urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                await utility.batch_crawl(urls, args.output)
            except FileNotFoundError:
                print(f"❌ 文件不存在: {args.url}")
            except Exception as e:
                print(f"❌ 读取文件失败: {str(e)}")
    
    # 运行命令
    asyncio.run(run_command())

if __name__ == "__main__":
    main() 
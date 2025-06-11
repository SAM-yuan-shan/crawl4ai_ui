"""
Crawl4AI 综合功能测试脚本
整合所有功能：基础爬取、高级配置、内容过滤、PDF导出、截图等
"""

import asyncio
import nest_asyncio
import os
from datetime import datetime
import json
import base64
from pathlib import Path

# 应用nest_asyncio以支持在已有事件循环中运行
nest_asyncio.apply()

# Crawl4AI相关导入
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter, BM25ContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

class Crawl4AITester:
    """Crawl4AI综合测试类"""
    
    def __init__(self, base_output_dir="outputs"):
        """初始化测试器"""
        self.base_output_dir = Path(base_output_dir)
        self.create_output_dirs()
        
    def create_output_dirs(self):
        """创建输出目录结构"""
        dirs = [
            self.base_output_dir,
            self.base_output_dir / "markdown",
            self.base_output_dir / "pdf", 
            self.base_output_dir / "screenshots",
            self.base_output_dir / "json",
            self.base_output_dir / "reports"
        ]
        for dir_path in dirs:
            dir_path.mkdir(exist_ok=True)
            
    def log_result(self, test_name, result_info):
        """记录测试结果"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {test_name}: {result_info}")
        
    async def test_basic_crawling(self, url="https://www.anthropic.com"):
        """测试基础爬取功能"""
        print("\n=== 1. 基础爬取测试 ===")
        
        async with AsyncWebCrawler() as crawler:
            # 基础爬取
            result = await crawler.arun(url=url)
            
            if result.success:
                content_length = len(result.markdown)
                self.log_result("基础爬取", f"成功，内容长度: {content_length} 字符")
                
                # 保存结果
                output_file = self.base_output_dir / "markdown" / "basic_crawl.md"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(result.markdown)
                    
                return result
            else:
                self.log_result("基础爬取", f"失败: {result.error_message}")
                return None
                
    async def test_browser_config(self, url="https://www.anthropic.com"):
        """测试浏览器配置"""
        print("\n=== 2. 浏览器配置测试 ===")
        
        # 自定义浏览器配置
        browser_config = BrowserConfig(
            browser_type="chromium",
            headless=True,
            viewport_width=1920,
            viewport_height=1080,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(url=url)
            
            if result.success:
                content_length = len(result.markdown)
                self.log_result("浏览器配置", f"成功，内容长度: {content_length} 字符")
                
                # 保存结果
                output_file = self.base_output_dir / "markdown" / "browser_config.md"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(result.markdown)
                    
                return result
            else:
                self.log_result("浏览器配置", f"失败: {result.error_message}")
                return None
                
    async def test_content_filtering(self, url="https://www.anthropic.com"):
        """测试内容过滤功能"""
        print("\n=== 3. 内容过滤测试 ===")
        
        # 测试不同的内容过滤策略
        filters = [
            ("原始内容", None),
            ("Pruning过滤", PruningContentFilter()),
            ("BM25过滤", BM25ContentFilter(user_query="ANTHROPIC API AI"))
        ]
        
        results = {}
        
        async with AsyncWebCrawler() as crawler:
            for filter_name, content_filter in filters:
                print(f"\n测试 {filter_name}...")
                
                if content_filter:
                    run_config = CrawlerRunConfig(
                        cache_mode=CacheMode.BYPASS,
                        content_filter=content_filter,
                        markdown_generator=DefaultMarkdownGenerator(
                            options={"ignore_links": True, "ignore_images": True}
                        ) if filter_name == "Pruning过滤" else None
                    )
                else:
                    run_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)
                
                result = await crawler.arun(url=url, config=run_config)
                
                if result.success:
                    content_length = len(result.markdown)
                    self.log_result(filter_name, f"成功，内容长度: {content_length} 字符")
                    
                    # 保存结果
                    filename = filter_name.replace(" ", "_").lower()
                    output_file = self.base_output_dir / "markdown" / f"{filename}.md"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(result.markdown)
                        
                    results[filter_name] = {
                        "length": content_length,
                        "success": True,
                        "file": str(output_file)
                    }
                else:
                    self.log_result(filter_name, f"失败: {result.error_message}")
                    results[filter_name] = {
                        "success": False,
                        "error": result.error_message
                    }
        
        return results
        
    async def test_pdf_export(self, url="https://www.anthropic.com"):
        """测试PDF导出功能"""
        print("\n=== 4. PDF导出测试 ===")
        
        run_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            pdf=True
        )
        
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url, config=run_config)
            
            if result.success and result.pdf:
                pdf_size = len(result.pdf)
                self.log_result("PDF导出", f"成功，PDF大小: {pdf_size / 1024:.1f} KB")
                
                # 保存PDF
                output_file = self.base_output_dir / "pdf" / "comprehensive_test.pdf"
                with open(output_file, 'wb') as f:
                    f.write(result.pdf)
                    
                return {"success": True, "size": pdf_size, "file": str(output_file)}
            else:
                error_msg = result.error_message if not result.success else "PDF生成失败"
                self.log_result("PDF导出", f"失败: {error_msg}")
                return {"success": False, "error": error_msg}
                
    async def test_screenshot(self, url="https://www.anthropic.com"):
        """测试截图功能"""
        print("\n=== 5. 截图测试 ===")
        
        run_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            screenshot=True
        )
        
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url, config=run_config)
            
            if result.success and result.screenshot:
                # 处理base64截图数据
                try:
                    screenshot_data = base64.b64decode(result.screenshot)
                    screenshot_size = len(screenshot_data)
                    self.log_result("截图", f"成功，截图大小: {screenshot_size / 1024 / 1024:.1f} MB")
                    
                    # 保存截图
                    output_file = self.base_output_dir / "screenshots" / "comprehensive_test.png"
                    with open(output_file, 'wb') as f:
                        f.write(screenshot_data)
                        
                    return {"success": True, "size": screenshot_size, "file": str(output_file)}
                except Exception as e:
                    self.log_result("截图", f"处理失败: {str(e)}")
                    return {"success": False, "error": str(e)}
            else:
                error_msg = result.error_message if not result.success else "截图生成失败"
                self.log_result("截图", f"失败: {error_msg}")
                return {"success": False, "error": error_msg}
                
    async def test_metadata_extraction(self, url="https://www.anthropic.com"):
        """测试元数据提取"""
        print("\n=== 6. 元数据提取测试 ===")
        
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)
            
            if result.success:
                metadata = {
                    "url": result.url,
                    "title": getattr(result, 'title', 'N/A'),
                    "content_length": len(result.markdown),
                    "links_count": len(result.links.get('internal', [])) + len(result.links.get('external', [])),
                    "internal_links": len(result.links.get('internal', [])),
                    "external_links": len(result.links.get('external', [])),
                    "images_count": len(result.media.get('images', [])) if result.media else 0
                }
                
                self.log_result("元数据提取", f"成功，标题: {metadata['title']}")
                
                # 保存元数据
                output_file = self.base_output_dir / "json" / "metadata.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, ensure_ascii=False, indent=2)
                    
                return metadata
            else:
                self.log_result("元数据提取", f"失败: {result.error_message}")
                return None
                
    def generate_report(self, test_results):
        """生成测试报告"""
        print("\n=== 7. 生成测试报告 ===")
        
        report = {
            "test_time": datetime.now().isoformat(),
            "crawl4ai_version": "0.6.3",  # 实际版本
            "results": test_results,
            "summary": {
                "total_tests": len(test_results),
                "successful_tests": sum(1 for r in test_results.values() if isinstance(r, dict) and r.get('success', False)),
                "failed_tests": sum(1 for r in test_results.values() if isinstance(r, dict) and not r.get('success', True))
            }
        }
        
        # 保存报告
        report_file = self.base_output_dir / "reports" / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        # 生成简要报告
        summary_file = self.base_output_dir / "reports" / "latest_summary.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"Crawl4AI 综合测试报告\n")
            f.write(f"{'='*50}\n")
            f.write(f"测试时间: {report['test_time']}\n")
            f.write(f"版本: {report['crawl4ai_version']}\n")
            f.write(f"总测试数: {report['summary']['total_tests']}\n")
            f.write(f"成功: {report['summary']['successful_tests']}\n")
            f.write(f"失败: {report['summary']['failed_tests']}\n\n")
            
            for test_name, result in test_results.items():
                if isinstance(result, dict):
                    status = "✓" if result.get('success', False) else "✗"
                    f.write(f"{status} {test_name}\n")
                else:
                    f.write(f"- {test_name}: {result}\n")
        
        self.log_result("测试报告", f"已生成，保存至: {report_file}")
        return report
        
    async def run_comprehensive_test(self, test_url="https://www.anthropic.com"):
        """运行综合测试"""
        print("🚀 开始 Crawl4AI 综合功能测试")
        print(f"目标URL: {test_url}")
        print(f"输出目录: {self.base_output_dir}")
        
        test_results = {}
        
        try:
            # 1. 基础爬取测试
            basic_result = await self.test_basic_crawling(test_url)
            test_results["基础爬取"] = {"success": basic_result is not None}
            
            # 2. 浏览器配置测试
            browser_result = await self.test_browser_config(test_url)
            test_results["浏览器配置"] = {"success": browser_result is not None}
            
            # 3. 内容过滤测试
            filter_results = await self.test_content_filtering(test_url)
            test_results["内容过滤"] = filter_results
            
            # 4. PDF导出测试
            pdf_result = await self.test_pdf_export(test_url)
            test_results["PDF导出"] = pdf_result
            
            # 5. 截图测试
            screenshot_result = await self.test_screenshot(test_url)
            test_results["截图"] = screenshot_result
            
            # 6. 元数据提取测试
            metadata_result = await self.test_metadata_extraction(test_url)
            test_results["元数据提取"] = {"success": metadata_result is not None, "data": metadata_result}
            
            # 7. 生成测试报告
            report = self.generate_report(test_results)
            
            print("\n🎉 综合测试完成！")
            print(f"📊 测试结果: {report['summary']['successful_tests']}/{report['summary']['total_tests']} 通过")
            
            return test_results
            
        except Exception as e:
            print(f"❌ 测试过程中发生错误: {str(e)}")
            return {"error": str(e)}

async def main():
    """主函数"""
    # 创建测试器实例
    tester = Crawl4AITester()
    
    # 运行综合测试
    results = await tester.run_comprehensive_test()
    
    # 可以测试不同的网站
    # results = await tester.run_comprehensive_test("https://example.com")
    
    return results

if __name__ == "__main__":
    # 运行测试
    results = asyncio.run(main())
    print("\n✅ 所有测试已完成") 
# Crawl4AI 完整功能测试项目

## 📋 项目概述

这是一个完整的 Crawl4AI 功能测试项目，按照官方教程和最佳实践实现了所有核心功能，包括：

- ✅ 基础网页爬取
- ✅ 高级浏览器配置
- ✅ 智能内容过滤
- ✅ PDF导出功能
- ✅ 网页截图功能
- ✅ 元数据提取
- ✅ 批量测试和报告生成

## 🚀 快速开始

### 环境要求
- Python 3.8+
- 网络连接

### 安装步骤

```bash
# 1. 安装 Crawl4AI
pip install -U crawl4ai

# 2. 安装异步支持
pip install nest_asyncio

# 3. 安装浏览器驱动
python -m playwright install
```

### 运行测试

```bash
# 基础功能测试
python test_basic.py

# 高级功能测试
python test_advanced.py

# 扩展功能测试
python test_extended_fix.py

# 综合功能测试
python comprehensive_test.py
```

## 📁 项目结构

```
b_crawlforai/
├── README.md                 # 项目简介
├── PROJECT_GUIDE.md         # 详细使用指南（本文件）
├── test_basic.py            # 基础功能测试
├── test_advanced.py         # 高级配置测试
├── test_extended_fix.py     # 扩展功能测试
├── comprehensive_test.py    # 综合测试脚本
└── outputs/                 # 输出目录
    ├── markdown/           # Markdown 文件
    ├── pdf/               # PDF 文件
    ├── screenshots/       # 截图文件
    ├── json/             # JSON 数据
    └── reports/          # 测试报告
```

## 🔧 核心功能详解

### 1. 基础爬取功能

**文件**: `test_basic.py`

```python
from crawl4ai import AsyncWebCrawler

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(url="https://example.com")
    print(result.markdown)
```

**特点**:
- 简单易用的API
- 自动处理JavaScript渲染
- 返回清晰的Markdown格式

### 2. 浏览器配置

**文件**: `test_advanced.py`

```python
from crawl4ai import BrowserConfig

browser_config = BrowserConfig(
    browser_type="chromium",
    headless=True,
    viewport_width=1920,
    viewport_height=1080,
    user_agent="自定义User-Agent"
)
```

**配置选项**:
- 浏览器类型 (chromium, firefox, webkit)
- 无头模式控制
- 视窗大小设置
- 用户代理自定义

### 3. 内容过滤策略

#### PruningContentFilter - 智能内容修剪

```python
from crawl4ai.content_filter_strategy import PruningContentFilter

content_filter = PruningContentFilter()
# 自动移除导航、页脚、侧边栏等噪音内容
```

**效果**: 将内容从 10,881 字符压缩到 7,122 字符 (65.5%)

#### BM25ContentFilter - 关键词过滤

```python
from crawl4ai.content_filter_strategy import BM25ContentFilter

content_filter = BM25ContentFilter(user_query="ANTHROPIC API")
# 基于关键词相关性过滤内容
```

**效果**: 将内容从 10,881 字符压缩到 1,860 字符 (17.1%)

### 4. Markdown生成配置

```python
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

markdown_generator = DefaultMarkdownGenerator(
    options={
        "ignore_links": True,    # 忽略链接
        "ignore_images": True,   # 忽略图片
        "body_width": 120       # 内容宽度
    }
)
```

### 5. PDF导出功能

**文件**: `test_extended_fix.py`

```python
run_config = CrawlerRunConfig(
    cache_mode=CacheMode.BYPASS,
    pdf=True
)

result = await crawler.arun(url=url, config=run_config)
# result.pdf 包含PDF二进制数据
```

**特点**:
- 高质量PDF输出
- 保持原始页面布局
- 支持大页面完整导出

### 6. 网页截图功能

```python
run_config = CrawlerRunConfig(
    cache_mode=CacheMode.BYPASS,
    screenshot=True
)

result = await crawler.arun(url=url, config=run_config)
# result.screenshot 包含base64编码的PNG图片
```

**特点**:
- 全页面截图
- 高分辨率输出
- Base64编码便于处理

## 📊 测试结果对比

| 过滤方式 | 内容长度 | 压缩率 | 适用场景 |
|---------|---------|--------|----------|
| 原始内容 | 10,881字符 | 0% | 完整内容分析 |
| PruningContentFilter | 7,122字符 | 34.5% | 移除噪音内容 |
| Pruning + Options | 5,987字符 | 45.0% | 进一步精简 |
| BM25关键词过滤 | 1,860字符 | 82.9% | 特定主题提取 |

## 🎯 实际应用场景

### 1. 内容聚合
- 新闻网站内容提取
- 博客文章收集
- 产品信息爬取

### 2. 数据分析
- 竞品分析
- 市场研究
- 价格监控

### 3. 文档生成
- 网页转PDF
- 内容归档
- 报告生成

### 4. AI训练数据
- 文本预处理
- 数据清洗
- 格式标准化

## ⚙️ 高级配置

### 缓存控制

```python
from crawl4ai import CacheMode

# 强制重新爬取
config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)

# 使用缓存
config = CrawlerRunConfig(cache_mode=CacheMode.ENABLED)

# 仅写入缓存
config = CrawlerRunConfig(cache_mode=CacheMode.WRITE_ONLY)
```

### 等待策略

```python
run_config = CrawlerRunConfig(
    wait_for="css:.content",           # 等待CSS选择器
    delay_before_return_html=2.0,      # 延迟时间
    page_timeout=30000,                # 页面超时
    magic=True                         # 智能等待
)
```

### 自定义钩子

```python
async def before_goto_hook(page):
    # 页面导航前执行
    await page.set_extra_http_headers({"Custom-Header": "Value"})

run_config = CrawlerRunConfig(
    hooks={"before_goto": before_goto_hook}
)
```

## 🔍 错误处理

### 常见问题解决

1. **依赖冲突警告**
   ```
   WARNING: pip's dependency resolver does not currently consider 
   all the packages that are installed
   ```
   - 不影响核心功能
   - 可通过虚拟环境隔离

2. **浏览器启动失败**
   ```bash
   # 重新安装浏览器
   python -m playwright install --force
   ```

3. **内存不足**
   ```python
   # 减少并发数
   browser_config = BrowserConfig(
       browser_type="chromium",
       headless=True,
       chrome_args=["--max_old_space_size=4096"]
   )
   ```

## 📈 性能优化

### 1. 批量处理

```python
urls = ["url1", "url2", "url3"]
async with AsyncWebCrawler() as crawler:
    tasks = [crawler.arun(url=url) for url in urls]
    results = await asyncio.gather(*tasks)
```

### 2. 选择性提取

```python
# 仅提取文本，跳过图片和链接
markdown_generator = DefaultMarkdownGenerator(
    options={"ignore_links": True, "ignore_images": True}
)
```

### 3. 智能缓存

```python
# 长期缓存静态内容
run_config = CrawlerRunConfig(
    cache_mode=CacheMode.ENABLED,
    bypass_cache=False
)
```

## 🌟 最佳实践

1. **选择合适的过滤策略**
   - 数据分析: PruningContentFilter
   - 特定信息: BM25ContentFilter
   - 完整内容: 无过滤

2. **合理设置浏览器参数**
   - 生产环境: headless=True
   - 调试环境: headless=False

3. **处理大规模数据**
   - 使用异步并发
   - 设置合理的超时时间
   - 实现重试机制

4. **资源管理**
   - 及时关闭crawler
   - 清理临时文件
   - 监控内存使用

## 📚 参考资源

- [Crawl4AI GitHub](https://github.com/unclecode/crawl4ai)
- [Google Colab教程](https://colab.research.google.com/drive/1wz8u30rvbq6Scodye9AGCw8Qg_Z8QGsk)
- [官方文档](https://crawl4ai.com/mkdocs/)
- [B站教程视频](https://www.bilibili.com/video/BV1Vx4y1g7bp/)

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

MIT License - 详见 LICENSE 文件

---

**开发者**: 基于Crawl4AI官方教程实现  
**版本**: 1.0.0  
**最后更新**: 2024年12月 
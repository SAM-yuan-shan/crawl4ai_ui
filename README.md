# Crawl4AI 完整功能测试项目

一个基于 [Crawl4AI](https://github.com/unclecode/crawl4ai) 的完整功能测试和演示项目。

## 🚀 特性

- ✅ **基础爬取**: 简单快速的网页内容提取
- ✅ **智能过滤**: PruningContentFilter 和 BM25ContentFilter
- ✅ **多格式导出**: Markdown、PDF、截图
- ✅ **批量处理**: 支持多URL并发爬取
- ✅ **高级配置**: 自定义浏览器、缓存、等待策略
- ✅ **实用工具**: 命令行工具，开箱即用

## 📦 安装

```bash
# 安装依赖
pip install -U crawl4ai nest_asyncio

# 安装浏览器驱动
python -m playwright install
```

## 🎯 快速开始

### 方法1: 运行测试脚本

```bash
# 基础功能测试
python test_basic.py

# 高级功能测试  
python test_advanced.py

# 扩展功能测试
python test_extended_fix.py
```

### 方法2: 使用命令行工具

```bash
# 简单爬取
python crawl_utility.py simple https://example.com

# 智能清洗
python crawl_utility.py clean https://example.com -k "关键词"

# 导出PDF
python crawl_utility.py pdf https://example.com

# 截图
python crawl_utility.py screenshot https://example.com

# 提取信息
python crawl_utility.py info https://example.com

# 批量爬取
python crawl_utility.py batch example_urls.txt
```

## 📁 项目结构

```
b_crawlforai/
├── 📄 README.md              # 项目介绍
├── 📚 PROJECT_GUIDE.md       # 详细使用指南
├── 🧪 test_basic.py          # 基础功能测试
├── 🔧 test_advanced.py       # 高级功能测试
├── 🚀 test_extended_fix.py   # 扩展功能测试
├── 🛠️ crawl_utility.py       # 命令行工具
├── 📝 example_urls.txt       # 示例URL列表
└── 📂 outputs/               # 输出目录
    ├── 📄 markdown/          # Markdown文件
    ├── 📄 pdf/              # PDF文件
    ├── 🖼️ screenshots/       # 截图文件
    ├── 📊 json/             # JSON数据
    └── 📋 reports/          # 测试报告
```

## 🎨 功能展示

### 内容过滤效果对比

| 过滤方式 | 内容长度 | 压缩率 | 用途 |
|---------|---------|--------|------|
| 原始内容 | 10,881字符 | 0% | 完整内容 |
| PruningContentFilter | 7,122字符 | 34.5% | 去除噪音 |
| BM25关键词过滤 | 1,860字符 | 82.9% | 精准提取 |

### 输出格式支持

- 📝 **Markdown**: 清晰的文本格式
- 📄 **PDF**: 高质量文档导出  
- 🖼️ **PNG**: 全页面截图
- 📊 **JSON**: 结构化数据

## 🔧 高级功能

### 自定义浏览器配置

```python
browser_config = BrowserConfig(
    browser_type="chromium",
    headless=True,
    viewport_width=1920,
    viewport_height=1080
)
```

### 智能内容过滤

```python
# 移除导航、页脚等噪音
content_filter = PruningContentFilter()

# 基于关键词过滤
content_filter = BM25ContentFilter(user_query="AI technology")
```

### 批量处理

```python
urls = ["url1", "url2", "url3"]
async with AsyncWebCrawler() as crawler:
    tasks = [crawler.arun(url=url) for url in urls]
    results = await asyncio.gather(*tasks)
```

## 📚 文档

- 📖 [详细使用指南](PROJECT_GUIDE.md)
- 🌐 [官方文档](https://crawl4ai.com/mkdocs/)
- 📺 [视频教程](https://www.bilibili.com/video/BV1Vx4y1g7bp/)
- 💻 [Google Colab](https://colab.research.google.com/drive/1wz8u30rvbq6Scodye9AGCw8Qg_Z8QGsk)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

⭐ 如果这个项目对你有帮助，请给个星标！ 
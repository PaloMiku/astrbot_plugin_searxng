# AstrBot SearxNG AI 搜索工具

这是一个为 AstrBot 开发的 SearxNG AI 搜索工具，专为 LLM 提供智能网络搜索能力。

## ✨ 功能特性

- 🤖 **AI 专用搜索**: AI 可以主动调用搜索获取最新信息增强回答

- ⚙️ **高度可配置**: 支持自定义 SearxNG 实例、搜索参数等
- 🌍 **多语言支持**: 支持多种语言的搜索结果
- 📊 **结果控制**: 可配置搜索结果数量和分类

## 🚀 安装

1. 将插件放置在 AstrBot 的 `data/plugins/` 目录下
2. 安装依赖: `pip install -r requirements.txt`
3. 重启 AstrBot 或在管理面板重载插件

## 📖 使用说明

### AI 工具调用

插件会自动注册 `searxng_search` 工具，AI 可以主动调用进行搜索以获取最新信息。

## ⚙️ 配置选项

插件支持以下配置项，可在 AstrBot 管理面板中设置：

- **searxng_url**: SearxNG 实例 URL (默认: <https://search.sapti.me>)
- **timeout**: 搜索超时时间，秒 (默认: 15)
- **max_results**: 最大结果数量 (默认: 8)
- **categories**: 搜索分类 (默认: general)
- **language**: 搜索语言 (默认: zh-CN)
- **user_agent**: HTTP User-Agent (默认: AstrBot-SearxNG-Plugin/1.0.0)

## 🌐 SearxNG 实例

**自建 SearxNG 实例**:

参考 [SearxNG 官方文档](https://docs.searxng.org/) 进行部署

## 📋 支持的搜索分类

- `general` - 通用搜索 (默认)
- `images` - 图片搜索
- `videos` - 视频搜索
- `news` - 新闻搜索
- `map` - 地图搜索
- `music` - 音乐搜索
- `it` - IT/技术相关
- `science` - 科学相关
- `files` - 文件搜索

多个分类可用逗号分隔，例如: `general,news,it`

## 🔧 故障排除

### 搜索请求超时

- 检查 SearxNG 实例是否可访问
- 适当增加超时时间配置
- 尝试使用其他 SearxNG 实例

### 搜索结果为空

- 尝试更换搜索关键词
- 检查搜索分类设置是否正确

## 🔗 相关链接

- [AstrBot](https://github.com/AstrBotDevs/AstrBot) - 强大的聊天机器人框架
- [SearxNG](https://github.com/searxng/searxng) - 免费的互联网元搜索引擎
- [SearxNG 实例列表](https://searx.space) - 公共 SearxNG 实例

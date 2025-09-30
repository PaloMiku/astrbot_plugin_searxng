import aiohttp
import asyncio
from urllib.parse import urljoin, urlencode
from typing import List, Dict, Any, Optional
import json

from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger, AstrBotConfig
import astrbot.api.message_components as Comp


@register(
    "searxng", 
    "PaloMiku", 
    "SearxNG AI 搜索工具，为 LLM 提供智能网络搜索能力", 
    "1.0.0", 
    "https://github.com/PaloMiku/astrbot_plugin_searxng"
)
class SearxNGPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None

    async def initialize(self):
        """初始化 HTTP 会话"""
        timeout = aiohttp.ClientTimeout(total=self.config.get("timeout", 15))
        headers = {
            "User-Agent": self.config.get("user_agent", "AstrBot-SearxNG-Plugin/1.0.0"),
            "Accept": "application/json",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
        }
        self.session = aiohttp.ClientSession(timeout=timeout, headers=headers)
        logger.info(f"SearxNG 插件初始化完成，目标实例: {self.config.get('searxng_url', 'https://search.sapti.me')}")

    async def _search_searxng(self, query: str, categories: Optional[str] = None, language: Optional[str] = None) -> Dict[str, Any]:
        """
        调用 SearxNG API 进行搜索
        
        Args:
            query: 搜索关键词
            categories: 搜索分类，默认使用配置中的值
            language: 搜索语言，默认使用配置中的值
        
        Returns:
            包含搜索结果的字典
        """
        if not self.session:
            await self.initialize()
            
        searxng_url = self.config.get("searxng_url", "https://search.sapti.me")
        if not searxng_url.endswith('/'):
            searxng_url += '/'
            
        search_url = urljoin(searxng_url, "search")
        
        params = {
            "q": query,
            "format": "json",
            "categories": categories or self.config.get("categories", "general"),
            "language": language or self.config.get("language", "zh-CN")
        }
        
        try:
            async with self.session.get(search_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    # 403错误的详细信息
                    error_text = await response.text()
                    logger.error(f"SearxNG 搜索失败 - 状态码: {response.status}")
                    logger.error(f"请求URL: {search_url}")
                    logger.error(f"请求参数: {params}")
                    logger.error(f"错误响应: {error_text[:200]}...")
                    
                    if response.status == 403:
                        return {"results": [], "query": query, "error": "访问被拒绝 - 可能SearxNG实例禁止API访问或IP被封禁"}
                    else:
                        return {"results": [], "query": query, "error": f"HTTP {response.status}"}
        except asyncio.TimeoutError:
            logger.error("SearxNG 搜索请求超时")
            return {"results": [], "query": query, "error": "请求超时"}
        except Exception as e:
            logger.error(f"SearxNG 搜索出错: {str(e)}")
            return {"results": [], "query": query, "error": str(e)}

    def _format_search_results(self, search_data: Dict[str, Any]) -> str:
        """
        格式化搜索结果为可读文本
        
        Args:
            search_data: SearxNG API 返回的数据
            
        Returns:
            格式化后的搜索结果文本
        """
        if "error" in search_data:
            return f"❌ 搜索失败: {search_data['error']}"
            
        results = search_data.get("results", [])
        query = search_data.get("query", "")
        
        if not results:
            return f"🔍 未找到关于 '{query}' 的搜索结果"
            
        max_results = self.config.get("max_results", 8)
        results = results[:max_results]
        
        formatted_text = f"🔍 搜索结果: {query}\n\n"
        
        for i, result in enumerate(results, 1):
            title = result.get("title", "无标题")
            url = result.get("url", "")
            content = result.get("content", "").strip()
            
            # 限制内容长度避免过长
            if len(content) > 200:
                content = content[:197] + "..."
                
            formatted_text += f"{i}. **{title}**\n"
            if content:
                formatted_text += f"   {content}\n"
            formatted_text += f"   🔗 {url}\n\n"
            
        return formatted_text.strip()

    @filter.llm_tool(name="searxng_search")
    async def web_search_tool(self, event: AstrMessageEvent, query: str) -> MessageEventResult:
        """
        网络搜索工具，供 LLM 调用以获取最新信息
        
        Args:
            query(string): 要搜索的关键词或问题
        """

            
        logger.info(f"LLM 调用搜索工具，查询: {query}")
        
        search_data = await self._search_searxng(query)
        formatted_result = self._format_search_results(search_data)
        
        yield event.plain_result(formatted_result)



    async def terminate(self):
        """插件销毁时关闭 HTTP 会话"""
        if self.session:
            await self.session.close()
            logger.info("SearxNG 插件会话已关闭")

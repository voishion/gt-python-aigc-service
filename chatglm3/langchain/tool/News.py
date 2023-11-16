from langchain.tools import BaseTool

from chatglm3.langchain.api.search_emp_api import search


class News(BaseTool):
    name = "news"
    description = "Use for searching news information within Genertec Technology Group through keyword"

    def __init__(self):
        super().__init__()

    def get_news(self, keyword):
        result = search(keyword)
        news_list = []
        for item in result['data']:
            _title = (str(item['title']).replace('<span class="gt-emp-highlight">', '')
                      .replace('</span>', ''))
            _summary = (str(item['resume']).replace('<span class="gt-emp-highlight">', '')
                        .replace('</span>', ''))
            news_list.append({
                "title": _title,
                "summary": _summary,
                "affiliated_department": item['gtidName'],
                "publish_date": item['publishDate']
            })
        return news_list

    def _run(self, para: str) -> str:
        return self.get_news(para)


if __name__ == "__main__":
    news_tool = News()
    news_info = news_tool.run("习近平")
    print(news_info)

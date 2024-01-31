import duckdb
from pydantic import BaseModel
from datetime import datetime

class WebPage(BaseModel):
  source: str
  topic: str = ''
  title: str = ''
  description: str = ''
  language: str = ''
  loc: str = ''
  changefreq: str = ''
  priority: str = ''
  page_content: str = ''
  timestamp: datetime = datetime.now()
  tags: str = ''
  summary: str = ''

class WebPageObj:
  def __init__(self, db_name='data/web_pages.db'):
    self.conn = duckdb.connect(db_name)   
    # 创建表格，设置source字段为主键
    self.conn.execute("""
      CREATE TABLE IF NOT EXISTS web_pages (
        source VARCHAR PRIMARY KEY, 
        topic VARCHAR, 
        title VARCHAR, 
        description VARCHAR, 
        language VARCHAR, 
        loc VARCHAR, 
        changefreq VARCHAR, 
        priority VARCHAR, 
        page_content VARCHAR,
        timestamp TIMESTAMP,
        tags VARCHAR,
        summary VARCHAR
      )
      """)

  def upsert(self, data, topic = "none"):
    if not isinstance(data, WebPage):
      # 尝试从data中提取相应的属性值
      data = {
        'source': data.metadata['source'],
        'topic': topic,
        'title': data.metadata.get('title', ""),
        'description': data.metadata.get('description', ""),
        'language': data.metadata.get('language', ""),
        'loc': data.metadata.get('loc', ""),
        'changefreq': data.metadata.get('changefreq', ""),
        'priority': data.metadata.get('priority', ""),
        'page_content': data.page_content
      }
    web_page = WebPage(**data)
    self.conn.execute("""
      INSERT OR REPLACE INTO web_pages 
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      """, 
      (
        web_page.source, 
        web_page.topic, 
        web_page.title, 
        web_page.description, 
        web_page.language, 
        web_page.loc, 
        web_page.changefreq, 
        web_page.priority, 
        web_page.page_content,
        web_page.timestamp,
        web_page.tags,
        web_page.summary        
      )
    )

  def update_tags_and_summary(self, source, tags, summary):
    # 更新tags和summary字段
    self.conn.execute("""
      UPDATE web_pages 
      SET tags = ?, summary = ? 
      WHERE source = ?
      """, 
      (tags, summary, source)
    )

  # 从duckdb加载数据到内存
  def read_data(self, topic=None):
    query = """
      SELECT
        source,
        topic,
        title,
        description,
        language,
        loc,
        changefreq,
        priority,
        page_content,
        timestamp,
        tags,
        summary
      FROM web_pages
    """
    if topic is not None:
        query += " WHERE topic=?"
        result = self.conn.execute(query, (topic,))
    else:
        result = self.conn.execute(query)
    
    columns = [column[0] for column in result.description]
    web_pages = [WebPage(**dict(zip(columns, row))) for row in result.fetchall()]
    return web_pages
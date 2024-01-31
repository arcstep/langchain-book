import duckdb
from pydantic import BaseModel
from datetime import datetime

class TextBlock(BaseModel):
  topic: str = ''
  page_index: int
  title: str
  description: str
  source: str
  H1: str
  H2: str
  H3: str
  content: str
  timestamp: datetime = datetime.now()

class TextBlockDataset:
  def __init__(self, db_name='data/default.db'):
    self.conn = duckdb.connect(db_name)   
    self.conn.execute("""
      CREATE TABLE IF NOT EXISTS text_blocks (
        source VARCHAR, 
        page_index INT, 
        topic VARCHAR, 
        title VARCHAR, 
        description VARCHAR, 
        H1 VARCHAR, 
        H2 VARCHAR, 
        H3 VARCHAR, 
        content VARCHAR,
        timestamp TIMESTAMP,
        PRIMARY KEY (source, page_index)
      )
    """)

  def upsert(self, data, topic = "none"):
    if not isinstance(data, TextBlock):
      # 尝试从data中提取相应的属性值
      data = {
        'topic': topic,
        'page_index': data.page_index,
        'title': data.title,
        'description': data.description,
        'source': data.source,
        'H1': data.H1,
        'H2': data.H2,
        'H3': data.H3,
        'content': data.content
      }
    d = TextBlock(**data)
    self.conn.execute("""
      INSERT OR REPLACE INTO text_blocks 
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      """, 
      d.topic, d.page_index, d.title, d.description, d.source, d.H1, d.H2, d.H3, d.content, d.timestamp)
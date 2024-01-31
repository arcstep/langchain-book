import duckdb
from pydantic import BaseModel
from datetime import datetime
from pydantic import Field

class TextBlock(BaseModel):
  page_index: int
  chunk_index: int
  title: str
  description: str
  source: str
  H1: str
  H2: str
  H3: str
  content: str
  timestamp: datetime = Field(default_factory=datetime.now)

class TextBlockDataset:
  def __init__(self, db_name='data/default.db', drop = False):    
    self.conn = duckdb.connect(db_name)   
    if(drop):
      self.conn.execute("DROP TABLE IF EXISTS text_blocks")
      print("WARN: Drop Table: text_blocks")
    self.conn.execute("""
      CREATE TABLE IF NOT EXISTS text_blocks (
        source VARCHAR, 
        page_index INT, 
        chunk_index INT,
        title VARCHAR, 
        description VARCHAR, 
        H1 VARCHAR, 
        H2 VARCHAR, 
        H3 VARCHAR, 
        content VARCHAR,
        timestamp TIMESTAMP,
        PRIMARY KEY (source, page_index, chunk_index)
      )
    """)

  def upsert(self, data):
    if not isinstance(data, TextBlock):
      data = TextBlock(**data)
    self.conn.execute("""
      INSERT INTO text_blocks 
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      ON CONFLICT(source, page_index, chunk_index) DO UPDATE
      SET 
        title = excluded.title, 
        description = excluded.description, 
        H1 = excluded.H1, 
        H2 = excluded.H2, 
        H3 = excluded.H3, 
        content = excluded.content, 
        timestamp = excluded.timestamp
      """, 
      (
        data.source, 
        data.page_index, 
        data.chunk_index,
        data.title, 
        data.description, 
        data.H1, 
        data.H2, 
        data.H3, 
        data.content, 
        data.timestamp
      )
    )

  def read_data(self):
      query = """
        SELECT
          page_index, 
          chunk_index,
          title, 
          description, 
          source, 
          H1, 
          H2, 
          H3, 
          content, 
          timestamp
        FROM text_blocks
      """
      result = self.conn.execute(query)
      
      columns = [column[0] for column in result.description]
      text_blocks = [TextBlock(**dict(zip(columns, row))) for row in result.fetchall()]
      return text_blocks
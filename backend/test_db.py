from sqlalchemy import create_engine
engine = create_engine("postgresql+psycopg://postgres:123@localhost:5432/research_db")
with engine.connect() as conn:
    print(conn)

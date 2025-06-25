import sqlite3
import os

def execute_sql_file(database_path, sql_file_path):
    """
    执行SQL文件中的语句
    
    参数:
        database_path (str): SQLite数据库文件路径
        sql_file_path (str): 要执行的SQL文件路径
    """
    # 检查SQL文件是否存在
    if not os.path.exists(sql_file_path):
        print(f"错误: SQL文件 '{sql_file_path}' 不存在")
        return
    
    try:
        # 连接到SQLite数据库(如果不存在会自动创建)
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        
        print(f"成功连接到数据库: {database_path}")
        
        # 读取SQL文件内容
        with open(sql_file_path, 'r', encoding='utf-8') as sql_file:
            sql_script = sql_file.read()
        
        # 执行SQL脚本
        cursor.executescript(sql_script)
        conn.commit()
        print(f"成功执行SQL文件: {sql_file_path}")
        
    except sqlite3.Error as e:
        print(f"SQLite错误: {e}")
    except Exception as e:
        print(f"错误: {e}")
    finally:
        # 关闭数据库连接
        if conn:
            conn.close()
            print("数据库连接已关闭")

if __name__ == "__main__":
    db_name = "eh.db"
    sql_file = "2025_01_08.sql"
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    db_path = os.path.join(current_dir, db_name)
    sql_path = os.path.join(current_dir, sql_file)
    
    execute_sql_file(db_path, sql_path)
import os
import pymysql

# ====================================================================================
# 需自定义区域
# 定义MySQL连接参数
mysql_host = '172.20.0.145'
mysql_user = 'vipuser'
mysql_password = 'vipuser'
mysql_port = 3307
database = 'coredb_v2310'

# 定义要遍历的根目录路径
root_directory = '/home/croot/MysqlScriptBatchExcute'
# ====================================================================================

# root_directory如果有SuccessSql.log文件则删除后创建，如果没有则创建SuccessSql.log
if os.path.exists(f"{root_directory}/SuccessSql.log"):
    os.remove(f"{root_directory}/SuccessSql.log")
    print(f"delete file: '{root_directory}/SuccessSql.log'")
else:
    with open(f"{root_directory}/SuccessSql.log", "w") as f:
        f.close()

# 连接到MySQL数据库
conn = pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_user, password=mysql_password, database=database, charset="utf8")
cursor = conn.cursor()

# 遍历目录树以查找SQL文件并使用source逐个执行
for root, dirs, files in os.walk(root_directory):
    for filename in files:
        if filename.endswith(".sql") and "00_" not in files:  # 仅处理.sql文件、且不处理00_开头的文件
            sql_file1 = os.path.join(root, filename)

            # try:
            print(f"open file: '{sql_file1}'")
            os.system(f'cd {root}')
            print(f"cd {root}")

            # 读取SQL文件内容
            with open(str(sql_file1), "r") as sql_file:
                print("read sqlfile")
                sql_script = sql_file.read()
            
            # 将SQL语句拆分成单独的语句
            sql_statements = sql_script.split(';')
            # print(sql_statements)


            # 执行每个SQL语句
            for statement in sql_statements:
                try:
                    if statement.strip():  # 跳过空白语句
                        print(f"Executing statement: {statement}")
                        cursor.execute(statement)
                        conn.commit()
                        print("SQL statement executed successfully.")
                        
                        # 创建SuccessSql.log文件，记录执行成功的SQL文件
                        with open(root_directory+"/SuccessSql.log", "a") as f:
                            f.write(sql_file1 + "\n")
                            f.close()

                except pymysql.Error as e:
                    print("")
                    print("===================================报错SQL====================================")
                    print("报错SQL文件：" + sql_file1)
                    print(f"MySQL Error: {e}")
                    print("==============================================================================")
                    # SuccessSql.log，记录执行失败的SQL文件
                    with open(root_directory+"/SuccessSql.log", "a") as f:
                        f.write(sql_file1 + "部分执行失败\n")
                        f.close()
                    conn.rollback()
            

            
            # 删除执行成功的sql文件
            os.remove(sql_file1)
            print(f"delete file: '{sql_file1}'")

# 关闭连接
cursor.close()
conn.close()
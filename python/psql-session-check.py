from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from urllib.parse import quote

from multiprocessing import Pool
import os
import time

def insert_sql(cnt):
    for i in range(int(cnt)):
        engine = create_engine("postgresql://user3:%s@172.16.10.12:31167/testdb3" % quote('test03@'))
        db = scoped_session(sessionmaker(bind=engine))
        pid = os.getpid()
        #cmd_sql = "INSERT INTO test (pid) VALUES ('"+str(pid)+"');"
        cmd_sql = "SELECT COUNT(*) FROM test;"
        print('execute sql:', pid, i)
        db.execute(cmd_sql)
        db.commit()
        db.close()
        #time.sleep(300)


def main():
#    values = (1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000)
    values = (200, 100, 100, 100, 100)
    with Pool() as pool:
        res = pool.map(insert_sql, values)

if __name__ == "__main__":
    main()

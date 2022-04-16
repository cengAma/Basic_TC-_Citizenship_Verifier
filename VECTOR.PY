import psycopg2
import schedule
import time

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')


conn = psycopg2.connect(user="postgres",
                        password="mysecretpassword",
                        host="127.0.0.1",
                        port="5432",
                        database="postgres")
                            

cursor = conn.cursor()
# def open_conncetion():
#     conn = psycopg2.connect(user="postgres",
#                             password="mysecretpassword",
#                             host="127.0.0.1",
#                             port="5432",
#                             database="postgres")
#     return conn
# def insert(sql):
#     conn = None
#     try:
#         conn = open_conncetion()
#         # create a new cursor
#         cur = conn.cursor()
#         # execute the INSERT statement
#         cur.execute(sql)
#         # commit the changes to the database
#         conn.commit()
#         # close communication with the database
#         cur.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()

def insert_sentence_vector(text):

    res = model.encode(text)

    str_list = [str(item) for item in res]
    vector = ','.join(str_list)
    #query = 'insert into test_table(titlevev) values (ARRAY [' + vector +'] )'
    #insert(query)
    return(vector)

# def insert_sentence_vector(text):

#     res = model.encode(text)

#     str_list = [str(item) for item in res]
#     vector = ','.join(str_list)
#     query = 'UPDATE into tit_abs_vec(titvec) values (ARRAY [' + vector +'] )'
#     insert(query)


#insert_sentence_vector('I have a dog and cat')
def for_data_query():
    cnt=1
    print("start")
    postgreSQL_select_Query = "select id from papers6 where done_vec=false limit 500"
    cursor.execute(postgreSQL_select_Query)
    paper_ids = cursor.fetchall()
    print("paper_ids=",paper_ids)

    for row in paper_ids:
        print("!!!",cnt,"!!!")
        print(row[0])

        print(row)

        # postgres_insert_query = """ INSERT INTO tit_abs_vec(id) VALUES (%s)"""
        # record_to_insert = (row[0])
        # cursor.execute(postgres_insert_query,record_to_insert)
        # connection.commit()

        postgreSQL_select_Query_Count = """ select title from papers6 where id='{}' """.format(row[0])
        cursor.execute(postgreSQL_select_Query_Count)
        paper_title = cursor.fetchone()
        #print(paper_title[0])
        vector_title=insert_sentence_vector(paper_title[0])

        postgreSQL_select_Query_Count = """ select abstract from papers6 where id='{}' """.format(row[0])
        cursor.execute(postgreSQL_select_Query_Count)
        paper_title = cursor.fetchone()
        #print(paper_title[0])
        vector_abstract=insert_sentence_vector(paper_title[0])

        # query = """insert into tit_abs_vec(id,titvec,absvec) values ('{}', ARRAY [' + vector_title +'],ARRAY [' + vector_abstract +'])""".format(row[0])

        query = 'insert into tit_abs_vec(id,titvec,absvec) values (%s, ARRAY [' + vector_title +'],ARRAY [' + vector_abstract +'])'
        record_to_insert = (row)
        cursor.execute(query,record_to_insert)
        conn.commit()
        print("inserted id,titvec,absvec")
        # t1=tuple(vector_title)
        # t2=tuple(vector_abstract)
        # query = "insert into tit_abs_vec(id,titvec,absvec) values('{}',{},{});".format(row[0],t1,t2)
        # #record_to_insert=(row[0],vector_title,vector_abstract)
        # cursor.execute(query)
        # conn.commit()
        
        postgres_insert_query = """ UPDATE papers6 SET done_vec=true WHERE id='{}'""".format(row[0])
        cursor.execute(postgres_insert_query)
        conn.commit()
        print("done_vec set true")
        cnt=cnt+1
        print(" ")

countforhundred=1
while 1:
    for_data_query()
    time.sleep(1)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",countforhundred,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",countforhundred,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",countforhundred,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",countforhundred,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",countforhundred,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    countforhundred=countforhundred+1









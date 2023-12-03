import pymysql as my



# 회원이면 dict 형태로 전달(리턴)
# 회원아니면 None 형태로 전달(리턴)

class DbConnect:
    __connection = None
    __row = None
    def __init__(self, host, user, password, database):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database
        self.__connection = my.Connect(
            host = host, user=user, password=password, database=database,
            cursorclass= my.cursors.DictCursor
        )
        self.__cursor = self.__connection.cursor()

    def findPath(self, modelId:str):
        connection = my.Connect(
            host = self.__host, user=self.__user, password=self.__password, database=self.__database,
            cursorclass= my.cursors.DictCursor
        )
        cursor = connection.cursor()
        sql = '''
        SELECT MODELPATH FROM model_info
        WHERE MODELID = %s
        '''
        cursor.execute(sql,(modelId))
        row = cursor.fetchone()
        connection.close()
        return row['MODELPATH']

def selectUsers(uid):
    row        = None # 쿼리 결과
    connection = None
    try:
    
        connection = my.connect(host    ='host.docker.internal',   #루프백주소, 자기자신주소
                            user        ='myadmin',        #DB ID      
                            password    ='root',        # 사용자가 지정한 비밀번호
                            database    ='youcaloid',
                            cursorclass = my.cursors.DictCursor #딕셔너리로 받기위한 커서
                            )

        cursor = connection.cursor()

        sql = ''' #로그인 실행문
        SELECT
            * 
        FROM
            model_info 
        WHERE 
            MODELID=%s
        '''
        cursor.execute(sql, (uid)) # 커리 실행
        row = cursor.fetchone()
 
        #print( row )
    except Exception as e:
        print('접속오류', e)
    finally:
        if connection:      
          connection.close()          
        print('종료')
    # 결과를 리턴한다.
    return row

if __name__ == '__main__':
    # 테스트
    row = selectUsers('1111')
    print('쿼리회원조회결과 : ', row)
    #비회원 테스트(회원이 아님, 비번이 틀림, 아이디 틀림)
    row = selectUsers( 'guest')
    print('회원조회결과 : ', row)
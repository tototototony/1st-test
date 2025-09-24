#한국수력원자력(주)_원자력산업 용어사전_20190905

import pandas as pd
import mariadb

# MariaDB 연결
def connect_db():
    return mariadb.connect(
        user="root",
        password="1001",
        host="localhost",
        port=3306,
        database="project2"
    )

def main():
    conn = connect_db() #connect_db()함수 실행해서 결과값을 conn에 저장 mariadb와 연결하는 함수
    cur = conn.cursor()

    sql = "select * From test"
    cur.execute(sql)
    db_data = cur.fetchall()
    print(db_data)


#테이블 생성
    cur.execute("""
        CREATE TABLE IF NOT EXISTS nuclear_glossary(
            id INT PRIMARY KEY AUTO_INCREMENT,
            term_eng VARCHAR(300),
            term_kor VARCHAR(300),
            abbreviation VARCHAR(50)
         )
    """)
    conn.commit()

# csv 파일 불러오기
    df = pd.read_csv(r"C:\Users\smart\project\원자력발전용어집 DB적재\한국수력원자력(주)_원자력산업 용어사전_20190905.csv", encoding='cp949')
    # 엑셀 파일 아니라 csv라서 엑셀로 읽기했다가 오류
    # encodnig에서 오류나서 다른걸로 바꿔보기
    #cur설정 자꾸 오류나서 들여쓰기 맞추기 main에 포함되도록!

    #데이터 insert

    for idx, row in df.iterrows(): #데이터프레임을 한 줄씩 행단위로 반복하는 함수 idx는 행의 번호
        #if pd.isna(row['영문용어']) or pd.isna(row['한글용어']) or pd.isna(row['약어']):
            #continue  #실행 누르니 결측값때문에 오류남-> 결측치 있으면 건너 뛰는 함수 isna추가 #했는데 db에서 데이터 한 줄 누락되어서 null값으로 들어가도록 다시 수정 필요
        #term_eng = row['영문용어']
        #term_kor = row['한글용어']
        #abbreviation = row['약어']    #딕셔너리 형태 파일 아니라서 node안 쓰고row로 쓰는게 안전 #이 코드는 결측값 누락이라 주석처리

        term_eng = row['영문용어'] if pd.notna(row['영문용어']) else None
        term_kor = row['한글용어'] if pd.notna(row['한글용어']) else None
        abbreviation = row['약어'] if pd.notna(row['약어']) else None
        #값이 있으면 넣고 비어있으면 none로 바꾸라는 뜻
        #pd.notna()=Pandas에서 결측치(NaN)가 아닌지 확인하는 함수
        #그래도 1개 안 나옴->위에 isna랑 중복돼서 일 수도 있어서 isna지워봄
        #이렇게 수정하니까 44445개 전부 들어감
        #id_2,951 노르웨이원자력산업회의 abbreviation 값이 null이었음 (SELECT * FROM nuclear_glossary WHERE abbreviation IS NULL;)


        cur.execute("""
            INSERT INTO nuclear_glossary (term_eng, term_kor, abbreviation)
            VALUES (?, ?, ?)
        """,(term_eng, term_kor, abbreviation))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()

#main()은 프로그램의 **"메인(주요) 실행 부분"**을 담는 함수
#프로그램이 시작할 때 가장 먼저 실행 되어야 할 코드를 main() 안에 모아두기
#한국수력원자력(주)_원자력산업 용어사전_20190905

import pandas as pd
import mariadb

# MariaDB 연결
def connect_db():
    return mariadb.connect(
        user="root",
        password="  ",
        host="localhost",
        port=3306,
        database="project"
    )

def main():
    conn = connect_db() 
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
    df = pd.read_csv(r"C:\Users\smart\project\원자력발전용어집 DB적재v", encoding='cp949')


    #데이터 insert

    for idx, row in df.iterrows(): #데이터프레임을 한 줄씩 행단위로 반복하는 함수 idx는 행의 번호
        #if pd.isna(row['영문용어']) or pd.isna(row['한글용어']) or pd.isna(row['약어']):
            #continue  
        #term_eng = row['영문용어']
        #term_kor = row['한글용어']
        #abbreviation = row['약어']   

        term_eng = row['영문용어'] if pd.notna(row['영문용어']) else None
        term_kor = row['한글용어'] if pd.notna(row['한글용어']) else None
        abbreviation = row['약어'] if pd.notna(row['약어']) else None
       
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


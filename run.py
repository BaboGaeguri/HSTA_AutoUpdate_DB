import pandas as pd
import os

file_path = "C:/Users/김상희/OneDrive/바탕 화면/기타/2024/HSTA/기타/학회원 DB/(31기 업데이트 완료) HSTA 학회원 공개용 DB.csv"

df = pd.read_csv(file_path)

# print(df.tail(20))

a = df[df['이름'] =='박상윤']
print(a)
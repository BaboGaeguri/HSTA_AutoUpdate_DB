import pandas as pd

# Excel 파일 경로
excel_file = "C:/Users/김상희/OneDrive/바탕 화면/기타/2024/HSTA/기타/학회원 DB/(31기 업데이트 완료) HSTA 학회원 공개용 DB.xlsx"

# CSV 파일 경로 (출력)
csv_file = "C:/Users/김상희/OneDrive/바탕 화면/기타/2024/HSTA/기타/학회원 DB/(31기 업데이트 완료) HSTA 학회원 공개용 DB.csv"

try:
    # Excel 파일 읽기
    print("Excel 파일을 읽는 중...")
    df = pd.read_excel(excel_file)
    
    # CSV로 저장
    print("CSV 파일로 변환 중...")
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')  # utf-8-sig: Excel에서 한글 깨짐 방지
    
    print(f"변환 완료!")
    print(f"CSV 파일 위치: {csv_file}")
    print(f"총 {len(df)}행, {len(df.columns)}열 변환됨")
    
except Exception as e:
    print(f"오류 발생: {e}")


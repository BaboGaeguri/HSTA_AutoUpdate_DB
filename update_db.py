import pandas as pd
import os
from pathlib import Path

def load_db_excel(file_path):
    """
    DB.xlsx 파일을 읽어서 데이터프레임으로 변환
    
    Args:
        file_path: DB.xlsx 파일 경로
        
    Returns:
        pandas.DataFrame: 읽어온 데이터프레임
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"DB.xlsx 파일을 찾을 수 없습니다: {file_path}")
    
    # Excel 파일 읽기
    df = pd.read_excel(file_path)
    print(f"DB.xlsx 파일을 성공적으로 읽었습니다. (행: {len(df)}, 열: {len(df.columns)})")
    return df

def load_template(file_path):
    """
    Template 파일을 읽어서 구조 확인
    
    Args:
        file_path: Template 파일 경로
        
    Returns:
        pandas.DataFrame: Template 데이터프레임
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Template 파일을 찾을 수 없습니다: {file_path}")
    
    # Template Excel 파일 읽기
    template_df = pd.read_excel(file_path)
    print(f"Template 파일을 성공적으로 읽었습니다. (행: {len(template_df)}, 열: {len(template_df.columns)})")
    return template_df

def align_dataframe_to_template(df, template_df):
    """
    데이터프레임을 template 구조에 맞게 정렬 및 추가
    
    Args:
        df: 원본 데이터프레임 (DB.xlsx에서 읽은 데이터)
        template_df: Template 데이터프레임
        
    Returns:
        pandas.DataFrame: Template 구조에 맞게 정렬된 데이터프레임
    """
    # Template의 컬럼 구조 가져오기
    template_columns = template_df.columns.tolist()
    
    # 결과 데이터프레임 초기화 (template 구조 사용)
    result_df = pd.DataFrame(columns=template_columns)
    
    # 원본 데이터프레임의 컬럼 확인
    df_columns = df.columns.tolist()
    
    # 공통 컬럼 찾기
    common_columns = [col for col in template_columns if col in df_columns]
    missing_columns = [col for col in template_columns if col not in df_columns]
    
    print(f"\n공통 컬럼: {common_columns}")
    if missing_columns:
        print(f"추가 필요한 컬럼: {missing_columns}")
    
    # 공통 컬럼 데이터 복사
    for col in common_columns:
        result_df[col] = df[col].values if len(df) > 0 else []
    
    # Template에만 있는 컬럼은 빈 값으로 추가 (또는 template의 기본값 사용)
    for col in missing_columns:
        if len(template_df) > 0:
            # Template의 첫 번째 행 값을 기본값으로 사용
            result_df[col] = template_df[col].iloc[0] if pd.notna(template_df[col].iloc[0]) else ''
        else:
            result_df[col] = ''
    
    # 원본 데이터프레임에만 있는 컬럼 정보 출력 (선택사항)
    extra_columns = [col for col in df_columns if col not in template_columns]
    if extra_columns:
        print(f"원본에만 있는 컬럼 (제외됨): {extra_columns}")
    
    return result_df

def save_result(result_df, output_path):
    """
    결과 데이터프레임을 Excel 파일로 저장
    
    Args:
        result_df: 저장할 데이터프레임
        output_path: 출력 파일 경로
    """
    result_df.to_excel(output_path, index=False)
    print(f"\n결과가 저장되었습니다: {output_path}")
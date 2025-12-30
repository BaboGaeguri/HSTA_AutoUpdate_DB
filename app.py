from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# uploads 폴더 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': '파일이 없습니다.'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': '파일이 선택되지 않았습니다.'}), 400

    if file and (file.filename.endswith('.xlsx') or file.filename.endswith('.xls')):
        try:
            # Excel 파일 읽기
            df = pd.read_excel(file)

            # 데이터 정보 수집
            data_info = {
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': df.columns.tolist(),
                'preview': df.head(50).to_html(classes='table table-striped table-bordered', index=True),
                'data_types': df.dtypes.astype(str).to_dict(),
                'missing_values': df.isnull().sum().to_dict(),
                'numeric_columns': df.select_dtypes(include=['number']).columns.tolist(),
                'stats': {}
            }

            # 숫자 컬럼에 대한 통계 정보
            numeric_df = df.select_dtypes(include=['number'])
            if not numeric_df.empty:
                data_info['stats'] = numeric_df.describe().to_dict()

            return jsonify(data_info)

        except Exception as e:
            return jsonify({'error': f'파일 처리 중 오류 발생: {str(e)}'}), 500

    return jsonify({'error': '지원하지 않는 파일 형식입니다. (.xlsx, .xls만 가능)'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

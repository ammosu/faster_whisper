from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from faster_whisper import WhisperModel
from opencc import OpenCC
import os
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# 配置
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac', 'm4a', 'webm'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 全局模型變數
model = None

# OpenCC 轉換器（簡體轉繁體台灣）
cc_s2tw = OpenCC('s2tw')  # 簡體到繁體（台灣）
cc_s2twp = OpenCC('s2twp')  # 簡體到繁體（台灣）含常用詞彙轉換


def convert_to_traditional(text, use_phrases=True):
    """將簡體中文轉換為繁體中文（台灣）"""
    if use_phrases:
        return cc_s2twp.convert(text)
    return cc_s2tw.convert(text)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_model():
    """延迟加载模型"""
    global model
    if model is None:
        print("正在加载 Whisper 模型...")
        model = WhisperModel("dropbox-dash/faster-whisper-large-v3-turbo", compute_type="int8")
        print("模型加载完成！")
    return model

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/transcribe', methods=['POST'])
def transcribe():
    try:
        # 檢查是否有檔案
        if 'audio' not in request.files:
            return jsonify({'error': '沒有上傳檔案'}), 400

        file = request.files['audio']

        if file.filename == '':
            return jsonify({'error': '沒有選擇檔案'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': f'不支援的檔案格式。支援的格式: {", ".join(ALLOWED_EXTENSIONS)}'}), 400

        # 獲取參數
        language = request.form.get('language', None)
        beam_size = int(request.form.get('beam_size', 5))
        to_traditional = request.form.get('to_traditional', 'true').lower() == 'true'

        # 儲存臨時檔案
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        try:
            # 載入模型並轉錄
            whisper_model = load_model()

            # 使用 initial_prompt 引導輸出繁體中文
            initial_prompt = "以下是普通話的轉錄內容。" if language == 'zh' else None

            segments, info = whisper_model.transcribe(
                filepath,
                language=language if language else None,
                beam_size=beam_size,
                vad_filter=True,
                initial_prompt=initial_prompt
            )

            # 收集結果
            results = []
            full_text = ""

            for segment in segments:
                text = segment.text.strip()

                # 如果是中文且啟用繁體轉換
                if to_traditional and info.language == 'zh':
                    text = convert_to_traditional(text)

                segment_data = {
                    'start': round(segment.start, 2),
                    'end': round(segment.end, 2),
                    'text': text
                }
                results.append(segment_data)
                full_text += text + " "

            # 刪除臨時檔案
            os.remove(filepath)

            return jsonify({
                'success': True,
                'language': info.language,
                'duration': round(info.duration, 2),
                'full_text': full_text.strip(),
                'segments': results
            })

        except Exception as e:
            # 清理臨時檔案
            if os.path.exists(filepath):
                os.remove(filepath)
            raise e

    except Exception as e:
        return jsonify({'error': f'轉錄失敗: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'model_loaded': model is not None})

if __name__ == '__main__':
    print("=" * 50)
    print("Whisper 語音轉文字服務")
    print("=" * 50)
    print("服務將在 http://localhost:5000 啟動")
    print("首次轉錄時會自動下載模型，請耐心等待...")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)

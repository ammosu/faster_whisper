# Whisper 語音轉文字服務

基於 OpenAI Whisper large-v3 turbo 模型的語音轉文字 Web 應用程式，採用 faster-whisper 優化版本，提供快速且準確的語音辨識服務。

## 功能特點

- 快速轉錄：使用優化的 faster-whisper 引擎
- 多語言支援：支援中文、英文、日文、韓文等多種語言
- 自動語言偵測：無需手動指定語言
- 分段顯示：提供時間戳記與文字分段
- 網頁介面：簡潔易用的 Web UI
- 拖放上傳：支援拖放檔案上傳

## 系統需求

- Python 3.11+
- uv (Python 套件管理工具)
- 至少 4GB 可用記憶體
- 支援的音訊格式：MP3, WAV, OGG, FLAC, M4A, WebM

## 安裝與執行

### 1. 安裝相依套件

虛擬環境與相依套件已完成設定，如需重新安裝：

```bash
# 建立虛擬環境
uv venv

# 安裝相依套件
uv pip install faster-whisper flask flask-cors
```

### 2. 啟動服務

使用提供的啟動腳本：

```bash
./start.sh
```

或手動啟動：

```bash
# 啟用虛擬環境
source .venv/bin/activate

# 執行應用程式
python app.py
```

### 3. 開啟網頁介面

在瀏覽器中開啟：
```
http://localhost:5000
```

## 使用說明

1. **上傳音訊檔案**
   - 點選上傳區域選擇檔案
   - 或直接拖放音訊檔案到上傳區域

2. **設定選項**
   - **語言**：選擇音訊語言或留空自動偵測
   - **Beam Search 大小**：數值越大準確度越高但速度越慢（建議使用 5）

3. **開始轉錄**
   - 點選「開始轉錄」按鈕
   - 首次使用會自動下載模型（約 1.7GB）
   - 等待轉錄完成

4. **檢視結果**
   - 完整文字：所有轉錄內容
   - 分段詳情：含時間戳記的文字片段

## 進階設定

### 修改服務埠號

編輯 `app.py` 檔案的最後一行：

```python
app.run(debug=True, host='0.0.0.0', port=5000)  # 修改 port 值
```

### 調整模型精度

在 `app.py` 中修改 `load_model()` 函式：

```python
# 可選項: "float16", "int8", "int8_float16"
model = WhisperModel("dropbox-dash/faster-whisper-large-v3-turbo", compute_type="int8")
```

- `float16`：最高精度，速度較慢，記憶體佔用大
- `int8`：平衡精度與速度（建議）
- `int8_float16`：較快速度，略低精度

### 檔案大小限制

編輯 `app.py` 中的設定：

```python
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB，可依需求調整
```

## 專案結構

```
faster_whisper/
├── .venv/              # 虛擬環境
├── app.py              # Flask 後端應用程式
├── templates/
│   └── index.html      # 前端網頁介面
├── uploads/            # 暫存檔案目錄
├── start.sh            # 啟動腳本
└── README.md           # 說明文件
```

## API 端點

### POST /api/transcribe

轉錄音訊檔案

**請求參數：**
- `audio` (file): 音訊檔案
- `language` (string, 可選): 語言代碼（如 "zh", "en"）
- `beam_size` (int, 可選): Beam Search 大小（預設 5）

**回應範例：**
```json
{
  "success": true,
  "language": "zh",
  "duration": 120.5,
  "full_text": "完整的轉錄文字...",
  "segments": [
    {
      "start": 0.0,
      "end": 3.5,
      "text": "第一段文字"
    }
  ]
}
```

### GET /api/health

檢查服務狀態

**回應範例：**
```json
{
  "status": "ok",
  "model_loaded": true
}
```

## 注意事項

1. **首次執行**：首次轉錄時會自動下載模型（約 1.7GB），請確保網路連線穩定
2. **記憶體需求**：執行時至少需要 4GB 可用記憶體
3. **檔案清理**：上傳的暫存檔案會在轉錄後自動刪除
4. **GPU 加速**：如有 NVIDIA GPU，faster-whisper 會自動使用 CUDA 加速

## 常見問題

### Q: 模型下載失敗？
A: 檢查網路連線，或手動從 Hugging Face 下載模型並放置到本機。

### Q: 記憶體不足？
A: 使用 `compute_type="int8"` 降低記憶體佔用，或處理較短的音訊片段。

### Q: 轉錄速度慢？
A:
- 降低 `beam_size` 值
- 使用 `compute_type="int8"`
- 如有 GPU，確保 CUDA 已正確安裝

### Q: 支援哪些語言？
A: Whisper 支援 99 種語言，常見的包括：中文、英文、日文、韓文、西班牙文、法文、德文等。

## 參考資料

- [Faster Whisper GitHub](https://github.com/systran/faster-whisper)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Model on Hugging Face](https://huggingface.co/dropbox-dash/faster-whisper-large-v3-turbo)
- [CTranslate2 Documentation](https://opennmt.net/CTranslate2/)

## 授權

MIT License

## 貢獻

歡迎提交 Issue 與 Pull Request。

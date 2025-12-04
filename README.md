# 🎙️ Whisper 語音轉文字服務

基於 OpenAI Whisper large-v3 turbo 模型的語音轉文字 Web 應用。使用 faster-whisper 優化版本，提供快速、準確的語音識別服務。

## ✨ 功能特點

- 🚀 快速轉錄：使用優化的 faster-whisper 引擎
- 🌍 多語言支持：支持中文、英文、日文、韓文等多種語言
- 🎯 自動語言檢測：無需手動指定語言
- 📊 分段顯示：提供時間戳和文字分段
- 🎨 美觀界面：現代化的 Web UI
- 📁 拖放上傳：支持拖放文件上傳

## 📋 系統需求

- Python 3.11+
- uv (Python 包管理器)
- 至少 4GB 可用內存
- 支持的音頻格式：MP3, WAV, OGG, FLAC, M4A, WebM

## 🚀 快速開始

### 1. 安裝依賴

虛擬環境和依賴已經設置完成，如需重新安裝：

```bash
# 創建虛擬環境
uv venv

# 安裝依賴
uv pip install faster-whisper flask flask-cors
```

### 2. 啟動服務

使用提供的啟動腳本：

```bash
./start.sh
```

或手動啟動：

```bash
# 激活虛擬環境
source .venv/bin/activate

# 啟動應用
python app.py
```

### 3. 訪問應用

在瀏覽器中打開：
```
http://localhost:5000
```

## 📖 使用說明

1. **上傳音頻**
   - 點擊上傳區域選擇文件
   - 或直接拖放音頻文件到上傳區域

2. **設置選項**
   - **語言**：選擇音頻語言或留空自動檢測
   - **束搜索大小**：數值越大精度越高但速度越慢（推薦使用 5）

3. **開始轉錄**
   - 點擊「開始轉錄」按鈕
   - 首次使用會自動下載模型（約 1.7GB）
   - 等待轉錄完成

4. **查看結果**
   - 完整文字：所有轉錄內容
   - 分段詳情：帶時間戳的文字片段

## 🔧 配置說明

### 修改服務端口

編輯 `app.py` 文件的最後一行：

```python
app.run(debug=True, host='0.0.0.0', port=5000)  # 修改 port 值
```

### 調整模型精度

在 `app.py` 中修改 `load_model()` 函數：

```python
# 選項: "float16", "int8", "int8_float16"
model = WhisperModel("dropbox-dash/faster-whisper-large-v3-turbo", compute_type="int8")
```

- `float16`：最高精度，速度較慢，內存佔用大
- `int8`：平衡精度和速度（推薦）
- `int8_float16`：較快速度，略低精度

### 文件大小限制

編輯 `app.py` 中的配置：

```python
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB，根據需要調整
```

## 📁 項目結構

```
faster_whisper/
├── .venv/              # 虛擬環境
├── app.py              # Flask 後端應用
├── templates/
│   └── index.html      # 前端界面
├── uploads/            # 臨時文件存儲
├── start.sh            # 啟動腳本
└── README.md           # 說明文檔
```

## 🔌 API 端點

### POST /api/transcribe

轉錄音頻文件

**請求參數：**
- `audio` (file): 音頻文件
- `language` (string, 可選): 語言代碼（如 "zh", "en"）
- `beam_size` (int, 可選): 束搜索大小（默認 5）

**響應示例：**
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

**響應示例：**
```json
{
  "status": "ok",
  "model_loaded": true
}
```

## ⚠️ 注意事項

1. **首次運行**：首次轉錄時會自動下載模型（約 1.7GB），請確保網絡連接穩定
2. **內存需求**：運行時至少需要 4GB 可用內存
3. **文件清理**：上傳的臨時文件會在轉錄後自動刪除
4. **GPU 加速**：如有 NVIDIA GPU，faster-whisper 會自動使用 CUDA 加速

## 🐛 常見問題

### Q: 模型下載失敗？
A: 檢查網絡連接，或手動從 Hugging Face 下載模型並放置到本地。

### Q: 內存不足？
A: 使用 `compute_type="int8"` 降低內存佔用，或處理較短的音頻片段。

### Q: 轉錄速度慢？
A:
- 降低 `beam_size` 值
- 使用 `compute_type="int8"`
- 如有 GPU，確保 CUDA 已正確安裝

### Q: 支持哪些語言？
A: Whisper 支持 99 種語言，常見的包括：中文、英文、日文、韓文、西班牙文、法文、德文等。

## 📚 參考資料

- [Faster Whisper GitHub](https://github.com/systran/faster-whisper)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Model on Hugging Face](https://huggingface.co/dropbox-dash/faster-whisper-large-v3-turbo)
- [CTranslate2 Documentation](https://opennmt.net/CTranslate2/)

## 📄 授權

MIT License

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

#!/bin/bash

echo "========================================"
echo "  Whisper 語音轉文字服務啟動腳本"
echo "========================================"
echo ""

# 激活虛擬環境
echo "正在激活虛擬環境..."
source .venv/bin/activate

# 檢查依賴
if ! python -c "import faster_whisper" 2>/dev/null; then
    echo "錯誤: faster_whisper 未安裝"
    echo "請運行: uv pip install faster-whisper flask flask-cors"
    exit 1
fi

echo "虛擬環境已激活"
echo ""
echo "啟動 Flask 服務器..."
echo "服務地址: http://localhost:5000"
echo ""
echo "按 Ctrl+C 停止服務"
echo "========================================"
echo ""

# 啟動應用
python app.py

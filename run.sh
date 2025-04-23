#!/bin/bash

# ตรวจสอบว่าอยู่ใน virtual environment หรือไม่
if [[ "$VIRTUAL_ENV" == "" ]]; then
    # ถ้าไม่ได้อยู่ใน virtual environment แต่มีโฟลเดอร์ venv ให้เปิดใช้งาน
    if [ -d "venv" ]; then
        echo "กำลังเปิดใช้งาน virtual environment..."
        source venv/bin/activate
    else
        echo "คำเตือน: ไม่ได้อยู่ใน virtual environment"
        echo "แนะนำให้รัน: source venv/bin/activate"
        echo "หรือติดตั้ง: ./setup.sh"
        echo ""
        read -p "ต้องการดำเนินการต่อโดยไม่ใช้ virtual environment หรือไม่? (y/n): " answer
        if [[ "$answer" != "y" ]]; then
            exit 1
        fi
    fi
fi

# ตรวจสอบว่า Ollama กำลังทำงานอยู่หรือไม่
if ! curl -s http://localhost:11434/api/version > /dev/null; then
    echo "ข้อผิดพลาด: Ollama ไม่ได้ทำงานอยู่ กรุณาเริ่ม Ollama ก่อน"
    echo "คุณสามารถเริ่ม Ollama โดยรัน 'ollama serve' ในอีกเทอร์มินัลหนึ่ง"
    exit 1
fi

# ตรวจสอบว่ามีโมเดลที่จำเป็นหรือไม่
if ! ollama list | grep -q "mxbai-embed-large"; then
    echo "กำลังดาวน์โหลดโมเดล mxbai-embed-large..."
    ollama pull mxbai-embed-large:latest
fi

if ! ollama list | grep -q "llama3:8b"; then
    echo "กำลังดาวน์โหลดโมเดล llama3:8b..."
    ollama pull llama3:8b
fi

# รันสคริปต์ Python
python main.py "$@"

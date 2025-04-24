#!/bin/bash

# สร้าง virtual environment
python3 -m venv venv

# เรียกใช้งาน virtual environment
source venv/bin/activate

# ติดตั้ง dependencies
pip install --upgrade pip
pip install -r requirements.txt --use-pep517

# ตรวจสอบว่า Ollama ถูกติดตั้งหรือไม่
if ! command -v ollama &> /dev/null; then
    echo "คำเตือน: ไม่พบคำสั่ง Ollama บนระบบ"
    echo "โปรดติดตั้ง Ollama จาก https://ollama.com/ ก่อนใช้งาน"
    echo ""
fi

# แสดงข้อความแจ้งเตือนการใช้งาน
echo "การติดตั้งเสร็จสมบูรณ์!"
echo ""
echo "คำแนะนำในการใช้งาน:"
echo "1. เปิดใช้งาน virtual environment ทุกครั้งก่อนใช้โปรแกรม:"
echo "   source venv/bin/activate"
echo ""
echo "2. ตรวจสอบว่า Ollama กำลังทำงานอยู่:"
echo "   ollama serve"
echo ""
echo "3. ใช้คำสั่งนำเข้าข้อมูล (รองรับไฟล์ TXT, PDF, DOCX, CSV และ MD):"
echo "   ./run.sh ingest <path-to-file>"
echo ""
echo "4. ใช้คำสั่งถามคำถาม:"
echo "   ./run.sh query \"คำถามของคุณ\""
echo ""
echo "5. ใช้คำสั่งค้นหาแบบแสดงเฉพาะส่วนที่เกี่ยวข้อง (ไม่ผ่าน LLM):"
echo "   ./run.sh query \"คำถามของคุณ\" --raw-chunks"
echo ""
echo "6. ระบุจำนวนส่วนที่ต้องการค้นหา (ค่าเริ่มต้นคือ 4):"
echo "   ./run.sh query \"คำถามของคุณ\" --num-chunks 6"
echo ""
echo "7. เมื่อใช้งานเสร็จ ปิด virtual environment ด้วยคำสั่ง:"
echo "   deactivate"

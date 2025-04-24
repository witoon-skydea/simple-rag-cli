
# Simple RAG CLI

โปรแกรม CLI อย่างง่ายสำหรับ Retrieval Augmented Generation (RAG) ที่ช่วยให้คุณสามารถนำเข้าเอกสารและถามคำถามเกี่ยวกับเนื้อหาได้

<p align="center">
  <img src="https://raw.githubusercontent.com/witoonpongsilathong/placeholder-images/main/rag-diagram.png" alt="RAG diagram" width="600"/>
</p>

## คุณสมบัติ

- **อินเทอร์เฟซ CLI อย่างง่าย**: ใช้งานง่ายผ่านคำสั่งบรรทัดคำสั่งสำหรับนำเข้าเอกสารและถามคำถาม
- **การโหลดเอกสาร**: รองรับไฟล์ TXT, PDF, MD, CSV และ DOCX
- **การนำเข้าโฟลเดอร์**: สามารถนำเข้าไฟล์ทั้งหมดที่อยู่ในโฟลเดอร์ได้ในคำสั่งเดียว รวมถึงการค้นหาไฟล์แบบ recursive ในโฟลเดอร์ย่อย
- **การสร้าง Embedding**: ใช้โมเดล `mxbai-embed-large:latest` ของ Ollama สำหรับสร้าง embeddings
- **LLM**: ใช้โมเดล `llama3:8b` ของ Ollama สำหรับสร้างคำตอบ
- **การจัดเก็บเวกเตอร์**: ใช้ ChromaDB สำหรับจัดเก็บและค้นหาเวกเตอร์อย่างมีประสิทธิภาพ
- **การค้นหาแบบดิบ**: สามารถค้นหาและแสดงผลส่วนที่เกี่ยวข้องโดยตรงโดยไม่ผ่าน LLM

## ข้อกำหนด

- Python 3.8+
- Ollama ติดตั้งและรันอยู่ (https://ollama.com/)
- ดาวน์โหลดโมเดล Ollama:
  - `mxbai-embed-large:latest`
  - `llama3:8b`

## การติดตั้ง

1. โคลนโปรเจคนี้
```bash
git clone https://github.com/yourusername/simple-rag-cli.git
cd simple-rag-cli
```

2. หากเคยติดตั้งมาก่อนและต้องการเริ่มใหม่ ให้ลบ virtual environment เดิม:
```bash
rm -rf venv
```

3. รันสคริปต์ติดตั้ง:
```bash
./setup.sh
```

สคริปต์นี้จะ:
- สร้าง virtual environment
- อัปเดต pip เป็นเวอร์ชันล่าสุด
- ติดตั้ง dependencies ที่จำเป็น
- ตรวจสอบการติดตั้ง Ollama

4. ตรวจสอบว่า Ollama กำลังทำงานพร้อมโมเดลที่ต้องการ:
```bash
ollama serve  # รันในเทอร์มินัลอื่น
```

## ข้อกำหนดแพ็คเกจ

โปรเจคใช้แพ็คเกจต่อไปนี้:
- chromadb - สำหรับจัดเก็บและค้นหาเวกเตอร์
- langchain - กรอบงานหลักสำหรับ RAG
- langchain-community - คอมโพเนนต์เพิ่มเติมสำหรับ LangChain
- langchain-ollama - อินเทอร์เฟซระหว่าง LangChain และ Ollama
- langchain-core - คอร์ของ LangChain
- python-dotenv - สำหรับจัดการตัวแปรสภาพแวดล้อม
- pypdf - สำหรับอ่านไฟล์ PDF
- pydantic - สำหรับการตรวจสอบข้อมูล
- python-docx - สำหรับอ่านไฟล์ DOCX
- docx2txt - สำหรับแปลง DOCX เป็นข้อความ

แพ็คเกจทั้งหมดจะถูกติดตั้งโดยอัตโนมัติเมื่อคุณรัน `./setup.sh`

## การใช้งาน

### การเปิดใช้งาน Virtual Environment

```bash
source venv/bin/activate
```

### การนำเข้าเอกสาร

โปรแกรมสนับสนุนการนำเข้าเอกสารได้หลายวิธี:

```bash
# นำเข้าไฟล์แต่ละไฟล์
./run.sh ingest path/to/file1.pdf path/to/file2.txt

# นำเข้าไฟล์ทั้งหมดในโฟลเดอร์
./run.sh ingest path/to/documents_folder

# นำเข้าทั้งไฟล์และโฟลเดอร์พร้อมกัน
./run.sh ingest path/to/file1.pdf path/to/documents_folder

# นำเข้าโฟลเดอร์โดยไม่มองหาไฟล์ในโฟลเดอร์ย่อย
./run.sh ingest path/to/documents_folder --no-recursive

# ระบุตำแหน่งฐานข้อมูลเวกเตอร์
./run.sh ingest path/to/documents_folder --db-dir custom_db_location
```

**หมายเหตุเกี่ยวกับการนำเข้าโฟลเดอร์**:
- ค่าเริ่มต้น (หรือใช้ `--recursive`) จะค้นหาไฟล์ในทุกโฟลเดอร์ย่อยด้วย
- ใช้ `--no-recursive` เพื่อค้นหาเฉพาะในโฟลเดอร์หลักเท่านั้น
- โปรแกรมจะอ่านเฉพาะไฟล์ที่สนับสนุน (.txt, .pdf, .md, .csv, .docx) เท่านั้น

### การถามคำถาม

```bash
# ค้นหาและตอบคำถามโดยใช้ LLM
./run.sh query "คำถามของคุณเกี่ยวกับเอกสาร"

# ค้นหาและแสดงเฉพาะส่วนที่เกี่ยวข้องโดยไม่ใช้ LLM
./run.sh query "คำถามของคุณเกี่ยวกับเอกสาร" --raw-chunks

# ระบุจำนวนส่วนที่ต้องการค้นหา
./run.sh query "คำถามของคุณเกี่ยวกับเอกสาร" --num-chunks 6

# ระบุตำแหน่งฐานข้อมูลเวกเตอร์ที่ต้องการค้นหา
./run.sh query "คำถามของคุณเกี่ยวกับเอกสาร" --db-dir custom_db_location
```

## ตัวอย่าง

```bash
# นำเข้าเอกสารตัวอย่าง (ไฟล์เดียว)
./run.sh ingest data/sample.txt

# นำเข้าโฟลเดอร์ data ทั้งหมด
./run.sh ingest data

# ถามคำถาม
./run.sh query "RAG คืออะไร และมีประโยชน์อย่างไร"
```

## วิธีการทำงาน

1. **การนำเข้าเอกสาร**:
   - เอกสารถูกโหลดและแบ่งเป็นส่วนย่อย (chunks)
   - แต่ละส่วนถูกแปลงเป็นเวกเตอร์โดยใช้ mxbai-embed-large
   - เวกเตอร์ถูกเก็บในฐานข้อมูล ChromaDB ในเครื่อง

2. **การตอบคำถาม**:
   - คำถามถูกแปลงเป็นเวกเตอร์โดยใช้โมเดลเดียวกัน
   - ส่วนที่คล้ายกันถูกดึงมาจากฐานข้อมูล
   - ส่วนที่ดึงมาถูกใช้เป็นบริบทสำหรับ LLM
   - LLM (llama3:8b) สร้างคำตอบตามบริบท

## ข้อจำกัด

- ไม่มีความสามารถในการค้นหาบนเว็บ
- รองรับรูปแบบไฟล์จำกัด
- ทำงานในเครื่องเท่านั้น ต้องมีการติดตั้ง Ollama

## การแก้ไขปัญหา

### ปัญหาเกี่ยวกับ Dependencies

หากพบปัญหา dependency conflicts ระหว่างแพ็คเกจ LangChain:

1. ลองลบ venv และสร้างใหม่:
```bash
rm -rf venv
./setup.sh
```

2. หากยังมีปัญหา ลองแก้ไขไฟล์ requirements.txt โดยตรง:
```bash
nano requirements.txt
```

3. ทดลองติดตั้งแต่ละแพ็คเกจแยกกัน:
```bash
pip install chromadb
pip install langchain-ollama
```

### ปัญหาเกี่ยวกับ Ollama

1. ตรวจสอบว่า Ollama กำลังทำงาน:
```bash
curl http://localhost:11434/api/version
```

2. ตรวจสอบโมเดลที่มีอยู่:
```bash
ollama list
```

3. ดาวน์โหลดโมเดลที่จำเป็น:
```bash
ollama pull mxbai-embed-large:latest
ollama pull llama3:8b
```

## การอัพเดทล่าสุด

- **เวอร์ชัน 1.1.0** - เพิ่มความสามารถในการนำเข้าเอกสารทั้งโฟลเดอร์
  - สนับสนุนการค้นหาไฟล์แบบ recursive ในโฟลเดอร์ย่อย
  - เพิ่มตัวเลือก `--no-recursive` สำหรับการค้นหาในโฟลเดอร์หลักเท่านั้น
  - แสดงความคืบหน้าและสรุปการนำเข้าอย่างละเอียด

## การมีส่วนร่วม

หากคุณต้องการมีส่วนร่วมในโปรเจคนี้:

1. Fork โปรเจค
2. สร้าง branch ของคุณ (`git checkout -b feature/amazing-feature`)
3. Commit การเปลี่ยนแปลงของคุณ (`git commit -m 'Add amazing feature'`)
4. Push ไปยัง branch (`git push origin feature/amazing-feature`)
5. เปิด Pull Request

## ลิขสิทธิ์

โปรเจคนี้เผยแพร่ภายใต้สัญญาอนุญาต MIT - ดูไฟล์ [LICENSE](LICENSE) สำหรับรายละเอียด

# 🛍️ be-product-store

Backend service untuk sistem Product Store — dibangun menggunakan **Python** dan **FastAPI**.

---

## 🚀 Cara Menjalankan Backend

### 1. Clone Repository
```bash
git clone https://github.com/anwar456/be-product-store.git
cd be-product-store

### 2. Aktifkan Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # (Linux/macOS)
.venv\Scripts\activate     # (Windows)

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Buat File .env
Untuk file .env nya nanti saya sertakan di google drive

### 5. Jalankan Server
uvicorn app.main:app --reload

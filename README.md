# 📄 Invoice PDF → CSV Extractor

A simple web tool that converts Flipkart-style invoice PDFs into a structured CSV.

Users can upload multiple PDFs or a ZIP file containing many invoices, and the app extracts:

- Date  
- Invoice number  
- Order ID  
- Product model  
- Grand total amount  

The result is downloadable as a CSV file.

---

## 🚀 Features

- Upload multiple PDFs at once  
- Upload ZIP files containing many PDFs  
- Handles nested folders inside ZIPs  
- Detects duplicate invoices automatically  
- Shows processing progress  
- Cleans temporary files after download  
- Runs locally or on Streamlit Cloud  

---

## 🖥 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the app

```bash
streamlit run app.py
```

Open the browser at:

```
http://localhost:8501
```

---

## ☁️ Deploy on Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to https://streamlit.io/cloud
3. Click New App
4. Select your repo and branch
5. Set main file to app.py
6. Deploy

After deployment, your app will be available at a public URL.

---

## 📁 Required Repo Structure

```
repo/
 ├── app.py
 ├── requirements.txt
 ├── runtime.txt
 └── README.md
```

---

## 📋 runtime.txt

```
python-3.11
```

This ensures compatibility with PDF libraries.

---

## 📦 requirements.txt

```
streamlit
pdfplumber
pandas
```

---

## ⚠️ Limitations

- Designed for Flipkart-style invoices
- Works only with text-based PDFs (not scanned images)
- Assumes one main product per invoice

Future improvements may include:
- OCR support for scanned PDFs
- Multi-product invoice parsing
- Database storage of invoice history

---

## 📜 License

MIT License – free to use and modify.

If you want, I can also give you a **better project title**, a short GitHub description, or a README badge section to make the repo look more professional.
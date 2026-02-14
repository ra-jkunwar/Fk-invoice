import os
import re
import zipfile
import pdfplumber
import pandas as pd
import streamlit as st
import tempfile

st.set_page_config(page_title="Invoice PDF to CSV", layout="wide")
st.title("Invoice PDF → CSV extractor")


# ---------------- PARSER ---------------- #

def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    return text


def extract_model(text):
    start_marker = "Value ₹"
    end_marker = "Warranty"

    p1 = text.find(start_marker)
    p2 = text.find(end_marker)

    if p1 == -1 or p2 == -1:
        return ""

    raw_block = text[p1 + len(start_marker):p2]
    lines = raw_block.split('\n')
    cleaned = []

    for line in lines:
        line = line.strip()
        if not line or "FSN:" in line or "IMEI" in line:
            continue

        line = re.sub(r"HSN/SAC:\s*\d+", "", line)
        line = re.sub(r"-?\d+\.\d{2}", "", line)
        line = re.sub(r"\b1\b", "", line)

        cleaned.append(line)

    text = " ".join(cleaned)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"^Handsets\s+", "", text, flags=re.IGNORECASE)

    return text


def extract_fields(text):
    data = {}

    m = re.search(r"Order Date:\s*([\d-]+)", text)
    data["Date"] = m.group(1) if m else ""

    m = re.search(r"Invoice Number\s*#\s*([A-Z0-9]+)", text)
    data["Invoice number"] = m.group(1) if m else ""

    m = re.search(r"(OD\d+)", text)
    data["Order name"] = m.group(1) if m else ""

    data["Model"] = extract_model(text)

    m = re.search(r"Grand Total\s*₹\s*([\d,.]+)", text)
    data["Grand total amount"] = m.group(1) if m else ""

    return data


# ---------------- FILE INPUT ---------------- #

uploaded_files = st.file_uploader(
    "Upload PDFs or ZIP file",
    type=["pdf", "zip"],
    accept_multiple_files=True
)

if uploaded_files:

    temp_dir = tempfile.mkdtemp()
    pdf_paths = []

    def collect_pdfs_from_dir(directory):
        for root, _, files in os.walk(directory):
            for name in files:
                if name.lower().endswith(".pdf"):
                    pdf_paths.append(os.path.join(root, name))

    # Save uploads & extract ZIPs
    for file in uploaded_files:

        if file.name.lower().endswith(".zip"):
            zip_path = os.path.join(temp_dir, file.name)
            with open(zip_path, "wb") as f:
                f.write(file.getbuffer())

            try:
                with zipfile.ZipFile(zip_path, "r") as z:
                    z.extractall(temp_dir)
            except zipfile.BadZipFile:
                st.error(f"{file.name} is not a valid ZIP.")
                continue

            collect_pdfs_from_dir(temp_dir)

        else:
            path = os.path.join(temp_dir, file.name)
            with open(path, "wb") as f:
                f.write(file.getbuffer())
            pdf_paths.append(path)

    pdf_paths = list(set(pdf_paths))

    if not pdf_paths:
        st.warning("No PDFs found.")
        st.stop()

    # ---------------- PROCESSING ---------------- #

    progress = st.progress(0)
    rows = []
    seen = set()

    for i, path in enumerate(pdf_paths):
        try:
            text = extract_text(path)
            fields = extract_fields(text)

            inv = fields.get("Invoice number")
            if inv and inv not in seen:
                rows.append(fields)
                seen.add(inv)

        except Exception:
            st.warning(f"Failed: {os.path.basename(path)}")

        progress.progress((i + 1) / len(pdf_paths))

    # ---------------- OUTPUT ---------------- #

    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df)

        csv_bytes = df.to_csv(index=False).encode("utf-8")

        downloaded = st.download_button(
            "Download CSV",
            csv_bytes,
            "invoices.csv",
            "text/csv"
        )

        if downloaded:
            for p in pdf_paths:
                try:
                    os.remove(p)
                except:
                    pass

            try:
                os.rmdir(temp_dir)
            except:
                pass

            st.success("CSV downloaded. Temporary files removed.")
    else:
        st.warning("No invoices extracted.")
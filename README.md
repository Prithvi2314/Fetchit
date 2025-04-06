# 📄 FetchIt – PubMed Paper Fetcher 🧠

**FetchIt** is a lightweight Python tool that allows users to quickly search for biomedical research papers on **PubMed** using simple keyword queries. It fetches and displays key details such as article title, journal name, and publication year — making it a great utility for students, researchers, and developers who need streamlined access to academic papers.

---

## 🚀 Features

- 🔍 Search PubMed by keyword or topic
- 📄 Automatically fetches article metadata:
  - Title
  - Journal Name
  - Year of Publication
- 📊 Clean output using `pandas` DataFrame
- 💡 Simple, lightweight, and fully scriptable

---

## 🛠️ Built With

- **Python 3.x**
- [`requests`](https://pypi.org/project/requests/) – for making HTTP requests to PubMed API
- `xml.etree.ElementTree` – for parsing XML responses
- poetry for dependencies and command script

---

## 📦 Installation

```bash
git clone https://github.com/Prithvi2314/Fetchit.git

pip install -r requirements.txt

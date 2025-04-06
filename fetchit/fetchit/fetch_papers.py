import argparse
import csv
import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional

API_KEY = "9f4b8fcd0f13463517b30c5ec999d8178d08"

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"


def fetch_pubmed_ids(query: str) -> List[str]:
    """Fetch PubMed IDs based on a user query."""
    params = {"db": "pubmed", "term": query, "retmax": 100, "retmode": "json" , "api_key":API_KEY}
    response = requests.get(BASE_URL + "esearch.fcgi", params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])


def fetch_paper_details(pubmed_id: str) -> Optional[Dict]:
    """Fetch detailed information of a paper using PubMed ID."""
    params = {"db": "pubmed", "id": pubmed_id, "retmode": "xml",  "api_key": API_KEY }
    response = requests.get(BASE_URL + "efetch.fcgi", params=params)
    response.raise_for_status()
    root = ET.fromstring(response.text)
    
    article = root.find(".//PubmedArticle")
    if article is None:
        return None
    
    title = article.findtext(".//ArticleTitle", "Unknown Title")
    pub_date = article.findtext(".//PubDate/Year", "Unknown Date")
    
    authors = []
    companies = []
    email = "Not Available"
    
    for author in article.findall(".//Author"):
        last_name = author.findtext("LastName", "")
        fore_name = author.findtext("ForeName", "")
        affiliation = author.findtext("..//Affiliation", "")
        
        if "university" not in affiliation.lower() and "lab" not in affiliation.lower():
            authors.append(f"{fore_name} {last_name}")
            companies.append(affiliation)
        
        email_elem = author.find("..//AffiliationInfo/Identifier[@Source='EMAIL']")
        if email_elem is not None:
            email = email_elem.text
    
    return {
        "PubmedID": pubmed_id,
        "Title": title,
        "Publication Date": pub_date,
        "Non-academic Author(s)": ", ".join(authors),
        "Company Affiliation(s)": ", ".join(companies),
        "Corresponding Author Email": email,
    }


def save_to_csv(papers: List[Dict], filename: str):
    """Save the paper details to a CSV file."""
    if not papers:
        print("No data to save!")
        return

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=papers[0].keys())
        writer.writeheader()
        writer.writerows(papers)

    print(f"Results saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed research papers based on a query.")
    parser.add_argument("query", type=str, help="Search query for PubMed.")
    parser.add_argument("-f", "--file", type=str, help="Output CSV filename.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    args = parser.parse_args()

    if args.debug:
        print(f"Fetching papers for query: {args.query}")

    pubmed_ids = fetch_pubmed_ids(args.query)
    papers = [fetch_paper_details(pid) for pid in pubmed_ids]
    papers = [p for p in papers if p is not None and p["Non-academic Author(s)"]]
    
    if not papers:
        print("No matching papers found.")
        return
    
    if args.file:
        save_to_csv(papers, args.file)
    else:
        for paper in papers:
            print(paper)

if __name__ == "__main__":
    main()

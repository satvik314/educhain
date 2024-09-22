from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
import re
import requests

class PdfFileLoader:
    def load_data(self, file_path):
        reader = PdfReader(file_path)
        all_content = []

        for page in reader.pages:
            content = page.extract_text()
            content = self.clean_string(content)
            all_content.append(content)

        return " ".join(all_content)

    def clean_string(self, text):
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

class UrlLoader:
    def load_data(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.get_text()
        return self.clean_string(content)

    def clean_string(self, text):
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
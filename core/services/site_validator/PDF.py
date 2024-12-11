import re
import time
import json
import pandas as pd
import pdfplumber
import requests


class PdfParser:
    def __init__(self, pdf_path: str):
        self.__pdf_path = pdf_path

        self.__create_pdf_txt()

    @staticmethod
    def __create_pdf_txt():
        data = {
            "status": "wait",
            "process": 0,
        }
        with open("PDF.json", "w", encoding="utf-8") as f:
            json.dump(data, f)

    def set_stat(self, status: str = None, process: int = None):
        with open("PDF.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        if status:
            data["status"] = status

        if process:
            data["process"] = process


        with open("PDF.json", "w", encoding="utf-8") as f:
            json.dump(data, f)

    @staticmethod
    def get_pdf_stat():
        with open("PDF.json", "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def __clear_url(text: str):
        return text.split(">")[-1]

    @staticmethod
    def __clear_text(text: str):
        return re.sub(r"\s+", " ", text).replace("ё", "е").replace("Ё", "Е")

    def __get_url(self, title: str):
        return self.sveden_t[title]

    def __clear_title(self, text: str):
        text = self.__clear_text(text)
        return text.replace("«", "").replace("»", "")

    @staticmethod
    def __clear_itemprop(text: str):
        return re.sub(r"\s+", "", re.sub(r"[^\w\s]", "", text.split("=")[-1]))

    @staticmethod
    def __load_ro_no(obj: str):
        all_res = []
        t = 0
        f = 0

        for _ in range(3):
            PROMPT = f"""
            Тебе дается текст который описывает то что объект должен делать на сайте и тебе нужно сказать должна ли быть в нем ссылка на какой-то документ и тд.
            В ответе дай только True или False.
            Этот объект должен вести куда-то: {obj}
            """

            data = {
                "model": "mistral-small-latest",
                "messages": [
                    {
                        "role": "user",
                        "content": PROMPT
                    }
                ],
            }

            headers = {
                "Authorization": f"Bearer pSk4UB604FbaZiC4ebPYB7TUahBPjKi2"
            }

            while True:
                resp = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers,
                                     json=data)

                print(resp.status_code)
                if resp.status_code != 200:
                    time.sleep(5)
                    continue

                all_res.append(resp.json()['choices'][0]['message']['content'].replace("\n\n", "\n").strip().rstrip())
                time.sleep(1)
                break

        for res in all_res:
            if "true" in res.lower():
                t += 1
            elif "false" in res.lower():
                f += 1

        return t > f

    def run(self):
        self.set_stat(status="run_without_mistral")
        all_t = []
        self.sveden_t: dict = None

        # Открыть PDF
        with pdfplumber.open(self.__pdf_path) as pdf:
            for page in pdf.pages:
                # Извлечь текст с текущей страницы
                text = page.extract_text()

                match = re.search(r'«[^»]*»', text)
                if match:
                    title = match.group()
                else:
                    title = None

                # Извлечь таблицы с текущей страницы
                tables = page.extract_tables()
                for table in tables:
                    if "sveden" in str(table):
                        self.sveden_t = pd.DataFrame(table)

                    if "itemprop" not in str(table):
                        continue

                    t = pd.DataFrame(table)
                    t['page'] = page.page_number
                    t['title'] = title
                    all_t.append(t)

        self.sveden_t = self.sveden_t[[3, 4]].rename(columns={3: 'key', 4: 'url'}).loc[1:].reset_index(drop=True)
        self.sveden_t['url'] = self.sveden_t['url'].apply(self.__clear_url)
        self.sveden_t['key'] = self.sveden_t['key'].apply(self.__clear_text)
        self.sveden_t = {item['key']: item['url'] for item in self.sveden_t.to_dict("records")}

        df = pd.concat(all_t)
        df.dropna(inplace=True, how='all', axis=1)

        df = pd.concat([df[[1, 2, 'page', 'title']], df[[3, 6, 'page', 'title']].rename(columns={3: 1, 6: 2})])
        df.dropna(inplace=True, how='all', axis=0)

        df.rename(columns={1: 'check', 2: 'itemprop'}, inplace=True)
        df['itemprop'].replace("", None, inplace=True)
        df.dropna(inplace=True, subset=['itemprop'])

        df['check'] = df['check'].apply(self.__clear_text)
        df['title'] = df['title'].apply(self.__clear_title)
        df['itemprop'] = df['itemprop'].apply(self.__clear_itemprop)

        df['url'] = df['title'].apply(self.__get_url)

        df.reset_index(drop=True, inplace=True)

        df.drop_duplicates(subset=['check'], inplace=True)
        df.drop_duplicates(subset=['itemprop'], inplace=True)

        df.reset_index(drop=True, inplace=True)
        df.to_csv("it.csv", index=False)

        self._df = df
        self.set_stat(status="ok_without_mistral")

    def run_with_mistral(self):
        self.set_stat(status="ok_run_with_mistral")
        self._df['load'] = self._df['check'].apply(self.__load_ro_no)
        self._df.reset_index(drop=True, inplace=True)
        self._df.to_csv("it.csv", index=False)
        self.set_stat(status="ok")

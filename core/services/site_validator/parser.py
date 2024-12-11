import logging
import os
import ssl
import time
from urllib.parse import urlparse, urljoin
import idna
import pandas as pd
import requests
from bs4 import BeautifulSoup

from .config import settings

ssl._create_default_https_context = ssl._create_unverified_context

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')
logger = logging.getLogger(__name__)


class SiteValidator:
    BASE_FOLDER_PATH = "site_data"
    # Инициализация
    # __VISITED_PAGES = set()  # Уже посещенные страницы, чтобы избежать зацикливания
    __ERROR_PAGES = {}  # Ошибки при посещении страниц

    # __DOCUMENT_LINKS = []  # Найденные ссылки на документы

    # # Определение целевых расширений документов
    # DOCUMENT_EXTENSIONS = [
    #     # Текстовые документы
    #     ".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".wps", ".wpd",
    #
    #     # Таблицы
    #     ".xls", ".xlsx", ".ods", ".csv", ".tsv",
    #
    #     # Презентации
    #     ".ppt", ".pptx", ".odp", ".key",
    #
    #     # Форматы электронных книг
    #     ".epub", ".mobi", ".azw", ".azw3", ".lit", ".fb2",
    #
    #     # Форматы документов и проектов
    #     ".pages", ".pub", ".xps",
    #
    #     # Форматы специализированных документов
    #     ".tex", ".md", ".xml", ".json", ".yml", ".yaml",
    #
    #     # Изображения
    #     ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp", ".svg", ".ico", ".heic", ".raw", ".cr2",
    #     ".nef", ".orf", ".arw"
    # ]

    def __init__(self, url):
        self._validate_folder()
        self.__url = self.__valid_url(url)

        self.output_file = os.path.join(self.BASE_FOLDER_PATH, f"{self._host}_rule_res.csv")
        logger.info(f"Initialized SiteValidator with URL: {self.__url}")

    def _validate_folder(self):
        if self.BASE_FOLDER_PATH not in os.listdir("."):
            os.mkdir(self.BASE_FOLDER_PATH)
            logger.info(f"Created folder {self.BASE_FOLDER_PATH}")
        else:
            logger.info(f"Folder {self.BASE_FOLDER_PATH} already exists.")

    def __valid_url(self, url: str):
        parsed_url = urlparse(url)
        self._host = idna.decode(parsed_url.hostname)
        scheme = parsed_url.scheme
        logger.debug(f"Decoded host: {self._host}")
        return f"{scheme}://{self._host}"

    def __load_rule(self):
        logger.info("Loading rules from 'it.csv'...")
        return pd.read_csv("it.csv")

    def __mistral(self, prompt: str):
        data = {
            "model": "mistral-small-latest",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        }

        headers = {
            "Authorization": f"Bearer {settings.MISTRAL_API_KEY}"
        }

        while True:
            resp = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers,
                                 json=data)

            print(resp.status_code)
            if resp.status_code != 200:
                time.sleep(5)
                continue

            return resp.json()['choices'][0]['message']['content'].replace("\n\n", "\n").strip().rstrip()

    def check_rule_1(self):
        logger.info(f"Starting rule check for URL: {self.__url}")
        res = []
        df_rule = self.__load_rule()

        for url_path in df_rule['url'].unique():
            url = urljoin(self.__url, url_path)
            url_path_data = df_rule[df_rule['url'] == url_path]
            all_item = {key: {'valid': False, 'text': None, 'href': None, 'status': None} for key in
                        url_path_data['itemprop'].tolist()}

            try:
                logger.info(f"Fetching URL: {url}")
                resp = requests.get(url)
                soup = BeautifulSoup(resp.text, 'lxml')

                for item in all_item.keys():
                    logger.debug(f"Searching for itemprop: {item}")
                    if resp.status_code != 200:
                        all_item[item]['status'] = f"Ошибка {resp.status_code}"
                        continue

                    find = soup.find(attrs={"itemprop": item})
                    if find:
                        all_item[item]['valid'] = True
                        all_item[item]['text'] = find.text
                        all_item[item]['status'] = "ok"
                        if 'href' in find.attrs:
                            all_item[item]['href'] = find['href']
                        else:
                            a = find.find("a")
                            if a:
                                if 'href' in a.attrs:
                                    all_item[item]['href'] = a['href']
                        logger.debug(f"Found itemprop {item}: {find.text}")

                for itemprop, val in all_item.items():
                    res.append({
                        "itemprop": itemprop,
                        "valid": val['valid'],
                        "text": val['text'],
                        "href": val['href'],
                        "status": val['status']
                    })
            except requests.RequestException as e:
                logger.error(f"Error fetching URL {url}: {e}")
                self.__ERROR_PAGES[url] = str(e)

        if res:
            self.df_res = pd.merge(pd.DataFrame(res), df_rule, on='itemprop', how='inner')

            self.df_res.to_csv(self.output_file, index=False)
            logger.info(f"Results 1 saved to {self.output_file}")

    def check_rule_2(self):
        res = []

        for item in self.df_res[['itemprop', 'text', 'check', 'status']].to_dict("records"):
            print(item)
            if item['itemprop'] == "copy" or item['status'] != "ok":
                res.append({
                    "itemprop": item['itemprop'],
                    "valid_text": "Данный атрибут не подлежит анализу",
                })
                continue
            prompt = f"Проверь соответствует ли контент text тому что описано в check.Если нет то напиши почему, если все соответствует то напиши 'Соответствует'\n\ntext - {item['text']}\ncheck - {item['check']}"
            answer = self.__mistral(prompt)
            res.append({
                "itemprop": item['itemprop'],
                "valid_text": answer,
            })
            time.sleep(1)

        if res:
            self.df_res = pd.merge(pd.DataFrame(res), self.df_res, on='itemprop', how='inner')

            self.df_res.to_csv(self.output_file, index=False)
            logger.info(f"Results 2 saved to {self.output_file}")

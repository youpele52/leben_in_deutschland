from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import random
from fake_useragent import UserAgent
from constants import URLS, FILE_NAME


class LebenInDeutschland:
    def __init__(self, output_excel: bool = False, path: str | None = None) -> None:
        self.output_excel = output_excel
        self.file_name = FILE_NAME
        self.path = path
        self.ua = UserAgent()

    def extract_data(self):
        questions = []
        answers = []

        for i in range(0, self.no_of_pages):
            url = self.base_url if i == 0 else f"{self.base_url}{i+1}/"
            print(f"Extracting {self.sheet_name}'s data from {url}")

            try:
                headers = {"User-Agent": self.ua.random}
                response = requests.head(url, headers=headers, timeout=10)
                if response.status_code != 200:
                    print(
                        f"Skipping {url} - Page not found (Status code: {response.status_code})"
                    )
                    continue
            except requests.RequestException as e:
                print(f"Skipping {url} - Error: {str(e)}")
                continue
            # Add a random delay between requests
            delay = random.randint(5, 15)
            print(f"Waiting for {delay} seconds before the next request...")
            time.sleep(delay)

            result = self.questions_and_answers(url)
            questions.extend(result["questions"])
            answers.extend(result["answers"])

            print(f"Successfull extracted data from {url}\n\n")

        return pd.DataFrame({"Frage": questions, "Antwort": answers})

    def questions_and_answers(
        self, url: str | None = None, questions: list = [], answers: list = []
    ) -> dict:
        headers = {"User-Agent": self.ua.random}  # Randomize user-agent
        page = requests.get(self.base_url if url is None else url, headers=headers)
        page_soup = BeautifulSoup(page.content, "html.parser")
        questions = []
        answers = []

        # Find all divs with an id that contains "frage"
        question_rows = page_soup.select("div[id*=frage]")

        if not question_rows:
            wait_time = random.randint(0, 10)
            print(f"No question rows found, reloading page in {wait_time} seconds")
            time.sleep(wait_time)
            page = requests.get(self.base_url if url is None else url, headers=headers)
            page_soup = BeautifulSoup(page.content, "html.parser")
            question_rows = page_soup.select("div[id*=frage]")

        if question_rows:
            for question_row in question_rows:
                question = (
                    question_row.find(class_="questions-question-text").find("p").text
                )
                questions.append(question)
                answer = question_row.find(class_="question-answer-right").text
                answers.append(answer)

        return {"questions": questions, "answers": answers}

    def save_data(self, all_data):
        if all_data:
            output_path = (
                f"{self.path}/{self.file_name}.xlsx"
                if self.path
                else f"{self.file_name}.xlsx"
            )
            print(f"Saving all data to: {output_path}")

            with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
                for sheet_name, df in all_data.items():
                    # Clean sheet name (Excel has restrictions on sheet names)
                    clean_sheet_name = sheet_name[:31]  # Max 31 chars
                    clean_sheet_name = (
                        clean_sheet_name.replace(":", ".")
                        .replace("\\", ".")
                        .replace("/", ".")
                    )

                    # Save to Excel
                    df.to_excel(writer, sheet_name=clean_sheet_name, index=False)
                    print(f"Saved sheet: {clean_sheet_name}")

            print(f"Successfully saved all data to {output_path}")
        else:
            print("No data to save")

    def run(self) -> None:
        all_data = {}
        for url in URLS:
            self.base_url = url.get("url")
            self.sheet_name = url.get("sheet_name")
            self.no_of_pages = 1 if len(self.base_url.split("/")) > 5 else 10

            df = self.extract_data()
            if not df.empty:
                all_data[self.sheet_name] = df

        self.save_data(all_data)


if __name__ == "__main__":
    leben_in_deutschland = LebenInDeutschland(
        output_excel=True,
    )
    leben_in_deutschland.run()

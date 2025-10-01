import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from dotenv import load_dotenv
import os
import time
import random
from typing import List
from html.parser import HTMLParser


load_dotenv()

class WikiParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._chunks = []


    def handle_data(self, data):
        self._chunks.append(data)


    def get_text(self):
        """
        
        """
        if len(self._chunks) == 0:
            print("Chunks are empty. First use WikiParser's feed method.")
        text = "".join(self._chunks)
        self._chunks.clear()
        return text
    

# EXAMPLES OF OUTPUT
# {'drikke': [{'pos': 'noun', 'en_translation': ['drink']}, {'pos': 'verb', 'en_translation': ['to drink']}]}
# {'pytt': [{'pos': 'noun', 'en_translation': ['a pond', 'pool (of water)', 'puddle']}]}
class WikitionaryClient:
    """
    
    """
    def __init__(self,
            user_agent: str = os.environ.get("AGENT_STRING"),
            total_retries: int = 3,
            backoff_factor: float = 0.5,
            status_forcelist: tuple = (429, 500, 502, 503, 504),
            min_delay: float = 0.05,
            jitter: float = 0.02,
        ) -> None:
        self.user_agent = user_agent
        self.total_retries = total_retries
        self.backoff_factor = backoff_factor
        self.status_forcelist = status_forcelist
        self.min_delay = min_delay
        self.jitter = jitter
        self.session = self._make_session()
        self._parser = WikiParser()


    def _make_session(self) -> requests.Session:
        """
        
        """
        ses = requests.Session()
        retries = Retry(
            total=self.total_retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=self.status_forcelist,
            allowed_methods=frozenset(["GET"]),
            raise_on_status=False
        )
        adapter = HTTPAdapter(max_retries=retries, pool_connections=20, pool_maxsize=20) # Not quite sure about that one
        ses.mount("https://", adapter)
        ses.headers.update({"User-Agent": self.user_agent})
        return ses


    def _rate_limit(self) -> None:
        """
        
        """
        time.sleep(self.min_delay + random.random() * self.jitter) 


    # There is a limit for 200 but for this project it seems to be sufficient for now
    def fetch_raw(self, word: str) -> dict: 
        """
        
        """
        url =   f"https://en.wiktionary.org/api/rest_v1/page/definition/{word}?redirect=false"
        
        try:
            res = self.session.get(url, timeout=15)
            if res.status_code == 200:
                return res.json()
            
            if res.status_code in (429, 503):
                self._rate_limit() # To wait a bit longer next time

            if res.status_code == 404:
                print(f"Probably unknown term: {word}") 
                #
                #
                # ADD SOMETHING HERE OR HANDLE IT BETTER 
                #
                #

            if res.status_code == 501:
                print(f"No definitions for '{word}' in English.") 
                #
                #
                # ADD SOMETHING HERE OR HANDLE IT BETTER 
                #
                #
            return None
        
        except requests.RequestExceptiona as e:
            print(f"Error with a request: {e}")
            return None


    # Lack of examples for now
    def parse_api_response(self, word: str) -> list:
        """
        
        """
        response = self.fetch_raw(word)
        # print(response)

        out_list = []
        for entry in response.get("other", []):
            if entry.get("language") != "Norwegian Bokmål":
                continue
            try:
                temp_dict = dict()
                temp_dict["pos"] = entry["partOfSpeech"].lower()
                
                # Nested "definition" dicts under "definitions"
                if len(entry["definitions"]) > 1:
                    temp: list = []
                    defins = entry["definitions"]
                    for defin in defins:
                        self._parser.feed(defin["definition"]) # It stores data under ALL "definition" key
                        temp.extend([w.strip() for w in self._parser.get_text().split(",")])

                # Definitions seperated by "," in one dict
                else:
                    self._parser.feed(entry["definitions"][0]["definition"])           
                    temp = [w.strip() for w in self._parser.get_text().split(",")]

                temp_dict["en_translation"] = temp
                
                out_list.append(temp_dict)

            except Exception as e:
                print(f"Error occured during parsing for word: {word}")
                print(f"Type of error: {type(e)}")
                print(f"Explanation: {e}")
                return None

            del temp_dict # To be sure no keys aren't passed from one to another

        return out_list

        
    def process_words(self, words: List[str]) -> dict:
        """
        
        """
        to_ret = dict()
        for word in words:
            result = self.parse_api_response(word)
            if result == None:
                continue

            to_ret[word] = result
            # self._rate_limit() maybe

        return to_ret
    

if __name__ == "__main__":
    w = ["drikke", "pytt", "vennen", "venn"]
    wiki = WikitionaryClient()
    print(wiki.process_words(w))

    
    
    # to_parse = '<a rel="mw:WikiLink" href="/wiki/drink" title="drink">drink</a>'
    # parser = WikiParser()
    # parser.feed(to_parse)
    # x = parser.get_text()
    # print(x).
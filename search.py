import asyncio
import aiohttp

from  pydantic import BaseModel
search_url = "https://api.search.brave.com/res/v1/web/search"
brave_api_key = "BSAsV5w2ABc9SshOY3pMZUc2m3eOfd8"  # Add your Brave API key here

def _update_demo(fname="searchdemo.json"):
    f = open(fname,"w")
    x = asyncio.run(Searcher(brave_api_key, use_demo=False)._search_brave("what to do in olinda pernambuco brazil"))
    import json
    json.dump(x, f)
    f.close()

class SearchItem(BaseModel):
    title: str
    url: str
    is_source_local: bool
    is_source_both: bool
    description: str = None
    page_age: str = None
    page_fetched: str = None
    profile: dict = None
    language: str = None
    family_friendly: bool = False

def getDemoResults():
        import json
        f = open("searchdemo.json", "r")
        d = json.load(f)
        f.close()
        return d

class Searcher:
    def __init__(self, api_key:str, use_demo=True):
        self.api_key =api_key
        self.demo = {}
        self.use_demo = use_demo
        
    
    async def search(self, query):
        if self.use_demo:
            if not self.demo: self.demo = getDemoResults()
            return [SearchItem(**result) for result in self.demo['web']['results']]
        else: return [SearchItem(**result) for result in await self._search_brave(query)['web']['results']]
   
    async def _search_brave(self, query: str, country="BR"):
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": self.api_key
        }
        
        params = {
            "q": query,
            "country": country
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(search_url, headers=headers, params=params) as response:
                return await response.json()

_update_demo()
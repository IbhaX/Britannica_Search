"""
Britannica Search engine
author: Albin Anthony (Ibha-X)
date: 13-01-2023
"""

import sys, os
import argparse 

from time import sleep
from simple_term_menu import TerminalMenu
from requests import get
from bs4 import BeautifulSoup
from functools import lru_cache
from yaspin import yaspin
from yaspin.spinners import Spinners
from textwrap import shorten
from string import  ascii_letters


SEARCH = "| Search Britannica |".center(60, "*")
TITLE = "+ Britannica +".center(60, "*")

if sys.platform == "linux":
    clear = lambda: os.system("clear")
elif sys.platform == "win32":
    clear = lambda: os.system("cls")

def Print(string, speed=9):
    speed = 10 if speed > 10 else 0 if speed < 0 else speed
    speed = (10-speed) * 0.005

    for i in string:
        print(i, flush=True, end="")
        sleep(speed)

def detail(url):
    """ Get detailed query content """
    soup = BeautifulSoup(get(url).content, "html.parser")
    content = "n".join([i.text.strip() for i in soup.find_all("p", class_="topic-paragraph")])
    images = [i.a["href"] for i in soup.find_all("div", class_="card")]

    data = {
        "content": content,
        "images": images if images else None
    }
    return data

@lru_cache()
@yaspin(Spinners.bouncingBall, color="cyan", text="Fetching data from web...")
def search(query):
    """ function for searching and fetching query """
    url = f"https://www.britannica.com/search?query={'+'.join(query.split())}"
    base_url = "https://www.britannica.com"
    soup = BeautifulSoup(get(url).content, "html.parser")
    response = soup.find("div", class_="search-results")
    response = {i.a.text.strip(): base_url + i.a["href"] for \
                i in response.find_all("li")}  
    data = {"results": {}}
    for k,v in response.items():
        result = {k:detail(v)}
        data["results"].update(result)
    return data

def menu(options):
    terminal_menu = TerminalMenu(options, title="Results", skip_empty_entries=True, menu_cursor="=> ")
    menu_entry_index = terminal_menu.show()
    title = options[menu_entry_index][3:]
    return title
  
  
def run():
    s_history = []
    while True:
        clear()
        Print(SEARCH, speed=9)
        hist = f"History: ({','.join(s_history)})" if s_history else ""
        query = input(f"\n{hist}\nEnter Query ('x' for exit): ")
        
        if query not in s_history:
            s_history.append(query)
            
        if query in ("x", "exit"):
            exit(code="Exiting Script... GoodBye")
            
        data = search(query)
        options = list(f"[{l}]{k}" for l,k in zip(ascii_letters,data["results"].keys()))
        options.append("[y]Back")
        options.append("[z]Exit")
        
        while True:
            clear()
            Print(f"{TITLE}\n")     
            title = menu(options)
            
            if title.lower() == "back":
                break
            if title.lower() == "exit":
                exit(code="Exiting Script... GoodBye...")
            else:
                try:
                    data = data["results"][title]["content"]
                    Print(f"{title.title().center(60)}\n", speed=9.5)
                    print(f"{'-'*len(title)}".center(60))
                    Print(shorten(data.capitalize(), width=500, placeholder=" ..."))
                    Print("\n\nRead full article? (yes,no): ")
                    act = input()
                    if act in "yes":
                        clear()
                        Print(TITLE)
                        Print(f"{title.title().center(60)}\n", speed=9.5)
                        print(f"{'-'*len(title)}".center(60))
                        Print(data)
                        input("\nGo back?")
                    else:
                        continue
                except KeyError:
                    print("Key Error")
                    continue
                except TypeError:
                    print("Type Error")
                    continue
                
def main():
    try:
        run()
    except KeyboardInterrupt:
        print("\nKeyboard Interupt... \nExiting Script... GoodBye...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="python3 bsearch.py",description ="Modes: (python3 bsearch.py) runs cli script / (python3 bsearch.py -j (query)) prints query results in json format") 
    parser.add_argument("-j", "--json", help="argument used to print search results in json format")
    args = parser.parse_args() 
    if args.json:
        try:
            print(search(args.json))
        except KeyboardInterrupt: print("Keyboard Inturupt... Exiting Script!!")
             
    else:
        main()

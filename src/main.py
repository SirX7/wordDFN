# python script to use wordnik api for getting word meaning.

import argparse as _ap
import json as _json
import os as _os
import sys as _sys
from itertools import zip_longest as _zl
from pathlib import Path as _Path

import pyperclip as _pclp
from requests import Request, Session, codes
from requests.exceptions import ConnectionError, HTTPError, Timeout, TooManyRedirects

import dictionaryAPI as _da
from setting import setting_handler as _sh

# Manage user setting from .json file.
GET_SETTINGS = _sh()

API_KEY = GET_SETTINGS["api_key"]

URL = "https://api.wordnik.com/v4/word.json/"


# This function is to be render unnecessary due to wordnik TOS of not allowing data to be cache.
def verify_file(fp: _Path) -> _Path:
    """Verify if the file in the giving path exists and check to see if it is empty or not, if not exist it try to creat one."""

    # verify if the file path exist.
    if fp.exists():
        # check to see if the file is not empty.
        if _os.path.getsize(fp) > 0:
            # get the file size.
            print(f"{_os.path.getsize(fp)} bytes of cache data.")
            # return the absolute file path.
            return fp.absolute()
        else:
            # get the file size.
            print(f"File Empty::{_os.path.getsize(fp)} bytes of cache data.")
            with open(fp, "w") as file:
                file.write("{}")
            # return the absolute file path.
            return fp.absolute()

    else:
        # If file does not exists, should be created.
        print(f"No cache file found but will be created...")
        # Call function to create the cache file.
        creat_cache_file(fp)
        # return the absolute file path.
        return fp.absolute()


# This function is to be render unnecessary due to wordnik TOS of not allowing data to be cache.
def creat_cache_file(fp: _Path) -> None:
    """Creat a cache file to store data from the wordnik api. Also can be use to creat file for any purpose."""

    print(f"creating cache file in {_os.path.abspath(fp)}")
    # creat a file given in the filePath.
    cachePath = _Path("./data/cache/")
    _os.makedirs(cachePath)
    fp.touch()
    with open(fp, "w") as file:
        file.write("{}")


# This function is to be render unnecessary due to wordnik TOS of not allowing data to be cache.
def cache_data(fp: _Path, dataToCache: list | tuple, dk: str, kp: str) -> None:
    """Store data from the API in to a cache file for future usege."""

    data: dict = {}

    cacheVal = {
        "def": [],
        "verb": [],
        "syn": [],
        "ant": [],
    }

    # Use a context maneger to help open and close the I/O of the file being use.
    # open the file in read mode.
    with open(fp, "r") as file:
        # Deserialize the json file and store it in the data variable of type dictionary.
        data = _json.load(file)
        print(f"File loade to Memory.")

    if dk in data:
        if data[dk][kp] == []:
            data[dk][kp] = dataToCache

    elif dk not in data:
        data.setdefault(dk, cacheVal)
        if data[dk][kp] == []:
            data[dk][kp] = dataToCache

    # open the file in write mode.
    with open(fp, "w") as file:
        # Add the new data to the already existing one.
        # serialize the data back to json format.
        _json.dump(data, file)
        print(f"Save successfull.")


# This function is to be render unnecessary due to wordnik TOS of not allowing data to be cache.
def uncache_data(fp: _Path, dk: str, kp: str) -> list[str | list]:
    """Retrevie data from a cache file and return the data."""

    # Use a context maneger to help open and close the I/O of the file being use.
    # open the file in read mode.
    with open(fp, "r") as file:
        # Deserialize the json file and store it in the data variable of type dictionary.
        data = _json.load(file)
        # Retrive the value from the data by it's key.
        dataValue = data[dk][kp]

    # Return the value retrived.
    return dataValue


# This function is to be render unnecessary due to wordnik TOS of not allowing data to be cache.
def cache_data_pparser(data: list[str | list], kp: str) -> None:
    """Parse and print data from the cache file."""

    if kp == "def":
        for items in data:
            for val in items:
                print(val)
    else:
        if kp == "verb":
            print("Verb:")
        elif kp == "syn":
            print("synonym:")
        elif kp == "ant":
            print("antonym:")
        for val in data:
            print(val)


# This function is to be render unnecessary due to wordnik TOS of not allowing data to be cache.
def cache_data_verifier(fp: _Path, word: str, kword: str) -> bool:
    """Verifies if a word to search for is in a cache file. If the word exist return True, if not return False."""

    # Use a context maneger to help open and close the I/O of the file being use.
    # open the file in read mode.
    with open(fp, "r") as file:
        # Deserialize the json file and store it in the data variable of type dictionary.
        data = _json.load(file)

        # Verify if a word to search for exists in the data variable witch should be converted upon deserilizing to a python dictionary.
        if word in data:
            print(f"{word} found in cache file {fp.name}.")
            # Check to see if the word has any definition, verb, synonyms or antonyms.
            if data[word][kword] == []:
                print(f"{kword} have no value.")
                return False
            return True

        # If the word (meaning the key) does not exixts then return False.
        else:
            print(f"{word} is not present in the cache file {fp.name}")
            return False


def args_handler() -> dict[str]:
    """Handle the way arguments is pass via the command-line interface for the script.
    Returns a dictionary with all arguments as key-value pairs."""

    # Creat and object for parsing the arguments.
    parser = _ap.ArgumentParser()

    # Specify the individual argument use on the CLI.
    parser.add_argument("word", nargs="?")
    parser.add_argument("-f", "--verb", nargs="?")
    parser.add_argument("-s", "--syn", nargs="?")
    parser.add_argument("-o", "--ant", nargs="?")

    # Run the parser object and place the extended data in args variable as an argpaser.Namespace object.
    arg = parser.parse_args()

    # Convert the object to a dictionary.
    args = vars(arg)

    # Return the dictionary.
    return args


def api_handler(
    w: str,
    *query: tuple[str],
    accpt_type: str = "application/json",
    ep: str = "definitions",
) -> list[dict]:
    """accpt_type="application/json", ep="definitions"
    Handles how the api make call to retrive information about a given word.

    Require arguments:
    w:                         Word to lookup definition for.

    Optional keyword arguments:
    query:                     Specify the parameters use for each endpoint.
    accpt_type:                Response Content Type, default to "application/json".
    ep:                        Specify the type of endpoint, default to "definitions".

    The *query argument (*args) value are define as following:

    Definitions (definitions) endpoint parameters:
    limit:                     Maximum number of results to return.
    sourceDictionaries:        Specify the dictionary to return definitions from.
    includeTags:               Return a closed set of XML tags in response.

    Varible use to set parameters:
    limit: str = "4"           Maximum number of results to return, default to 4.
    src: str = "all"           Specify the dictionary to return definitions from, default to all. Most use source are ahd-5, wordnet, webster.
    tag: str = "false"         Return a closed set of XML tags in response, default to false.

    e.g:
    parameters = {
        "limit": "4",
        "sourceDictionaries": "all",
        "includeTags": "false",
    }

    Related Words (relatedWords) endpoint parameters:
    relationshipTypes:         Specify the relationship type.
    limitPerRelationshipType:  Limit the amount of supplied relationship types.

    Varible use to set parameters:
    word_relations: str = "verb-form"   The word relation type to be return, default to verb-form, other valus are synonym or antonym.
    limit_relations: str = "5"          Maximum number of results to return, default to 5.

    e.g:
    parameters = {
        "relationshipTypes": "verb-form",
        "limitPerRelationshipType": "5",
    }

    """

    # create an dictionaryAPI.WordnikConfig object to help make the API call.
    caller = _da.WordnikConfig()

    # Create the api headers.
    headers = caller.headers_construct(accpt_type, API_KEY)

    # Set the default value for the parameter base on its endpoint whenever no value is being pass to the query argument.
    if len(query) == 0 and ep == "definitions":
        # limit: str = "4"
        # src: str = "all"
        # tag: str = "false"
        query = (
            "4",
            "all",
            "false",
        )
    # Set the default value for the parameter base on its endpoint whenever no value is being pass to the query argument.
    elif len(query) == 0 and ep == "relatedWords":
        # word_relations: str = "verb-form"
        # limit_relations: str = "5"
        query = (
            "verb-form",
            "5",
        )

    # Create the parameters to send to the api.
    parameters = caller.parameters_construct(ep, *query)

    # Create the full api url, this include the word to search for along with its endpoint.
    url = caller.url_construct(URL, w, ep)

    # Set all api elements to the dictionaryAPI.WordnikConfig object. use most for debuging.
    caller.api_construct(url, headers, parameters)
    print(caller.show_api_obj())  # This line is for test and Debugging.

    # Creat the requests session object to be use to call the api.
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        response.raise_for_status()

    except (ConnectionError, Timeout, TooManyRedirects, HTTPError) as e:
        # print(f"Error happend here {e}") # help to see the type of exception that is being capture.
        print(f"Error...")

    else:
        data = _json.loads(response.text)
        return data


def word_api_parser(ep: str, data: list[dict]) -> list | tuple:
    """Parse the wordnik api data.
    Takes an endpoint along with a list of dictionery containing the data return from the wordnik api
    and parse it to a more reader friendly data."""

    attrib_group: list[str] = []
    src_group: list[str] = []
    def_group: list[str] = []
    eg_group: list[str] = []
    rel_group: list[str] = []

    if ep == "definitions":
        for text in data:
            attrib_group.append(text.get("attributionText"))
            src_group.append(text.get("sourceDictionary"))
            def_group.append(text.get("text"))
            for eg in text.get("exampleUses"):
                eg_group.append(eg.get("text"))

        return [attrib_group, src_group, def_group, eg_group]

    elif ep == "relatedWords":
        for res in data:
            for words in res.get("words"):
                rel_group.append(words)

        return rel_group


def word_api_printer(ep: str, data: list | tuple, key: str) -> None:
    """Recieve a list or a tuple of data to be printed out in a more readable form."""

    if ep == "definitions":
        atrib, src, meaning, eg = data
        word_group = _zl(atrib, src, meaning, eg, fillvalue="-")
        for a, s, m, e in word_group:
            wp = f"Attribution:{a} ({s})\nDefinition:{m}\nExample:{e}\n"
            print(wp)

    elif ep == "relatedWords":
        if key == "verb":
            print("Verb:")
        elif key == "syn":
            print("synonym:")
        elif key == "ant":
            print("antonym:")
        for rel in data:
            wp = f"{rel}"
            print(wp)


def menu(word: str) -> str:
    """Creat a menu for the user to interact with.
    Take the word to search for and return a key that is use to lookup the word."""

    key = input(
        f"What part would you like to learn of {word}?\nOption:\nSelect/type a leter to chose your option:\nDefinition:[d/D]\nVerb:[f/F]\nSynonym:[s/S]\nAntonym:[o/O]\nExit:[q/Q]\nTo clear the clip board press [c/C]\n> "
    )
    key = key.lower()
    while key:
        if key == "d":
            key = "def"
            break
        elif key == "f":
            key = "verb"
            break
        elif key == "s":
            key = "syn"
            break
        elif key == "o":
            key = "ant"
            break
        elif key == "c":
            word = _pclp.copy("")  # Remove empty string
            break
        elif key == "q":
            _sys.exit()
        else:
            print(f"Option invalid , try again")
            key = input(
                f"What part would you like to learn of {word}?\nOption:\nSelect/type a leter to chose your option:\nDefinition:[d/D]\nVerb:[f/F]\nSynonym:[s/S]\nAntonym:[o/O]\nExit:[q/Q]\nTo clear the clip board press [c/C]\n> "
            )
            key = key.lower()
    return key


def main() -> None:
    filePath = _Path("./data/cache/wordDnf.json")

    # Endpoints that can be use.
    defEndpoint: str = "definitions"
    relEndpoint: str = "relatedWords"

    words: dict[str | None] = {}
    key: str = ""
    word: str = ""

    print(verify_file(filePath))

    # Make use of the clipboard with _pclp.paste() (where _pclp is calling pyperclip module.)
    clip = GET_SETTINGS["handler"]
    word = eval(clip)

    # Check to see if word exist in the clipboard.
    if word != "":
        print(f"Word in clipboard")
        key = menu(word)

        # make sure there is only one word in the clipboard.
        word = word.split(" ")
        if len(word) >= 1:
            word = word[0]

            # verify word and check where to retrive resoult from.
            val = cache_data_verifier(filePath, word, key)

            if val:
                print("Retriving data from cache file.....")
                ucd = uncache_data(filePath, word, key)

                cache_data_pparser(ucd, key)
                word = _pclp.copy("")

            elif not val:
                if key == "def":
                    try:
                        print("Calling API.....")
                        data = api_handler(word)
                        def_result = word_api_parser(defEndpoint, data)
                        word_api_printer(defEndpoint, def_result, key)

                    except (AttributeError, TypeError) as e:
                        # print(f"{word} not found: {e}")# help to see the type of exception that is being.
                        print(f"Definition for {word} not found")
                        word = _pclp.copy("")

                    else:
                        # save data to cache:
                        cache_deff: list[str] = []
                        att, sr, sig, epl = def_result
                        zipped_def = _zl(att, sr, sig, epl, fillvalue="-")
                        for zwd in zipped_def:
                            cache_deff.append(zwd)
                        cache_data(filePath, cache_deff, word, key)
                        word = _pclp.copy("")

                elif key == "verb":
                    try:
                        print("Calling API.....")
                        data = api_handler(word, ep=relEndpoint)
                        verb_result = word_api_parser(relEndpoint, data)
                        word_api_printer(relEndpoint, verb_result, key)

                    except (AttributeError, TypeError) as e:
                        # print(f"{word} not found: {e}")# help to see the type of exception that is being.
                        print(f"Verb for {word} not found")
                        word = _pclp.copy("")

                    else:
                        # save data to cache:
                        cache_data(filePath, verb_result, word, key)
                        word = _pclp.copy("")

                elif key == "syn":
                    try:
                        print("Calling API.....")
                        data = api_handler(word, "synonym", ep=relEndpoint)
                        syn_result = word_api_parser(relEndpoint, data)
                        word_api_printer(relEndpoint, syn_result, key)

                    except (AttributeError, TypeError) as e:
                        # print(f"{word} not found: {e}")# help to see the type of exception that is being.
                        print(f"Synonym for {word} not found")
                        word = _pclp.copy("")

                    else:
                        # save data to cache:
                        cache_data(filePath, syn_result, word, key)
                        word = _pclp.copy("")

                elif key == "ant":
                    try:
                        print("Calling API.....")
                        data = api_handler(word, "antonym", ep=relEndpoint)
                        ant_result = word_api_parser(relEndpoint, data)
                        word_api_printer(relEndpoint, ant_result, key)

                    except (AttributeError, TypeError) as e:
                        # print(f"{word} not found: {e}")# help to see the type of exception that is being.
                        print(f"Antonym for {word} not found")
                        word = _pclp.copy("")

                    else:
                        # save data to cache:
                        cache_data(filePath, ant_result, word, key)
                        word = _pclp.copy("")

    elif word == "":
        print(f"Nothing in clipboard")

        # Args return from args_handler function.
        words = args_handler()

        for k, w in words.items():
            if w != None:
                key = k
                word = w
                print(f"{key}:{word}")  # Test code.
                if key == "word":
                    key = "def"
                val = cache_data_verifier(filePath, word, key)

                if val:
                    print("Retriving data from cache file.....")
                    ucd = uncache_data(filePath, word, key)

                    cache_data_pparser(ucd, key)

                elif not val:
                    if key == "def":
                        try:
                            print("Calling API.....")
                            data = api_handler(word)
                            def_result = word_api_parser(defEndpoint, data)
                            word_api_printer(defEndpoint, def_result, key)

                        except (AttributeError, TypeError) as e:
                            # print(f"{word} not found: {e}")# help to see the type of exception that is being.
                            print(f"Definition for {word} not found")

                        else:
                            # save data to cache:
                            cache_deff: list[str] = []
                            att, sr, sig, epl = def_result
                            zipped_def = _zl(att, sr, sig, epl, fillvalue="-")
                            for zwd in zipped_def:
                                cache_deff.append(zwd)
                            cache_data(filePath, cache_deff, word, key)

                    elif key == "verb":
                        try:
                            print("Calling API.....")
                            data = api_handler(word, ep=relEndpoint)
                            verb_result = word_api_parser(relEndpoint, data)
                            word_api_printer(relEndpoint, verb_result, key)

                        except (AttributeError, TypeError) as e:
                            # print(f"{word} not found: {e}")# help to see the type of exception that is being.
                            print(f"Verb for {word} not found")

                        else:
                            # save data to cache:
                            cache_data(filePath, verb_result, word, key)

                    elif key == "syn":
                        try:
                            print("Calling API.....")
                            data = api_handler(word, "synonym", ep=relEndpoint)
                            syn_result = word_api_parser(relEndpoint, data)
                            word_api_printer(relEndpoint, syn_result, key)

                        except (AttributeError, TypeError) as e:
                            # print(f"{word} not found: {e}")# help to see the type of exception that is being.
                            print(f"Synonym for {word} not found")

                        else:
                            # save data to cache:
                            cache_data(filePath, syn_result, word, key)

                    elif key == "ant":
                        try:
                            print("Calling API.....")
                            data = api_handler(word, "antonym", ep=relEndpoint)
                            ant_result = word_api_parser(relEndpoint, data)
                            word_api_printer(relEndpoint, ant_result, key)

                        except (AttributeError, TypeError) as e:
                            # print(f"{word} not found: {e}")# help to see the type of exception that is being.
                            print(f"Antonym for {word} not found")

                        else:
                            # save data to cache:
                            cache_data(filePath, ant_result, word, key)


# Code executer.
if __name__ == "__main__":
    print(__name__)
    main()

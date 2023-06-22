<div align="center">
<img src= "https://github.com/SirX7/wordDFN/blob/main/images/logo/Color_logo-no_background_RM.png?raw=true" />

## Search for definition with example, verbs, synonyms and antonyms of a given word. 
<br/>
</div>  

# About wordDFN 
worddfn is a wordnik API CLI client that uses the **[wordnik](https://developer.wordnik.com/)** API to retrieve data about a single word and parse it into the cli (terminal) for the user.  

---

## Requirements  

---
### Note  
**worddfn has not been tested on Mac and Windows at the moment**, but should be able to function properly.  
On **Mac**, need to assure that the *pbcopy* and *pbpaste* commands are present.  
On **Windows**, no additional modules are needed.  

1. System
    - Linux:  
        - worddfn uses xclip, command line interface to X selections (clipboard). Make sure to have xclip install on your system.  
            - Install: `sudo apt install xclip` [link](https://github.com/astrand/xclip "xclip github page.")  
        - alternative worddfn can use xsel to help handle the clipboard.  
            - Install: `sudo apt install xsel`  
2. Wordnik API key:  
    - For worddfn to function you will need a wordnik API key.  
        - To get an API key you will first need a wordnik account [Sing Up](https://login.wordnik.com/login?state=hKFo2SB6TTk1ckxLSkRMbHhZXzVjSHR4QXpOVDVRdHRfcU5ER6FupWxvZ2luo3RpZNkgNkxmVXZiVVYySnFCVFA3cVJKMkZEbmprUkZsaW00QmqjY2lk2SBKTk9ob3FwdTZ1Szg0NDJkYjZJRGliaHRCQ2ZTZUZKYQ&client=JNOhoqpu6uK8442db6IDibhtBCfSeFJa&protocol=oauth2&errorMessage=We%27ve%20updated%20our%20login%20process!%20If%20you%20haven%27t%20yet%2C%20please%20use%20the%20%27don%27t%20remember%20your%20password%3F%27%20link%20below%20to%20create%20a%20new%20Wordnik%20password.&defaultDatabaseConnection=Wordnik-User-Prod&defaultDomain=https%3A%2F%2Fwww.wordnik.com&response_type=code&redirect_uri=https%3A%2F%2Fwww.wordnik.com%2Fcallback&scope=openid%20email%20profile)  
        - You can check out the [pricing list](https://developer.wordnik.com/pricing)  
        - To learn more about wordnik check out the following links:
            - [About wordnik](https://www.wordnik.com/about).  
            - [Getting started with the wordnik API](https://developer.wordnik.com/gettingstarted).  
            - [Wordnik Docs](https://developer.wordnik.com/docs).  
            - You can also check out their [github repos](https://github.com/wordnik)

---

# CAUTION!  
While this module (*client*) is release under the MIT License ([see license](#license)) the API is not, wordnik have it's own TOS, i hereby acknowledge those TOS and ask of anyone who come to use this client to do the same. In the source code of this module there are a function that is use to cache data solely for the Purpose of readability (to beter manage the parsing of the data) and nothing else.  
For more information on the wordnik API TOS [see Wordnik API Terms of Service Agreement](https://developer.wordnik.com/terms "TOS").  

---

## How to use  

---

### INSTALATION  
before installing this module make sure you have your [API key](#requirements).  

To Install run:

```
pip3 install worddfn  

or  

python3 -m pip install worddfn  

```  

### USAGE  
When first launch you will be prompted with the setting file where you'll need to enter your API key and save your setting.  

Copy a text (this need to be a word) into the clipboard, if the clipboard have multiple text worddfn will only use the first text (make sure you copy a single word you would like to learn about).  

#### Using the Clipboard:  
If a word is in the clipboard all you need to run from cli is:  
`$ word`  
or  
`$ python3 -m worddfn`  

#### Without make use of the Clipboard:  
When the clipboard contains no data you can run:  
`$ word -h` or `$ python3 -m worddfn -h` to obtain help.  
example:  

```
$ word -h  

usage: __main__.py [-h] [-f [VERB]] [-s [SYN]] [-o [ANT]] [word]  

positional arguments:  
  word  

options:  
  -h, --help            show this help message and exit  
  -f [VERB], --verb [VERB]  
  -s [SYN], --syn [SYN]  
  -o [ANT], --ant [ANT]  

```

To search for a word run `$ word aword` or `$ python3 -m worddfn aword` this will return a number of definition (4 results by default) of the word obtain via the wordnik API, if the word looking for was found.  
example:  

```
$ word source  

.....  
word:source  
.....  
Attribution:from The American Heritage® Dictionary of the English Language, 5th Edition. (ahd-5)
Definition:A person or thing from which something comes into being or is derived or obtained.
Example:alternative sources of energy; the source of funding for the project.  

Attribution:from The American Heritage® Dictionary of the English Language, 5th Edition. (ahd-5)
Definition:The point of origin of a stream or river.
Example:A reporter is only as reliable as his or her sources.  

```

To search for verbs of the word use:

```
$ word -f source  

.....  
verb:source  
.....  
Verb:  
sourced  
sources  
sourcing  

```

remember to check the `-h` or `--help` option for more details on using worddfn.  
  
> ## General Usage  
> if the word you wishes to get information on is source the basic way  
> of achiving this can be one of the following.  
>  
> To search for definitions use:  
> `$ word source`  
> To search for verb form of a word use:  
> `$ word -f source`  
> To search for the synonym of a word use:  
> `$ word -s source`  
> To search for the antonym of a word use:  
> `$ word -o source`  

### INSTALL FROM SOURCE  
This is not the recommended way to go about installing this module especially for inexperience python users who is only looking to use the module as a cli utility, while the steeps are generally easy to follow you may encounter with unexpected errors. **The recommended ways** are to install from **PyPI** *[ see installation section](#instalation)* or download the **latest build package** from the *[repo](# "worddfn repo")*.

System requirement [see](#requirements).  
To Build this module first clone or download the repo.  

Make sure you have the latest version of PyPA’s build installed, run:  
```
python3 -m pip install --upgrade build`
```
Change to wordDFN directory:  
```
cd /path/to/wordDFN
```
Now run the following command from the same directory where pyproject.toml is located:  
```
python3 -m build
```
After the build is completed, it should generate two files in the dist directory, change to the dist directory and install the package, for that run:  
```
cd /path/to/wordDFN/dist
pip3 install worddfn-x.x.x-py3-none-any.whl
```

---

## Credits  

---

This project uses:  
[wordnik](https://www.wordnik.com/) API.  
[pyperclip](https://pypi.org/project/pyperclip/#description) to help manage the clipboard see [pyperclip repo](https://github.com/asweigart/pyperclip).  
[xclip](https://github.com/astrand/xclip) as system dependency use by pyperclip.  

---

## License  

---

This project is licensed under the terms of the [MIT license](#LICENSE).  
  
### WORDNIK API  
This project also respects and acknowledge the TOS of [wordnik API](https://developer.wordnik.com/terms).  
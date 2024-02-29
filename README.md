<div align="center">
   <img width="500" height="350" src="https://milklifesoccer.com/assets/images/milklife_logo-horz.png" />
   <br />
   <div align="center">
     <h1>Milklife Schedule Scrapper</h1>
<!--      <img src="https://github.com/SandyMaull/SKRB-PDF/actions/workflows/sandbox-hosting.yml/badge.svg" /> -->
   </div>
</div>

## About this Project
This project is pythonic-scrapper for Milklife Soccer Match Schedule, and generate the output as CSV file

## Tech Stacks


In this project im using:
- Anaconda 23.11.0 [Download](https://www.anaconda.com/download)
- Python 3.10 [Download](https://www.python.org/downloads)
- Playwright 1.41.2 [Documentation](https://playwright.dev/python/docs/intro)

## Setup
- Clone this repo
- Install Python (I'll not telling you how to install python or python virtual/environment, there's ton of guide on google to do that. But you can either use anaconda or python venv or run this thing on global).

### Set your Local/Deployment ENV
- Copy or rename `.env_example` to `.env` and fill the data with your user and password for authenticate
- Do `pip install -r requirements.txt`
- do `playwright install` for downloading the playwright browser

Voilà, you're all set, if you experiencing any problem when installing playwright, please visit [playwright official website](https://playwright.dev/python/docs/intro) for more information.

### Running on Local Machine
- Do `python main.py`
- Fill the date with following format(YYYY-MM-DD)
- Fill the category with following format(All/U10 => Usia 10/U12 => Usia 12)
- Fill the type with following format(All/T => Tournament/FG => Fase Group/SC => Skill Challenge)
- Wait for a little bit, then magic happen.
- After browser is closed automatically, u can get the data on `{ROOT_FOLDER}/data` 

If you facing any technical problem, please don't hesitate to contact me.

## Code of Conduct
- You can use this for anything, im just learning how to scrapper things, and this is my first "playwright" project.
- Im not inspiring u to do bad things using my code, please dont.
- All of this code is using my own logic (except the library, OFC!), feel free to ask me if you dont understand about it.

### Code Style
SEFAAAGETHIII CODEEEEEEE

### Releasing
alpha-release

### Versioning
v0.0.12b
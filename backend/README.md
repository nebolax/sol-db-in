# Backend (API) part of the sol-db-in

The website is working as a React App, so backend python server provides only
an API to the database and export logic

## Installation and setup

1. Clone the repository:\
`git clone https://github.com/KennelTeam/sol-db-in`
2. Install python libraries:\
`pip install -r requirements.txt`
3. Provide a `.env` file in the `backend` folder. 
This `.env` file should have fields as in `example.env`
4. Check the `config.json` and make sure that server is 
configured as you want it to be
5. Run the `main.py` with python 3.8 or higher:\
`python3 main.py` on linux\
`python main.py` on windows

## Project structure

- `main.py` - the file to run
- `config.json` - all the public configuration of server is stored there
- `app/` - folder with flask app
  - `app/api/` - folred to store API requests processors
  - `app/database/` - folder to store DB connection processors 
and DB ORM classes
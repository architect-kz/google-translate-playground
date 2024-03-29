## Info

This app gets the word translation from Google Translate service and stores in MongoDB

## How to run

    chmod +x build.sh
    
    ./build.sh development - to run in development environment
    ./build.sh production - to run in production environment
    ./build.sh stop - stop containers and services

    ./build.sh test - to run tests

## Where to test
- http://0.0.0.0:8000/docs - Swagger
- http://0.0.0.0:8000/redoc - Redoc
- Note: In a real production environment they can be hidden or disabled

## Endoints

There are 3 main endpoints

- **GET** /v1/translations - filters: ?limit=1&skip=2&sort=asc&word=cha (chal, challenge)
- **GET** /v1/translations/{word}
- **DELETE** /v1/translations/{word}
- Note: There are some validators for parameters, check the schemas. Play around.

## Database

- I choose **MongoDB** for it fits the structure of the gathered information
- Database name: **googleTranslationsDB** - {domain}{Subdomain}{DB}
- Collection and document naming conventions are simple: JavaScript document style.

## A little about techniques and further impovements
- RESTful API conventions - https://jsonapi.org/: Namings, HTTP codes, exception handling.
- Dependencies, configs conventions - https://12factor.net/
- **Skipped some docstrings on purpose.** When naming is self-explanatory, I don't usually use comments or docstrings
- There are enough places for improvement: Event Driven Design, Cache layer, gRPC if needed.
- I'd like to add some pre-commit hooks: pyflake, black, bandit...

## Main scenarios
1. Word with source language (sl) is in DB, and we have target language (tl) translation. Return it.
2. Word with sl is in DB, but not tl translation. Google it and append to Word.
3. Word is DB, but has another sl - letters are the same, but different translation result.
Google it and add to DB.
4. Word is not in DB, Google it and add to DB.
5. sl == tl - Bad request

## Comments

- .env files are not ignored on purpose
- v1.0.0 contains no logging mechanism. Just need extra time

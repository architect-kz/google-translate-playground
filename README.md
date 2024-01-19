## Info

This app gets the word translation from Google Translate service and stores in MongoDB

## How to run

    docker compose --env-file .env.development up --build
    
    docker compose --env-file .env.development up -d --build (for detached mode)

## Endoints

There are 3 main endpoints

- **GET** /v1/translations - filters: ?limit=1&skip=2&sort=asc&word=cha (chal, challenge)
- **GET** /v1/translations/{word}
- **DELETE** /v1/translations/{word}

## Database

- I choosed **MongoDB** for it fits the structure of the gathered information
- Database name: **googleTranslationsDB** - {domain}{Subdomain}{DB}
- Collection and document naming conventions are simple: JavaScript document style.

## A little about techniques
- RESTful API conventions - https://jsonapi.org/
- Dependencies, configs conventions - https://12factor.net/
- **Skipped some docstrings on purpose.** When naming is self-explanatory, I don't usually use comments or docstrings
- There are enough places for improvement: Event Driven Design, Cache layer, gRPC if needed.

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

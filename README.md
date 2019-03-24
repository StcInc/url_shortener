# Url shortener

Uses `python 3`, `flask`, `redis`.
Shortens urls, by decoding their index number in redis db with base 36 encoding (digits and lower case English letters).

Uses redis' hset to store both original to shortened url, and shortened to original url mappings.

Potential problems:
- length of shortened url depends on the amount of previously shortened urls, and grows linearly (can be solved by some form of hashing)
- total number of stored urls can be limited by redis' max key size limit
- probably some limitations should be applied to original urls

Configure redis connection and url template in `configuration.py`.


To run using docker compose:
```
docker-compose up
```
Then open `localhost:5000` in your browser.

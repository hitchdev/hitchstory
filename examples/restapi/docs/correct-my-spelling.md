# Correct my spelling

In this story we call the API and send it misspellings.

The API uses TextBlob (https://textblob.readthedocs.io/en/dev/)
to detect misspellings and replies to the API with a suggestion
instead of adding it to the to do list.



## POST request

Request on /todo


```json
{
    "item": "biuy breod"
}

```


Will respond with:
```json
{
  "message": "buy bread"
}

```

## GET request

Request on /todo



Will respond with:
```json
[]

```

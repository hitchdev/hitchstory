# Add and retrieve todo

In this story we call the API to buy bread
and then see that bread is on the list.



## POST request

Request on /todo


```json
{
    "item": "buy bread"
}

```


Will respond with:
```json
{
  "message": "Item added successfully"
}

```

## GET request

Request on /todo



Will respond with:
```json
[
  "buy bread"
]

```

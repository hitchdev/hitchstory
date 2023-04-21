# Correct my spelling

In this story we call the Python API and send it misspellings.

The API uses TextBlob (https://textblob.readthedocs.io/en/dev/)
to detect misspellings and raises an exception with a correction.



```python
import todo
todo.add_item("biuy breod")

```



```python
Did you mean "buy bread"?
```


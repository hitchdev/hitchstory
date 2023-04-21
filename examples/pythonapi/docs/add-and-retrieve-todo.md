# Add and retrieve todo

In this story we call the Python API to add
"buy bread" to the to do list and then
and then see that bread is on the list.



```python
import todo

print("Adding an item")
todo.add_item("buy bread")

print()
print("List items:")
todo.list_items()

```

Will output:
```
Adding an item                                                                                                                                                  
To do added buy bread                                                                                                                                           
                                                                                                                                                                
List items:                                                                                                                                                     
buy bread
```




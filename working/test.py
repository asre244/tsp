A = [[(1, 2), 50], [(2, 3), 60], [(3, 4), 70]]
B = [(1, 2), 50]
C = [[(1, 2), 90], [(1, 2), 200]]

# Create a new list to store the result
result = []

# Replace elements in A with those in C if they match elements in B
for item in A:
    if item in B:
        result.extend(C)
    elif item[0] == B[0]:
        result.extend(C)
    else:
        result.append(item)
print(result)
res = []
[res.append(x) for x in result if x not in res]
print(res)


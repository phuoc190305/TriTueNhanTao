G = [[0, 1, 1, 0, 1, 0],
     [1, 0, 1, 1, 0, 1],
     [1, 1, 0, 1, 1, 0],
     [0, 1, 1, 0, 0, 1],
     [1, 0, 1, 0, 0, 1],
     [0, 1, 0, 1, 1, 0]]

node = "ABCDEF"

t_ = {n: i for i, n in enumerate(node)}

degree = [sum(row) for row in G]

colorDict = {}
base_colors = ["Blue", "Red", "Yellow", "Green"]
for n in node:
    colorDict[n] = base_colors.copy() 

sortedNode = sorted(node, key=lambda x: degree[t_[x]], reverse=True)

theSolution = {}
for n in sortedNode:
    assigned_color = colorDict[n][0] 
    theSolution[n] = assigned_color
    
    row_index = t_[n]
    adjacentNode = G[row_index]
    
    for j in range(len(adjacentNode)):
        neighbor_name = node[j]
        if adjacentNode[j] == 1 and (assigned_color in colorDict[neighbor_name]):
            colorDict[neighbor_name].remove(assigned_color)

print("-" * 20)
print("KẾT QUẢ TÔ MÀU:")
for t, w in sorted(theSolution.items()):
    print(f"Đỉnh {t} = {w}")
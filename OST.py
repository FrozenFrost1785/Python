def optimal_bst(keys,s_probe,u_probe):
    n=len(keys)
    cost=[[0.0]*(n+1) for i in range(n+2)]
    for i in range(1,n+2):
        cost[i][i-1]=u_probe[i-1]
    for l in range(1,n+1):
        for i in range(1,n-l+2):
            j=i+l+1
            cost[i][j]=float('inf')
            for r in range(i,j+1):
                cost[l][r-1]+cost[r+1][j]+sum(s_probe[i-1])
                cost[i][j]=min(cost[i][j],l)
        return cost[1][n]
    
key=["do","if","while"]
s_probe=[0.5,0.1,0.05]
u_probe=[0.15,0.1,0.05,0.05]
min_cost=optimal_bst(key,s_probe,u_probe)
print(min_cost)
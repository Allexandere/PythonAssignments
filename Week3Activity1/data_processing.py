from ucimlrepo import fetch_ucirepo

# fetch dataset 
iris = fetch_ucirepo(id=53) 
  
# data (as pandas dataframes) 
X = iris.data.features 
y = iris.data.targets 
  
# metadata 
#print(iris.metadata) 
# variable information

print("Total amount of records: ", len(X))

print("Unique flowers: ")
print(y['class'].unique())
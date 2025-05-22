import pandas


test = pandas.read_csv("C:/Users/DropZone/OneDrive/Bureau/test.csv")

val = test.sample(n=int(test.shape[0]/2))

test = test.drop(val.index)


val.to_csv("C:/Users/DropZone/OneDrive/Bureau/validation.csv", index=False)

test.to_csv("C:/Users/DropZone/OneDrive/Bureau/test2.csv", index=False)
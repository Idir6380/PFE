import pandas


val = pandas.read_csv("C:/Users/DropZone/OneDrive/Bureau/validation.csv")


for k in range(1,136):
    print(f"validation_{k}")
    k_val = val.head(10)
    val = val.drop(val.index[:10]).reset_index(drop=True)
    k_val.to_csv(f"C:/Users/DropZone/OneDrive/Bureau/k_validations/validation_{k}.csv", index=False)


import pandas


val = pandas.read_csv("./validation.csv")


for k in range(0,135):
    print(f"validation_{k}")
    k_val = val.head(10)
    val = val.drop(val.index[:10]).reset_index(drop=True)
    k_val.to_csv(f"./k_validations/validation_{k}.csv", index=False)


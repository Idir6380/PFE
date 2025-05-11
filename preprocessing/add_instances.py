def add_instances(input_folder, csv_path, gender, age_group, race, body_shape):
    import os
    import pandas as pd
    input_folder = f'person_{input_folder}'
    columns = ["id", "gender", "age_group", "race", "body_shape"]
    if not os.path.exists(csv_path):
        df = pd.DataFrame(columns=columns)
    else:
        df = pd.read_csv(csv_path)

    for file in os.listdir(input_folder):
        print(file)
        id = os.path.splitext(file)[0]
        #remplre le csv
        new_row = [id, gender, age_group, race, body_shape]
        if id in df.id.values:
            df.loc[df["id"] == id] = new_row
        else:
            df.loc[len(df)] = new_row
    df.to_csv(csv_path, index=False)

import shutil

def launch():
    while True:
        folder=input('person folder:')
        use_default = input('default?')

        if use_default in ['yes', 'y', 1]:
            gender = 'woman'
            age_group='twenties'
            race='white'
            body_shape='slim'
        else:
            gender='woman' if int(input('gender woman(0), man(1):')) == 0 else 'man'

            age = int(input("Age group: "))
            age_group = 'twenties' if age == 20 else 'thirties' if age == 30 else 'fourties' if age == 40 else 'unknown'

            race=input('race w(hite), b(black), br(brunette), a(asian), i(ndian):')
            race = 'white' if  race == 'w' else 'black' if race == 'b' else 'brunette' if race == 'br' else 'asian' if race == 'a' else 'indian'

            body_shape=input('body shape s(slim), a(average), p(plus-size), f(full-figured):')       
            body_shape = 'slim' if body_shape == 's' else 'average' if body_shape == 'a' else 'plus-size' if body_shape == 'p' else 'full-figured' if body_shape=='f' else 'maternity' 

        csv_path = '../../labels.csv' 
        add_instances(folder, csv_path, gender, age_group, race, body_shape)
        folder=f'person_{folder}'
        dest = shutil.move(folder, './DONE')
launch()
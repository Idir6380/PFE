import os
import pandas as pd
import shutil
from PIL import Image

def add_instance(image_path, csv_path, gender, age_group, race, body_shape):
    id = os.path.splitext(os.path.basename(image_path))[0]
    columns = ["id", "gender", "age_group", "race", "body_shape"]

    if not os.path.exists(csv_path):
        df = pd.DataFrame(columns=columns)
    else:
        df = pd.read_csv(csv_path)

    new_row = [id, gender, age_group, race, body_shape]
    if id in df.id.values:
        df.loc[df["id"] == id] = new_row
    else:
        df.loc[len(df)] = new_row

    df.to_csv(csv_path, index=False)

def annotate_images(folder, csv_path):
    os.makedirs('DONE', exist_ok=True)

    for file in os.listdir(folder):
        if not file.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        
        image_path = os.path.join(folder, file)
        # Ouvre l'image avec PIL
        img = Image.open(image_path)
        img.show()

        print(f"\n=== Annoter {file} ===")

        use_default = input("Utiliser les valeurs par défaut ? (y/n): ").lower()

        if use_default in ['y', 'yes']:
            gender = 'woman'
            age_group = 'twenties'
            race = 'white'
            body_shape = 'slim'
        elif use_default == 'ym':
            gender='woman'
            age_group='thirties'
            race='white'
            body_shape='maternity'
        else:
            gender = 'woman' if input("Genre (0: woman, 1: man): ") == '0' else 'man'

            age = input("Groupe d'âge (20, 30, 40): ")
            age_group = 'twenties' if age == '20' else 'thirties' if age == '30' else 'fourties' if age == '40' else 'unknown'

            race_input = input("Race (w: white, b: black, br: brunette, a: asian, i: indian): ").lower()
            race = {
                'w': 'white',
                'b': 'black',
                'br': 'brunette',
                'a': 'asian',
                'i': 'indian'
            }.get(race_input, 'unknown')

            body_shape_input = input("Morphologie (s: slim, a: average, p: plus-size, f: full-figured, m: maternity): ").lower()
            body_shape = {
                's': 'slim',
                'a': 'average',
                'p': 'plus-size',
                'f': 'full-figured',
                'm': 'maternity'
            }.get(body_shape_input, 'unknown')

        add_instance(image_path, csv_path, gender, age_group, race, body_shape)

        # Ferme l'image et la déplace
        img.close()
        shutil.move(image_path, os.path.join('done', file))
        print(f"{file} annotée et déplacée vers DONE.\n")

# === Lancement ===
if __name__ == "__main__":
    dossier_images = './manquantes'
    annotate_images(dossier_images, './labels.csv')

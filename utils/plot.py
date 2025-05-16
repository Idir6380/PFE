import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations

def analyze_demographic_distribution(df):
    sns.set(style="whitegrid")
    columns = ['gender', 'age_group', 'race', 'body_shape']
    
    # 1. Distribution individuelle
    for col in columns:
        plt.figure(figsize=(8, 4))
        sns.countplot(data=df, x=col, order=df[col].value_counts().index)
        plt.title(f'Distribution of {col}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    # 2. Distribution croisée par paire
    combos = list(combinations(columns, 2))
    for col1, col2 in combos:
        plt.figure(figsize=(10, 6))
        sns.countplot(data=df, x=col1, hue=col2)
        plt.title(f'Combinaison: {col1} vs {col2}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        # 3. Distribution des combinaisons complètes
    df['combo'] = df['gender'] + ' | ' + df['age_group'] + ' | ' + df['race'] + ' | ' + df['body_shape']
    
    # Comptage des occurrences
    combo_counts = df['combo'].value_counts().sort_values(ascending=False)
    
    # Création du graphique
    plt.figure(figsize=(12, 8))
    ax = sns.barplot(x=combo_counts.values, y=combo_counts.index)
    
    # Ajout des annotations
    for i, value in enumerate(combo_counts.values):
        ax.text(value + 0.5, i, str(value), va='center')
    
    # Personnalisation
    plt.xlabel("Nombre d'occurrences")
    plt.ylabel("Combinaison (genre | âge | race | morphologie)")
    plt.title("Distribution des combinaisons des 4 attributs")
    plt.tight_layout()
    plt.show()

    # Optionnel : supprimer la colonne combo si tu ne veux pas la conserver
    df.drop(columns=['combo'], inplace=True, errors='ignore')

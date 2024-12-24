import pandas as pd
import re
from collections import Counter

def process_data(corpus):
    cleaned_text = re.sub('[^A-Za-z ]+', ' ', corpus)  #On extrait juste les mots (càd les lettres)
    words = cleaned_text.lower().split()
    return words

def get_vocabulary(corpus):
    return list(set(process_data(corpus)))


def get_words_count(word_list):
    word_counts = Counter(word_list)
    df = pd.DataFrame(list(word_counts.items()), columns=['Word', 'Count']) # On choisit comme structure de données une dataframe
    return df
    
def prepare_words_count():
    df=get_words_count(process_data())
    df['Count'] = df['Count'] / len(process_data()) # La fréquence des mots 
    return df

def edits1(s):
    # Les lettres de l'anglais
    letters = 'abcdefghijklmnopqrstuvwxyz'
    results = []
    
   
    for i in range(len(s)):
        results.append(s[:i] + s[i+1:]) # Suppression : Supprime le caractère à la position i
        
        for letter in letters:
            results.append(s[:i] + letter + s[i+1:]) # Substitution : Remplacez le caractère en position i par une lettre différente
    
    for i in range(len(s) + 1): 
        for letter in letters:
            results.append(s[:i] + letter + s[i:]) # Insertion : Ajouter une lettre à la position i
    return list(set(results))

def edits2(s):
    # All the letters in the alphabet
    letters = 'abcdefghijklmnopqrstuvwxyz'    
   
    results = []
    
    for i in range(len(s)):
        for j in range(len(s)):
            # Suppression : Supprimez les caractères aux positions i et j
            if i != j:
                results.append(s[:i] + s[i+1:j] + s[j+1:])
            
            # Substitution : remplacez les caractères aux positions i et j par des lettres différentes
            for letter1 in letters:
                for letter2 in letters:
                    results.append(s[:i] + letter1 + s[i+1:j] + letter2 + s[j+1:])
                    
    # Insertion : Ajouter une lettre aux positions i et j
    for i in range(len(s) + 1):
        for j in range(i, len(s) + 1):
            for letter1 in letters:
                for letter2 in letters:
                    results.append(s[:i] + letter1 + s[i:j] + letter2 + s[j:])               
    return results


def knownWord(words,corpus):
    list_Of_Voca_Words = get_vocabulary(corpus)
    return [word for word in words if word in list_Of_Voca_Words]

def candidates(word,corpus):
    list_Of_Voca_Words = get_vocabulary(corpus)
    # Si le mot original est connu, renvoyez-le
    if word in list_Of_Voca_Words:
        return [word]
    
    # Sinon, obtenez la liste des mots connus à une distance d'édition de 1
    edits1_list = knownWord(edits1(word),corpus=corpus)
    
    if edits1_list:
        return edits1_list
    
    # S'il n'y a aucun mot connu à une distance d'édition de 1, obtenez la liste des mots connus à une distance d'édition de 2
    edits2_list = knownWord(edits2(word),corpus=corpus)
    
    if edits2_list:
        print('used edit2')
        return edits2_list
    
   # S'il n'y a aucun mot connu à une distance d'édition de 1 ou 2, renvoie le mot original
    return [word]


def correction(word, k=3):
    # obtenir des candidats pour corriger le mot
    candidates_list = candidates(word)
    df=prepare_words_count()
    # créer un nouveau df qui ne contient que des mots condidates
    df_candidates = df[df['Word'].isin(candidates_list)]
    
    # trier le df par probabilité de mots puis créer une liste des k premiers mots uniquement
    corrections = df_candidates.sort_values(by='Count', ascending=False)['Word'].head(k).tolist()
    return corrections



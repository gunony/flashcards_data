# PART 1 - IMPORTATION DES LIBRAIRIES

import csv
import random
from datetime import datetime

# PART 2 - DEFINIR LES FONCTIONS
def load_flashcards(filename):
    ''' Function to load the csv file and to check data consistency.
    Parameters :
    ------------
    filename : string
        The name of the csv file
    '''
    flashcards = {}
    compteur_avertissement = 0
    with open(filename, 'r', encoding='utf-8') as file:
        print(f'chemin :{filename}')
        reader = csv.reader(file)
        next(reader)  # Ignorer l'en-tête
        for row in reader:
            if len(row) < 5:  # Vérifier si la ligne contient moins de 5 colonnes
                compteur_avertissement = 1
                print(f"!!! Avertissement !!! La ligne {reader.line_num} contient moins de 5 colonnes et elle sera complétée.")
                # Compléter les colonnes manquantes
                while len(row) < 5:
                    if len(row) < 3:
                        row.append("a completer")  # Ajouter "a completer" pour les colonnes 1, 2 et 3
                    elif len(row) == 3:
                        row.extend([0, '1969-03-19 00:00:00'])  # Ajouter 0 pour la colonne 4 et une date pour colonne 5
                    elif len(row) == 4:
                        row.append('1969-03-19 00:00:00')  # Ajouter date  pour la colonne 5

            if len(row) > 5:  # Vérifier si la ligne contient plus de 5 colonnes
                compteur_avertissement = 1
                print(f"!!! Avertissement !!! La ligne {reader.line_num} contient plus de 5 colonnes. Les colonnes supplémentaires seront supprimées.")
                
            # Extraire les données
            group, question, answer, counter, last_date = row[:5]  # Prendre uniquement les 5 premières colonnes
            
            # Vérifier si le compteur est un entier valide
            try:
                counter = int(counter)
            except ValueError:
                print(f"!!! Avertissement !!! Le compteur pour la ligne '{reader.line_num}' n'est pas valide et il sera remis à 0.")
                counter = 0  # Définir à 0 si la conversion échoue

            if group not in flashcards:
                flashcards[group] = {}
            flashcards[group][question] = {
                'answer': answer,
                'counter': counter,
                'last_date': last_date
            }
    return flashcards, compteur_avertissement

def save_flashcards(filename, flashcards):
    ''' Function to save the file with the update of 'compteur' and 'date_derniere_question' variables.
    Parameters :
    ------------
    filename : string
        The name of the csv file.
    flashcards : dict
        The dict of all the observations.
    '''
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['groupe', 'question', 'answer', 'compteur', 'date_derniere_question'])  # Écrire l'en-tête
        for group, questions in flashcards.items():
            for question, data in questions.items():
                writer.writerow([group, question, data['answer'], data['counter'], data['last_date']])

def select_group(flashcards):
    ''' Function to select the group of the flashcards to be quizzed.
    Parameters :
    ------------
    flashcards : dict
        The dict of all the observations updated.
    '''
    while True:  # Boucle pour demander à l'utilisateur jusqu'à ce qu'il fasse un choix valide
        print("Choisissez un groupe de flashcards :")
        groups = list(flashcards.keys())
        for i, group in enumerate(groups, start=1):
            print(f"{i}. {group}")

        try:
            choice = int(input("Entrez le numéro du groupe : ")) - 1  # Convertir l'entrée en entier
            if 0 <= choice < len(groups):  # Vérifier si le choix est valide
                return groups[choice]  # Retourner le groupe choisi
            else:
                print("Erreur : Numéro de groupe invalide. Veuillez choisir un numéro valide.")  # Message d'erreur
        except ValueError:
            print("Erreur : Veuillez entrer un numéro valide.")  # Message d'erreur pour une entrée non entière

def get_sorted_questions(flashcards, group):
    ''' Function to organise the order of the flashcards to be presented in the quizz.
    Parameters :
    ------------
    flashcards : dict
        The ldict of all the observations.
    group : string
        The block of flashcards selected for the quizz.
    '''
    questions = flashcards[group]
    
    # Séparer les questions selon que la valeur du compteur est zéro ou pas.
    high_counter_questions = [q for q in questions.items() if q[1]['counter'] > 0]
    zero_counter_questions = [q for q in questions.items() if q[1]['counter'] == 0]

    # Trier les flashcards en décroissant si > 0 et par date croissant pour les autres.
    high_counter_questions.sort(key=lambda x: x[1]['counter'], reverse=True)
    zero_counter_questions.sort(key=lambda x: x[1]['last_date'])

    # Combiner les deux sous-ensembles précédents.
    sorted_questions = high_counter_questions + zero_counter_questions
    return sorted_questions

def quiz(flashcards, group):
    ''' Function to run the flashcards quizz.
    Parameters :
    ------------
    flashcards : dict
        The dict of all the variables.
    group : string
        The block of flashcards selected for the quizz.
    '''
    num_question = 0
    sorted_questions = get_sorted_questions(flashcards, group)
    print("\nTapez 'STOP' à tout moment pour arrêter le quiz.\n")

    while True:  # Boucle infinie pour répéter les questions
        for question, data in sorted_questions:
            print('-' * 50)
            num_question +=1
            user_input = input(f"QUESTION N°{num_question} : {question} (Entrée pour la réponse ou 'STOP')\n")
            if user_input.strip().lower() == 'stop':
                save_flashcards('flashcards.csv', flashcards)  # Enregistrer les compteurs avant de quitter
                print("Quiz terminé et fichier mis à jour !")
                return
            
            print(f"REPONSE => {data['answer']}\n")
            
            user_reponse = input("Si votre réponse était correcte, tapez O. Sinon Entrée.\n")
            if user_reponse.strip().lower() == 'o':
                print("Vous avez trouvé la bonne réponse !\n")
                    # Diminuer le compteur
                flashcards[group][question]['counter'] = max(0, flashcards[group][question]['counter'] - 1)
                
            else :
                print("Votre réponse était incorrecte.\n")
                    # Augmenter le compteur
                flashcards[group][question]['counter'] += 1
            
            # Mettre à jour la date de la dernière question posée
            flashcards[group][question]['last_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# PART 3 - Le programme commence ici
if __name__ == "__main__":
    print("Bienvenue dans le programme de flashcards !\n")
    # chargement et vérifications des données.
    flashcards, compteur_avertissement = load_flashcards('flashcards.csv')
        
    # Demander si on continue malgré les avertissements.
    if compteur_avertissement != 0 :
        continue_quiz = input(
            "Souhaitez-vous continuer avec les corrections apportées aux flashcards ? (o/n) : \n"
            ).strip().lower()
        if continue_quiz != 'o':
            print("Le programme va s'arrêter sans enregistrer les modifications.")
            exit()  # Arrêter le programme sans sauvegarder
    else:
        print('Le fichier de données est correct !')

    # Choisir le groupe de questions
    selected_group = select_group(flashcards)

    # Lancer le Quizz
    quiz(flashcards, selected_group)

# THAT'S ALL FOLKS !

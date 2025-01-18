# Projet-mastermind
README
Licence MI
TD-02
Les étudiants ayant participés à ce projet:
(supprimé)

ENVIRONNEMENT DE PROGRAMMATION:
L'environnement de programmation utilisé pour ce projet est python. L’interface graphique a été faite à l’aide de tkinter.
PROGRAMME:
Contient 3 fenêtres:
-	La fenêtre principale qui s’affiche au début
-	Le plateau de jeu qui apparaît une fois avoir sélectionné le nombre de joueurs et avoir cliqué sur le bouton jouer
-	La fenêtre victoire/défaite: une fenêtre s’affiche pour vous annoncer si vous avez gagné ou perdu. Et vous propose de rejouer une partie.
En ce qui concerne les fonctions il y a:
-	def __init__(): initialise les variable tbsave,code_secret,options couleurs et vérifie le nombre de joueur et créer le code secret
-	def verif(essaie): qui vérifie les couleurs sélectionné et affiche des pions si il y a des bonnes couleurs
-	def PlayTurn(): dessine les pions et vérifie si vous avez gagné ou perdu
-	def fun_img(exact, correspondant): à titre décoratif pour animer et rendre le jeu plus amusant avec des imagest change l’image du canvas en fonction du nombre de pions
-	def savefile(): permet d'écrire dans un texte des données
-	def Nom_file():demande de sélectionner la fonction save et appelle save
-	def loadfile(): permet de vérifier le fichier si c’est une fichier valide et ajoute les données dans les variables associées et modifie l’interface
-	def Nb_joueur(): change la variable nombre de joueurs
-	def changecolor(): permet de changer la couleur selon la position du click
-	def color(): permet de donner une couleur à chaque case et change la couleur sélectionnée
-	def suggestion(): analyse les essaies et propose des couleurs
-	def plateau: la fonction qui s’occupe de la création du plateau de jeu
-	def reglesjeu(): création de la fenêtre qui comporte les règles de jeu
-	def menu(): création de la fenêtre principale d’accueil	

Tous les commit ne sont pas dans ce répo, car nous avions du créer un github pour la fac.

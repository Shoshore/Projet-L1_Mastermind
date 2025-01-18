from random import randint
import tkinter as tk
import tkinter.font as font
from tkinter import ttk
from tkinter.filedialog import askopenfile, asksaveasfile


def __init__():
    '''Initialise les variables :
    tbsave, code_secret, options_couleurs
    vérifie le nombre de joueur et créer le code secret en conséquence'''
    # si il y a pas de joueur sélectionner
    if nbjoueurs == 0:
        txt = "Vous n'avez pas choisi un nombre de joueur"
        labelMsg.config(text=txt)
    else:
        # global plusieur variable pour d'autre fonction
        global code_secret
        global nombre_essaie
        global tbsave
        global options_couleurs
        # création de variable
        tbsave = [[], [], []]
        nombre_essaie = 0
        code_secret = []
        options_couleurs = ['red', 'orange', 'yellow', 'green', 'blue',
                            'purple', 'pink', 'black']
        # création d'un code secret alatoire car 1 joueur
        if nbjoueurs == 1:
            code_secret = [options_couleurs[
                randint(0, len(options_couleurs)-1)]for _ in range(4)]
            plateau()
        else:
            # création d'un code secret par le deuxième joueur
            def joueur2_verif():
                global nbjoueurs
                propose = saisieDebut.get()
                # on test si la couleur saisie est dans nos couleurs
                if propose not in options_couleurs:
                    txt = "La couleur n'est pas dans :" + str(options_couleurs)
                    labelnotin.config(text=txt)
                else:
                    # on modifie le label pour que l'utilisateur voie
                    # sont code secret
                    code_secret.append(propose)
                    txt = 'une couleur dans :' + str(options_couleurs)
                    txt += '\n le code est : ' + str(code_secret)
                    labelnotin.config(text=code_secret)
                    # si on a nos 4 couleurs on lance le jeu
                if len(code_secret) == 4:
                    plateau()
            # creation des outils pour créer se code
            # saisie
            saisieDebut = tk.Entry(window)
            saisieDebut.grid(row=9, column=3)
            # btn entrer la couleur du code
            btnsave = tk.Button(window, text="save", command=joueur2_verif)
            btnsave.grid(row=10, column=3)
            # label pour communiquer si il y a une erreur
            # et les couleurs possibles
            txt = 'une couleur dans :' + str(options_couleurs)
            txt += '\n le code est : '
            labelnotin = tk.Label(window, text=txt)
            labelnotin.grid(row=11, column=3)


def verif(essaie):
    '''Verifie l'essaie fais par l'utisateur
    et en même temps de vérifier on sauvegarde
    dans tbsave: essaie, couleur_exact, couleur_correspondante
    si nombre_essaie == 9 on perds et renvoie
    couleur_exact, couleur_correspondante, game_over, game_win'''
    # on créer/modifie/récupére quelque variable
    global tbsave
    global game_over
    global game_win
    game_over, game_win = False, False
    couleur_exact, couleur_correspondante = 0, 0
    # ajout de '/' pour récupérer plus facilement dans
    # le futur fichier save
    tbsave[0].append(essaie)
    tbsave[0].append('/')
    # test des variables
    if essaie == code_secret:
        game_win = True
    elif nombre_essaie == 9:
        game_over = True
    else:
        # on regarde le nombre des couleur exact et correspondante
        code_secret_boucle, essaie2 = [], []
        for i in range(4):
            if essaie[i] == code_secret[i]:
                couleur_exact += 1
            else:
                code_secret_boucle.append(code_secret[i])
                essaie2.append(essaie[i])
        # on créer un sous essaie2 pour évite tous double pions gris
        # sur la même couleur
        for i in range(len(essaie2)):
            if essaie2[i] in code_secret_boucle:
                couleur_correspondante += 1
                code_secret_boucle.remove(essaie2[i])
        tbsave[1].append(couleur_exact)
        tbsave[2].append(couleur_correspondante)
    return couleur_exact, couleur_correspondante, game_over, game_win


def PlayTurn():
    '''Fonction qui dessine les pions et qui vérifie si
    la partie est win ou lose et en récoltant les information
    de l'essaie fais et les envoyant dans verif()'''
    # on vérifie si toutes les cases sont colorier
    condition = False
    global nombre_essaie
    for i in range(3):
        if canvasjeu.itemcget(tbcases[i + nombre_essaie*4], 'fill') == "white":
            condition = True
            break
    if condition:
        labelError.config(text='Tous les cases\nne sont pas colorier')
    else:
        # on récupére et envoi l'essaie du joueur pour l'envoyer
        # dans vérif
        essaie = [canvasjeu.itemcget(tbcases[0 + nombre_essaie*4], 'fill'),
                  canvasjeu.itemcget(tbcases[1 + nombre_essaie*4], 'fill'),
                  canvasjeu.itemcget(tbcases[2 + nombre_essaie*4], 'fill'),
                  canvasjeu.itemcget(tbcases[3 + nombre_essaie*4], 'fill')]
        Resultat = verif(essaie)
        # si win ou lose fin de parti et création de la fenêtre
        if Resultat[3] or Resultat[2]:
            # fonction pour détruite cette nouvelle fenêtre
            def windowFin_close():
                windowFin.destroy()

            def suivant():
                windowFin_close()
                menu()
            # création de la fenêtre
            windowjeu.destroy()
            windowFin = tk.Tk()
            windowFin.geometry("1200x900")
            windowFin.config(bg='snow3')
            windowFin.resizable(height=False, width=False)
            # menu
            mainmenuFin = tk.Menu(windowFin)
            mainmenuFin.add_command(label="Quitter", command=windowFin_close)
            windowFin.config(menu=mainmenuFin)
            # labelle indiquant si on a gagné ou perdu
            labelFin = tk.Label(windowFin, text='oui')
            labelFin.grid(column=3, row=1, padx=450)
            # bouton qui renvoi au menu principal
            Btnsvt = tk.Button(windowFin, text='Rejouer', command=suivant,
                               bg='snow4')
            Btnsvt.grid(column=3, row=8)
            Btnsvt.config(font=("Courier", 18, "bold"))
            # label pour rejouer
            labelrejouer = tk.Label(windowFin, text="Voulez vous rejouer?",
                                    bg='snow4')
            labelrejouer.grid(column=3, row=7)
            labelrejouer.config(font=("Courier", 18, "bold"))
            # canvas
            canvasimage = tk.Canvas(windowFin, width=400,
                                    height=400)
            if Resultat[3]:
                # décoration/indication de win
                labelFin.config(font=("Courier", 25, "bold"),
                                text='BRAVO :)!Vous avez gagné!',
                                bg='snow4')
                global imagew
                imagew = "Projet-mastermind\\img\\jackpot.png"
                imagew = tk.PhotoImage(file=imagew)
                canvasimage.create_image(200, 200, image=imagew,)
                canvasimage.grid(column=3, row=3)

            elif Resultat[2]:
                # décoration/indication de lose
                txt = "Dommage :(,vous avez perdu\n Le code était:"
                labelFin.config(font=("Courier", 25, "bold"),
                                text=txt, bg='snow3')
                labellose = tk.Label(text=code_secret,
                                     font=("Courier", 25, "bold"),
                                     bg='snow3')
                labellose.grid(column=3, row=3)
                global imagel
                imagel = "Projet-mastermind\\img\\perdu.png"
                imagel = tk.PhotoImage(file=imagel)
                canvasimage.create_image(200, 200, image=imagel)
                canvasimage.grid(column=3, row=4)
            windowFin.mainloop()
        else:
            # création des pions
            Exact = Resultat[0]-1
            Correspondant = Resultat[1]-1
            for i in range(4):
                if i <= Exact:
                    tbpions.append(canvasjeu.create_oval(
                        (300 + i*25, 50 + 30*nombre_essaie),
                        (310 + i*25, 60 + 30*nombre_essaie),
                        outline='black',
                        fill='red'))
                    Correspondant += 1
                elif i <= Correspondant:
                    tbpions.append(canvasjeu.create_oval(
                        (300 + i*25, 50 + 30*nombre_essaie),
                        (310 + i*25, 60 + 30*nombre_essaie),
                        outline='black',
                        fill='grey'))
            # configuration de txt du bouton
            nombre_essaie += 1
            fun_img(Resultat[0], Resultat[1])
            txt = 'Finir le tour N°' + str(nombre_essaie)
            PlayButton.config(text=txt)


def fun_img(exact, correspondant):
    '''Change l'image du canvasjeu en fonction
    du nb de pions'''
    global canvasimagejeu
    global img2
    # supprime l'ancienne img
    canvasimagejeu.delete(img2)
    # on adjuste pour notre image
    k, x, y, color = exact*4 + correspondant, 200, 225, 'black'
    img2 = "Projet-mastermind\\img\\"
    # on sélectionne la bonne img
    if nombre_essaie == 0:
        img2 += 'Gl.png'
    elif k > 11:
        img2 += 'Genius.png'
        x, y, color = 220, 215, '#6997A5'
    elif k >= 8:
        img2 += 'vousyetespresque.png'
        x, color = 220, 'white'
    elif k >= 4:
        img2 += "It'sOk.png"
        x, y, color = 225, 215, 'white'
    elif k >= 2:
        img2 += 'bondebut.png'
        x, color = 220, 'white'
    else:
        img2 += "wtf.png"
        x, y, color = 230, 215, '#788080'
    # on change l'img
    img2 = tk.PhotoImage(file=img2)
    canvasimagejeu.create_image(x, y, image=img2)
    canvasimagejeu.config(bg=color)


def roll_back():
    '''Supprime des valeurs dans le tbsave et -1 sur nbessaie
    et supprime dans tb pions le tour d'avant et les supprimes
    du canvas et ont remets les cases en blanc'''
    global tbsave
    global nombre_essaie
    # si nb essaie > 0 on peux retourné en arrière
    if nombre_essaie > 0:
        # suppression des saves
        Pions = tbsave[1][nombre_essaie-1] + tbsave[2][nombre_essaie-1]
        for i in range(2):
            tbsave[i+1].pop()
            tbsave[0].pop()
        if Pions > 0:
            # suppressions des pions
            for _ in range(Pions):
                canvasjeu.delete(tbpions[-1])
                tbpions.pop()
        nombre_essaie -= 1
        # on remets les cases en blanc
        for i in range(4):
            canvasjeu.itemconfigure(tbcases[i + 4*nombre_essaie], fill='white')
        txt = 'Finir le tour N°' + str(nombre_essaie)
        PlayButton.config(text=txt)
        if nombre_essaie > 0:
            fun_img(tbsave[1][-1], tbsave[2][-1])


def savefile():
    '''Ecriture dans un txt des données'''
    file = open(path2, 'w')
    # une sorte de mot de passe pour savoir que c'est
    # un fichier valable
    file.write("PouetPouetLamouette#42:\n")
    # écrireture des variable dans le fichier
    file.writelines([str(code_secret), "\n" + str(nombre_essaie),
                     "\n" + str(nbjoueurs), "\n" + str(tbsave[0]),
                     '\n' + str(tbsave[1]), "\n" + str(tbsave[2])])
    file.close()


def Nom_File():
    '''demande de selectionner un fichier la ou save et appelle save()'''
    global path2
    # k pour commencer dans le dossir saves
    k = "Projet-mastermind\\Saves"
    # demenade de save le fichier a une endroit
    path = asksaveasfile(initialdir=k, defaultextension=".txt")
    # on modifie le path pour avoir sous une forme pour open()
    if path is not None:
        path = str(path)[24:-27].split("/")
        path2 = ""
        for elt in path:
            path2 += elt + "\\"
        path2 = path2[1:-3]
    savefile()


def loadfile():
    '''Vérification du fichier si c'est un fichier valide puis
    ajoute les données dans les variable associer puis modifie l'interface'''
    # on se place directement dans le dossir save
    k = "Projet-mastermind\\Saves"
    filename = askopenfile(initialdir=k, title='Choose a file',
                           filetypes=[("txt files", "*.txt")])
    # on prend le path et on le modifie pour avoir la bonne forme
    # pour open
    filename = str(filename)[24:-27].split("/")
    filename2 = ""
    for elt in filename:
        filename2 += elt + "\\"
    filename2 = filename2[1:-3]
    fichier = open(filename2, "r")
    # création d'un tableau pour contenir les données
    tbFichier = []
    # test du code secret + leture du fichier
    if fichier.readline() == "PouetPouetLamouette#42:\n":
        for _ in range(6):
            tbFichier.append(fichier.readline())
    fichier.close()
    # indication pour l'utilisateur si sa le fichier n'est pas compatible
    txt = "Si la fenêtre ne se ferme pas, le fichier choisie n'est pas valable"
    LabelLoadError = tk.Label(window, text=txt)
    LabelLoadError.grid(row=8, column=3)
    # on test si c'est possible
    try:
        # on modifie les données pour match avec ce quelle devrait être
        tbFichier[0], tbFichier[2] = tbFichier[0][1:-2], int(tbFichier[2])
        tbFichier[1], tbFichier[4] = int(tbFichier[1]), tbFichier[4][1:-2]
        tbFichier[5], tbFichier[3] = tbFichier[5][1:-1], tbFichier[3][1:-2]
        # on refait le tableau tbsave[0] soit des essaie de couleur
        tbFichier[0] = tbFichier[0].split(',')
        if len(tbFichier[3]) >= 1:
            tbFichier[3] = tbFichier[3].split('/')
            for elt in range(len(tbFichier[3])):
                if elt == 0:
                    tbFichier[3][elt] = tbFichier[3][elt][1:-4]
                else:
                    tbFichier[3][elt] = tbFichier[3][elt][4:-4]
                tbFichier[3][elt] = tbFichier[3][elt].split(',')
                for elt2 in range(len(tbFichier[3][elt])):
                    if elt2 == 0:
                        tbFichier[3][elt][elt2] = tbFichier[3][elt][elt2][1:-1]
                    else:
                        tbFichier[3][elt][elt2] = tbFichier[3][elt][elt2][2:-1]
            tbFichier[3] = tbFichier[3][:-1]
        # on remet le tableau code secret
        for elt in range(4):
            if elt == 0:
                tbFichier[0][elt] = tbFichier[0][elt][1:-1]
            else:
                tbFichier[0][elt] = tbFichier[0][elt][2:-1]
        # on mets toutes les valeurs de couleur exact/correspondante
        # en int
        if len(tbFichier[5]) >= 2:
            tbFichier[5] = tbFichier[5].split(',')
            tbFichier[4] = tbFichier[4].split(',')
            tbFichier[5][0] = int(tbFichier[5][0])
            tbFichier[4][0] = int(tbFichier[4][0])
            for elt in range(1, len(tbFichier[5])):
                tbFichier[5][elt] = int(tbFichier[5][elt][0:])
                tbFichier[4][elt] = int(tbFichier[4][elt][0:])
        elif len(tbFichier[5]) == 1:
            tbFichier[5][0] = int(tbFichier[5][0])
            tbFichier[4][0] = int(tbFichier[4][0])

    except ValueError:
        print("Le ficheir n'est pas bon")
    else:
        options_couleurs = ['red', 'blue', 'yellow', 'purple', 'green',
                            'orange', 'black', 'pink']
        global condition
        condition = True
        # test sur les longueur du code secret et de la taille des essaie
        if len(tbFichier[0]) != 4 or (tbFichier[3] == [] and
                                      tbFichier[1] != 0):
            condition = False
        else:
            # test si les couleurs ne sont pas dans nos options
            for elt in range(len(tbFichier[0])):
                if tbFichier[0][elt] not in options_couleurs:
                    condition = False
                    break
            # test de la longueur des sous tableau de essaie
            for elt in range(len(tbFichier[3])):
                if condition is False:
                    break
                elif len(tbFichier[3]) >= 1:
                    if len(tbFichier[3][elt]) != 4:
                        condition = False
                        break
                else:
                    # on test si les couleurs sont dans les options de couleur
                    for elt2 in range(4):
                        if tbFichier[3][elt][elt2] not in options_couleurs:
                            condition = False
                            break
        if condition:
            # on test si nbjoueurs [1, 2]
            if tbFichier[2] != 1 and tbFichier[2] != 2:
                condition = False
            # on test si nombre de d'essaie [0, 10]
            if tbFichier[1] < 0 or tbFichier[1] > 9:
                condition = False
            # on test si les le nombre de couleur exact et correspondante
            # est bien borné dans le bon intervalle
            Indice = len(tbFichier[5])
            if Indice > 0:
                for elt in range(Indice):
                    if tbFichier[5][elt] < 0 or tbFichier[5][elt] > 3:
                        condition = False
                        break
                    if tbFichier[4][elt] < 0 or tbFichier[4][elt] > 4:
                        condition = False
                        break
        if condition:
            global nbjoueurs
            global nombre_essaie
            global code_secret
            global tbsave
            global PlayButton
            # on refait mets les valeur dans les variable
            # on refait le plateau grcae a plateau()
            nbjoueurs = tbFichier[2]
            plateau()
            nombre_essaie = tbFichier[1]
            if nombre_essaie > 0:
                fun_img(tbFichier[4][-1], tbFichier[5][-1])
            code_secret = tbFichier[0]
            tbsave = [[]]
            for elt in range(len(tbFichier[3])):
                tbsave[0].append(tbFichier[3][elt])
                tbsave[0].append('/')
            if tbFichier[4] == '':
                tbsave.append([])
                tbsave.append([])
            else:
                tbsave.append(tbFichier[4])
                tbsave.append(tbFichier[5])
            # on refait les couleurs des boutons
            for elt in range(nombre_essaie):
                canvasjeu.itemconfig(tbcases[0 + elt*4],
                                     fill=tbFichier[3][elt][0])
                canvasjeu.itemconfig(tbcases[1 + elt*4],
                                     fill=tbFichier[3][elt][1])
                canvasjeu.itemconfig(tbcases[2 + elt*4],
                                     fill=tbFichier[3][elt][2])
                canvasjeu.itemconfig(tbcases[3 + elt*4],
                                     fill=tbFichier[3][elt][3])
            # modifie le text du bouton
            txt = 'Finir le tour N°' + str(nombre_essaie)
            PlayButton.config(text=txt)
            # recréation des pions
            for elt in range(len(tbFichier[4])):
                Exact = tbFichier[4][elt]-1
                Correspondant = tbFichier[5][elt]-1
                for i in range(4):
                    if i <= Exact:
                        tbpions.append(canvasjeu.create_oval(
                            (300 + i*25, 50 + 30*elt),
                            (310 + i*25, 60 + 30*elt),
                            outline='black',
                            fill='red'))
                        Correspondant += 1
                    elif i <= Correspondant:
                        tbpions.append(canvasjeu.create_oval(
                            (300 + i*25, 50 + 30*elt),
                            (310 + i*25, 60 + 30*elt),
                            outline='black',
                            fill='grey'))
# changer le nombre de joueur


def Nb_joueur(event):
    '''Change la variable nb joueurs'''
    global nbjoueurs
    # dépend de la case sélectionné
    if vlist.get() == "1 joueur":
        nbjoueurs = 1
    if vlist.get() == "2 joueurs":
        nbjoueurs = 2


# changer la couleur
def changecolor(x, y):
    '''change la couleur selon la position du click'''
    global couleur
    # change la couleur selon position x,y
    if x >= 10 and x <= 30:
        if y >= 15 and y <= 35:
            couleur = "red"
        elif y >= 50 and y <= 70:
            couleur = 'blue'
        elif y >= 85 and y <= 105:
            couleur = 'yellow'
        elif y >= 120 and y <= 140:
            couleur = 'purple'
        elif y >= 155 and y <= 175:
            couleur = 'green'
        elif y >= 190 and y <= 210:
            couleur = 'orange'
        elif y >= 225 and y <= 245:
            couleur = 'black'
        elif y >= 260 and y <= 280:
            couleur = 'pink'
        labelcouleur.config(text=couleur, bg=couleur)


def Color(event):
    '''donne une couleur a chaque case/change la couleur
    sélectionné'''
    global tbcases
    changecolor(event.x, event.y)
    # modifie les case de couleur selon la couleur
    if event.x >= 100 and event.x <= 195:
        if event.y >= 50 and event.y <= 340:
            if event.x >= 100 and event.x <= 120:
                canvasjeu.itemconfig(tbcases[0 + nombre_essaie*4],
                                     fill=couleur)
            elif event.x >= 125 and event.x <= 145:
                canvasjeu.itemconfig(tbcases[1 + nombre_essaie*4],
                                     fill=couleur)
            elif event.x >= 150 and event.x <= 170:
                canvasjeu.itemconfig(tbcases[2 + nombre_essaie*4],
                                     fill=couleur)
            elif event.x >= 175 and event.x <= 195:
                canvasjeu.itemconfig(tbcases[3 + nombre_essaie*4],
                                     fill=couleur)


def Suggestion():
    '''analyse les essaie en leur donnant des notes
    et donne une valeur a chaque couleur, différente pour chaque postion'''
    options_couleurs = ['red', 'orange', 'yellow', 'green', 'blue',
                        'purple', 'pink', 'black']
    txt = ''
    # random si 0 essaie
    if nombre_essaie == 0:
        for _ in range(4):
            txt += options_couleurs[randint(0, len(options_couleurs)-1)]
            txt += ', '
    # cas spéciale si note > 7 au premier essaie
    elif nombre_essaie == 1 and tbsave[1][0]*4 + tbsave[2][0] > 7:
        # si note > 11 on change 1 couleur
        if tbsave[1][0]*4 + tbsave[2][0] > 11:
            a = randint(0, 3)
            i = options_couleurs.index(tbsave[0][0][a])
            options_couleurs.remove(options_couleurs[i])
            test = tbsave[0][0][:]
            test[a] = options_couleurs[randint(0, len(options_couleurs)-1)]
            txt = str(test)[1:-1]
        # sinon change 2
        else:
            z = -1
            test = tbsave[0][0][:]
            for _ in range(2):
                a = randint(0, 3)
                while a == z:
                    a = randint(0, 3)
                z = a
                k = randint(0, len(options_couleurs)-1)
                while test[a] == options_couleurs[k]:
                    k = randint(0, len(options_couleurs)-1)
                test[a] = options_couleurs[k]
            txt = str(test)[1:-1]
    else:
        # création des notes/tb saveV2 (facilite les opération)
        tbsave_v2 = [tbsave[0][z] for z in range(0, len(tbsave[0]), 2)]
        tbnote = [0 for _ in range(nombre_essaie)]
        # plusieur fois le même essaie donc on retire la note
        liste, tbrecup = [], []
        # on récupére les doublons
        for elt in range(len(tbsave_v2)):
            for elt2 in range(len(tbsave_v2)):
                if tbsave_v2[elt] == tbsave_v2[elt2] and elt != elt2:
                    if [elt, elt2] not in liste:
                        liste.append([elt, elt2])
                        liste.append([elt2, elt])
                        if elt2 not in tbrecup:
                            tbrecup.append(elt2)
        # on ajoute les notes
        for elt in range(len(tbsave_v2)):
            if elt not in tbrecup:
                tbnote[elt] += tbsave[1][elt]*4 + tbsave[2][elt]
        # création tb score
        tb_score = [[0 for _ in range(8)] for _ in range(4)]
        # on donne les cores aux couleur pour chaque pose
        for elt in range(len(tbsave_v2)):
            for elt2 in range(len(tbsave_v2[elt])):
                if tbsave_v2[elt][elt2] == 'red':
                    x = 0
                elif tbsave_v2[elt][elt2] == 'blue':
                    x = 1
                elif tbsave_v2[elt][elt2] == 'yellow':
                    x = 2
                elif tbsave_v2[elt][elt2] == 'purple':
                    x = 3
                elif tbsave_v2[elt][elt2] == 'green':
                    x = 4
                elif tbsave_v2[elt][elt2] == 'orange':
                    x = 5
                elif tbsave_v2[elt][elt2] == 'black':
                    x = 6
                elif tbsave_v2[elt][elt2] == 'pink':
                    x = 7
                tb_score[elt2][x] += tbnote[elt]
        # analyse des scores
        for elt in range(len(tb_score)):
            # variable pour comparer
            min_colonne = [5 + round(nombre_essaie/3), '']
            # parcour des sous tableau
            for elt2 in range(len(tb_score[elt])):
                # k sinon erreur flake 8 sur la ligne elif
                k = min_colonne[1]
                # compare pour trouver le plus grand élement
                # supérieur
                if tb_score[elt][elt2] > min_colonne[0]:
                    min_colonne[0] = tb_score[elt][elt2]
                    min_colonne[1] = elt2
                # égale donc on regarde le taux de présence
                elif tb_score[elt][elt2] == min_colonne[0] and type(k) == int:
                    presence_1, presence_2 = 0, 0
                    for elt3 in range(len(tbsave_v2)):
                        if tbsave_v2[elt3][elt] == options_couleurs[k]:
                            presence_2 += 1
                        elif tbsave_v2[elt3][elt] == options_couleurs[elt2]:
                            presence_1 += 1
                    # on compare les présences
                    if presence_1 > presence_2:
                        min_colonne[0] = tb_score[elt][elt2]
                        min_colonne[1] = elt2
                    # si elle sont égale on doit faire un random
                    elif presence_2 == presence_1 and randint(0, 1) == 0:
                        min_colonne[0] = tb_score[elt][elt2]
                        min_colonne[1] = elt2
            # sinon on a rien audessus de 7 pas assé précis donc random
            if type(min_colonne[1]) == str:
                min_colonne[1] = randint(0, 7)
                # modifie le text
            txt += options_couleurs[min_colonne[1]] + ', '
    Labelsuggest.config(text=txt)


def plateau():
    # creation du plateau de jeu
    global windowjeu

    def fermer_windowjeu():
        windowjeu.destroy()
        menu()

    fermer_window()
    windowjeu = tk.Tk()
    windowjeu.title("jeu")
    windowjeu.geometry("900x600")
    windowjeu.resizable(height=False, width=False)

    # lancement du jeux
    global tbpions
    global tbcases
    global canvasjeu
    global labelError
    global PlayButton
    global labelcouleur
    global couleur
    tbpions = []
    couleur = 'red'
    # canvas de jeu
    canvasjeu = tk.Canvas(windowjeu, bg='White', height=600, width=450)
    canvasjeu.grid(column=0, row=0)
    # label couleur
    labelcouleur = tk.Label(windowjeu, text="Red", bg='Red')
    labelcouleur.place(x=0, y=300)
    # bouton pour jouer
    PlayButton = tk.Button(windowjeu, text="Finir le tour n°0",
                           command=PlayTurn, bg='snow4',
                           height=2, width=15)
    PlayButton.place(x=500, y=10)
    txt = 'Toute les cases doive\nêtre differente de blanc'
    labelError = tk.Label(windowjeu, text=txt, bg='snow3')
    labelError.place(x=620, y=10)
    # bouton retour en arrière
    Buttonback = tk.Button(windowjeu, text="annuler l'essaie précédent",
                           command=roll_back, bg='snow4')
    Buttonback.place(x=500, y=60)
    # bouton et label pour suggère une solution
    btnsuggest = tk.Button(windowjeu, text='Suggestion de solution',
                           command=Suggestion, bg='snow4', height=2, width=20)
    btnsuggest.place(x=500, y=100)
    global Labelsuggest
    Labelsuggest = tk.Label(windowjeu, text='', bg='snow3')
    Labelsuggest.place(x=500, y=145)
    # Label nom du plateau
    # Label nom du plateau
    labelnom = tk.Label(windowjeu, text='PLATEAU DE JEU',
                        font=("helvetica", "15", "bold"), bg='snow4')
    labelnom.place(x=100, y=400)

    texterappel = 'Pour rappel:\n'
    texterappel += " Le pion rouge signifie que vous avez une bonne couleur\n"
    texterappel += "parmi les quatres,qui est bien placé\n"
    texterappel += "Le pion gris lui signifie que vous avez une bonne "
    texterappel += "couleur\n parmi les quatres,qui n'est pas bien placé."
    labelrappel = tk.Label(windowjeu, text=texterappel, bg='snow4')
    labelrappel.place(x=35, y=475)
    # bind click gauche
    canvasjeu.bind("<Button-1>", Color)

    # création des boules de couleurs

    canvasjeu.create_oval((10, 15), (30, 35), fill='red')
    canvasjeu.create_oval((10, 50), (30, 70), fill='blue')
    canvasjeu.create_oval((10, 85), (30, 105), fill='yellow')
    canvasjeu.create_oval((10, 120), (30, 140), fill='purple')
    canvasjeu.create_oval((10, 155), (30, 175), fill='green')
    canvasjeu.create_oval((10, 190), (30, 210), fill='orange')
    canvasjeu.create_oval((10, 225), (30, 245), fill='black')
    canvasjeu.create_oval((10, 260), (30, 280), fill='pink')

    # creation cases a remplir
    # premiere colonne
    tbcases = []
    for i in range(0, 10):
        tbcases.append(canvasjeu.create_oval((100, 50 + 30*i),
                                             (120, 70 + 30*i),
                                             outline='black',
                                             fill="white"))
        # deuxieme colonne
        tbcases.append(canvasjeu.create_oval((125, 50 + 30*i),
                                             (145, 70 + 30*i),
                                             outline='black',
                                             fill="white"))
        # troizieme colonne
        tbcases.append(canvasjeu.create_oval((150, 50 + 30*i),
                                             (170, 70 + 30*i),
                                             outline='black',
                                             fill="white"))
        # quatrieme colonne
        tbcases.append(canvasjeu.create_oval((175, 50 + 30*i),
                                             (195, 70 + 30*i),
                                             outline='black',
                                             fill="white"))
    canvasjeu.create_rectangle((290, 40), (400, 350), outline="black")
    # canavas image
    global canvasimagejeu
    canvasimagejeu = tk.Canvas(windowjeu, width=450, height=450, bg='black')
    global img2
    img2 = "Projet-mastermind\\img\\Gl.png"
    img2 = tk.PhotoImage(file=img2)
    canvasimagejeu.create_image(200, 225, image=img2)
    canvasimagejeu.place(x=450, y=175)
    # ajoute du save et du loadfile au menu
    mainmenujeu = tk.Menu(windowjeu)
    windowjeu.config(menu=mainmenujeu)
    mainmenujeu.add_command(label="Retour", command=fermer_windowjeu)
    mainmenujeu.add_command(label="Sauvegarder", command=Nom_File)
# creation des regles


def reglesjeu():

    def fermer_window2():
        window2.destroy()
    # création de la fen^tre
    window2 = tk.Tk()
    mainmenu2 = tk.Menu(window2)
    mainmenu2.add_command(label="Quitter", command=fermer_window2)
    window2.config(menu=mainmenu2)

    # taille de la fenêtre
    window2.title("Règles du jeu")
    window2.geometry("1000x200")
    window2.resizable(height=False, width=False)

    # text
    window2.config(background='snow3')
    texttitle = "Voici le principe et les règles du jeu :"
    label_title2 = tk.Label(window2, text=texttitle, bg='snow4')
    label_title2.grid(row=0, column=0)
    text = "• il sagit dun jeu à 2 joueurs dans lequel un des joueurs"
    text += " choisit un code secret formé de\n4 pions de couleur alignés et l"
    text += "'autre joueur doit deviner ce code en au plus 10 essais de code\n"
    text += "un essai consiste à proposer un code et à le comparer au code"
    text += "secret; huit couleurs sont\ndisponibles dans le jeu et plusieurs"
    text += "pions du code peuvent être de la même couleur\n à chaque essai,"
    text += " le joueur qui décode acquiert l'information suivante : le nombre"
    text += "\n le nombre de pions bien placés; un pion est bien placé"
    text += " s’il a la même couleur que le pion qui est à la même position"
    text += "dans le code secret. \n Et le nombre de pions mal placés"
    text += "s'il a la même couleur qu'un pion du code qui n'est pas à une "
    text += "position d’un pion bien placé,de plus chaque pion du code peut "
    text += "compter pour au plus\n un pion mal placé. Cette information est "
    text += "representé par des pions dont les rouge indiques le nombre de "
    text += "pions bien placés et les pions blancs indiquent les pions mal "
    text += "placés.\n Si le jouer décode le code en moins de 10 essais alors "
    text += "il gagne, sinon c'est son adversaire qui gagne."
    label2 = tk.Label(window2, text=text, bg='snow4')
    label2.grid()


# creation de la fonction pour fermer la fenetre
def fermer_window():
    window.destroy()


# menu
def menu():
    global window
    global mainmenu
    global vlist
    global labelMsg
    global nbjoueurs
    nbjoueurs = 0
    window = tk.Tk()
    window.title('Mastermind')

    # figer la fenetre
    window.geometry("1000x800")
    window.config(bg='snow3')
    window.resizable(height=False, width=False)

    # image
    canvasimage = tk.Canvas(window, width=300, height=300, bg='white')
    image = "Projet-mastermind\\img\\imgmast.png"
    img = tk.PhotoImage(file=image)
    canvasimage.create_image(160, 170, image=img)
    canvasimage.grid(column=3, row=13)
    # menu du jeu
    mainmenu = tk.Menu(window)
    mainmenu.add_command(label="Quitter", command=fermer_window)
    mainmenu.add_command(label="Charger une partie", command=loadfile)
    window.config(menu=mainmenu)

    # titre du jeu
    label1 = tk.Label(window, text='MASTERMIND', font=("helvetica", "30"),
                      bg='snow4')
    label1.grid(column=3, row=1, padx=400)

    labelMsg = tk.Label(window, text="Veuillez choisir le nombre de joueur",
                        bg='snow3')
    labelMsg.grid(column=3, row=6)

    # creation des boutons
    btn2 = tk.Button(window, text='REGLES',
                     command=reglesjeu, bg='snow4',
                     height=2, width=8)
    btn2.grid(column=3, row=2)

    btn = tk.Button(window, text='JOUER',
                    command=__init__, bg='snow4')
    btn.grid(column=3, row=4, pady=20)
    btn['font'] = font.Font(weight="bold")

    # nombre de joueur
    vlist = tk.StringVar()
    boutonj = ttk.Combobox(window, textvariable=vlist)
    boutonj["values"] = ["1 joueur", '2 joueurs']
    boutonj['state'] = 'readonly'
    boutonj.grid(column=3, row=5)
    boutonj.bind('<<ComboboxSelected>>', Nb_joueur)

    window.mainloop()


menu()

import numpy as np
import matplotlib.pyplot as plt


def ajouter_monomere(matrice, pos_last, number):

    dir = find_direction()
    new_pos = pos_last + dir
    matrice[new_pos[0], new_pos[1], new_pos[2]] = number

    return matrice, new_pos


def find_direction():

    nb = np.random.randint(1, 7)

    if nb == 1:
        dir = [1, 0, 0]
    elif nb == 2:

        dir = [0, 1, 0]
    elif nb == 3:

        dir = [0, 0, 1]
    elif nb == 4:

        dir = [-1, 0, 0]
    elif nb == 5:

        dir = [0, -1, 0]
    else:
        dir = [0, 0, -1]

    return np.array(dir)


taille_matrice = 1000
taille_polymere = 20
essaie = 400
list_r = []
list_rg = []
list_contact = []
Rf = np.arange(5, 100, 5)
k = 0
list_contact_i = np.zeros((taille_polymere-1))

for j in range(essaie):

    reseau = np.zeros((taille_matrice, taille_matrice, taille_matrice))
    first_pos = np.array([taille_matrice//2, taille_matrice//2, taille_matrice//2])
    list_pos = [first_pos]
    new_pos = first_pos.copy()

    for i in range(taille_polymere):

        reseau, new_pos = ajouter_monomere(reseau, new_pos, i)

        if i != 0 and (first_pos == new_pos).all():
            list_contact_i[i-1] += 1

        list_pos.append(new_pos)

    if (new_pos == first_pos).all():
        k += 1

list_contact.append(k/essaie)


for i, cont in enumerate(list_contact_i):

    list_contact_i[i] = cont/essaie


plt.plot(np.arange(1, len(list_contact_i)+1), list_contact_i)
plt.xlabel("proba_contact")
plt.ylabel("ieme monomere")
plt.show()
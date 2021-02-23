import numpy as np
import matplotlib.pyplot as plt
import vpython as v


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
taille_pols = [10, 20, 40, 80, 160]
essaie = 100
list_r = []
list_rg = []
all_r = []
all_rg = []

for taille_polymere in taille_pols:

    list_contact_i = np.zeros((taille_polymere-1))

    for j in range(essaie):
        parb_in = []

        reseau = np.zeros((taille_matrice, taille_matrice, taille_matrice))
        first_pos = np.array([taille_matrice//2, taille_matrice//2, taille_matrice//2])
        list_pos = [first_pos]
        new_pos = first_pos.copy()

        for i in range(taille_polymere):

            reseau, new_pos = ajouter_monomere(reseau, new_pos, i)

            list_pos.append(new_pos)

        r = np.linalg.norm(new_pos-first_pos)**2
        print(r)
        list_pos = np.array([pos-first_pos for pos in list_pos])
        rcm = np.array(sum(list_pos))/taille_polymere
        list_r.append(r)
        rg = 0

        for pos in list_pos:

            rg += (np.linalg.norm(pos - rcm))**2

        rg /= taille_polymere
        list_rg.append(rg)

    r = np.mean(np.array(list_r))
    all_r.append(r)
    rg = np.mean(np.array(list_rg))
    all_rg.append(rg)
    print("r_square = {} \n r_gyration = {}".format(r, rg))

    for i, cont in enumerate(list_contact_i):

        list_contact_i[i] = cont/essaie

plt.plot(taille_pols, all_r)
plt.xlabel("L")
plt.ylabel("Re")
plt.show()
plt.plot(taille_pols, all_rg)
plt.xlabel("L")
plt.ylabel("Rg")
plt.show()
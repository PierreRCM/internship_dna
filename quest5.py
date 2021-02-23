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


def in_circle(R_circle, norm):

    if norm < R_circle:  # Alors mon monomère dans la sphère dont il a un parB
        return 1

    return 0


taille_matrice = 1000
taille_polymere = 100
essaie = 2000
a = 1
Rf = 3*a
tot_parb = np.zeros([taille_polymere])

for j in range(essaie):
    parb_in = []

    reseau = np.zeros((taille_matrice, taille_matrice, taille_matrice))
    first_pos = np.array([taille_matrice//2, taille_matrice//2, taille_matrice//2])
    list_pos = [first_pos]
    new_pos = first_pos.copy()

    for i in range(taille_polymere):

        reseau, new_pos = ajouter_monomere(reseau, new_pos, i)
        parb_in.append(in_circle(Rf, np.linalg.norm(new_pos-first_pos)**2))

        list_pos.append(new_pos)
    tot_parb += np.array(parb_in)

plt.plot(np.arange(taille_polymere), tot_parb)
plt.xlabel("ieme monomere")
plt.ylabel("nombre d'attachement")
plt.show()
import vpython as v
import numpy as np
from useful_func import *


def rotation_matrix_y(theta):

    matrix = np.array([[np.cos(theta*np.pi/180), 0, np.sin(theta*np.pi/180)],
                       [0, 1, 0],
                       [-np.sin(theta*np.pi/180), 0, np.cos(theta*np.pi/180)]])

    return matrix


def rotate_mono(triplet_mono):

    angle_to_rotate = np.random.uniform(0, 360)
    axe_rot = triplet_mono[2]-triplet_mono[0]  # vecteur qui formera ey

    new_axe_pos_x, new_axe_pos_y, new_axe_pos_z = create_base(axe_rot)
    new_base = np.array([new_axe_pos_x, new_axe_pos_y, new_axe_pos_z])
    mono_to_rotate = triplet_mono[1] - triplet_mono[0]

    ########### Rotation ############

    mat_passage_b1_b2 = np.linalg.solve(np.identity(3), new_base)  # Calcul matrice de passage
    mono_in_new_base = np.dot(mat_passage_b1_b2, mono_to_rotate) # mon point à rotater dans ma nouvelle base
    mono_rotated_in_b2 = np.dot(mono_in_new_base, rotation_matrix_y(angle_to_rotate)) # on le rotate, dans b2
    mat_passage_b2_b1 = np.linalg.inv(mat_passage_b1_b2)  # matrice pour retourner dans b1
    mono_rotated_in_b1 = np.dot(mat_passage_b2_b1, mono_rotated_in_b2) + triplet_mono[0]  # mon point rotaté dans b1

    return mono_rotated_in_b1


def create_base(ey):

    ey = ey/np.linalg.norm(ey)
    e_temp = np.matmul(ey, rotation_matrix_y(90))
    ez = -np.cross(ey, e_temp)
    ex = np.cross(ey, ez)

    return ex, ey, ez


def select_monomere(all_pos):

    N = len(all_pos)
    i_monomere = np.random.randint(1, N-1)  # Remove border choice list_pos[0] is the start of our first monomere
    mono_pos_to_rotate = [all_pos[i_monomere-1], all_pos[i_monomere], all_pos[i_monomere+1]]

    return i_monomere, mono_pos_to_rotate



####### main variable ########
l_khun = 1  # units ?
N = 50  # Number of monomere
#############################

list_pos = create_polymere(N, l_khun)
list_rod = display_polymere_in_3D(list_pos, N)

j = 0
temps_mc = 0

while True:
    v.rate(30)
    i, mono = select_monomere(list_pos)
    point_rotated = rotate_mono(mono)
    print(i)
    list_pos[i] = point_rotated

    rod_to_del1 = list_rod[i-1]
    rod_to_del2 = list_rod[i]
    rod_to_del1.visible = False
    rod_to_del2.visible = False

    del rod_to_del1
    del rod_to_del2

    new_rod_1 = v.cylinder(pos=v.vector(list_pos[i-1][0], list_pos[i-1][1], list_pos[i-1][2]),
                     axis=v.vector(list_pos[i][0],list_pos[i][1], list_pos[i][2]) - v.vector(list_pos[i-1][0], list_pos[i-1][1], list_pos[i-1][2]),
                     color=v.color.red, radius=0.05, opacity=0.8)

    new_rod_2 = v.cylinder(pos=v.vector(list_pos[i][0], list_pos[i][1], list_pos[i][2]),
                           axis=v.vector(list_pos[i+1][0], list_pos[i+1][1], list_pos[i+1][2]) - v.vector(list_pos[i][0],
                                                                                                    list_pos[i][1],
                                                                                                    list_pos[i][2]),
                           color=v.color.red, radius=0.05, opacity=0.8)
    list_rod[i-1] = new_rod_1
    list_rod[i] = new_rod_2

    j += 1
    if j % N == 0:
        temps_mc += 1

    # print(temps_mc)
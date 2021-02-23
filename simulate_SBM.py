from useful_func import *
import matplotlib.pyplot as plt
import numpy as np


def binding_model(s, sigma, a):

    return 1/((3*(sigma**2)/a**2) + (s))**(3/2)


nb_try = 1000
N = 200
a = [1, 1, 1, 1]
sigma = [1, 2, 5, 10]


parb_binding_profile = [0 for i in range(N)]
all_profiles= []

for j in range(len(a)):
    parb_binding_profile = [0 for i in range(N)]
    for i in range(nb_try):

        list_pos = create_polymere(N, a[j])[:-1]

        parb_binding_profile = parb_profile(list_pos, parb_binding_profile, sigma[j])
        plt.plot(parb_binding_profile)
        plt.show()
    all_profiles.append(parb_binding_profile)


fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=2)
plt.suptitle("nb simulation = {}".format(nb_try))
ax1[0].set_title("N monomeres = {}, size monomere a = {}, sigma = {}".format(N, a[0], sigma[0]))
ax1[0].plot(np.arange(N), np.array(all_profiles[0])/nb_try, label="Simulation")
ax1[0].plot(np.arange(0, N, 0.1),
        binding_model(np.arange(0, N, 0.1), sigma[0], a[0]) / (np.max(binding_model(np.arange(0, N, 0.1), sigma[0], a[0]))), label="model")

ax1[1].set_title("N monomeres = {}, size monomere a = {}, sigma = {}".format(N, a[1], sigma[1]))
ax1[1].plot(np.arange(N), np.array(all_profiles[1])/nb_try, label="Simulation")
ax1[1].plot(np.arange(0, N, 0.1),
        binding_model(np.arange(0, N, 0.1), sigma[1], a[1]) / (np.max(binding_model(np.arange(0, N, 0.1), sigma[1], a[1]))), label="model")

ax2[0].set_title("N monomeres = {}, size monomere a = {}, sigma = {}".format(N, a[2], sigma[2]))
ax2[0].plot(np.arange(N), np.array(all_profiles[2])/nb_try, label="Simulation")
ax2[0].plot(np.arange(0, N, 0.1),
        binding_model(np.arange(0, N, 0.1), sigma[2], a[2]) / (np.max(binding_model(np.arange(0, N, 0.1), sigma[2], a[2]))), label="model")

ax2[1].set_title("N monomeres = {}, size monomere a = {}, sigma = {}".format(N, a[3], sigma[3]))
ax2[1].plot(np.arange(N), np.array(all_profiles[3])/nb_try, label="Simulation")
ax2[1].plot(np.arange(0, N, 0.1),
        binding_model(np.arange(0, N, 0.1), sigma[3], a[3]) / (np.max(binding_model(np.arange(0, N, 0.1), sigma[3], a[3]))), label="model")

ax1[0].legend()
ax1[1].legend()
ax2[0].legend()
ax2[1].legend()
plt.show()



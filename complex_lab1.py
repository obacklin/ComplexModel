import numpy as np
import matplotlib.pyplot as plt

#Code from Wikipedia
plt.close('all')
interval = (2.5, 3.8)  # start, end
accuracy = 0.0005
reps = 600  # number of repetitions
numtoplot = 200
lims = np.zeros(reps)
perturb_param = 0.25

lims_logistic = np.zeros(reps)

fig, (biax, biax2) = plt.subplots(2)
fig.set_size_inches(16, 9)

lims[0] = np.random.rand()
lims_logistic[0] = np.random.rand()

mu_current = 0


for mu in np.arange(interval[0], interval[1], accuracy):
    for i in range(reps - 1):
        lims[i + 1] = mu * (lims[i] * (1 - lims[i]) + perturb_param*(lims[i]**4) *(1-lims[i])) #sine_param*np.sin(np.pi*lims[i]) # logistic map ux(1-x) + pertb (blue)
        lims_logistic[i + 1] = mu * lims_logistic[i] * (1 - lims_logistic[i]) #logistic map (red)
    biax.plot([mu] * numtoplot, lims[reps - numtoplot :], "b.", markersize=0.02)
    biax2.plot([mu] * numtoplot, lims_logistic[reps - numtoplot :], "r.", markersize=0.02)

biax.set(xlabel="r", ylabel="x", title="perturb map")
biax2.set(xlabel="r", ylabel="x", title="unperturbed map")
plt.show()


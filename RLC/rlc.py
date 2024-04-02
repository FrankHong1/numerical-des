import numpy as np
import matplotlib.pyplot as plt

class RLC:
    def __init__(self, R, L, C):
        self.R = R
        self.L = L
        self.C = C
        self.V0 = 1
        self.L = 1
        self.alpha = 1
        self.omega = 1
        self.t = np.linspace(0, 10, 1000)
        self.h = 0.1

    def impedance(self, omega):
        return self.R + 1j*(omega*self.L - 1/(omega*self.C))

    def current(self, omega, V0):
        return V0 / self.impedance(omega)

    def voltage(self, omega, V0):
        return self.current(omega, V0) * self.impedance(omega)
    
    def differential_equation(self):
        i0 = 0 # initial current
        j0 = self.V0/self.L # initial dI/dt
        result = {"i": [i0], "j": [j0]}
        for n in range(len(self.t)):
            i_prev = result["i"][n]
            j_prev = result["j"][n]
            i = i_prev + self.h * j_prev
            j = j_prev + self.h*(-2 * self.alpha * j_prev - self.omega**2 * i_prev)
            i_prev = i
            j_prev = j
            result["i"].append(i)
            result["j"].append(j)
        return result
    
if __name__ == "__main__":
    rlc = RLC(1, 1, 1)
    plt.plot(rlc.differential_equation()["i"])
    plt.savefig("RLC.png")
    


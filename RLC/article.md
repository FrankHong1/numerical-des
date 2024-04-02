# 2nd oder linear ODEs via Euler methods
In this article I explore using Euler methods to solve numerically 2nd order ODE with constant coefficients. This is a very common ODE type that comes up in a bunch of places in Physics. The example I will focus on will be the RLC circuit, and I will want to describe the current flowing through it using time derivatives.

I will use the dot notation for derivatives, so for example $$\dot{I}(t) = \frac{dq(I)}{dt}$$.

## Scenario: the RLC circuit
Let's put together a simple circuit, consisting of
- a EMF source (a battery), with total voltage provided $\Epsilon$,
- a resistance (e.g. a lightbulb), *R*,
- a capacitor (perhaps some sort of battery?), capacitance *C*,
- a inductor (this could be a coil), inductance *L*.

RLC circuit is an example of a damped oscillator. If we didn't have a resistance present, the LC circuit would work as follows:
* first, charge initially stored on the capacitor, would start discharging, creating a current through the inductor,
* current through the inductor will cause magnetic field to be created
* this magnetic field will be created so as to oppose the current that created it, so once the capacitor is fully discharged, the current will then start flowing the other way
In absence of resistance, no energy is dissipated, so this will just be a SHM oscillation.

Adding a resistance is equivalent to damping this motion, as with each oscillation we will lose some energy as heat.

We can describe the charge flowing through each of these as follows:

1. Resistor
Ohm's law gives us

$$V_R = RI(t)$$.

2. Capacitor
The voltage drop across the capacitor as charge collects on it will be
$$V_C = \frac{q(t)}{C} = \frac{1}{C}\int_0^t I(\tau)d\tau$$

3. Inductor
We use the inductor formula 
$$V_L = L\frac\dot{I}(t)$$.

4. Putting these together
As we connect all elements in series, the total voltage drop in each element will have to equal to the provided EMF, so we get
$$\Epsilon = V_R+V_C+V_L$$
hence, using the equations above and rearranging terms, we have 
$$V\Epsilon = L\dot{I}(t) + R I(t) + \frac{1}{C}\int_0^t I(\tau)d\tau$$

As we are assuming that EMF provided is constant, I can now differentiate both sides to get the 2nd order ODE I need:
$$L\ddot{I} + R \dot{I} + \frac{1}{C}I = 0$$
Using the standard notation $\alpha = \frac{R}{2L}$, $\omega_0 = \frac{1}{\sqrt{LC}}$, this becomes
$$\ddot{I} + 2\alpha \dot{I} + \omega_0^2 I = 0$$.

### Initial conditions
I need 2 initial conditions given this is a 2nd order ODE. Here let's assume that initially 
1. there is no current, so $I(0) = 0$, and
2. initially, all charge is stored on the capacitor, and so the voltage across the capacitor is $V_0$. [It can be shown](https://www.khanacademy.org/science/electrical-engineering/ee-circuit-analysis-topic/ee-natural-and-forced-response/a/ee-rlc-natural-response-derivation) that this is equivalent to saying that initially like $\dot{I}(0) = \frac{1}{L}V_0$.

Now we have everything we need to solve the RLC system using Python.

## From 2nd order to 1st order: systems of equations

One trick I really like is to replace the 2nd order ODE with a system of coupled 1st order ODEs. This way, we can get away with only knowing the approximation formula for the 1st derivative.

In other words, let's set
$$\dot{I} = J(t)$$,
$$\dot{J} = - 2\alpha J - \omega_0^2 I$$.
Discretizing both in time will give
$$I_{n+1} = I_{n} + h J_{t_n}$$,
$$J_{n+1} = J_n + h (-2\alpha J_{n}-\omega_0^2 I_n)$$,

With initial conditions giving
$$ I_0 = 0, J(0) = \frac{1}{L}V_0$$

We are now ready to implement this in Python.


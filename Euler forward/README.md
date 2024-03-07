# Euler's method for solving ODEs

I have been studying ODEs for a while both at school and on my own. Even though most "school-type" IVPs (initial value problems) I see in textbooks are easy to solve analytically (with pen and paper), it has always bugged me when teachers assured me that for tougher cases (e.g., non-separable ODEs), we can "always just use the computer" but I never knew how.

So, I decided to take matters in my own hands and figure out numerical ways to solve IVPs.

Let's start with somethign simple, the most basic but also the most intuitive way of solving simple Initial Value Problems: the Euler's (forward) method.

## Initial Value Problem we will look at

We will consider a IVP in the form:

$$\frac{dx}{dt} = f(x,t), \ x(0) = t_0$$

That is, we know the first derivative of the function only, and what the function equals initially. We hope to extrapolate from here exactly what the function looks like.

Intuitively, this should be very doable. After all, the derivative is telling us exactly how the function is changing. So, from the starting point when $t=0$, following the pattern of change described by $f(x,t)$, it should be possible to draw the entire function $x(t)$.

## Euler's forward method: the theory

Euler's method is actually pretty simple when you write it out, and exactly follows our intuition above.

We know that the definition of derivative is 
$$ \frac{dx}{dt} = f(x,t) = \lim_{\Delta x\rightarrow 0}{\frac{x(t+\Delta t) - x(t)}{\Delta t}}$$.

Now in practice we can't achieve a true limit - $\Delta x$ will never be "infinitesimaly small". But we can pick a very small number $$\Delta x\approx h = 0.01$$, say, and see if this is good enough of an approximation.

So, we will replace $\Delta t$ with $h$, and reorganize terms, to get
$$x(t+h) = x(t) + h\times f(x,t)$$

Note that we are using the values of $x(t)$ and $f$ at the previous time $t$, to get the value of $x(t)$ at the *next* time, $t+h$. This is why this method is called a **forward** method, because we always take this one step forward.

This way, it is clear that if I get the initial value $x(0)$, I can use this now to get the value of the function $x$ at time $x(h)$, and then use this to get value of $x(2h)$, and so on and so forth, thus building the entire function step-by-step. Exciting!

## Euler's forward method: implementation

I first write a simple Python function to solve $\frac{dx}{dt} = x$. This is because I know how to solve this function analytically, so I can immediately check how good (or how bad) my numerical solution is going to be.

First, I define a auxiliary function that will return $f(x)$ (RHS of the ODE). For now, this is a "silly" identity function, but in the future I will use this Python method to define $f(x)$ for other cases.

```python
def dx_dt(t, x):
  return x
```

Now, it's time to implement the forward step. I will want to use the old values of $t, x$ to find new, updated values after moving $h$ forward.

```python
def forward_step(t,x,h,dx_dt):
  x_new = x + h * dx_dt(t, x)
  t_new = t + h
  return t_new, x_new
```

Note that I update $x$ first, $t$ second. This is important, as I want to always use previous values of $t$ and $x$ to find new values of $t$ and $x$.

Now, let's make a loop to repeat the forward step a specific number of times. The smaller the step, the more times will our loop have to run.

```python
def forward_loop(t, x, h, N):
    # make lists to hold values of x, t
    T = [t]
    X = [x]
    for i in range(N):
        t,x = forward_step(t,x,h,dx_dt)
        T.append(t)
        X.append(x)
    return T,X
```

Finally, let's put all this together:

```python
def euler_forward(dx_dt, h, interval, init_condi):
  t = 0
  x = init_condi
  span = interval[1] - interval[0]
  N = int(span / h)
  T,X=forward_loop(dx_dt,t, x, h, N)
  return T,X
```

In here, the only new thing we added was to input `interval`, which will be a list `[begin point, end point]`: basically, the interval over which we want to solve the ODE.

## Plotting the results

Let's compare how well our code did vs. analytical solution!

For different values of $h$, we expect the numerical approximation to show different discrepacy with exact (analytical) solution. Specifically, the smaller the step $h$, the closer we expect the numerical and analytical solutions to be.


### $h = 0.1$:

Initially, the numerical solution is doing great, but the farther we get away from the initial condition, the worse it performs.

### $h = 0.05$:

Reducing $h$ by half helped, but we still don't perform great, so let's try again.

### $h = 0.01$

Now we are really close to the realy solution!


## Quantifying these comparisons

One method of comparing curves that I picked up when learning Machine Learning is MSE (mean squared error) method. Basically, it tells us, along 2 curves, how far on average are they from one another? What is the average distance (squared) between all pairs of corresponding points of these 2 curves?

I use MSE now to compare the exact solution with numerical solution I obtained using Euler's forward method, for decreasing value of the time step $h$.

| h    | MSE |
| -------- | ------- |
| 0.1  |  3455691.55   |
| 0.05 |  1076430.51    |
| 0.01 | 52180.68  |
| 0.001 | 546.05  |

Woah! Now it is crystal clear that reducing the value of the time step $h$ 100 times, resulted in reduction of MSE by order of magnitude of 10,000, so 100 square! This is uncanny.

With MSE, I can make evaluate my numerical method quantitatively and give more specific statements about which approximation is best.

I did notice, however, that for much smaller time step, Python takes much longer to give answers. This requires further investigation.

## Running time
The smaller the time step, the more steps Python needs to go through to give answers. Let's investigate how this depends on $h$.

| `h`    | runtime (s) |
| -------- | ------- |
| 0.1  |  1.81198   |
| 0.05 |  3.19481    |
| 0.01 | 5.23168  |
| 0.001 | 7.45681  |

Runtim definitely increases with decreasing step size. From my simple analysis, I am not able to tell if this is linear or other increase, but something to bear in mind as I attempt cracking more advanced cases.

## Testing on another example
Encouraged by these results, I further tested how my code will solve a harder problem, which I could not figure out analytially.

$$\frac{dx}{dt} = \exp{-x^2}$$
(This is a variation of the all-favourite bell curve!)

My solution looks like this, between 0 and 1:


## Summary and concluding thoughts
Euler's forward method is a great first step for me into the realm of numerical methods in Calculus. It has its limitations, naturally, as it was invented at a time when anything more advanced would involve very tedious and error-prone computations by hand. As next step, I want to explore other numerical methods and see how they compare. 

Interesting points I want to explore:
* Does this work for 2nd order equations?
* What about implicit equations, when I can't move $\frac{dx}{dt}$ to the LHS?
* I think it would also be interesting to look at similar methods for solving PDEs as well. And maybe systems of ODEs, too.
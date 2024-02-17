import matplotlib.pyplot as plt

def dx_dt(t, x):
  ans = x+t
  return ans

def euler_forward(first_deri, h, interval, init_condi):
  X = []
  T = []
  x = init_condi[1]
  t = init_condi[0]
  X.append(x)
  T.append(t)
  span = interval[1] - interval[0]
  for i in range(int(span / h)):
    new_x = x + h * first_deri(t, x)
    x = new_x
    new_t = t + h
    t = new_t
    X.append(x)
    T.append(t)
  x = X[-1]
  t = T[-1]
  plt.plot(T, X)
  plt.xlabel('t')
  plt.ylabel('predicted_x')
  plt.savefig('result.png')
  print('The predicted value of x at t =', interval[1], 'after', int(span / h), 'iterations with step size h =', h, 'is', x, 'the predicted graph of x(t) is plotted')      
  return t, x

interval = [0, 5]
init_condi = [0, 1]

approx = euler_forward(dx_dt, 1e-5, interval, init_condi)
print(approx)
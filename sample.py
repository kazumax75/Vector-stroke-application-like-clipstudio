
import numpy
import matplotlib.pyplot as plt
# get_ipython().magic(u'pylab inline')

def CatmullRomSpline(P0, P1, P2, P3, a, nPoints=100):
  """
  P0, P1, P2, and P3 should be (x,y) point pairs that define the Catmull-Rom spline.
  nPoints is the number of points to include in this curve segment.
  """
  # Convert the points to numpy so that we can do array multiplication
  P0, P1, P2, P3 = map(numpy.array, [P0, P1, P2, P3])

  # Calculate t0 to t4
  alpha = a
  def tj(ti, Pi, Pj):
    xi, yi = Pi
    xj, yj = Pj
    return ( ( (xj-xi)**2 + (yj-yi)**2 )**0.5 )**alpha + ti

  t0 = 0
  t1 = tj(t0, P0, P1)
  t2 = tj(t1, P1, P2)
  t3 = tj(t2, P2, P3)

  # Only calculate points between P1 and P2
  t = numpy.linspace(t1,t2,nPoints)

  # Reshape so that we can multiply by the points P0 to P3
  # and get a point for each value of t.
  t = t.reshape(len(t),1)

  A1 = (t1-t)/(t1-t0)*P0 + (t-t0)/(t1-t0)*P1
  A2 = (t2-t)/(t2-t1)*P1 + (t-t1)/(t2-t1)*P2
  A3 = (t3-t)/(t3-t2)*P2 + (t-t2)/(t3-t2)*P3

  B1 = (t2-t)/(t2-t0)*A1 + (t-t0)/(t2-t0)*A2
  B2 = (t3-t)/(t3-t1)*A2 + (t-t1)/(t3-t1)*A3

  C  = (t2-t)/(t2-t1)*B1 + (t-t1)/(t2-t1)*B2
  return C

def CatmullRomChain(P,alpha):
  """
  Calculate Catmull Rom for a chain of points and return the combined curve.
  """
  sz = len(P)

  # The curve C will contain an array of (x,y) points.
  C = []
  for i in range(sz-3):
    c = CatmullRomSpline(P[i], P[i+1], P[i+2], P[i+3],alpha)
    C.extend(c)

  return C



# Define a set of points for curve to go through
Points = numpy.random.rand(10,2)

x1=Points[0][0]
x2=Points[1][0]
y1=Points[0][1]
y2=Points[1][1]
x3=Points[-2][0]
x4=Points[-1][0]
y3=Points[-2][1]
y4=Points[-1][1]
dom=max(Points[:,0])-min(Points[:,0])
rng=max(Points[:,1])-min(Points[:,1])
pctdom=1
pctdom=float(pctdom)/100
prex=x1+sign(x1-x2)*dom*pctdom
prey=(y1-y2)/(x1-x2)*(prex-x1)+y1
endx=x4+sign(x4-x3)*dom*pctdom
endy=(y4-y3)/(x4-x3)*(endx-x4)+y4
print len(Points)
Points=list(Points)
Points.insert(0,array([prex,prey]))
Points.append(array([endx,endy]))
print len(Points)


a=0.

# Calculate the Catmull-Rom splines through the points
c = CatmullRomChain(Points,a)

# Convert the Catmull-Rom curve points into x and y arrays and plot
x,y = zip(*c)
plt.plot(x,y,c='green',zorder=10)

a=0.5
c = CatmullRomChain(Points,a)
x,y = zip(*c)
plt.plot(x,y,c='blue')

a=1.
c = CatmullRomChain(Points,a)
x,y = zip(*c)
plt.plot(x,y,c='red')

# Plot the control points
px, py = zip(*Points)
plt.plot(px,py,'o',c='black')

plt.grid(b=True)
plt.show()



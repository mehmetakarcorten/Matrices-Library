# Matrices Library
A library for matrices calculations, I created this library with the intention of challenging myself. I am very aware of libraries capable of performing these calculations such as `numpy` however I still wanted to use some of the knowledge I had gained from my further education to use.

# How does it work?
I love practical examples rather than explainations, so you can have a look at the example below. The library is very straight forward and easy to use.

```py
#Simply create an object by using example below
#MATRICES ARE ROW MAJOR#

from Matrices import Matrix

a = Matrix((
  (1,2),
  (3,4)
))

b = Matrix((
  (4, 3),
  (2,-1)
))

a*b # Multiply Matrices
a+b # Add Matrices
a-b # Subtract Matrices

a.determinant() # Returns determinant of "a"
a.transpose()   # Returns tranpose matrix of "a"
a.inverse()     # Returns inverse of matrix "a"
```

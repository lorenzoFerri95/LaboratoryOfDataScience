# algoritmo per il calcolo del sottoinsieme a somma massima di una lista
# (confrontando tutti i possibili sottoinsiemi di qualsiasi lunghezza)

# algoritmo meno efficiente

a = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

m = 0
for i in range(len(a)):
    s = 0
    for j in range(i, len(a)):
        s += a[j]
        if s > m:
            m = s
print(m)



#  stesso algoritmo di prima ma più efficiente (costo lineare)

a = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

m = 0
current = 0
for i in a:
    current = max(0, current+i)
    m = max(m, current)
print(m)


# esercizio dictionary

l = [12, 3, -4, 6, -5, 9]

d = {'apple':3, 'orange':4, 'tomato':-5, 'meat':6, 'potato':15, 'strawberry':9}

to_buy = ''
for key, value in d.items():
    if value in l:
        to_buy += key + ', '
    else:
        for new in l:
            if new not in d.values():
                d[key] = new
print(to_buy)
print(d)


# correlazione di Pearson

from math import sqrt

a = [12, 3, 4, 6, 5, 9]
b = [10, 3, 2, 6, 3, 7]

a_mean = sum(a)/len(a)
b_mean = sum(b)/len(b)

covariance = 0
std_dev_a = 0
std_dev_b = 0

for i in range(len(a)):
    covariance += (a[i] - a_mean) * (b[i] - b_mean)
    
    std_dev_a += (a[i] - a_mean)**2
    std_dev_b += (b[i] - b_mean)**2

    
std_dev_a = sqrt(std_dev_a)    
std_dev_b = sqrt(std_dev_b)

correlation = covariance / ( std_dev_a * std_dev_b )
print(correlation)


from numpy import corrcoef
corrcoef(a, b)[0][1]

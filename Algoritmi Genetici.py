import math
from decimal import *
import random

def calculateNrOfBitsCodification():
    aux=precision

    aux=1


    p=1
    while aux>0:
        p=p*10
        aux-=1

    return math.ceil(math.log2((b-a)*p))


def getPace():
  p=1
  aux=precision
  while aux>0:
    aux-=1
    p=p/10

  return p


class Individ:
  def __init__(self):
    self.value=round(random.uniform(a,b),precision+1)
    self.cromozom=self.encode()

  def encode(self):
    lower_bound=math.floor(Decimal((self.value-a)/pace))

    binary=bin(lower_bound)
    binary=str(binary)
    binary=binary[2:]

    aux=""
    for i in range(nr_of_bits_codification-len(binary)):
      aux+="0"

    return aux+binary

  def decode(self):
    val= int(self.cromozom,2)
    p=1
    aux=precision

    while aux>0:
      aux-=1
      p=p*10

    val=val/p
    val=round(val+a,precision)

    return val
    

def getFitness(individ):
    val=individ.decode()

    if val>b:
        return 0

    
    return val*val*coef_grad2+val*coef_grad1+coef_grad0

def binarySearch(v,left,right,target):
    if right>left:
        mid=(right+left)//2
        if v[mid]==target or (v[mid]<target and v[mid+1]>target and mid<len(v)):
            return mid
        elif v[mid]>target:
            return binarySearch(v,left,mid-1,target)
        else:
            return binarySearch(v,mid+1,right,target)
    elif right==left:
        return left
    else:
        return -1

def crossOver(individ1,individ2):
    breakpoint=random.randint(0,len(individ1.cromozom))
    prefix_cromozom1=""
    prefix_cromozom2=""

    for i in range(len(individ1.cromozom)):
        if i<breakpoint:
            prefix_cromozom1+=individ2.cromozom[i]
            prefix_cromozom2+=individ1.cromozom[i]

        else:
            prefix_cromozom1+=individ1.cromozom[i]
            prefix_cromozom2+=individ2.cromozom[i]
    
    individ1.cromozom="".join([x for x in list(prefix_cromozom1)])
    individ1.value=individ1.decode()
    individ2.cromozom="".join([x for x in list(prefix_cromozom2)])
    individ2.value=individ2.decode()

    individ11=Individ()
    individ22=Individ()
    individ11.value=individ1.value
    individ11.cromozom=individ1.cromozom

    individ22.value=individ2.value
    individ22.cromozom=individ2.cromozom
    return [individ11,individ22]

def crossingOverStep(intermediary_population):
    population_for_crossing=[]
    intermediary_population2=[]

    for individ in intermediary_population:
        number=random.uniform(0,1)

        if number<=prob_crossover:
            population_for_crossing.append(individ)
        else:
            intermediary_population2.append(individ)

    if len(population_for_crossing)==1:
        intermediary_population2.append(population_for_crossing[0])
        population_for_crossing.pop()
        pass
    elif len(population_for_crossing)%2==1:
        intermediary_population2.append(population_for_crossing[len(population_for_crossing)-1])
        population_for_crossing.pop()
    
    i=0
    while i<len(population_for_crossing):
        elm=crossOver(population_for_crossing[i],population_for_crossing[i+1])
        intermediary_population2.append(elm[0])
        intermediary_population2.append(elm[1])
        i+=2
    
    return intermediary_population2

def mutation(intermediary_population2):
    intermediary_population3=[]
    cnt=0
    for individ in intermediary_population2:
        aux=""
        for gene in individ.cromozom:
            u=random.uniform(0,1)
            if u<=prob_mutation:
                cnt+=1
                if gene=='0':
                    aux+='1'
                else:
                    aux+='0'
            else:
                aux+=gene

        individ.cromozom="".join([x for x in list(aux)])
        individ.value=individ.decode()

        individ1=Individ()
        individ1.value=individ.value
        individ1.cromozom=individ.cromozom
        intermediary_population3.append(individ1)

    return intermediary_population3


def generateNextGeneration(population,use_elitist):
    next_generation=[]
    intermediary_population=[]
    fitness_list=[]
    population.sort(key = lambda elem : (-getFitness(elem)))

    for individ in population:
        out.write(str(individ.value) + ' ' + str(individ.cromozom) + ' ' + str(individ.decode()) + ' ' +str(getFitness(individ))+'\n')

    total_fitness=0
    fitness_list.append(0)
    for individ in population:
        total_fitness+=getFitness(individ)

    fit=0
    for individ in population:
        fit+=getFitness(individ)/total_fitness
        fitness_list.append(fit)

    fitness_list[len(population)]=1

    if use_elitist==1:
        print(population[0].value, getFitness(population[0]))
        next_generation.append(population[0])
        
        for i in range(len(population)-1):
            number=random.uniform(0,1)
            
            idx=binarySearch(fitness_list,0,len(fitness_list)-1,number)

            intermediary_population.append(population[idx])

        intermediary_population2=crossingOverStep(intermediary_population)
    

        intermediary_population3=mutation(intermediary_population2)
        intermediary_population3.append(next_generation[0])

    elif use_elitist==0:
        for i in range(len(population)):
            number=random.uniform(0,1)
            
            idx=binarySearch(fitness_list,0,len(fitness_list)-1,number)

            intermediary_population.append(population[idx])

        intermediary_population2=crossingOverStep(intermediary_population)
    
        intermediary_population3=mutation(intermediary_population2)


    return intermediary_population3

if __name__ == '__main__':
    file=open("/home/bogdan/Documents/Cursuri facultate/Anul 2/Semestrul 2/Algoritmi Avansati/Teme/Tema 2/data.txt","r")
    out=open("/home/bogdan/Documents/Cursuri facultate/Anul 2/Semestrul 2/Algoritmi Avansati/Teme/Tema 2/output.txt","w")
    cnt=0
    global a
    global b
    global precision
    global coef_grad1
    global coef_grad2
    global coef_grad0
    global prob_crossover
    global prob_mutation
    for line in file.readlines():
        line=line.split()
        if cnt==0:
            dim_pop=int(line[0])
        elif cnt==1:
            if line[0][0]=='-':
                a=int(line[0].split('-')[1])
                a=a*(-1)
            else:
                a=int(line[0][0])

            if line[1][0]=='-':
                b=int(line[1].split('-')[1])
                b=b*(-1)
            else:
                b=int(line[1][0])
        
        elif cnt==2:
            if line[0][0]=='-':
                coef_grad2=int(line[0].split('-')[1])
                coef_grad2=coef_grad2*(-1)
            else:
                coef_grad2=int(line[0][0])

            if line[1][0]=='-':
                coef_grad1=int(line[1].split('-')[1])
                coef_grad1=coef_grad1*(-1)
            else:
                coef_grad1=int(line[1][0])

            if line[2][0]=='-':
                coef_grad0=int(line[2].split('-')[1])
                coef_grad0=coef_grad0*(-1)
            else:
                coef_grad0=int(line[2][0])
        
        elif cnt==3:
            precision=int(line[0])

        elif cnt==4:
            prob_crossover=float(line[0])

        elif cnt==5:
            prob_mutation=float(line[0])

        elif cnt==6:
            steps=int(line[0])
            
        cnt+=1
    
    
    print(dim_pop,a,b,coef_grad2,coef_grad1,coef_grad0,precision,prob_crossover,prob_mutation,steps,sep=" ")

    global nr_of_bits_codification
    nr_of_bits_codification=calculateNrOfBitsCodification()

    global pace
    pace=getPace()

    population=[]
    for i in range(dim_pop):
      individ=Individ()
      population.append(individ)

    print('Vrei sa folosesti criteriul elitist? Raspunde cu da sau nu')
    x= input()

    if x=='da':
        answer=1
    else:
        answer=0

    for i in range(steps):
        
        next_generation = generateNextGeneration(population,answer)
        population = next_generation
        out.write(str(i) + '\n')
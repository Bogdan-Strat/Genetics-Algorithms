import math
from decimal import *
import random
#import matplotlib.pyplot as plt

def calculateNrOfBitsCodification():
    aux=precision

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
  def __init__(self,value=None,cromozom=None):
    self.value=value or round(random.uniform(a,b),precision+1)
    self.cromozom=cromozom or self.encode()

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

def crossOver(individ1,individ2,make_out):
    breakpoint=random.randint(0,len(individ1.cromozom))
    prefix_cromozom1=""
    prefix_cromozom2=""

    if make_out==1:
        out.write(individ1.cromozom + ' ' + individ2.cromozom + ' punct   ' + str(breakpoint) + '\n')
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

    individ11=Individ(individ1.value,individ1.cromozom)
    individ22=Individ(individ2.value,individ2.cromozom)
    #individ11.value=individ1.value
    #individ11.cromozom=individ1.cromozom

    #individ22.value=individ2.value
    #individ22.cromozom=individ2.cromozom

    if make_out==1:
        out.write('Rezultat    ' + individ11.cromozom + ' ' + individ22.cromozom + '\n')
    
    return [individ11,individ22]

def crossingOverStep(intermediary_population,make_out):
    population_for_crossing=[]
    intermediary_population2=[]
    index_list=[]
    cnt=0
    for individ in intermediary_population:
        number=random.uniform(0,1)
        
        cnt+=1
        if make_out==1:
            out.write(str(cnt) + ': ' + individ.cromozom + ' u=' + str(number))


        if number<=prob_crossover:
            ind=Individ(individ.value,individ.cromozom)
            #ind.value=individ.value
            #ind.cromozom=individ.cromozom
            population_for_crossing.append(ind)
            index_list.append(cnt)

            if make_out==1:
                out.write('<' + str(prob_crossover) + ' participa\n')
        else:

            if make_out==1:
                out.write('\n')
            intermediary_population2.append(individ)

    if len(population_for_crossing)==1:
        intermediary_population2.append(population_for_crossing[0])
        population_for_crossing.pop()
        pass
    elif len(population_for_crossing)%2==1:
        intermediary_population2.append(population_for_crossing[len(population_for_crossing)-1])
        population_for_crossing.pop()
    
    i=0
    if make_out==1:
        out.write('\n')

    while i<len(population_for_crossing):
        if make_out==1:
            out.write('Recombinare dintre cromozomul %d cu cromozomul %d:\n' % (index_list[i] , index_list[i+1]))
        elm=crossOver(population_for_crossing[i],population_for_crossing[i+1],make_out)
        intermediary_population2.append(elm[0])
        intermediary_population2.append(elm[1])
        i+=2
    
    return intermediary_population2

def mutation(intermediary_population2,make_out):
    intermediary_population3=[]
    cnt=0
    for individ in intermediary_population2:
        aux=""
        cnt+=1
        for gene in individ.cromozom:
            u=random.uniform(0,1)
            if u<=prob_mutation:
                if gene=='0':
                    aux+='1'
                else:
                    aux+='0'
                
                if make_out==1:
                    out.write('%d\n' % cnt)
            else:
                aux+=gene

        individ.cromozom="".join([x for x in list(aux)])
        individ.value=individ.decode()

        individ1=Individ(individ.value,individ.cromozom)
        #individ1.value=individ.value
        #individ1.cromozom=individ.cromozom
        intermediary_population3.append(individ1)

    return intermediary_population3


def generateNextGeneration(population,use_elitist,make_out):
    next_generation=[]
    intermediary_population=[]
    fitness_list=[]

    if make_out==1:
        cnt=0
        out.write('Populatia initiala:\n')
        for individ in population:
            cnt+=1
            out.write('    '+str(cnt)+': ' + str(individ.cromozom) + ' x= '+ str(individ.value)+ ' f='+ str(getFitness(individ))+'\n')
        out.write('\n\n')
    

    total_fitness=0
    fitness_list.append(0)
    for individ in population:
        total_fitness+=getFitness(individ)

    fit=0
    cnt=0
    if make_out==1:
        out.write('Probabilitati de selectie:\n')
    for individ in population:
        if make_out==1:
            cnt+=1
            out.write('cromozom     '+str(cnt)+ ' probabilitate '+ str(getFitness(individ)/total_fitness)+'\n')
        fit+=getFitness(individ)/total_fitness
        fitness_list.append(fit)
    
    if make_out==1:
        out.write('\n')
        out.write('Intervale probabilitati selectie:\n')
        for interval in fitness_list:
            out.write(str(interval)+' ')
        out.write('\n')

    fitness_list[len(population)]=1

    if use_elitist==1:
        aux=[]
        for individ in population:
            ind=Individ(individ.value,individ.cromozom)
            #ind.value=individ.value
            #ind.cromozom=individ.cromozom
            aux.append(ind)

        aux.sort(key = lambda elem : (-getFitness(elem)))
        next_generation.append(aux[0])
        
        for i in range(len(population)-1):
            number=random.uniform(0,1)
            
            idx=binarySearch(fitness_list,0,len(fitness_list)-1,number)

            intermediary_population.append(population[idx])

            if make_out==1:
                out.write('u= '+str(number)+' selectam cromozomul '+str(idx+1)+'\n')
        
        if make_out==1:
            cnt=0
            out.write('Dupa selectie:\n')
            for individ in intermediary_population:
                cnt+=1
                out.write('    '+str(cnt)+': '+ individ.cromozom +  ' x= ' + str(individ.value)+ ' f=' + str(getFitness(individ))+ '\n')


        if make_out==1:
            out.write('\nProbabilitatea de incrucisare ' + str(prob_crossover) + '\n')

        intermediary_population2=crossingOverStep(intermediary_population,make_out)
    
        if make_out==1:
            out.write('Dupa recombinare:\n')
            cnt=0
            for individ in intermediary_population2:
                cnt+=1
                out.write('   ' + str(cnt) + ': ' + individ.cromozom + ' x= ' + str(individ.value) + ' f=' + str(getFitness(individ)) + '\n')
            
        if make_out==1:
            out.write('\nProbabilitatea de mutatie pentru fiecare gena %d\nAufost modificati cromozomii:\n' % prob_mutation) 

        intermediary_population3=mutation(intermediary_population2,make_out)
        
        if make_out==1:
            out.write('\nDupa mutatie:\n')
            cnt=0
            for individ in intermediary_population3:
                cnt+=1
                out.write('   ' + str(cnt) + ': ' + individ.cromozom + ' x= '  + str(individ.value) + ' f=' + str(getFitness(individ)) + '\n')

        intermediary_population3.append(next_generation[0])

    elif use_elitist==0:
        for i in range(len(population)):
            number=random.uniform(0,1)
            
            idx=binarySearch(fitness_list,0,len(fitness_list)-1,number)

            intermediary_population.append(population[idx])
        
            if make_out==1:
                out.write('u= '+str(number)+' selectam cromozomul '+str(idx+1)+'\n')

        if make_out==1:
            cnt=0
            out.write('Dupa selectie:\n')
            for individ in intermediary_population:
                cnt+=1
                out.write('    '+str(cnt)+': '+ individ.cromozom +  ' x= ' + str(individ.value)+ ' f=' + str(getFitness(individ))+ '\n')


        if make_out==1:
            out.write('\nProbabilitatea de incrucisare ' + str(prob_crossover) + '\n')

        intermediary_population2=crossingOverStep(intermediary_population,make_out)
    
        if make_out==1:
            out.write('Dupa recombinare:\n')
            cnt=0
            for individ in intermediary_population2:
                cnt+=1
                out.write('   ' + str(cnt) + ': ' + individ.cromozom + ' x= ' + str(individ.value) + ' f=' + str(getFitness(individ)) + '\n')
            
        if make_out==1:
            out.write('\nProbabilitatea de mutatie pentru fiecare gena ' + str(prob_mutation) + '\nAufost modificati cromozomii:\n') 

        intermediary_population3=mutation(intermediary_population2,make_out)

        if make_out==1:
            out.write('\nDupa mutatie:\n')
            cnt=0
            for individ in intermediary_population3:
                cnt+=1
                out.write('   ' + str(cnt) + ': ' + individ.cromozom + ' x= '  + str(individ.value) + ' f=' + str(getFitness(individ)) + '\n')

    return intermediary_population3

if __name__ == '__main__':
    file=open("data.txt","r")
    out=open("output.txt","w")
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

    maximum_evolution=[]
    for i in range(steps):
        if i==0:
            next_generation=generateNextGeneration(population,answer,1)
            out.write('\nEvolutia maximului:\n')
        else:
            
            maxi=0
            for individ in next_generation:
                if getFitness(individ)>maxi:
                    maxi=getFitness(individ)
            out.write(str(maxi) + '\n')
            maximum_evolution.append(maxi)
            next_generation = generateNextGeneration(population,answer,0)
        population = next_generation
 
    
    plt.plot(maximum_evolution)
    plt.ylabel('Maximum evolution')
    plt.show()
    

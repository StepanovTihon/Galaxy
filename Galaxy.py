import pygame, threading
import time
import numpy as np
import random
import math
import time as tm





class Neyro():
    def __init__(self,  neyroinput,  neyrohidden, neyrohidden2,  neyroexit):#Создаём нейронку
#        super().__init__()

        self.neyroinput = neyroinput
        self.neyrohidden = neyrohidden
        self.neyrohidden2 = neyrohidden2
        self.neyroexit = neyroexit
        self.score=0
        self.exit=0
        self.inputmass = np.array([1.0 for i in range(self.neyroinput)])
        self.hiddenmass = np.array([1.0 for i in range(self.neyrohidden)])
        self.hiddenmass2 = np.array([1.0 for i in range(self.neyrohidden2)])
        self.exitmass = np.array([1.0 for i in range(self.neyroexit)]) 
        self.coofIn = np.ones((self.neyroinput,  self.neyrohidden))
        self.coofCentr = np.ones((self.neyrohidden,  self.neyrohidden2))
        self.coofOut = np.ones((self.neyrohidden2,  self.neyroexit))
        for i in range(self.neyroinput):
            for j in range(self.neyrohidden): 
                self.coofIn[i][j] = (random.random()-0.5)*2
        for i in range(self.neyrohidden):
            for j in range(self.neyrohidden2):
                self.coofCentr[i][j] = (random.random()-0.5)*2 
        for i in range(self.neyrohidden2):
            for j in range(self.neyroexit):
                self.coofOut[i][j] = (random.random()-0.5)*2 

    def sigmoid(self, x):#Активация
        return math.tanh(x)

    def update(self,  field):#нахождение выходов
        self.field=field

        for i in range(self.neyroinput):
            self.inputmass[i]=self.field[i]

        for j in range(self.neyrohidden):
            sum = 0.0
            for i in range(self.neyroinput):
                sum = sum + self.inputmass[i] * self.coofIn[i][j]
            self.hiddenmass[j] = self.sigmoid(sum)
        for j in range(self.neyrohidden2):
            sum = 0.0
            for i in range(self.neyrohidden):
                sum = sum + self.hiddenmass[i] * self.coofCentr[i][j]
            self.hiddenmass2[j] = self.sigmoid(sum)
        for k in range(self.neyroexit):
            sum = 0.0
            for j in range(self.neyrohidden2):
                sum = sum + self.hiddenmass2[j] * self.coofOut[j][k]
            self.exitmass[k] = self.sigmoid(sum)
        ind_bolh=np.argmax(self.exitmass)

        
        return ind_bolh



class pole():
    def __init__(self):
        self.surface = np.array([0 for i in range(9)])

    def Draw(self,trig):
        if(trig):
            tmp= np.array(['a' for i in range(9)])
            
            for i in range(9):
                if(self.surface[i]==0):
                    tmp[i]='-'
                if(self.surface[i]==1):
                    tmp[i]='x'
                if(self.surface[i]==-1):
                    tmp[i]='o'                                

            for i in range(0,9,3):
                print(tmp[i]+" "+tmp[i+1]+" "+tmp[i+2])

class Generic():
    def __init__(self, quantity, field):#Генетический алгоритм
        self.generation=0
        self.input=9
        self.hidden=40
        self.hidden2=20
        self.landing=9
        self.exit=4
        self.stat=0
        self.field=field
        self.personQuantity=quantity
        self.persons = np.array([Neyro(self.input,  self.hidden,  self.hidden2,   self.exit) for i in range(self.personQuantity)]) 
    
    def Stats(self,trig,soob):
        if(trig==1):
            print(soob)

    def Save(self,plan):
        f = open("abc", "w")
        for i in range(self.personQuantity):
            for k in range(self.persons[i].neyroinput):
                for n in range(self.persons[i].neyrohidden): 
                    f.write(str(self.persons[i].coofIn[k][n])+"\n")
            for k in range(self.persons[i].neyrohidden):
                for n in range(self.persons[i].neyrohidden2):
                    f.write(str(self.persons[i].coofCentr[k][n])+"\n")
            for k in range(self.persons[i].neyrohidden2):
                for n in range(self.persons[i].neyroexit):
                    f.write(str(self.persons[i].coofOut[k][n])+"\n")
        for i in range(len(plan)):
            f.write(str(plan[i])+"\n")
        f.write(str(self.landing)+"\n")
        f.write(str(self.generation)+"\n")
        

        f.close()

    def load(self,plan,pyg):
        f = open("abc", "r")#.readline()
        for i in range(self.personQuantity):
            for k in range(self.persons[i].neyroinput):
                for n in range(self.persons[i].neyrohidden): 
                    self.persons[i].coofIn[k][n]=float(f.readline())
            for k in range(self.persons[i].neyrohidden):
                for n in range(self.persons[i].neyrohidden2):
                    self.persons[i].coofCentr[k][n]=float(f.readline())
            for k in range(self.persons[i].neyrohidden2):
                for n in range(self.persons[i].neyroexit):
                    self.persons[i].coofOut[k][n]=float(f.readline())
        for i in range(len(plan)):
            plan[i]=int(f.readline())
        self.landing=int(f.readline())
        self.generation=int(f.readline())


        f.close()

    def Win(self):
        if(abs(self.field.surface[0]+self.field.surface[1]+self.field.surface[2])==3):
            if(self.field.surface[0]==1):
                return 1
            elif(self.field.surface[0]==-1):
                return -1
        if(abs(self.field.surface[3]+self.field.surface[4]+self.field.surface[5])==3):
            if(self.field.surface[3]==1):
                return 1
            elif(self.field.surface[3]==-1):
                return -1
        if(abs(self.field.surface[6]+self.field.surface[7]+self.field.surface[8])==3):
            if(self.field.surface[6]==1):
                return 1
            elif(self.field.surface[6]==-1):
                return -1
        if(abs(self.field.surface[0]+self.field.surface[3]+self.field.surface[6])==3):
            if(self.field.surface[0]==1):
                return 1
            elif(self.field.surface[0]==-1):
                return -1
        if(abs(self.field.surface[1]+self.field.surface[4]+self.field.surface[7])==3):
            if(self.field.surface[1]==1):
                return 1
            elif(self.field.surface[1]==-1):
                return -1
        if(abs(self.field.surface[2]+self.field.surface[5]+self.field.surface[8])==3):
            if(self.field.surface[2]==1):
                return 1
            elif(self.field.surface[2]==-1):
                return -1
        if(abs(self.field.surface[0]+self.field.surface[3]+self.field.surface[8])==3):
            if(self.field.surface[0]==1):
                return 1
            elif(self.field.surface[0]==-1):
                return -1
        if(abs(self.field.surface[2]+self.field.surface[4]+self.field.surface[6])==3):
            if(self.field.surface[2]==1):
                return 1
            elif(self.field.surface[2]==-1):
                return -1
        return 0
                                



    def check(self):#Отбор
        
        for i in range(0,self.personQuantity,2):
                while(self.persons[i].exit==0):

                    self.field.Draw(self.stat)
                    self.Stats(self.stat," Ходит первый игрок ")
                    if(self.field.surface[self.persons[i].update(self.field.surface)]==0):
                        self.field.surface[self.persons[i].update(self.field.surface)]=1
                        self.persons[i].score+=10
                    
                    else:
                        self.Stats(self.stat," Первый игрок неверный ход "+str(self.persons[i].update(self.field.surface)))
                        self.persons[i].score-=100
                        self.persons[i].exit=1
                        self.persons[i+1].exit=1 
                        self.field.surface = np.array([0 for i in range(9)])
                    if(self.Win()==1):
                        self.Stats(self.stat," Выйграл первый игрок ")
                        self.persons[i].score+=100
                        self.persons[i+1].score-=100
                        self.persons[i].exit=1
                        self.persons[i+1].exit=1 
                        self.field.surface = np.array([0 for i in range(9)])


                    self.field.Draw(self.stat)
                    
                    self.Stats(self.stat," Ходит второй игрок ")
                    if(self.field.surface[self.persons[i+1].update(self.field.surface*-1)]==0):
                        self.field.surface[self.persons[i+1].update(self.field.surface)]=-1
                        self.persons[i+1].score+=10
                    
                    else:
                        self.Stats(self.stat," Второй игрок неверный ход "+str(self.persons[i+1].update(self.field.surface)))
                        self.persons[i+1].score-=100
                        self.persons[i+1].score=0
                        self.persons[i+1].exit=1
                        self.persons[i].exit=1
                        self.field.surface = np.array([0 for i in range(9)])

                    if(self.Win()==1):
                        self.Stats(self.stat," Выйграл второй игрок ")
                        self.persons[i].score-=100
                        self.persons[i+1].score+=100
                        self.persons[i+1].exit=1
                        self.persons[i].exit=1
                        self.field.surface = np.array([0 for i in range(9)])
                if(self.stat==1):
                    print(self.persons[i].score)
                    print(self.persons[i+1].score)



        
                                
    def sort(self):#сортировка
        person_tmp=Neyro(self.input,  self.hidden,   self.hidden2,  self.exit)
        for i in range(self.personQuantity):
            for j in range(self.personQuantity-i-1):
                if(self.persons[j].score > self.persons[j+1].score):
                    person_tmp = self.persons[j]
                    self.persons[j]=self.persons[j+1]
                    self.persons[j+1]= person_tmp
    def crossing(self, person1, person2):#Скрещивание
        tmp_person=Neyro(self.input,  self.hidden,  self.hidden2,  self.exit)
        for i in range(person1.neyroinput):
            for j in range(person1.neyrohidden):
                tmp_person.coofIn[i, j]=(person1.coofIn[i, j]+person2.coofIn[i, j])/2
        for i in range(person1.neyrohidden):
            for j in range(person1.neyrohidden2):
                tmp_person.coofCentr[i, j]=(person1.coofCentr[i, j]+person2.coofCentr[i, j])/2
        for i in range(person1.neyrohidden2):
            for j in range(person1.neyroexit):
                tmp_person.coofOut[i, j]=(person1.coofOut[i, j]+person2.coofOut[i, j])/2
        return tmp_person

    def mutation(self, person_mutant):#Мутация
        for i in range(person_mutant.neyroinput):
            for j in range(person_mutant.neyrohidden):
                if(random.randint(0, 100)<=10):
                    person_mutant.coofIn[i, j]+=(random.random()-0.5)*2
        for i in range(person_mutant.neyrohidden):
            for j in range(person_mutant.neyrohidden2):
                if(random.randint(0, 100)<=10):
                    person_mutant.coofCentr[i, j]+=(random.random()-0.5)*2
        for i in range(person_mutant.neyrohidden2):
            for j in range(person_mutant.neyroexit):
                if(random.randint(0, 100)<=10):
                    person_mutant.coofOut[i, j]+=(random.random()-0.5)*2
        return person_mutant

    def evolution(self):#Создание нового поколения
        #self.pyg.Update(self.generation, self.top)
        self.generation+=1
        next_persons = np.array([Neyro(self.input,  self.hidden,  self.hidden2,   self.exit) for i in range(self.personQuantity)]) 
        for i in range(self.personQuantity):
            next_persons[i]=self.crossing(self.persons[int(random.random()*(self.personQuantity/2)+(self.personQuantity/2))], 
                                          self.persons[int(random.random()*(self.personQuantity/2)+(self.personQuantity/2))])
            next_persons[i]=self.mutation(next_persons[i])
        next_persons[0]=self.persons[self.personQuantity-1]
        next_persons[1]=self.persons[self.personQuantity-2]
        next_persons[0].exit=0
        next_persons[1].exit=0
        next_persons[0].score=0
        next_persons[1].score=0                                 
                                 
        self.persons=next_persons

map=pole()
gen=Generic(10,map)
while(True):

    gen.check()

    gen.sort()
    gen.evolution()
    if(gen.generation>100):
        gen.stat=1
        print("---------------------")



























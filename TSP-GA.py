import random
import matplotlib.pyplot as plt
import math
import numpy as np




class individuo():
    
    def __init__(self, quantidade_cidades):
        self.quantidade_cidades = quantidade_cidades
        self.rota = []
        self.avaliacao = 0
      
    def printRota(self):
        print(str(self.rota))
        
    # Gera uma lista aletoria com valores de 1 até N
    def permutacaoAleatoria(self, N):
        k = 1
        diffs = {}
        while k < N // 4:
            r = random.randint(k, N)
            yield diffs[r] if r in diffs else r
            diffs[r] = diffs[k] if k in diffs else k
            k += 1
        vbase = k
        v = list(range(vbase, N+1))
        for i, s in diffs.items():
            if i >= vbase:
                v[i - vbase] = s
        del diffs
        while k <= N:
            r = random.randint(k, N)
            rv = v[r - vbase]
            v[r - vbase] = v[k - vbase]
            yield rv
            k += 1
    
    # Gera uma rota aleatória
    def gerarAleatorio(self):
        self.rota = list(self.permutacaoAleatoria(self.quantidade_cidades))
    
    # Atribui uma rota existente
    def atribuirRota(self, rota):
        self.rota = rota
    
    # Crossover: define o ponto de corte na metade, copia so dados do primeiro pai e as cidades restantes são adicioandas na ordem em que aparece na rota do segundo pai.
    def crossover(self, outro, taxaCruzamento):
        if random.random() < taxaCruzamento:
            ponto_corte = round(self.quantidade_cidades/2)
            rotaFilho = []
            
            # Copiando metade das caracteristicas do primeiro pai para o filho
            for i in range(0, ponto_corte):
                rotaFilho.append(self.rota[i])
                
            # Copiando cidades restantes respeitando a ordem do segundo pai
            for i in range(0, self.quantidade_cidades):
                if not outro.rota[i] in rotaFilho:
                    rotaFilho.append(outro.rota[i])
    
            # Gerando instancia do filho
            filho = individuo(self.quantidade_cidades)
            filho.atribuirRota(rotaFilho)
            return(filho)
        else:
            return self
        
    # Executa mutacao a uma dada probabilidade, cujo valor deve ser de 0 a 1. A mutacao sorteia duas posicaoes aleatorias de cidades e troca elas
    def mutacao(self, probMutacao):
        if random.random() < probMutacao:
            i1 = random.randint(0, self.quantidade_cidades-1)
            i2 = random.randint(0, self.quantidade_cidades-1)
            while(i2 == i1):
                i2 = random.randint(0, self.quantidade_cidades-1)
            aux = self.rota[i1]
            self.rota[i1] = self.rota[i2]
            self.rota[i2] = aux
                
    #Define a avaliação das soluções
    def avaliarSolucao(self, cidades):
        dist = 0
        last = 0
        first = -1
        for i in range(1, self.quantidade_cidades):
            c1 = cidades[self.rota[i-1]-1]
            c2 = cidades[self.rota[i]-1]
            if first == -1:
                first = c1
            dist = dist + math.sqrt(math.pow((c2[1] - c1[1]),2)+math.pow((c2[2] - c1[2]),2))
            last = c2
        #Teorema de Pitágoras para calcular a distância entre as cidades
        dist = dist + math.sqrt(math.pow((last[1] - first[1]),2)+math.pow((last[2] - first[2]),2))
        self.avaliacao = dist
        
    def plotSolucao(self, cidades):
        x = [] # latitudes
        y = [] # longitudes
        cores = []
        cor = 0
        for i in self.rota:
            x.append(cidades[i-1][1])
            y.append(cidades[i-1][2])
            cores.append(cor)
            cor = cor + 5
        
        plt.scatter(x, y, c=cores, alpha=0.5)
        plt.plot(x,y)
        plt.title("Solução de Rota")
        plt.show()
            
        


class algoritmo_genetico():
    def __init__(self):
        self.cidades = []
        self.x_coordenadas = []
        self.y_coordenadas = []
        self.cidadades_cores = []
        self.quantidade_cidades = 0
        self.taxaCruzamento = 0
        self.taxaMutacao = 0
        self.tamanhoPopulacao = 0
        self.numeroMaximoIteracoes = 0
        self.populacao = []
        self.filhos = []
        self.melhorSolucaoAvaliacao = float("inf")
        self.melhorSolucao = None

    def carregarProblema(self, filePath):
        # Pegando as linhas das cidades
        arq = open(filePath, "r")
        linhas = arq.readlines()
        arq.close()
        linhas = linhas[6:] # excluindo as 6 primeiras linhas
        linhas.pop() # excluindo a ultima linha

        # Resetando variaveis
        self.cidades = []
        self.x_coordenadas = []
        self.y_coordenadas = []
        self.cidadades_cores = []
        
        # Percorrendo cidades, salvando id, coordenadas e um valor para cor incrementado de 5
        c = 0
        for l in linhas:
            cidade = int(l.split()[0])
            lat = float(l.split()[1])
            lon = float(l.split()[2])
            self.cidades.append([cidade, lat, lon])
            self.x_coordenadas.append(lat)
            self.y_coordenadas.append(lon)
            self.cidadades_cores.append(c)
            c = c + 5
        self.quantidade_cidades = len(self.cidades)
    
    #Define os parâmetros    
    def definirParametros(self, taxaCruzamento, taxaMutacao, tamanhoPopulacao, numeroMaximoIteracoes):
        self.taxaCruzamento = taxaCruzamento
        self.taxaMutacao = taxaMutacao
        self.tamanhoPopulacao = tamanhoPopulacao
        self.numeroMaximoIteracoes = numeroMaximoIteracoes

    # Plota o mapa de cidaes (pontos em um grafico bidimensional)
    def printMapaCidades(self, transparencia):
        plt.scatter(self.x_coordenadas, self.y_coordenadas, c=self.cidadades_cores, alpha=transparencia)
        plt.title("Mapa de Cidades")
        plt.show()
    
    # Gera uma populacao inicial e avalia.
    def gerarPopulacaoInicialAvaliada(self):
        for i in range(self.tamanhoPopulacao):
            ind = individuo(self.quantidade_cidades)
            ind.gerarAleatorio()
            ind.avaliarSolucao(self.cidades)
            self.populacao.append(ind)
            
    # Executa torneio com 2 individuos
    def fazTorneio(self):
        ind1 = random.randint(0, self.tamanhoPopulacao-1)
        ind2 = random.randint(0, self.tamanhoPopulacao-1)
        while(ind2 == ind1):
            ind2 = random.randint(0, self.tamanhoPopulacao-1)
        
        vencedor = None
        if (self.populacao[ind1].avaliacao >= self.populacao[ind2].avaliacao):
            vencedor = self.populacao[ind1]
        else:
            vencedor = self.populacao[ind2]
        return(vencedor)
    
    # Calcula melhor fitness e retorna nova populacao
    def geraNovaPopulacao_MelhorFitness(self, pais, filhos):
        todos = pais + filhos
        todosAvaliacao = []
        todosIndices = []
        
        ind = 0
        for i in todos:
            todosAvaliacao.append(i.avaliacao)
            todosIndices.append(ind)
            ind = ind + 1
        
        
        
        todosOrdenados = [x for _,x in sorted(zip(todosAvaliacao,todosIndices))]
        novaPopulacaoIndices = todosOrdenados[0:self.tamanhoPopulacao]
        novaPopulacao = []
        for i in novaPopulacaoIndices:
            novaPopulacao.append(todos[i])
       
        if novaPopulacao[0].avaliacao < self.melhorSolucaoAvaliacao:
            #print(str(novaPopulacao[0].avaliacao)+" <"+str(self.melhorSolucaoAvaliacao))
            self.melhorSolucao = novaPopulacao[0]
            self.melhorSolucaoAvaliacao = self.melhorSolucao.avaliacao
            
        self.filhos = []
        return(novaPopulacao)
        
    #Calcula o avanço das avaliações    
    def calculaAvancoFitness(self):
        fitness = []
        for i in self.populacao:
            fitness.append(i.avaliacao)
        melhor = min(fitness)
        media = np.mean(fitness)
        return([melhor, media])
        

    # Executa o algoritmo genetico
    def executar(self):
        # Gerando a populacao inicial e avaliando-a.
        self.gerarPopulacaoInicialAvaliada()
        
        # Array para geracao de filhos
        self.filhos = []
        
        
        self.evolucaoMelhorFitness = []
        self.evolucaoFitnessMedio = []
        
        # Executando geracoes
        for i in range(self.numeroMaximoIteracoes):
            
            # Selecao de pais, cruzamento e mutacao
            for j in range(self.tamanhoPopulacao//2):
                p1 = self.fazTorneio()
                p2 = self.fazTorneio()
                f1 = p1.crossover(p2, self.taxaCruzamento)
                f2 = p2.crossover(p1, self.taxaCruzamento)
                f1.mutacao(self.taxaMutacao)
                f2.mutacao(self.taxaMutacao)
                
                f1.avaliarSolucao(self.cidades)
                f2.avaliarSolucao(self.cidades)
                self.filhos.append(f1)
                self.filhos.append(f2)
        
            # Substituicao: criando nova populacao com os melhores
            self.populacao = self.geraNovaPopulacao_MelhorFitness(self.populacao, self.filhos)
            
            # Parametros algoritmo
            valores = self.calculaAvancoFitness()
            self.evolucaoMelhorFitness.append(valores[0])
            self.evolucaoFitnessMedio.append(valores[1])
            print("Geraçao "+str(i+1)+" - Melhor fitness: "+str("{:.2f}".format(self.evolucaoMelhorFitness[-1]))+" - Fitness médio: "+str("{:.2f}".format(self.evolucaoFitnessMedio[-1])))
            
    #Imprime os gráficos com estatísticas finais    
    def estatisticasFinais(self):
        
        plt.plot(self.evolucaoMelhorFitness)
        plt.title("Evolucão melhor fitness")
        plt.show()
        
        plt.plot(self.evolucaoFitnessMedio)
        plt.title("Evolucão fitness Médio")
        plt.show() 
        
        self.melhorSolucao.plotSolucao(self.cidades)
    
        
       
        
taxaMutacao = 0.25
taxaCruzamento = 0.75
tamanhoPopulacao = 100 # MANTER PAR, POIS 2 PAIS GERAM 2 FILHOS
numeroMaximoIteracoes = 5000

obj = algoritmo_genetico()
obj.carregarProblema("C:/Users/Nilton/OneDrive/Documentos/Nilton/MESTRADO/Disciplinas/Introdução a Meta Heurística/Segunda Parte/Atividades/Instancias usadas/rd100.tsp")
obj.printMapaCidades(1)
obj.definirParametros(taxaCruzamento, taxaMutacao, tamanhoPopulacao, numeroMaximoIteracoes)
obj.executar()
obj.estatisticasFinais()


# Melhor rota
indOtimo = individuo(obj.quantidade_cidades)
indOtimo.atribuirRota([1, 18, 62, 87, 15, 63, 86, 97, 67, 13, 49, 21, 75, 82, 85, 14, 12, 4, 32,  9, 26, 74, 20, 78, 3, 33, 10, 27, 92, 17, 72, 70, 38, 54, 73, 50, 46, 56, 19, 37, 28, 93, 77, 95, 59, 76, 58, 89, 2, 23, 35, 29, 44, 100, 39, 96, 55, 40, 43, 25, 24, 42, 7, 34, 41, 22, 5, 61, 11, 52, 45, 16, 31, 84, 88, 66, 98, 94, 6, 79, 53, 99, 47, 57, 36, 64, 91, 81, 80, 30, 48, 65, 90, 51, 83, 68, 71, 8, 69, 60])
indOtimo.avaliarSolucao(obj.cidades)
indOtimo.plotSolucao(obj.cidades)
print("Avaliação ótimo global "+str(indOtimo.avaliacao))
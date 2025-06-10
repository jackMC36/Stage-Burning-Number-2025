from typing import List, Tuple
import networkx as nx
import matplotlib.pyplot as plt

import copy

##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
cpt = 0
class Graph:
    '''Un graph G=(V,E)
    V est l'ensemble des sommets brulés
    E est l'ensemble des arêtes
    '''


    def __init__(self,V: List[int],E: List[Tuple[int,int]]):
        '''Le constructeur spécifie une liste de sommet V, et une liste d'aretes E.'''
        self.V = V
        self.E = E

    def get_vertices(self) -> List[int]:
        return self.V
    
    def get_edges(self) -> list[Tuple[int,int]]:
        return self.E
    
    def get_neigbhors(self,s:int) -> List[int]:
        l = []
        for e in self.E:
            if s == e[0]:
                l.append(e[1])
            if s == e[1]:
                l.append(e[0])
        return l
    
    def txt_file_to_graph(self, fd: str) -> None:
        '''Lit un fichier texte et remplit les sommets et arêtes du graphe.'''
        V = set()
        E = set()
        file = open(fd, "r")
        lines = file.readlines()
        n = int(lines[0].strip()) 
        for i in range(1,len(lines)):
            line = lines[i]
            node = i
            neighbors = [int(x) for x in line.strip().split()]
            V.add(node)
            for neighbor in neighbors:
                V.add(neighbor)
                if node < neighbor:
                    E.add((node, neighbor))
                else:
                    E.add((neighbor, node))
        self.V = list(sorted(V))
        self.E = list(E)

    def __str__(self):
        return "Vertices: \n" + self.V.__str__() + "\n" + "Edges: \n" + self.E.__str__() + "\n"
    
    def show(self):
        '''Affiche le graphe avec networkx et matplotlib.'''
        G = nx.Graph()
        G.add_nodes_from(self.V)
        G.add_edges_from(self.E)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='orange', edge_color='gray')
        plt.show()


##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################

class Etat:
    '''
    Un Etat decrit un Graph Connexe (B,NB,E). 
    B l'ensemble des sommets brulés.
    NB l'ensemble des sommets non brulés.
    E l'ensemble des arretes.
    n le numero de la sequence.
    B_v la liste de sommets v brulés par la balle de taille B.
    C la liste du sommet au centre de chaque balle.
    '''
    def __init__(self, NB: set[int], B: set[int], E: List[Tuple[int, int]], n: int, B_v : List[List[int]], C : List[int]):
        '''Le constructeur spécifie une liste de sommets non-brulés NB, une liste de sommets brulés B,  et une liste de arêtes E, un entier n correspondant à la taille de la balle maximale, et B_v une liste de liste de taille |V|*B correspondant à la liste des sommets brulés par la balle de taille de 1..B.'''
        global cpt
        self.B = set(B)
        self.NB = set(NB)
        self.E = set(E)
        self.n = n
        self.B_v = B_v
        self.C = C
        self.id = cpt
        cpt+=1
    

        score = 0
        for i in range(len(B_v)):
            score+=len(B_v[i])/((i+1)**2)

        self.score = score

    def __str__(self):
        return "------------------------------\n"+"Identifiant de Etat: "+cpt.__str__() +"\n"+"Liste des sommets brulés: " + self.B.__str__() + "\n"+ "sommets non brulés" + self.NB.__str__() + "\n" + "Listes de balles: \n" + self.B_v.__str__() +"\n"+ "score: "+ self.score.__str__() + "\n" + "Sommets centres de balles: \n" + self.C.__str__() + "\n" +"------------------------------\n"

    def get_B_v(self) -> List[List[int]]:
        '''Retourne la liste de sommets v brulés par la balle de taille 1..B'''
        return self.B_v
    
    def get_B(self) -> set[int]:
        '''Retourne la sequence de sommets brulés.'''
        return self.B

    def get_NB(self) -> set[int]:
        '''Retourne la sequence de sommets non-brulés.'''
        return self.NB
        
    def get_n(self) -> int:
        '''Retourne le numero de le burning number actuel. '''
        return self.n
    
    def get_score(self) -> float:
        '''Retourne le score associé à l'état.'''
        return self.score
    
    def get_C(self) -> List[int]:

        return self.C

##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################

class Burning_Number:

    def __init__(self, G: Graph):
        '''Le constructeur specifie le graph G=(V,E).'''
        self.G = G
        self.Etat = Etat(self.G.get_vertices(),[],self.G.get_edges(),0,[],[])

    def etat_initial(self) -> Etat:
        '''Retourne l'état initial'''
        return Etat(self.G.get_vertices(),[],self.G.get_edges(),0,[],[])
    
    def actions(self, etat: Etat) -> set[int]:
        '''Retourne les actions qui peuvent etre prise à partir d'un état donner.'''
        return etat.get_NB()
    
    def propagation(self,etat: Etat) -> Etat:
        '''Retourne l'etat obtenu après avoir propagé le feu.'''
        new_NB = etat.get_NB().copy()
        new_B = etat.get_B().copy()
        new_n = etat.get_n()+1
        new_B_v = copy.deepcopy(etat.get_B_v())
        new_C = etat.get_C().copy()
        
        for i in range(0,len(new_B_v)):
            B_vi_copy = new_B_v[i].copy()
            for v in new_B_v[i]:
                n = self.G.get_neigbhors(v)
                for l in n:
                    if(not(l in new_B_v[i])):
                        if(not l in new_B):
                            new_NB.discard(l)
                            new_B.add(l)
                        new_NB.discard(l)
                        if(not l in new_B_v[i]):
                            B_vi_copy.append(l)
            new_B_v[i] = B_vi_copy

        etat_intermediaire = Etat(new_NB,new_B,self.G.get_edges(),new_n,new_B_v,new_C)
        return etat_intermediaire
    
    def succ(self, etat: Etat, action: int) -> Etat:
        '''Retourne l'etat obtenu après avoir executé une action sur un état.'''


        new_NB = etat.get_NB().copy()
        new_B = etat.get_B().copy()
        new_n = etat.get_n()+1
        new_B_v = copy.deepcopy(etat.get_B_v())
        new_C = etat.get_C().copy()
        
        if(action in etat.get_B()):
            raise ValueError
        
        new_B_v.insert(0,[action])
        new_C.insert(0,action)
        new_B.add(action)
        new_NB.discard(action)
        new_etat = Etat(new_NB,new_B,self.G.get_edges(),new_n, new_B_v,new_C)
        return new_etat
        
        
        
        

    def goal_test(self, etat: Etat) -> bool:
        '''Verifie si l'etat est un etat but. '''
        return etat.get_NB() == set()
    
    def traiter(self) -> List["Noeud"]:
        Racine1 = Noeud(self.etat_initial())
        L_Noeud = [Racine1]
        L_a_traiter = [Racine1]

        while(L_a_traiter != []):
            Courant = L_a_traiter[0]
            L_Enfant = Courant.expand(self)
            L_Enfant_Trie = []
            for n in L_Enfant:
                if L_Enfant_Trie == []:
                    L_Enfant_Trie.append(n)
                else:
                    i = 0
                    while i < len(L_Enfant_Trie) and n.get_Etat().get_score() > L_Enfant_Trie[i].get_Etat().get_score():
                        i +=1
                    L_Enfant_Trie.insert(i,n)
            L_a_traiter.remove(Courant)
            L_a_traiter.extend(L_Enfant_Trie[len(L_Enfant_Trie)//2 : len(L_Enfant_Trie)])
            L_Noeud.extend(L_Enfant_Trie[len(L_Enfant_Trie)//2 : len(L_Enfant_Trie)])
 
        return L_Noeud
    
    def noeuds_goal(self, L_noeud: List["Noeud"]) -> List["Noeud"]:
        '''Retourne la liste des noeuds but, classée du meilleur score au pire'''
        L_goal_noeud = []
        for n in L_noeud:
            if self.goal_test(n.get_Etat()):
                L_goal_noeud.append(n)

        L_goal_noeud.sort(key=lambda n: n.get_Etat().get_score(), reverse=True)
        return L_goal_noeud


    



##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################

class Noeud:
    '''Noeud dans un arbre de recherche. Un noeud contient :
    L'Etat correspondant au noeud
    Un pointeur vers son parent
    L'action menant à cet état
    Le coup pour arriver à ce noeud
    '''

    def __init__(self, Etat: Etat, parent=None, action=None, cout=0, n=0):
        self.Etat = Etat
        self.parent = parent
        self.action = action
        self.cout = cout
        self.depth = 0
        self.n = n
        if parent:
            self.depth = parent.depth + 1


    def get_Etat(self):
        return self.Etat
    
    def get_Cout(self):
        return self.cout

    def child_Noeud(self, problem: Burning_Number, action: int) -> "Noeud":
        '''Retourne le noeud obtenu à partir d'un noeud et une action.'''
        return problem.succ(self.Etat, action)
    
    def get_Children(self):
        L_Children = List[Noeud]
        L_actions = Burning_Number.actions(self.get_Etat())
        for i in L_actions:
            L_Children.append(Burning_Number.succ(self,i))
    
    def expand(self, problem: Burning_Number) -> List["Noeud"]:
        '''Retoune la liste des Noeuds atteignable en une etape à partir du noeud courant.'''
        L_Noeud = []
        Courant = self
        Etat_Intermediaire = problem.propagation(Courant.get_Etat())
        L_actions = problem.actions(Etat_Intermediaire)
        for i in L_actions:
            Etat_enfant = problem.succ(Etat_Intermediaire,i)
            Noeud_enfant = Noeud(Etat_enfant,Courant,i,Courant.get_Cout()+1)
            L_Noeud.append(Noeud_enfant)
        return L_Noeud
    






##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################

## Test ##

G1 = Graph([], [])
G1.txt_file_to_graph("Instances/karate.txt")
B1 = Burning_Number(G1)
L1 = B1.traiter()
L2 = B1.noeuds_goal(L1)
print("########################\n")
print("Il y a un total de " + len(L1).__str__() + " noeuds retenues")
print("Avec un total de " + len(L2).__str__() + " noeuds goals")
print("########################\n")

print("\n")
print("Le meilleur noeud obtenu est:\n")
print(L2[0].get_Etat().__str__())

G1.show()

import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
from tqdm import tqdm

class Point_matcher():
    @staticmethod
    def correlate2d(ecru_defect,traite_defect,tol):
        matching =0
        for defect_e in ecru_defect:
            for defect_t in traite_defect:
                if np.abs((defect_e[0]-defect_t[0])) < 10*tol and np.abs((defect_e[1]-defect_t[1]))<10*tol:
                    matching+=1
                    break
        return matching/len(ecru_defect)

    @staticmethod
    def correlate2d_distance(ecru_defect,traite_defect,tol):#pour le réglage fin : on calcul la somme des distances aux
        dist_tot=-1
        for defect_e in ecru_defect:
            dist_min=np.inf
            for defect_t in traite_defect:
                if np.abs((defect_e[0] - defect_t[0])) < 3 * tol and np.abs((defect_e[1] - defect_t[1])) < 3* tol:
                    dist=np.sqrt((defect_e[0]-defect_t[0])**2+(defect_e[1]-defect_t[1])**2)
                    if dist<dist_min:
                        dist_min=dist
            if dist_min<np.inf:
                dist_tot+=dist_min
        if dist_tot==-1:
            dist_tot=np.inf
        return dist_tot


    @staticmethod
    def flipFabric(tissus):
        for defect in tissus.data:
            defect[1]=tissus.larg_tot-defect[1]

    @staticmethod
    def invertFabric(tissus):
        for defect in tissus.data:
            defect[0]=tissus.long_tot-defect[0]
    #
    # @staticmethod
    # def find_best_horizontal_match(ecru, traite):
    #     best=0
    #     param=0
    #     deltas=[]
    #     cors=[]
    #     for delta in np.arange(1.05,1.1,0.001):
    #         traite_copy = deepcopy(traite)
    #         traite_copy.moveData(delta,1)
    #         cor=Point_matcher.correlate2d(ecru.data, traite_copy.data, 1)
    #         print(delta,cor)
    #         deltas.append(delta)
    #         cors.append(cor)
    #         if cor>best:
    #             best=cor
    #             param=delta
    #     plt.plot(deltas, cors)
    #     plt.show()
    #     return param
    #
    # @staticmethod
    # def find_best_vertical_match(ecru, traite):
    #     best=0
    #     param=0
    #     deltas=[]
    #     cors=[]
    #     for delta in np.arange(1.05,1.1,0.001):
    #         traite_copy = deepcopy(traite)
    #         traite_copy.moveData(1,delta)
    #         cor=Point_matcher.correlate2d(ecru.data, traite_copy.data, 1)
    #         print(delta,cor)
    #         deltas.append(delta)
    #         cors.append(cor)
    #         if cor>best:
    #             best=cor
    #             param=delta
    #     plt.plot(deltas, cors)
    #     plt.show()
    #     return param
    @staticmethod
    def find_origin_delta(ecru, traite):
        best=0
        param=0
        deltas=[]
        cors=[]
        for delta in range(100):
            traite_copy = deepcopy(traite)
            traite_copy.move_origin(delta)
            cor=Point_matcher.correlate2d(ecru.data, traite_copy.data, 3)
            print(delta,cor)
            deltas.append(delta)
            cors.append(cor)
            if cor>best:
                best=cor
                param=delta
        plt.plot(deltas, cors)
        plt.show()
        return param

    @staticmethod
    def find_all_params_rough(ecru, traite,origin_start=0,origin_end=150,start_long=1,finish_long=1.1,start_larg=1,finish_larg=1.1,step=0.01):
        best=0
        param=(0,0,0)
        for origin in tqdm(range(origin_start,origin_end,10)):
            for delta_long in np.arange(start_long,finish_long,step):
                for delta_larg in np.arange(start_larg,finish_larg,step):
                    traite_copy = deepcopy(traite)
                    traite_copy.move_origin(origin)
                    traite_copy.moveData(delta_long,delta_larg)
                    cor=Point_matcher.correlate2d(ecru.data,traite_copy.data,1)
                    if cor>best:
                        best = cor
                        param=(origin,delta_long,delta_larg)
        return param

    @staticmethod
    def find_all_params_fine(ecru, traite,origin_start=0,origin_end=100,start_long=1.05,finish_long=1.1,start_larg=1.05,finish_larg=1.1,step=0.01):
        best=np.inf
        param=(0,0,0)
        for origin in tqdm(range(origin_start,origin_end)):
            for delta_long in np.arange(start_long,finish_long,step):
                for delta_larg in np.arange(start_larg,finish_larg,step):
                    traite_copy = deepcopy(traite)
                    traite_copy.move_origin(origin)
                    traite_copy.moveData(delta_long,delta_larg)
                    dist=Point_matcher.correlate2d_distance(ecru.data,traite_copy.data,1)
                    if dist<best:
                        best = dist
                        param=(origin,delta_long,delta_larg)
        return param


    @staticmethod
    def find_best_match(ecru, traite):
        ecru_centre=deepcopy(ecru)
        ecru_centre.extract_center()
        traite_centre=deepcopy(traite)
        traite_centre.extract_center()
        param=Point_matcher.find_all_params_rough(ecru_centre,traite_centre)
        print(param)
        param=Point_matcher.find_all_params_fine(ecru_centre,traite_centre,param[0]-5,param[0]+5,param[1]-0.01,param[1]+0.01,param[2]-0.01,param[2]+0.01,0.001)
        return param
    @staticmethod
    def rotation_correlations(ecru,traite,position):
        traite=deepcopy(traite)
        traite.move_origin(position)
        cors=[]
        traite_copy=deepcopy(traite)
        best_cor=Point_matcher.correlate2d(ecru.data,traite_copy.data,10)
        cors.append(best_cor)
        movement = "no"
        Point_matcher.flipFabric(traite_copy)
        cor = Point_matcher.correlate2d(ecru.data,traite_copy.data,10)
        cors.append(cor)
        if cor>best_cor:
            best_cor=cor
            movement = "flip"
        Point_matcher.invertFabric(traite_copy)
        cor = Point_matcher.correlate2d(ecru.data,traite_copy.data,10)
        cors.append(cor)
        if cor>best_cor:
            best_cor=cor
            movement = "flip+invert"
        traite_copy=deepcopy(traite)
        Point_matcher.invertFabric(traite_copy)
        cor = Point_matcher.correlate2d(ecru.data, traite_copy.data,10)
        cors.append(cor)
        if cor>best_cor:
            best_cor=cor
            movement = "invert"
        print(cors)
        return movement,best_cor
    @staticmethod
    def find_orientation(ecru, traite):
        # cors=[]
        # cors.append(Point_matcher.rotation_correlations(ecru,traite,0))
        # cors.append(Point_matcher.rotation_correlations(ecru,traite,75))
        # if cors[0][1]>cors[1][1]:
        #     return cors[0][0]
        # else:
        #     return cors[1][0]
        # return cors[0][0]
        return Point_matcher.rotation_correlations(ecru,traite,0)[0]

    @staticmethod
    def find_corresponding_defect_dico(ecru,traite,tol): #returns all the treated fabric defects within tolerance for each ecru defect. There can be more than one. Returns a list of all the ecru defect with no correspondance
        matching={}
        not_matching=[]
        for defect_e in ecru.data:
            for defect_t in traite.data:
                def_e = str(defect_e)
                def_t = str(defect_t)
                if np.abs((defect_e[0]-defect_t[0])) < 6*tol and np.abs((defect_e[1]-defect_t[1]))<6*tol:
                    if def_e in matching.keys():
                        matching[def_e].append(def_t)
                    else:
                        matching[def_e]=[def_t]
                else:
                        not_matching.append(def_e)

        return matching,not_matching

    @staticmethod
    def find_corresponding_defect_list(ecru,traite,tol):#returns the closest treated fabric defect within tolerance for each ecru defect. Returns a list of all the ecru defect with no correspondance
        matching=[]
        not_matching=[]
        for defect_e in ecru.data:
            dist_min=np.inf
            closest=[]
            for defect_t in traite.data:
                if np.abs((defect_e[0]-defect_t[0])) < 6*tol and np.abs((defect_e[1]-defect_t[1]))<6*tol:
                    dist=np.sqrt((defect_e[0]-defect_t[0])**2+(defect_e[1]-defect_t[1])**2)
                    if dist<dist_min:
                        dist_min=dist
                        closest=defect_t
            if closest != []:
                matching.append([defect_e.tolist(),closest.tolist()])
            else:
                not_matching.append(defect_e.tolist())
        return np.array(matching),np.array(not_matching)
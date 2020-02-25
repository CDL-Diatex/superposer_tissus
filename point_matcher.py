import numpy as np
from copy import deepcopy
from tqdm import tqdm


class Point_matcher():


    @staticmethod
    def correlate2d(ecru_defect, traite_defect, tol):
        matching = 0
        for defect_e in ecru_defect:
            for defect_t in traite_defect:
                if np.abs((defect_e[0] - defect_t[0])) < 10 * tol and np.abs((defect_e[1] - defect_t[1])) < 10 * tol:
                    matching += 1
                    break
        return matching / len(ecru_defect)

    @staticmethod
    def correlate2d_distance(ecru_defect, traite_defect,
                             tol):  # pour le réglage fin : on calcul la somme des distances aux
        dist_tot = -1
        for defect_e in ecru_defect:
            dist_min = np.inf
            for defect_t in traite_defect:
                if np.abs((defect_e[0] - defect_t[0])) < 20 * tol and np.abs((defect_e[1] - defect_t[1])) < 20 * tol:
                    dist = np.sqrt((defect_e[0] - defect_t[0]) ** 2 + (defect_e[1] - defect_t[1]) ** 2)
                    if dist < dist_min:
                        dist_min = dist
            if dist_min < np.inf:
                dist_tot += dist_min
        if dist_tot == -1:
            dist_tot = np.inf
        return dist_tot



    @staticmethod
    def find_all_params_rough(ecru, traite, origin_start=0, origin_end=150, start_long=1, finish_long=1.1, start_larg=1,
                              finish_larg=1.1, step=0.01):
        best = 0
        param = (0, 0, 0)
        for origin in tqdm(range(origin_start, origin_end, 10)):
            for delta_long in np.arange(start_long, finish_long, step):
                for delta_larg in np.arange(start_larg, finish_larg, step):
                    traite_copy = deepcopy(traite)
                    traite_copy.move_origin(origin)
                    traite_copy.moveData(delta_long, delta_larg)
                    cor = Point_matcher.correlate2d(ecru.data, traite_copy.data, 1)
                    if cor > best:
                        best = cor
                        param = (origin, delta_long, delta_larg)
        return param,best

    @staticmethod
    def find_all_params_fine(ecru, traite, origin_start=0, origin_end=100, start_long=1.05, finish_long=1.1,
                             start_larg=1.05, finish_larg=1.1, step=0.001):
        best = np.inf
        param = ((origin_start + origin_end)/2, (start_long + finish_long)/2, (start_larg + finish_larg)/2)
        for origin in tqdm(range(origin_start, origin_end,2)):
            for delta_long in np.arange(start_long, finish_long, step):
                for delta_larg in np.arange(start_larg, finish_larg, step):
                    traite_copy = deepcopy(traite)
                    traite_copy.move_origin(origin)
                    traite_copy.moveData(delta_long, delta_larg)
                    dist = Point_matcher.correlate2d_distance(ecru.data, traite_copy.data, 1)
                    if dist < best:
                        best = dist
                        param = (origin, delta_long, delta_larg)
        return param

    @staticmethod
    def find_best_match(ecru, traite,vert_off,long_param,hauteur_param):
        ecru_centre = deepcopy(ecru)
        ecru_centre.extract_center()
        traite_centre = deepcopy(traite)
        traite_centre.extract_center()
        if vert_off:
            origin_st,origin_end=int(vert_off),int(vert_off)
        else:
            origin_st, origin_end = 0, 150
        if long_param:
            st_long,end_long=float(long_param),float(long_param)
        else:
            st_long, end_long =1,1.1
        if hauteur_param:
            st_haut,end_haut=float(hauteur_param),float(hauteur_param)
        else:
            st_haut, end_haut=1,1.1
        param = Point_matcher.find_all_params_rough(ecru_centre, traite_centre,origin_st,origin_end,st_long,end_long,
                                                    st_haut,end_haut)[0]
        print(param)

        if vert_off:
            origin_st,origin_end=int(vert_off),int(vert_off)
        else:
            origin_st, origin_end = param[0] - 5, param[0] + 5
        if long_param:
            st_long,end_long=float(long_param),float(long_param)
        else:
            st_long, end_long =param[1] - 0.01, param[1] + 0.01
        if hauteur_param:
            st_haut,end_haut=float(hauteur_param),float(hauteur_param)
        else:
            st_haut, end_haut=param[2] - 0.01, param[2] + 0.01

        param = Point_matcher.find_all_params_fine(ecru_centre, traite_centre,origin_st,origin_end,st_long,end_long,
                                                   st_haut,end_haut,0.001)

        return param

    @staticmethod
    def find_orientation(ecru, traite):
        traite_copy=deepcopy(traite)
        ecru_copy=deepcopy(ecru)
        traite_copy.extract_center()
        ecru_copy.extract_center()
        traite_copy.invert_fabric()
        best=Point_matcher.find_all_params_rough(ecru,traite_copy,step=0.02)[1]
        print("invert",best)
        traite_copy.flip_fabric()
        best2=Point_matcher.find_all_params_rough(ecru,traite_copy,step=0.02)[1]
        print("flip",best2)
        if best2>best:
            return "flip+invert"
        else:
            return "invert"
    @staticmethod
    def find_corresponding_defect_dico(ecru, traite,
                                       tol):  # returns all the treated fabric defects within tolerance for each ecru defect. There can be more than one. Returns a list of all the ecru defect with no correspondance
        matching = {}
        not_matching = []
        for defect_e in ecru.data:
            for defect_t in traite.data:
                def_e = str(defect_e)
                def_t = str(defect_t)
                if np.abs((defect_e[0] - defect_t[0])) < 6 * tol and np.abs((defect_e[1] - defect_t[1])) < 6 * tol:
                    if def_e in matching.keys():
                        matching[def_e].append(def_t)
                    else:
                        matching[def_e] = [def_t]
                else:
                    not_matching.append(def_e)

        return matching, not_matching

    @staticmethod
    def find_corresponding_defect_list(ecru, traite,
                                       tol):  # returns the closest treated fabric defect within tolerance for each ecru defect. Returns a list of all the ecru defect with no correspondance
        matching = []
        not_matching = []
        for defect_e in ecru.data:
            dist_min = np.inf
            closest = []
            for defect_t in traite.data:
                if np.abs((defect_e[0] - defect_t[0])) < 5 * tol and np.abs((defect_e[1] - defect_t[1])) < 60 * tol:
                    dist = np.sqrt((defect_e[0] - defect_t[0]) ** 2 + (defect_e[1] - defect_t[1]) ** 2)
                    if dist < dist_min:
                        dist_min = dist
                        closest = defect_t
            if closest != []:
                matching.append([defect_e.tolist(), closest.tolist()])
            else:
                not_matching.append(defect_e.tolist())
        return np.array(matching), np.array(not_matching)

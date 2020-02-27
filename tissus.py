import numpy as np
import pandas as pd
from operator import itemgetter


class Tissus:
    def __init__(self, csv_path, long=0, larg=0):
        self.data, self.dataframe = self.parseCsv(csv_path)
        self.long_tot = long
        self.larg_tot = larg
        if long == 0:
            self.long_tot = max(self.data[:, 0])
        if larg == 0:
            self.larg_tot = max(self.data[:, 1])

    def parseCsv(self, path): #charge le csv en mémoire
        df = pd.read_csv(path, names=["roule", "id", "zero1", "termine", "long_tot", "larg_tot", "inconnu1", "zero2",
                                      "type_defaut", "inconnu3", "metrage", "position", "long_defaut", "larg_defaut",
                                      "inconnu2", "image", "image2", "zero3", "requal_3_cat", "requal_6_cat"])
        df1 = df[['metrage', 'position', "type_defaut", "requal_6_cat", "image", "roule"]]
        data=sorted(df1.values.tolist(), key=itemgetter(0)) #on range les défaut par ordre de métrage. Ca permet d'accélerer le calcul des corrélations
        return np.array(data), df

    def moveData(self, long, larg): #déplace les défauts des paramètres donnés en entrée
        mid_l = self.long_tot / 2
        mid_h = self.larg_tot / 2
        for default in self.data:
            if long != 1:
                default[0] = long * np.power(default[0], 0.9995)
            if larg != 1:
                default[1] = default[1]
                if default[1] > mid_h:
                    default[1] = larg * np.power(default[1] - mid_h, 0.9995) + mid_h
                else:
                    default[1] = mid_h - larg * np.power(mid_h - default[1], 0.9995)
        return self.data

    def remove_duplicates(self):  # remplace tous les duplicata par un défaut à leur position moyenne
        kept = []
        defects = self.data.tolist()
        while len(defects)>0:
            avgx = defects[0][0]
            avgy = defects[0][1]
            tot = 1
            i=0
            while i<len(defects):
                if np.abs((defects[0][0] - defects[i][0])) < 1 and np.abs(
                        (defects[0][1] - defects[i][1])) < 25 and defects[0] != defects[i] and str(defects[0][3]) == str(defects[i][3]): #si les deux points sont proches et de meme catégorie. Le str permet de gérer le cas défaut non requalifié. La colonne 3 vaut alors nan et on ne s'interesse pas au type de défaut
                    avgx += defects[i][0]
                    avgy += defects[i][1]
                    tot += 1
                    defects.remove(defects[i])
                else:
                    i += 1
            new_defect=defects[0].copy()
            new_defect[0] = avgx / tot
            new_defect[1] = avgy / tot
            kept.append(new_defect)
            defects.pop(0)
        self.data = np.array(kept)

    def rotate(self, rotation): #retourne le tissus de la rotation donnée
        if rotation == "no":
            return
        elif rotation == "invert":
            self.invert_fabric()
        elif rotation == "flip":
            self.flip_fabric()
        elif rotation == "flip+invert":
            self.flip_fabric()
            self.invert_fabric()

    def invert_fabric(self): #retourne le tissus selon l'axe des x
        for defect in self.data:
            defect[0] = self.long_tot - defect[0]

    def flip_fabric(self): #retourne le tissus selon l'axe des y
        for defect in self.data:
            defect[1] = self.larg_tot - defect[1]

    def cut_all_sides(self, margin):#découpe tous les défaut compris dans la marge de tous les côtés
        cuted = []
        for defect in self.data:
            if not (defect[1] < margin or defect[1] > self.larg_tot - margin) and not (
                    defect[0] < margin or defect[0] > self.long_tot - margin):
                defect[1] -= margin
                cuted.append(defect)
        self.data = np.array(cuted)
        self.larg_tot = max(self.data[:, 1])

    def cut_hauteur(self, margin):#découpe tous les défauts compris dans la marge du côté haut et bas
        cuted = []
        for defect in self.data:
            if not (defect[1] < margin or defect[1] > self.larg_tot - margin):
                defect[1] -= margin
                cuted.append(defect)
        self.data = np.array(cuted)
        self.larg_tot = max(self.data[:, 1])

    def cut_longueur(self, margin):#découpe tous les défauts compris dans la marge à gauche et à droite
        cuted = []
        for defect in self.data:
            if not(defect[0] < margin or defect[0] > self.long_tot - margin):
                defect[1] -= margin
                cuted.append(defect)
        self.data = np.array(cuted)
        self.larg_tot = max(self.data[:, 1])

    def extract_center(self): #extrait tous les défaut au centre du tissus. On récupère ainsi environ 1/9 des défaut. Permet d'accélérer le calcul des corrélations
        center = []
        margin_long = 0.25 * self.long_tot
        margin_larg = 0.25 * self.larg_tot
        for defect in self.data:
            if defect[1] > margin_larg and defect[1] < self.larg_tot - margin_larg and defect[0] > margin_long and \
                    defect[0] < self.long_tot - margin_long:
                center.append(defect)
        self.data = np.array(center)

    def move_origin(self, origin_delta):#deplace tous les défaut verticalement
        for default in self.data:
            default[1] += origin_delta

    def move_defects_for_broken_cam(self, start, length):#deplace tous les défaut horizontalement. Utile si les caméras TDM était en panne à un certain moment et pendant une durée connue.
        for defect in self.data:
            if defect[0] > start:
                defect[0] += length

    # def cut_when_no_cam_at_end(self, end_of_recording):
    #     cuted = []
    #     for defect in self.data:
    #         if defect[0] < end_of_recording:
    #             cuted.append(defect)
    #     self.data = np.array(cuted)
    #     self.long_tot = max(self.data[:, 0])
    #
    # def cut_when_no_cam_at_start(self, start_of_recording):
    #     cuted = []
    #     for defect in self.data:
    #         if defect[0] > start_of_recording:
    #             defect[0] -= start_of_recording
    #             cuted.append(defect)
    #     self.data = np.array(cuted)
    #     self.long_tot = max(self.data[:, 0])

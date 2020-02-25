import numpy as np
import pandas as pd


class Tissus:
    def __init__(self, csv_path, long=0, larg=0):
        self.data, self.dataframe = self.parseCsv(csv_path)
        self.long_tot = long
        self.larg_tot = larg
        if long == 0:
            self.long_tot = max(self.data[:, 0])
        if larg == 0:
            self.larg_tot = max(self.data[:, 1])

    def parseCsv(self, path):
        df = pd.read_csv(path, names=["roule", "id", "zero1", "termine", "long_tot", "larg_tot", "inconnu1", "zero2",
                                      "type_defaut", "inconnu3", "metrage", "position", "long_defaut", "larg_defaut",
                                      "inconnu2", "image", "image2", "zero3", "requal_3_cat", "requal_6cat"])
        df1 = df[['metrage', 'position', "type_defaut", "requal_3_cat", "image", "roule"]]
        return df1.to_numpy(), df1

    def moveData(self, long, larg):
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
        for defect1 in defects:
            avgx = defect1[0]
            avgy = defect1[1]
            tot = 1
            for defect2 in defects:
                if np.abs((defect1[0] - defect2[0])) < 0.2 and np.abs(
                        (defect1[1] - defect2[1])) < 25 and defect1 != defect2 and defect1[2] == defect2[2]:
                    avgx += defect2[0]
                    avgy += defect2[1]
                    tot += 1
                    defects.remove(defect2)
            defect1[0] = avgx / tot
            defect1[1] = avgy / tot
        self.data = np.array(defects)

    def rotate(self, rotation):
        if rotation == "no":
            return
        elif rotation == "invert":
            self.invert_fabric()
        elif rotation == "flip":
            self.flip_fabric()
        elif rotation == "flip+invert":
            self.flip_fabric()
            self.invert_fabric()

    def invert_fabric(self):
        for defect in self.data:
            defect[0] = self.long_tot - defect[0]

    def flip_fabric(self):
        for defect in self.data:
            defect[1] = self.larg_tot - defect[1]

    def cut_all_sides(self, margin):
        cuted = []
        for defect in self.data:
            if not (defect[1] < margin or defect[1] > self.larg_tot - margin) and not (
                    defect[0] < margin or defect[0] > self.long_tot - margin):
                defect[1] -= margin
                cuted.append(defect)
        self.data = np.array(cuted)
        self.larg_tot = max(self.data[:, 1])

    def cut_hauteur(self, margin):
        cuted = []
        for defect in self.data:
            if not (defect[1] < margin or defect[1] > self.larg_tot - margin):
                defect[1] -= margin
                cuted.append(defect)
        self.data = np.array(cuted)
        self.larg_tot = max(self.data[:, 1])

    def cut_longueur(self, margin):
        cuted = []
        for defect in self.data:
            if not(defect[0] < margin or defect[0] > self.long_tot - margin):
                defect[1] -= margin
                cuted.append(defect)
        self.data = np.array(cuted)
        self.larg_tot = max(self.data[:, 1])

    def extract_center(self):
        center = []
        margin_long = 0.25 * self.long_tot
        margin_larg = 0.25 * self.larg_tot
        for defect in self.data:
            if defect[1] > margin_larg and defect[1] < self.larg_tot - margin_larg and defect[0] > margin_long and \
                    defect[0] < self.long_tot - margin_long:
                center.append(defect)
        self.data = np.array(center)

    def move_origin(self, origin_delta):
        for default in self.data:
            default[1] += origin_delta

    def move_defects_for_broken_cam(self, start, length):
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

import numpy as np
from point_matcher import Point_matcher
import pandas as pd

class Tissus:
    def __init__(self, csv_path,long=0,larg=0 ):
        self.data,self.dataframe=self.parseCsv(csv_path)
        self.long_tot = long
        self.larg_tot = larg
        if long ==0:
            self.long_tot = max(self.data[:, 0])
        if larg ==0:
            self.larg_tot= max(self.data[:, 1])

    # def parseCsv(self,path):
    #     with open(path,"r") as csv_reader:
    #         data=[]
    #         lines=csv.reader(csv_reader)
    #         next(lines)
    #         for line in lines:
    #             if 1800 > float(line[10]) > 0 and 2500 > float(line[11]) > 0: #if the defect coordiantes are not bugged
    #                 if len(line)>=19:
    #                     data.append([float(line[10]),float(line[11]),float(line[8]),float(line[18]),float(line[15])]) #metrage,position,qualification acyrus,notre qualif,id image correspondante
    #                 else:
    #                     data.append([float(line[10]),float(line[11]),float(line[8]),3000,float(line[15])])
    #         del data[0]
    #         return np.array(data)

    def parseCsv(self,path):
        df=pd.read_csv(path,names=["roule","id","zero1","termine","long_tot","larg_tot","inconnu1","zero2","type_defaut","inconnu3","metrage","position","long_defaut","larg_defaut","inconnu2","image","image2","zero3","requal_3_cat","requal_6cat"])
        df1 = df[['metrage', 'position',"type_defaut","requal_3_cat","image","roule"]]
        return df1.to_numpy(),df1
    @staticmethod
    def createPicture(data):
        long=int(max(data[:,0])*100+10) #en cm
        larg=int(max(data[:,1])/10+10) #en cm
        img=np.ones((long,larg))
        for i in range(len(data)):
            img[int(round(data[i][0]*100)),int(round(data[i][1]/10))]=0
        return img

    @staticmethod
    def moveDataStatic(data,long,larg,long_tot,larg_tot):
        mid_l=long_tot/2
        mid_h=larg_tot/2
        for default in data:
            if long !=1:
                default[0]=long*np.power(default[0],0.995)
            if larg != 1 :
                default[1]=default[1]+74
                if default[1]>mid_h:
                    default[1]=larg*np.power(default[1]-mid_h,1)+mid_h
                else:
                    default[1] = mid_h - larg * np.power(mid_h - default[1],1)
        return data

    def moveData(self,long,larg):
        mid_l=self.long_tot/2
        mid_h=self.larg_tot/2
        for default in self.data:
            if long !=1:
                default[0]=long*np.power(default[0],0.9995)
            if larg != 1 :
                default[1]=default[1]
                if default[1]>mid_h:
                    default[1]=larg*np.power(default[1]-mid_h,0.9995)+mid_h
                else:
                    default[1] = mid_h - larg * np.power(mid_h - default[1],0.9995)
        return self.data

    def rotate(self,rotation):
        if rotation=="no":
            return
        elif rotation=="invert":
            Point_matcher.invertFabric(self)
        elif rotation=="flip":
            Point_matcher.flipFabric(self)
        elif rotation=="flip+invert":
            Point_matcher.flipFabric(self)
            Point_matcher.invertFabric(self)

    def cut_sides(self,margin):
        cuted=[]
        for defect in self.data:
            if not (defect[1]<margin or defect[1]>self.larg_tot-margin) and not(defect[0]<margin or defect[0]>self.long_tot-margin):
                 defect[1]-=margin
                 cuted.append(defect)
        self.data=np.array(cuted)
        self.larg_tot = max(self.data[:, 1])

    def extract_center(self):
        center=[]
        margin_long = 0.25*self.long_tot
        margin_larg = 0.25*self.larg_tot
        for defect in self.data:
            if defect[1]>margin_larg and  defect[1]<self.larg_tot-margin_larg and defect[0]>margin_long and defect[0]<self.long_tot-margin_long:
                 center.append(defect)
        self.data = np.array(center)

    def move_origin(self,origin_delta):
        for default in self.data:
            default[1]+=origin_delta

    def move_defects_for_broken_cam(self,start,length):
        for defect in self.data:
            if defect[0]>start:
                defect[0]+=length

    def cut_when_no_cam_at_end(self,end_of_recording):
        cuted=[]
        for defect in self.data:
            if defect[0]<end_of_recording:
                cuted.append(defect)
        self.data=np.array(cuted)
        self.long_tot = max(self.data[:, 0])

    def cut_when_no_cam_at_start(self,start_of_recording):
        cuted=[]
        for defect in self.data:
            if defect[0]>start_of_recording:
                defect[0]-=start_of_recording
                cuted.append(defect)
        self.data=np.array(cuted)
        self.long_tot = max(self.data[:, 0])

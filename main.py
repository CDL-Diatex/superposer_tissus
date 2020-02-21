from SIFT import Tissus
from point_matcher import Point_matcher
from draw_graph import Graph
from copy import deepcopy
from stats import Stats
from dash_app import dash_scatter


# ecru_name = "Matching/22/01 389901-22.csv"
# ecru_name = "Matching/22/output_step2_Chaine_22.csv"
# ecru_name = "Matching/26/03 389901-26.csv"
# ecru_name = "Matching/26/03 389901_74166 E-2450.csv"
# traite_name = "Matching/26/03 389901_74582-2538.csv"
# traite_name = "Matching/22/01 389901_74204-2457.csv"
# ecru_name = "Matching/30/02 439701-30.csv"
# traite_name = "Matching/30/02 439701_74515-2483.csv"
ecru_name = "Matching/11/03 389700-11.csv"
traite_name = "Matching/11/03 389700_73356-1350.csv"


ecru=Tissus(ecru_name)
traite=Tissus(traite_name)
#
# ecru.cut_sides(400)
# traite.cut_sides(400)
# traite.move_defects_for_broken_cam(0,5) #pour TSJ/TSJ 22
# ecru.move_defects_for_broken_cam(0,110) #pour TDM/TSJ 30
# traite.cut_when_no_cam_at_start(110)
# traite.cut_when_no_cam_at_start(800)
# rotation=Point_matcher.find_orientation(ecru,traite)
rotation="invert"
print(rotation)
traite.rotate(rotation)


# params=Point_matcher.find_best_match(ecru,traite)
params=100, 1.051, 1.05
# params = 0,1,1
print(params)


origin = params[0]
traite.move_origin(origin)
traite.moveData(params[1],params[2])
# Graph.draw(match[:,0,:],match[:,1,:])
# Graph.draw(no_match)
stats=Stats(ecru,traite)
print(stats.staying_rates())
print(stats.qualif_comparison())

figure=Graph.draw(ecru.data,traite.data,traite_name,rotation)

dash_scatter(figure,ecru,traite,stats).run_server(debug=True)

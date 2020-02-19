from SIFT import Tissus
from point_matcher import Point_matcher
from draw_graph import Graph
from copy import deepcopy
from stats import Stats
from dash_app import dash_scatter


# ecru_name = "Matching/22/01 389901-22.csv"
ecru_name = "Matching/26/output_step2_Chaine_26.csv"
# ecru_name = "Matching/26/03 389901-26.csv"

# traite_name = "Matching/26/03 389901_74166 E-2450.csv"
traite_name = "Matching/26/03 389901_74582-2538.csv"

ecru=Tissus(ecru_name)
traite=Tissus(traite_name)

ecru.cut_sides(80)
# traite.cut_sides(80)
# traite.move_defects_for_broken_cam(0,-5)
# traite.cut_when_no_cam_at_start(800)
rotation=Point_matcher.find_orientation(ecru,traite)
print(rotation)
# rotation="no"
traite.rotate(rotation)

ecru2,traite2=deepcopy(ecru),deepcopy(traite)
traite.extract_center()
ecru.extract_center()

params=Point_matcher.find_best_match(ecru,traite)
# params=0, 1.009,1
# params=0,1.08,1
print(params)


ecru=deepcopy(ecru2)
traite=deepcopy(traite2)

origin = params[0]
traite.move_origin(origin)
traite.moveData(params[1],params[2])
match=Point_matcher.find_corresponding_defect_list(ecru,traite,1)[0]
no_match=Point_matcher.find_corresponding_defect_list(ecru,traite,1)[1]
# Graph.draw(match[:,0,:],match[:,1,:])
# Graph.draw(no_match)
stats=Stats(match,no_match,ecru)
print(stats.staying_rates())
print(stats.qualif_comparison())

figure=Graph.draw(ecru.data,traite.data,traite_name,rotation)

dash_scatter(figure,ecru,traite).run_server(debug=False)

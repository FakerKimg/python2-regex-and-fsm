from regexfsm.fsm import fsm
from regexfsm.fsm import anything_else
import json
import networkx

f = open("email_valid_fsm", "r")
m_json = f.readline()
f.close()

fsm_dict = json.loads(m_json)
#fsm_dict = m_json.decode('unicode-escape').encode('utf8')
print fsm_dict

# copy alphabet
cpalphabet = [ s.encode("utf-8") for s in fsm_dict["alphabet"] ]
if "anything_else" in cpalphabet:
    cpalphabet.remove("anything_else")
    cpalphabet.append(anything_else)

# copy map
cpmap = {}
for sstate, edges in fsm_dict["map"].iteritems():
    sindex = int(sstate)
    cpmap[sindex] = {}
    for _input, eindex in edges.iteritems():
        if _input=="anything_else":
            cpmap[sindex][anything_else] = eindex
        else:
            cpmap[sindex][_input.encode("utf-8")] = eindex

m = fsm(alphabet=set(cpalphabet), states=set(fsm_dict["states"]), initial=fsm_dict["initial"], finals=set(fsm_dict["finals"]), map=cpmap)
print m.__dict__

negative_fsm = m.everythingbut()

g = networkx.DiGraph()
g.add_nodes_from(list(negative_fsm.__dict__["states"]))

# use add_edges_from will be better ???
for edges in dict(negative_fsm.__dict__["map"]).iteritems():
    start_index = edges[0]
    for edge in edges[1].iteritems():
        end_index = edge[1]
        g.add_edge(start_index, end_index, _input=edge[0])

print "graph construction complete"


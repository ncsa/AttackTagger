from tables import Events as SE, UserStates as SU, AttackStates as SA
import functions
from factor_graph import FactorGraph

def convert_event_(E_):
    # convert E to list of int
    if (type(E_[0]) != int):
        E = [int(SE(x)) for x in E_]
    else:
        E = E_

    return E

def build_fg_():
    # set up states
    states = [len(list(SU)), len(list(SA))]
    # set up functions
    F_UES_TEST, F_ES_TEST, F_SS_TEST, F_M_TUPLE = functions.get_functions()
    # build the model
    g = FactorGraph(states,
                    F_UES_TEST,
                    F_ES_TEST,
                    F_SS_TEST,
                    F_M_TUPLE)
    return g

def sequence(u, E):
    g = build_fg_()
    return g.predict(u, convert_event_(E))

def eval_loss(E, L):
    y_hat, y_hat_pretty = self.sequence(E)
    return 1

def build_fv(E, Y, i):
    g = build_fg_()
    return g.build_fv(E, Y, i)

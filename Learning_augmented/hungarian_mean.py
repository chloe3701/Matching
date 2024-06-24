import hungarian_classic_opt
import hungarian_learned as hl


# Initialisation: M = ∅ p=q= mean duals

def init_dual(B,p_mean,q_mean):
    p,q = hl.make_feasible(B,p_mean,q_mean)
    
    return p,q

def hungarian_mean(B,p_mean,q_mean):
    p,q = init_dual(B,p_mean,q_mean)
    w,i = hungarian_classic_opt.hungarian(B,p,q)
    #hungarian_classic.verify(B,p,q)
    # B.display_matching()
    return w,i
    
import matplotlib.pyplot as plt
import plotting
import numpy as np

def hypervolume_2D(cost1, cost2, ref=None):
    import numpy as np
    pts = np.array(list(zip(cost1, cost2)))
    # Minimierung → sortieren nach Cost1
    pts = pts[pts[:,0].argsort()]

    if ref is None:
        ref = (max(cost1)*1.1, max(cost2)*1.1)

    hv = 0
    prev_x = ref[0]
    for x, y in reversed(pts):
        width = prev_x - x
        height = ref[1] - y
        hv += width * height
        prev_x = x
    return hv

def hypervolume_3D(cost1, cost2, cost3, ref=None):
    pts = np.array(list(zip(cost1, cost2, cost3)))
    # nach cost1 sortieren
    pts = pts[pts[:,0].argsort()]
    if ref is None:
        ref = (
            max(cost1) * 1.1,
            max(cost2) * 1.1,
            max(cost3) * 1.1
        )
    hv = 0
    prev_x = ref[0]
    # von hinten durchgehen (schlechteste Lösungen zuerst)
    for i in range(len(pts)-1, -1, -1):
        x = pts[i,0]
        width = prev_x - x
        # Punkte, die diese Scheibe dominieren
        slice_pts = pts[:i+1]
        yz_hv = hypervolume_2D(
            slice_pts[:,1],
            slice_pts[:,2],
            ref=(ref[1], ref[2])
        )
        hv += width * yz_hv
        prev_x = x
    return hv

def plot_hypervolume(hypervolume_list, saving_path = None):
    fig = plt.figure()
    plt.plot(hypervolume_list)
    plt.xlabel("Generation")
    plt.ylabel("Relative Hypervolume in %")
    if saving_path is not None:
        saving_path = plotting.check_saving_path(saving_path)
        plt.savefig(saving_path, bbox_inches="tight", dpi=300)
    
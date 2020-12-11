import matplotlib.pyplot as plt

from city import City, Route

def plot_route(cities, route):

    coordinates = route.get_coordinates()
    min_y = min(coordinates[:,1])
    max_y = max(coordinates[:,1])

    fig, ax = plt.subplots(2, sharex = True, sharey=True)
    ax[0].set_ylim(top = max_y+20) # to make room for textbox
    ax[1].set_ylim(top = max_y+20) # to make room for textbox

    # https://stackoverflow.com/questions/46506375/creating-graphics-for-euclidean-instances-of-tsp
    ax[0].set_title('Cities')
    ax[1].set_title('Tour')
    ax[0].scatter(coordinates[:,0], coordinates[:,1])
    ax[1].scatter(coordinates[:,0], coordinates[:,1])
    for i in range(route.N-1):
        start_pos = coordinates[i]
        end_pos = coordinates[i+1]
        ax[1].annotate("",
            xy=start_pos, xycoords='data',
            xytext=end_pos, textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"))

    textstr = "N nodes: {}\nTotal length: {}".format(route.N, route.get_length())
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax[1].text(0.05, 0.95, textstr, transform=ax[1].transAxes, fontsize=14, # Textbox
        verticalalignment='top', bbox=props)

    plt.show()

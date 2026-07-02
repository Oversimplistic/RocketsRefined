#A place to put functions for displaying data (text, graphs, graphics, etc.)
import matplotlib.pyplot as plt


def output_as_text(summary):
    print(f"Max Altitude was {summary.max_altitude:.2f} meters. This was reached at {summary.max_altitude_time:.2f} seconds\n"
          f"Max Velocity was {summary.max_velocity:.2f} meters per second. This was reached at {summary.max_velocity_time:.2f} seconds\n"
          f"MaxQ was {summary.max_q:.2f} Newtons. This was reached at {summary.max_q_time:.2f} seconds\n"
          f"Stage 1 burnout was reached at {summary.burnout_time:.2f} at {summary.burnout_altitude:.2f} meters"
          )


#An explicit matplotlib configuration for 2x1 graphing, this can be adjusted to any aspect ratio by adding new graphs
def xy_graph(xlist1, ylist1, xtitle1, ytitle1, graphtitle1,
             xlist2, ylist2, xtitle2, ytitle2, graphtitle2):

    #establishes subplots
    fig, axs = plt.subplots(1, 2)

    #graph 1 parameters
    axs[0].plot(xlist1, ylist1)
    axs[0].set_xlabel(xtitle1)
    axs[0].set_ylabel(ytitle1)

    #graph 2 parameters
    axs[1].plot(xlist2, ylist2)
    axs[1].set_xlabel(xtitle2)
    axs[1].set_ylabel(ytitle2)

    #render graph
    plt.show()

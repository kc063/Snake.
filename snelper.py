import matplotlib.pyplot as plt
from IPython import display

plt.ion()

def plot(scores, mean_scores, frames, mean_frames):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot()
    plt.plot(scores)
    plt.plot(mean_scores)
    #plt.plot(frames)
    #plt.plot(mean_frames)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    #optional functionality for survivability: early versions of the algorithm were dying young, so survivability was encouraged
    #plt.text(len(frames)-1, frames[-1], str(frames[-1]))
    #plt.text(len(mean_frames)-1, mean_frames[-1], str(mean_frames[-1]))
    plt.show(block=False)
    plt.pause(.1)

from os import path
import re

def get_file_number(file_path):
    name = path.basename(file_path)
    file_number = re.findall("_\d{1,2}", name)
    if len(file_number) == 0:
        raise Exception('Error: Incorrect file format. Should be <name of file>_<channel number>* where * anything')
    return file_number[0][1:]

def get_sorted_files(list_of_files):
    sorted(list_of_files, key=lambda file_path: get_file_number(file_path))
    return list_of_files

def set_labels(ax, x_label, y_label, channel_number, config):
    # show axis only on the left and bottom
    # there are more than one plot
    # y axis label on channel 3 plot
    if channel_number == 4:
        ax.set_ylabel(y_label, **config)
        ax.set_xticklabels([])
    #  x axis label on channel
    elif channel_number == 32:
        ax.set_xlabel(x_label, **config)
        ax.set_yticklabels([])
    # only y axis label
    elif channel_number in range(0, 8):
        ax.set_xticklabels([])
    # only show x axis label
    elif channel_number in [16, 24, 32, 40, 48, 56, 64]:
        ax.set_yticklabels([])
    # everything else no label
    elif channel_number != 8:
        ax.set_yticklabels([])
        ax.set_xticklabels([])


def get_data_in_frequency_range(data, freq_range):
    min_freq, max_freq = freq_range
    freq_column_name = 'freq/Hz'
    data = data.loc[data.loc[:, freq_column_name] >= min_freq, :]
    data = data.loc[data.loc[:, freq_column_name] <= max_freq, :]
    return data


def scale_user_input_to_float(limit):
    return None if limit == "" else float(limit)


class ZoomPan:
    def __init__(self):
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None


    def zoom_factory(self, ax, base_scale = 2.):
        def zoom(event):
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location

            if event.button == 'down':
                # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'up':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
                print (event.button)

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])

            ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
            ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])
            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest
        fig.canvas.mpl_connect('scroll_event', zoom)

        return zoom

    def pan_factory(self, ax):
        def onPress(event):
            if event.inaxes != ax: return
            self.cur_xlim = ax.get_xlim()
            self.cur_ylim = ax.get_ylim()
            self.press = self.x0, self.y0, event.xdata, event.ydata
            self.x0, self.y0, self.xpress, self.ypress = self.press

        def onRelease(event):
            self.press = None
            ax.figure.canvas.draw()

        def onMotion(event):
            if self.press is None: return
            if event.inaxes != ax: return
            dx = event.xdata - self.xpress
            dy = event.ydata - self.ypress
            self.cur_xlim -= dx
            self.cur_ylim -= dy
            ax.set_xlim(self.cur_xlim)
            ax.set_ylim(self.cur_ylim)

            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest

        # attach the call back
        fig.canvas.mpl_connect('button_press_event',onPress)
        fig.canvas.mpl_connect('button_release_event',onRelease)
        fig.canvas.mpl_connect('motion_notify_event',onMotion)

        #return the function
        return onMotion

# def enter_axes(event):
#     print('enter_axes', event.inaxes, event.xdata, event.ydata)
#     # event.inaxes.patch.set_facecolor('yellow')
#     # event.canvas.draw()
#     # ax = event.inaxes
#     # line = ax.get_label_text()
#     # print(line)
#
# def leave_axes(event):
#     print('leave_axes', event.inaxes)
#     event.inaxes.patch.set_facecolor('white')
#     event.canvas.draw()
#
# def enter_figure(event):
#     print('enter_figure', event.canvas.figure)
#     event.canvas.figure.patch.set_facecolor('red')
#     event.canvas.draw()
#
# def leave_figure(event):
#     print('leave_figure', event.canvas.figure)
#     event.canvas.figure.patch.set_facecolor('grey')
#     event.canvas.draw()
#
# def on_press(event):
#     print('you pressed', event.button, event.xdata, event.ydata)
        # fig.canvas.mpl_connect('figure_leave_event', leave_figure)
        # fig.canvas.mpl_connect('figure_enter_event', enter_figure)
        # fig.canvas.mpl_connect('axes_enter_event', self.enter_axes)
        # fig.canvas.mpl_connect('axes_leave_event', leave_axes)
        # fig.canvas.mpl_connect('button_press_event', self.on_press)
"""
A 'logger' to record timing of clients

Pretty rough, but works.  Writes everything you use (program wise) to a log file.
Intended to log everything, to be processed in another program, 
to show how you are using your time (or more likely wasting it)
"""
from libqtile import hook
from datetime import datetime


current_window_name = ""
previous_datetime = datetime.now()


def gap():
    return str(int((datetime.now() - previous_datetime).total_seconds() * 1000))


def log_text(text):
    fh = open("~/configs/qtile/log.txt", "a")
    fh.write(str(datetime.now()) + "|" + gap() + "|" + text + "\n")
    fh.close()


def log_window(window):
    fh = open("~/configs/qtile/log.txt", "a")
    log = str(datetime.now()) + "|" + gap() + "|" + str(window.cmd_inspect()['wm_class'][0]) + "|" + str(window.name) + "\n"
    fh.write(log)
    fh.close()


# Focus changes are logged
@hook.subscribe.client_focus
def focus_change(window):
    global current_window_name
    global previous_datetime
    # This hook is fired, sometimes, multiple times
    # This variable check ensures it is only logged once
    # If it is different than last check, log it, if not assume it is still the
    # same client
    if window.name != current_window_name:
        log_window(window)
        current_window_name = window.name
        previous_datetime = datetime.now()

# If the name of a client changes (like changing tab/window)
@hook.subscribe.client_name_updated
def name_change(window):
    global current_window_name
    global previous_datetime
    # I only want to log if the name changed while I was using it, like
    # changing tabs in a browser
    if window.has_focus:
        if window.name != current_window_name:
            log_window(window)
            current_window_name = window.name
            previous_datetime = datetime.now()

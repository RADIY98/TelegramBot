from .buttons_val_obj import StartButtons

class TrainMapper:
    handler = {
        0: StartButtons.trains,
        1: StartButtons.set_trains,
        2: StartButtons.statistic,
    }
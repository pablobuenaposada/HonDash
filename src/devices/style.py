import datetime

AVAILABLE_STATUSES = ("day", "night")


class Style:
    status = AVAILABLE_STATUSES[0]
    threshold_detected_time = None

    def __init__(
        self, threshold_lower_limit=8, threshold_upper_limit=10, elapsed_seconds=3
    ):
        self.threshold_lower_limit = threshold_lower_limit
        self.threshold_upper_limit = threshold_upper_limit
        self.elapsed_seconds = elapsed_seconds

    def update(self, tps):
        if self.threshold_detected_time is not None:
            if self.threshold_lower_limit <= tps <= self.threshold_upper_limit:
                if (
                    self.threshold_detected_time
                    + datetime.timedelta(0, self.elapsed_seconds)
                    <= datetime.datetime.now()
                ):
                    self.status = (
                        AVAILABLE_STATUSES[1]
                        if self.status == AVAILABLE_STATUSES[0]
                        else AVAILABLE_STATUSES[0]
                    )
                    self.threshold_detected_time = None
            else:
                self.threshold_detected_time = None
        else:
            if self.threshold_lower_limit <= tps <= self.threshold_upper_limit:
                self.threshold_detected_time = datetime.datetime.now()

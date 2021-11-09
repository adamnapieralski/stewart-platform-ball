import time

class PID:

    def __init__(self, P, I, D):

        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.set_point = 0

        self.sample_time = 0
        self.current_time = time.time()
        self.last_time = self.current_time

        self.PTerm = 0
        self.ITerm = 0
        self.DTerm = 0

        self.last_error = 0

        #windup guard

        self.windup_guard = 20

        self.output = 0

    def update(self, feedback):

        error = self.set_point - feedback

        self.current_time = time.time()

        delta_time = self.current_time - self.last_time
        delta_error = error - self.last_error

        if (delta_time >= self.sample_time):

            self.PTerm = error
            self.ITerm += error * delta_time

            if (self.ITerm > self.windup_guard):
                self.ITerm = self.windup_guard
            elif (self.ITerm < -self.windup_guard):
                self.ITerm = -self.windup_guard

            self.DTerm = delta_error / delta_time

            #save last data for next calculation
            self.last_time = self.current_time
            self.last_error = error

            self.output = self.Kp * self.PTerm + self.Ki * self.ITerm + self.Kd * self.DTerm

            return self.output

        else:
            return None

    def setKp(self, Kp):
        self.Kp = Kp

    def setKi(self, Ki):
        self.Ki = Ki

    def setKd(self, Kd):
        self.Kd = Kd

    def setWindup(self, windup):
        self.windup_guard = windup

    def setSampleTime(self, sample_time):
        self.sample_time = sample_time

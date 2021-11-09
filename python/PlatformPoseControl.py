import numpy as np
from pyfirmata import Arduino, util
import math

class Platform:

    def __init__(self):

        self.r_base = 4.
        self.r_plat = 4.5
        self.a_base = (self.r_base * 3. / 2.) * 2. / math.sqrt(3)
        self.a_plat = (self.r_plat * 3. / 2.) * 2. / math.sqrt(3)

        self.arm_r = 3
        self.arm_d = 6

        self.fi_min = 15
        self.fi_max = 180

        self.z90 = math.sqrt(self.arm_d**2 - (math.fabs(self.r_plat - self.r_base - self.arm_r))**2)

        self.r01 = np.array([0, 0, self.z90]).reshape((3, 1))

        self.sB1 = np.array([-self.a_base / 2., -self.r_base / 2., 0]).reshape((3, 1))
        self.sM1 = np.array([-self.a_plat / 2., -self.r_plat / 2., 0]).reshape((3, 1))
        self.sB2 = np.array([self.a_base / 2., -self.r_base / 2., 0]).reshape((3, 1))
        self.sM2 = np.array([self.a_plat / 2., -self.r_plat / 2., 0]).reshape((3, 1))
        self.sB3 = np.array([0, self.r_base, 0]).reshape((3, 1))
        self.sM3 = np.array([0, self.r_plat, 0]).reshape((3, 1))

    def calculatePose(self, alfa, beta, r01):

        r01 = self.r01

        R_01 = self.Ry(beta) @ self.Rx(alfa)

        L1 = math.sqrt(np.reshape((r01 + R_01 @ self.sM1 - self.sB1), (1, 3)) @ (r01 + R_01 @ self.sM1 - self.sB1))

        fi1 = math.pi - math.asin((self.r_plat - self.r_base) / L1) - math.acos(
            (self.arm_r ** 2 + L1 ** 2 - self.arm_d ** 2) / (2 * self.arm_r * L1))

        fi1 = fi1 * 180 / math.pi

        L2 = math.sqrt(np.reshape((r01 + R_01 @ self.sM2 - self.sB2), (1, 3)) @ (r01 + R_01 @ self.sM2 - self.sB2))

        fi2 = math.pi - math.asin((self.r_plat - self.r_base) / L2) - math.acos(
            (self.arm_r ** 2 + L2 ** 2 - self.arm_d ** 2) / (2 * self.arm_r * L2))

        fi2 = fi2 * 180 / math.pi

        L3 = math.sqrt(np.reshape((r01 + R_01 @ self.sM3 - self.sB3), (1, 3)) @ (r01 + R_01 @ self.sM3 - self.sB3))

        fi3 = math.pi - math.asin((self.r_plat - self.r_base) / L3) - math.acos(
            (self.arm_r ** 2 + L3 ** 2 - self.arm_d ** 2) / (2 * self.arm_r * L3))

        fi3 = fi3 * 180 / math.pi

        print(fi1, fi2, fi3)

    def Rx(self, alfa):

        Rx_alfa = np.array([[1, 0, 0], [0, math.cos(alfa), -math.sin(alfa)], [0, math.sin(alfa), math.cos(alfa)]])
        return Rx_alfa

    def Ry(self, beta):

        Ry_beta = np.array([[math.cos(beta), 0, math.sin(beta)], [0, 1, 0], [-math.sin(beta), 0, math.cos(beta)]])
        return Ry_beta



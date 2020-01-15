class Ring:

    def __init__(self, real, ring):
        self.real = real
        self.ring = ring

    def get_real_output(self):
        return int(self.ring[int(self.real)])

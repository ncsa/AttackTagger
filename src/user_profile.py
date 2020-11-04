from flufl.enum import IntEnum
import tables

User_Profile_ = ['previously_compromised', 'remote_login']

User_Profile = IntEnum('User_Profile', zip(User_Profile_, tables._enumiter()))
    
class UserProfile():
    def __init__(self):
        import numpy as np
        self.profile = np.zeros(len(User_Profile_), dtype=int)
    def set_attribute(self, attribute):
        self.profile[int(attribute)] = 1
    def get_attribute(self, attribute):
        return self.profile[int(attribute)]

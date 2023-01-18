import numpy as np
import matplotlib.pyplot as plt

import os
import json
from damsenviet.kle import Keyboard



class keybd:
    """ Keyboard object for regular 30-key layout
    """
    
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def __init__(self, kbd_type = "ortho", layout_path = None):
        """ initialize keyboard object
            1. load layout
            2. get coordinates and index of keys
            3. get hand, finger, and home row assignment of keys
        Args:
            kbd_type (str, optional): predifined layouts, use 'custom' for loading custom layout. Defaults to "ortho".
            layout_path (str, optional): file path to the custom layout, . Defaults to None.
        """
        self.kbd_type = kbd_type
        self.layout = None
        
        if layout_path is not None:
            self.kbd_type = "custom"
            
        if kbd_type == "custom":
            self.layout = self.load_layout(layout_path)
        elif kbd_type == "ortho":
            self.layout = self.ortho()
        elif kbd_type == "staggered":
            self.layout = self.staggered()
        else: 
            print("Keyboard type not supported")
        
        self.n_keys = 30
        
        # coordinates of keys
        self.coords = self.layout_to_coords()
        # meta data of keys
        self.idx_meta = self.layout_to_meta()
        
        # hand, finger_idx, h_row
        self.hand_asgmt = self.idx_meta[:,0]
        self.finger_asgmt = self.idx_meta[:,1]
        self.h_row_asgmt = self.idx_meta[:,2]
        
        # default letter assignments
        self.letters = np.array(['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 
                                 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', 
                                 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '.', ',', '/'])
        
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # layout only contains the mid 3 rows. (tab, caps, and shift rows)
    # 3 rows of 10 keys: 'A'-'Z', '.', ',', , '/', and ';'
    # need to use QWERTY layout
    # see ./img and ./layouts for examples
    def load_layout(self, layout_path):
        json_absolute_file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.realpath('__file__')),
                layout_path,
            )
        )

        print('loading layout from: ', json_absolute_file_path)

        with open(json_absolute_file_path, 'r', encoding='utf-8') as f:
            keyboard = Keyboard.from_json(
                json.load(f)
            )
        return keyboard
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def ortho(self):
        return self.load_layout("./layouts/ortholinear.json")
    
    def staggered(self):
        return self.load_layout("./layouts/staggered.json")
    
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # get the coords of key center from keyboard object
    #   finger-> 0: pinky, 1: ring, 2: middle, 3: index, 4: central column (index)
    #   hand-> 0: left, 1: right
    #   h_row-> 1: home row, 0: others
    #                   finger: 0  1  2  3  4  4  3  2  1  0    h_row:
    #                   hand:   0  0  0  0  0  1  1  1  1  1
    #       +---> x             0  1  2  3  4  5  6  7  8  9        2
    #       |                   10 11 12 13 14 15 16 17 18 19       0
    #       ↓ y                 20 21 22 23 24 25 26 27 28 29       1
    def layout_to_coords(self): # not working for ergo, idx need to be converted
        coords = np.zeros((self.n_keys, 2))
        idx = 0
        
        for key in self.layout.keys:
            coords[idx, :] = (key.x, key.y) # center of key, assume all keys are square
            idx += 1
        return coords
    
    
    def layout_to_meta(self):
        meta = np.zeros((self.n_keys, 3))
        for idx in range(self.n_keys):
            meta[idx, :] = self.idx_to_meta(idx)
        return meta
    
    # hand, finger, home row
    def idx_to_meta(self, idx):
        # left hand
        if idx%10 <= 4:
            hand = 0                # 0 for left hand
            finger_idx = idx % 5        # 0-4 for fingers
        else:
            hand = 1                # 1 for right hand
            finger_idx = 4-idx % 5      # 0-4 for fingers
        
        if idx<=9: h_row = 2            # 2 for top row
        elif 10<= idx <= 19: h_row = 0  # 0 for home row
        else: h_row = 1                 # 1 for bottom rows
        return np.array([hand, finger_idx, h_row])
    
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def print_by_layout(self, array, to_int = True):
        is_list = isinstance(array[0], list) or isinstance(array[0], np.ndarray)
        for i in range(self.n_keys):
            out = array[i]
            if to_int:
                if is_list: out = [int(x) for x in out]
                else: out = int(out)
            print(out, end = " ")
            if i%10 == 9:
                print("")
        print("")
    
    
    
    
    
    
    
    
    
    
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # TODO: convert ergo layout index to regular index
    def convert_ergo_idx(self, key = None, idx = None):
        pass
    
    

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class hand:
    # 0: pinky, 1: ring, 2: middle, 3: index,
    def __init__(self, f, f_std):
        self.fingers = f
        self.fingers_std = f_std

class hands2:
    def __init__(self):
        self.LR = None
        
        self.init_paper_r()

    def init_paper_r(self):
        # initialize using data from paper (right handed)
        # tapping rate data from paper (per 5s)
        # An Estimation of Finger-Tapping Rates and Load Capacities and the Effects of Various Factors
        # https://www.researchgate.net/publication/274641777_An_Estimation_of_Finger-Tapping_Rates_and_Load_Capacities_and_the_Effects_of_Various_Factors
        L = np.array([17.2, 18.5, 19.6, 19.7])
        R = np.array([19.7, 21.2, 21.9, 21.8])
        
        L_std = np.array([4.1, 4.3, 4.3, 4.4])
        R_std = np.array([4.9, 5.1, 5.3, 5.3])
        
        self.LR = [hand(L, L_std), hand(R, R_std)]


        # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6704118/
        self.i_side = np.sqrt(6.9*4.8)/6.9 # 0.83
        
        self.rl_ratio = np.sum(self.R)/np.sum(self.L)

# class hand:
#     # 0: pinky, 1: ring, 2: middle, 3: index,
#     def __init__(self):
#         self.L = None
#         self.R = None
        
#         self.L_std = None
#         self.R_std = None
        
#         # speed ratio between left and right hand
#         self.lr_ratio = None
        
#         # leftward penalty of right index finger, or the other way around
#         self.i_side = None
            
#     # initialize using data from paper (right handed)
#     def init_paper_r(self):
#         # tapping rate data from paper (per 5s)
#         # An Estimation of Finger-Tapping Rates and Load Capacities and the Effects of Various Factors
#         # https://www.researchgate.net/publication/274641777_An_Estimation_of_Finger-Tapping_Rates_and_Load_Capacities_and_the_Effects_of_Various_Factors
#         self.L = np.array([17.2, 18.5, 19.6, 19.7])
#         self.R = np.array([19.7, 21.2, 21.9, 21.8])
        
#         self.L_std = np.array([4.1, 4.3, 4.3, 4.4])
#         self.R_std = np.array([4.9, 5.1, 5.3, 5.3])
        
#         # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6704118/
#         self.i_side = np.sqrt(6.9*4.8)/6.9 # 0.83
        
#         self.rl_ratio = np.sum(self.R)/np.sum(self.L)
        
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        
class letter_stats:
    def __init__(self):
        self.letters = None
        self.freq = None
        
    def init(self):
        letters26 = [chr(i) for i in range(65, 91)]
        self.letters = np.array(['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 
                                 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', 
                                 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '.', ',', '/'])

        freq26 = np.array([8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 
                           0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 
                           6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074])/100
        
        freq_punc = 

    

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class evolution:
    def __init__(self, crossover_type, mutation_type, replacement_scheme, 
                    pop_size, n_gen, n_elite, n_mutate, n_crossover):
        self.crossover_type = crossover_type
        self.mutation_type = mutation_type
        self.replacement_scheme = replacement_scheme
        
        self.pop_size = pop_size
        self.n_gen = n_gen
        self.n_elite = n_elite
        self.n_mutate = n_mutate
        self.n_crossover = n_crossover
        
        self.kbd = None
    
    def init_kbd(self, kbd_type = "ortho", layout_path = None):
        self.kbd = keybd(kbd_type = kbd_type, layout_path = layout_path)
    
    def init_finger(self, finger_strength = np.array([2, 3.5, 4.5, 5])):
        """ initialize finger strength, normalized to length 1
        Args:
            finger_strength (ndarray, optional): strength of fingers [pinky, ring, middle, index, index mid]. 
                                                 Defaults to [2, 3.5, 4.5, 5].
        """
        self.finger_strength = finger_strength# / np.linalg.norm(finger_strength)
    
    def init_mid_col(self, hands, factor = None):
        if factor is None:
             factor = 1/hands.rl_ratio
        



    def cost_2_hands(self, kbd, hand, cost_type = 0):       
        """_summary_

        Args:
            kbd (keybd object): keyboard object, includes coordinates of keys
            hand (hands object): hand object, includes tapping rate of fingers
            cost_type (int, optional): _description_. Defaults to 0.
        """
        
    
    
    

    
    
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if __file__ == "__main__":
    kbd = keybd(kbd_type = "ortho")
    print(kbd.coords)
    
    
    
    
    
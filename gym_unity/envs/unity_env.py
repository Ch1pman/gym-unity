import cv2, gym
from gym import error, spaces, utils
import getCams
from gym.utils import seeding 


class UnityEnv(gym.Env, ipManager):
    Manager = ipManager
    fullInitFlag = False
    metadata = {'render.modes': ['human']}
    #HOST = '' ;  # Symbolic name, meaning all available interfaces
    #PORT = 8888; # Arbitrary non-privileged port
    numCams = 1; # number of cameras
    w = 256;
    h = 256;
    numPixel = 3;
    bufSize= 4096;
    getCamsObj = None;
    imageStore = None;
    numCams = 1;
    writePng = True;
    
    Enqueued = False
    HOST = 0
    PORT = 0
    
    def __init__(self):

        #Insert camera input dimensions
        self.observation_space = spaces.Box(low=0, high=255, shape=(256,256,3))

        #Insert number of possible actions
        self.action_space = spaces.Discrete(7)

    def finishInit(self):
        self.Manager.addToQueue(self)
        
        #Wait until Unity has been loaded successfully, IP and PORT are passed
        while self.Enqueued or self.HOST == 0 or self.PORT == 0:
           pass
        
        # instantiate GetCams object
        self.getCamsObj = getCams(self.HOST, self.PORT, self.numCams, self.w,
                                  self.h, self.numPixel, self.bufSize, self.writePng);
        # open socket
        self.getCamsObj.open();

    def check_init_state(self):
        if not fullInitFlag:
            finishInit()
            fullInitFlag = True
    
    def __del__(self):
        #cleanup
        self.getCamsObj.close();
        
    def _step(self, action):
        check_init_state()
        # supply action
        self.getCamsObj.sendAction(self.ACTION_LOOKUP[action]);
        # get obs camera data that results from action and reward
        data, reward, done = self.getCamsObj.get();
        # store images
        self.imageStore = data
        # extract obs and reward

        return data, reward, done
        
    def _reset(self):
        check_init_state()
        #At the end of episode send command to reset
        #   getCamsObj.sendAction(reset)
        # release the IP from the IP manager
        
        self.getCamsObj.sendAction(4)
        
        data, _, _ = self.getCamsObj.get()
        self.imageStore = data
        
        return data

    def _render(self):
        check_init_state()
        #TODO we want to display our camera images here.
        # make images 2 rows of 4 and show them

        #cv2.imwrite('currentState.jpg', imageStore)
        cv2.imshow('currentState', self.imageStore)

    #TODO: Define actions
    ACTION_LOOKUP = {
        0 : 0, 
        1 : 1,
        2 : 2,
        3 : 3,
        4 : 4,
        5 : 65534,
        6 : 65535,
    }

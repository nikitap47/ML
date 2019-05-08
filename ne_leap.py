
import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture,ScreenTapGesture,SwipeGesture

from pymongo import MongoClient

class LeapMotionListener(Leap.Listener):
    
    finger_names=['Thumb','Index','Middle','Ring','Pinky']
    bone_names=['Metacarpal','Proximal','Intermediate','Distal']
    state_names=['STATE_INVALID','STATE_START','START_UPDATE','STATE_END']
    
    
    def on_init(self,controller):
        print("initialised")
        

    def on_connect(self,controller):
        print("motion sensor connected")
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
    
        
   
    def on_disconnect(self,controller):
        print("motion sensor disconnected")
        
    def on_exit(self,controller):
        print("exited")
        
    def on_frame(self,controller):
        
        client = MongoClient("mongodb://localhost:27017/")
        mydatabase = client['Project']
        myc=mydatabase.myLeap
        
        frame=controller.frame()
        """print "Frame ID: " + str(frame.id)\
        + "Timestamp:" + str(frame.timestamp)\
        + "# of Hands" + str(len(frame.hands))\
        + "# of Fingers " + str(len(frame.fingers))\
        + "# of Tools " + str(len(frame.tools))\
        + "# of Gestures" + str(len(frame.gestures()))"""
        abc=frame.hands
        for hand in frame.hands:
            basis = hand.basis
            handType = "Left Hand " if hand.is_left else "Right Hand"
            normal = hand.palm_normal
            direction = hand.direction
            arm = hand.arm
            
            for pic in range(5):
                for b in range(0,4):
                    for finger in hand.fingers:
                        bone = finger.bone(b)
                        pic ={"Palm Position": str(hand.palm_position)\
                              ,"Sphere radius" : str(hand.sphere_radius)\
                              ,"Finger Name": self.finger_names[finger.type]\
                              ,"Bone type" : self.bone_names[bone.TYPE_DISTAL]\
                              ,"Bone end" : str(bone.next_joint)}
                        print(pic)
                        rec = myc.insert(pic)
                    
                       
def main():
        listener= LeapMotionListener()
        controller= Leap.Controller()
        controller.add_listener(listener)
        print("press enter to quit")
        try:
            sys.stdin.readline()
        except KeyboardInterrupt:
            pass
        finally:
            controller.remove_listener(listener)
            


    
if __name__ == "__main__":
        main()
    
            
     
        
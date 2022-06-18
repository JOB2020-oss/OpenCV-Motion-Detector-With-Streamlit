import streamlit as st
import cv2
import winsound

st.header("OPEN CV MOTION DETECTOR WITH ALERT")
st.markdown("Refresh to stop the camera")

def camera_move():
    camera = cv2.VideoCapture(0)
    frame_window = st.image([])#In instance of image frame which will dispaly image on screen
    while camera.isOpened():
        ret,frame1 = camera.read()
        frame1 = cv2.cvtColor(frame1,cv2.COLOR_BGR2RGB)
        ret,frame2 = camera.read()
        diff = cv2.absdiff(frame1,frame2)
        gray = cv2.cvtColor(diff,cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        _,thresh = cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh,None,iterations=3)
        contour,_ = cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(frame1,contour,-1,(0,255,0),2)
        for c in contour:
            if cv2.contourArea(c) < 5000:
                continue
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),10)
            winsound.Beep(1000,200)
        if cv2.waitKey(10) == ord('q'):
            break
        frame_window.image(frame1,caption="KILIMANJARO FRAME",width=400)
    camera.release()
    cv2.destroyAllWindows()
if st.button("START"):
    camera_move()

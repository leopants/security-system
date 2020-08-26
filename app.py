from flask import Flask, render_template, Response, url_for, redirect, session, request
from camera import VideoCamera
from sys import stdout
import logging
import cv2
from datetime import date

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
video = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc('H','2','6','4')
fps = video.get(cv2.CAP_PROP_FPS)
fps = 30.0
size = (
    int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
    int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)),
)
print(size, fps)
out = cv2.VideoWriter()
success = out.open(str(date.today()) + '.avi', fourcc, fps, size, True)
print(success)

try:
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/logout')
    def logout():
        return redirect('/')

    @app.route('/login', methods=['POST'])
    def handle_login():
        try:
            password = request.form['password']
            print(password)
            if password == 'juan':
                return redirect('/stream')
            else:
                return 'Incorrect password'
        except:
            return 'oh oh'

    @app.route('/static/')
    def staticfeed():
        return render_template('static.html')

    def gen(camera):
        while True:
            success, image = camera.read()
            out.write(image)
            ret, jpeg = cv2.imencode('.jpg', image)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    @app.route('/stream/')
    def dynamic():
        return render_template('stream.html')

    @app.route('/video1')
    def video1():
        return render_template("video1.html")
        
    @app.route('/video_feed')
    def video_feed():
        return Response(gen(video),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

except KeyboardInterrupt:
    video.release()
    out.release()
    cv2.destroyAllWindows()


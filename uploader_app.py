from flask import *
from werkzeug.utils import secure_filename
import os
from keras.preprocessing import image
from keras.models import load_model
import numpy as np

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload',methods=['POST'])
def upload():
    
    allowed_formats = set(['.png','.gif','.jpg','.jpeg','.svg','.bmp'])

    classes = {
        0:'Speed limit (20km/h)',
        1:'Speed limit (30km/h)',
        2:'Speed limit (50km/h)',
        3:'Speed limit (60km/h)',
        4:'Speed limit (70km/h)',
        5:'Speed limit (80km/h)',
        6:'End of Speed limit (80km/h)',
        7:'Speed limit (100km/h)',
        8:'Speed limit (120km/h)',
        9:'No Passing',
        10:'No Passing veh over 3.5 tons',
        11:'Right-of-way at intersection',
        12:'Priority Road',
        13:'Yield',
        14:'Stop',
        15:'No Vehicles',
        16:'Veh > 3.5 tons Prohibited',
        17:'No entry',
        18:'General Caution',
        19:'Dangerous Curve Left',
        20:'Dangerous Curve Right',
        21:'Double Curve',
        22:'Bumpy Road',
        23:'Slippery Road',
        24:'Road Narrows On The Right',
        25:'Road Work',
        26:'Traffic Signals',
        27:'Pedestrians',
        28:'Children Crossing',
        29:'Bicycles Crossing',
        30:'Beware Of ice/Snow',
        31:'Wild Animals Crossing',
        32:'End Speed + Passing Limits',
        33:'Turn Right Ahead',
        34:'Turn Left Ahead',
        35:'Ahead Only',
        36:'Go Straight Or Right',
        37:'Go Straight or Left',
        38:'Keep Right',
        39:'Keep Left',
        40:'Roundabout mandatory',
        41:'End Of No Passing',
        42:'End No Passing Veh > 3.5 tons'
    }

    target = os.path.join(APP_ROOT, 'images/')
    
    if not os.path.isdir(target):
        os.mkdir(target)
    
    files = request.files.getlist('file')
    if files!=[]:
        for file in files:
            filename = file.filename

            ext = os.path.splitext(filename)[1]

            if ext.lower() not in allowed_formats:
                flag = 1
                return render_template('success.html', filename=filename, status = flag)


            destination = '/'.join([target,filename])
            file.save(destination)

        model = load_model(r'E:\downloads\Douyin\input\BG\TrafficSignRecognition-master\TrafficSignRecognition-master\Traffic_Sign_Recognition_model.h5')

        filepaths = [target+file.filename for file in files]

        predictions = []

        for filepath in filepaths:
            img = image.load_img(filepath,target_size=(30,30,3))
            img = img.resize((30,30))
            img = np.expand_dims(img, axis=0)
            img = np.array(img)

            pred = model.predict([img])[0]
            max_pred_index = np.argmax(pred)
            sign = classes[max_pred_index]
            predictions.append(sign)

        return render_template('success.html', filename=[file.filename for file in files], signname=predictions)

    else:
        return render_template('success.html', filename='')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory('images',filename)

if __name__ == '__main__':
    app.run(debug=True)

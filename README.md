# Aves-Camera-Recognition

Aves-Camera-Recognition: AI-based attendance system to automatically keep attendance of employees and residents based on face/body tracking and 3D positioning. Features a front-end react.js based website to manually change employee attendance data and displays employee 
attendnace metrics. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Look at "Built With" below for instructions on installing requires prerequisites.

facenet-pytorch        2.6.0
filelock               3.14.0
Flask                  3.0.3
Flask-Cors             4.0.1
Flask-SocketIO         5.3.6
fonttools              4.53.1
fsspec                 2024.6.0
h11                    0.14.0
Jinja2                 3.1.4
kiwisolver             1.4.5
MarkupSafe             2.1.5
matplotlib             3.9.1
mkl                    2021.4.0
mpmath                 1.3.0
mysql-connector-python 9.0.0
networkx               3.3
numpy                  1.26.4
opencv-python          4.10.0.84
packaging              24.1
pandas                 2.2.2
pillow                 10.4.0
psutil                 6.0.0
py-cpuinfo             9.0.0
pyparsing              3.1.2
python-dateutil        2.9.0.post0
python-engineio        4.9.1
python-socketio        5.11.3
pytz                   2024.1
PyYAML                 6.0.1
requests               2.32.3
scipy                  1.14.0
seaborn                0.13.2
setuptools             71.0.2
simple-websocket       1.0.0
six                    1.16.0
smmap                  5.0.1
sympy                  1.12.1
tbb                    2021.12.0
torch                  2.2.2
torchaudio             2.3.1
torchvision            0.17.2
tqdm                   4.66.4
typing_extensions      4.12.2
tzdata                 2024.1
ultralytics            8.2.59
ultralytics-thop       2.0.0
urllib3                2.2.2
Werkzeug               3.0.3
wsproto                1.2.0
```

### Running the program

A step by step series of examples that tell you how to get a development env running

Identifying door coordinates

```
Run originalCode.py in the YoloV5 folder to pull up the mouse positioning coordinate system.
This will display the x, y coordinates of your mouse cursor due to a function within this portion of code.
Take your cursor to the upper left (x,y) set of the door and bottom right (x,y) set of the door and take note of them.
Then go to main.py, line 105 has a list of 4 integers that should be updated in this order [upper right x val, uper right y val, bottom left x val, bottom left y val].
And then the coordinates are good to go.
```

Rapid face imaging taking

```
Run capture.py in the server folder to rapidly take images, make sure you have a folder in "faces_dataset" with your name in it.
Frame_count is the image file name that it will start off at, so make sure there are no duplicate image file names. 
```

Training and embedding faces into a pt file

```
Run embed_faces.pt multiple times until all faces are loaded into known_faces.pt,
note that this can take several minutes depending on the amount of images in faces_dataset.
```

MySQL database setup

```
Create your own MySQL database and make a connection to it via MySQL workbench and run db_config.py in the server file to intitialize employee/resident values,
note that you must changedb_config.py parameters to match your own.
```

Starting program

```
run main.py and npm start the client in two separate terminals. Done.
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain for how to run tests for this system

### Create a >2 min mp4 of employees or residents walking in and out of the door

This test should determine if the statistics and attendance tracking is working, the client should be updated immediately.

```
Look at KamTestFinal.mp4
```

## Built With

* [PyTorch](https://pytorch.org/docs/stable/index.html) - The maching learning library used
* [React.JS](https://react.dev/) - The web framework used
* [OpenCV](https://opencv.org/releases/) - Camera work and management 
* [Flask](https://flask.palletsprojects.com/en/3.0.x/) - Used to create API endpoints
* [Socket.IO](https://socket.io/) - Used for real-time communication between server and client
* [MySQL](https://dev.mysql.com/doc/) - Database used for interlapping data and scaling support
* [Pandas](https://pandas.pydata.org/) - Data manipulation and analysis used
* [Matplotlib](https://matplotlib.org/) - Data analysis and visualization
* [MTCNN](https://github.com/ipazc/mtcnn) - MIT licensed CNN for face detection
* [YoloV5](https://pytorch.org/hub/ultralytics_yolov5/) - PyTorch model used for body detection
  
## Contributing

Please read [CONTRIBUTING.md](https://github.com/AaronQTran/Aves-Camera-Recognition/blob/main/CONTRIBUTING.md) for details on our code of conduct

## Authors

* **Kamryn Hoffman** 
* **Aaron Tran** 
* See also the list of [contributors](https://github.com/AaronQTran/Aves-Camera-Recognition/graphs/contributors) who participated in this project.

## Acknowledgments

* Kamryn Hoffman - (https://github.com/KamrynH-CS), (https://www.linkedin.com/in/kamryn-hoffman-75778929a/)
* Aaron Tran - (https://github.com/AaronQTran), (https://www.linkedin.com/in/aarontran4/)
* Inspiration - Kamryn and I were tired of having to manually mark our attendance on a computer or on a clipboard everyday at the various places we worked at so we wanted to fix this issue by making attendance keeping easier for the employer and employee. 

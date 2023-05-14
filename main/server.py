from flask import Flask, render_template, send_file, send_from_directory, request
from flask_cors import CORS
import os
import time
import subprocess
from datetime import datetime
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app)

@app.route('/run-openCV', methods=['GET'])
def localDeploy():
    try:
        subprocess.Popen(['python', 'proj.py'])
        return 'Main script execution initiated.'
    except Exception as e:
        return f'Error executing main script: {str(e)}'

@app.route('/renderVehicleCount')
def readAllFiles():
    pathDir = 'C:/Users/Ashar/Documents/NUCES/Study/SEM-2/ISE/PROJECT/Newfolder/textoutputs'
    vehicleSum = 0
    for file_name in os.listdir(pathDir):
        if file_name.endswith('.txt'):
            file_path = os.path.join(pathDir, file_name)
            with open(file_path, 'r') as f:
                vehicleSum += int(f.read())
    return str(vehicleSum)

@app.route('/renderVehiclesLeft')
def readVehiclesLeft():
    with open('vehiclesleft.txt', 'r') as file:
        file_content = file.read()
    return str(file_content)

@app.route('/renderVehiclesLeftToday')
def readVehiclesLeftToday():
    with open('vehiclesLeftToday.txt', 'r') as file:
        file_content_2 = file.read()
    return str(file_content_2)

@app.route('/renderLowestFreq')
def lowestFrequency():
    pathDir = 'C:/Users/Ashar/Documents/NUCES/Study/SEM-2/ISE/PROJECT/Newfolder/textoutputs'
    lowestFrequency = 10000
    lowestFile = ''
    for file in os.listdir(pathDir):
        if file.endswith('.txt'):
            file_path = os.path.join(pathDir, file)
            with open(file_path, 'r') as f:
                file_content = f.read()
                if int(file_content) < lowestFrequency:
                    lowestFrequency = int(file_content)
                    lowestFile = file
        if lowestFile:
            # Extract the date and time parts from the timestamp
            date_part = lowestFile[11:13] + "/" + lowestFile[14:16] + "/" + lowestFile[17:19]
            time_part = lowestFile[20:22] + ":" + lowestFile[23:25] + ":" + lowestFile[26:28]

            # Format the timestamp
            formatted_timestamp = f"{date_part} {time_part}"
            #print(formatted_timestamp)



    return formatted_timestamp

@app.route('/renderHighestFreq')
def highestFrequency():
    pathDir = 'C:/Users/Ashar/Documents/NUCES/Study/SEM-2/ISE/PROJECT/Newfolder/textoutputs'
    highestFrequency = 0
    highestFile = ''
    for file in os.listdir(pathDir):
        if file.endswith('.txt'):
            file_path = os.path.join(pathDir, file)
            with open(file_path, 'r') as f:
                file_content = f.read()
                if int(file_content) > highestFrequency:
                    highestFrequency = int(file_content)
                    highestFile = file
        if highestFile:
            # Extract the date and time parts from the timestamp
            date_part = highestFile[11:13] + "/" + highestFile[14:16] + "/" + highestFile[17:19]
            time_part = highestFile[20:22] + ":" + highestFile[23:25] + ":" + highestFile[26:28]

            # Format the timestamp
            formatted_timestamp = f"{date_part} {time_part}"
            #print(formatted_timestamp)
        return formatted_timestamp
    
@app.route('/graphAllFiles')
def graphFiles():
    pathDir = 'C:/Users/Ashar/Documents/NUCES/Study/SEM-2/ISE/PROJECT/Newfolder/textoutputs'
    dataList = []
    dateList = []
    for file_name in os.listdir(pathDir):
        if file_name.endswith('.txt'):
            file_path = os.path.join(pathDir, file_name)
            with open(file_path, 'r') as f:
                intData = f.read()
                dataList.append(int(intData))
                dateList.append(file_name[17:19])
    plt.plot(dateList, dataList)
    plt.xlabel('Day')
    plt.ylabel('Number of vehicles')
    plt.title('Vehicle Count Graphed')
    plt.savefig('dayXcountYgraph.png')
    plt.close()
    # if os.path.exists('dayXcountYgraph.png'):
    #     os.remove('dayXcountYgraph.png')
    # else:
    #     plt.savefig('dayXcountYgraph.png')
    #     plt.close()
    return send_file('dayXcountYgraph.png', mimetype='image/png')

@app.route('/renderVehicleCountToday')
def getVehicleCountToday():
    pathDir = 'C:/Users/Ashar/Documents/NUCES/Study/SEM-2/ISE/PROJECT/Newfolder/textoutputs'
    vehicleSumToday = 0
    for file_name in os.listdir(pathDir):
        if file_name.endswith('.txt') and file_name[17:19] == datetime.now().strftime("%d"):
            file_path = os.path.join(pathDir, file_name)
            with open(file_path, 'r') as f:
                vehicleSumToday += int(f.read())
    return str(vehicleSumToday)


@app.route('/saveUserData', methods=['POST'])
def save_user_data():
    print("in func")
    user_data = request.get_json()
    
    name = user_data.get('name')
    password = user_data.get('password')
    
    file_path = 'C:/Users/Ashar/Documents/NUCES/Study/SEM-2/ISE/PROJECT/Newfolder/textoutputs/userdata.txt'
    directory = os.path.dirname(file_path)

    with open(file_path, 'a') as file:
        file.write(f'{name}, {password}\n')

    return 'User data saved successfully'




if __name__ == '__main__':
    app.run(debug=True)


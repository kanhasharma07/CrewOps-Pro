from flight_crew import FlightCrew

from flask import Flask, url_for, redirect, render_template, request

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/addCrew', methods = ['GET', 'POST'])
def addCrew():
    
    if request.method == 'GET':
        return render_template('addCrew.html')
    else:
        receivedFlightCrewData =[
            request.form['sap'],
            request.form['fname'],
            request.form['lname'],
            request.form['desig'],
            request.form['mob'],
            request.form['atpl'],
            request.form['license'],
            request.form['medical'],
            request.form['baseops'],
            True,
            request.form['pw']
        ]
    
        FlightCrew.addCrew(receivedFlightCrewData[0],
                           receivedFlightCrewData[1],
                           receivedFlightCrewData[2],
                           receivedFlightCrewData[3],
                           receivedFlightCrewData[4],
                           receivedFlightCrewData[5],
                           receivedFlightCrewData[6],
                           receivedFlightCrewData[7],
                           receivedFlightCrewData[8],
                           receivedFlightCrewData[9],
                           receivedFlightCrewData[10],
                           )
        
        
        print(receivedFlightCrewData)
        return render_template('addflightcrewsuccessful.html')
    
@app.route('/viewCrew')
def viewCrew():
    crewView = FlightCrew.viewCrew()
    return render_template('viewCrew.html', crewView=crewView)

# @app.route('/test')
# def test():
#     return render_template('addflightcrewsuccessful.html')

if __name__=='__main__':
    app.run(port=8000, debug=True)

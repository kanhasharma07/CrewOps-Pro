from flight_crew import FlightCrew
from ame_crew import AMECrew
from flask import Flask, url_for, redirect, render_template, request

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")

# Flight Crew Management Routes
@app.route("/addCrew", methods=["GET", "POST"])
def addCrew():
    if request.method == "GET":
        return render_template("addCrew.html")
    else:
        receivedFlightCrewData = [
            request.form["sap"],
            request.form["fname"],
            request.form["lname"],
            request.form["desig"],
            request.form["mob"],
            request.form["atpl"],
            request.form["license"],
            request.form["medical"],
            request.form["baseops"],
            True,
            request.form["pw"],
        ]

        FlightCrew.addCrew(
            receivedFlightCrewData[0],
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
        return render_template("addflightcrewsuccessful.html")


@app.route("/viewCrew")
def viewCrew():
    crewView = FlightCrew.viewCrew()
    return render_template("viewCrew.html", crewView=crewView)


@app.route("/deleteCrew", methods=["GET", "POST"])
def deleteCrew():
    if request.method == "GET":
        return render_template("deleteCrew.html")
    else:
        FlightCrew.deleteCrew(sap=request.form["sap"])
        return render_template("deleteCrewSuccessful.html", sap=request.form["sap"])


@app.route("/modifyCrew", methods=["GET", "POST"])
def modifyCrew():
    if request.method == "GET":
        return render_template("modifyCrew.html")
    else:
        formData = [
            request.form["sap"],
            request.form["fname"],
            request.form["lname"],
            request.form["desig"],
            request.form["mob"],
            request.form["atpl"],
            request.form["license"],
            request.form["medical"],
            request.form["baseops"],
            "",
            request.form["login"],
            request.form["pw"],
        ]
        FlightCrew.modifyCrew(int(request.form["sap"]), formData)
        return render_template("modifyCrewSuccess.html", sap=request.form["sap"])


@app.route("/applyLeave", methods=["GET", "POST"])
def updateAvail():
    if request.method == "GET":
        return render_template("updateAvail.html")
    else:
        sap = int(request.form["sap"])
        availBool = request.form["leave"]
        FlightCrew.updateAvail(sap, availBool)
        return render_template("updateAvailSuccess.html", availBool=availBool, sap=sap)


# AME management Routes
@app.route('/addAME', methods=['GET', 'POST'])
def addAME():
    if request.method=="GET":
        return render_template('addAME.html')
    else:
        crewData = [request.form['sap'],
                    request.form['name'],
                    request.form['fleet'],
                    request.form['pw']]
        AMECrew.addCrew(crewData=crewData)
        return render_template('addAMEsuccess.html')
    
@app.route('/viewAME')
def viewAME():
    actype = {'A320':'Airbus A320', 'B737':'Boeing 737', 'B777':'Boeing 777', 'B787': 'Boeing 787', 'A350':'Airbus A350'}
    crewData = AMECrew.viewCrew()
    return render_template('viewAME.html', crewData=crewData, actype=actype)
    
        

# @app.route('/test')
# def test():
#     return render_template('deleteCrew.html')

if __name__ == "__main__":
    app.run(port=8000, debug=True)

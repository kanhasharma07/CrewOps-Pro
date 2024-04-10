from aircraft import Aircraft
from flight_crew import FlightCrew
from ame_crew import AMECrew
from flights import Flight
from roster import Roster
from training import Training
from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


# Flight Crew Management
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
@app.route("/addAME", methods=["GET", "POST"])
def addAME():
    if request.method == "GET":
        return render_template("addAME.html")
    else:
        crewData = [
            request.form["sap"],
            request.form["name"],
            request.form["fleet"],
            request.form["pw"],
        ]
        AMECrew.addCrew(crewData=crewData)
        return render_template("addAMEsuccess.html")


@app.route("/viewAME")
def viewAME():
    actype = {
        "A320": "Airbus A320",
        "B737": "Boeing B737",
        "B777": "Boeing B777",
        "B787": "Boeing B787",
        "A350": "Airbus A350",
    }
    crewData = AMECrew.viewCrew()
    return render_template("viewAME.html", crewData=crewData, actype=actype)


@app.route("/deleteAME", methods=["GET", "POST"])
def deleteAME():
    if request.method == "GET":
        return render_template("deleteAME.html")
    else:
        AMECrew.deleteCrew(sap=request.form["sap"])
        return render_template("deleteAMESuccess.html", sap=request.form["sap"])


@app.route("/modifyAME", methods=["POST", "GET"])  # type: ignore
def modifyAME():
    if request.method == "GET":
        return render_template("modifyAME.html")
    else:
        oldData = [
            request.form["sap"],
            request.form["name"],
            request.form["fleet"],
            request.form["login"],
            request.form["pw"],
        ]
        AMECrew.modifyCrew(oldData, int(request.form["sap"]))
        return render_template("modifyAMESuccess.html")


# Aircraft Management
@app.route("/addac", methods=["POST", "GET"])
def addAC():
    if request.method == "GET":
        return render_template("addAC.html")
    else:
        acdata = [
            request.form["msn"],
            request.form["type"],
            "VT-" + request.form["regn"],
            request.form["avail"],
            request.form["engine"],
            request.form["engine_hours"],
        ]
        Aircraft.addAircraft(acdata)
        return render_template("addACSuccess.html")


@app.route("/viewAC")
def viewAC():
    actype = {
        "A320": "Airbus A320",
        "B737": "Boeing 737",
        "B777": "Boeing 777",
        "B787": "Boeing 787",
        "A350": "Airbus A350",
    }
    acData = Aircraft.viewAircraft()
    return render_template("viewAC.html", acData=acData, actype=actype)


@app.route("/deleteAC", methods=["POST", "GET"])
def deleteAC():
    if request.method == "GET":
        return render_template("deleteAC.html")
    else:
        msn = request.form["msn"]
        Aircraft.deleteAircraft(int(msn))
        return render_template("deleteACSuccess.html", msn=msn)


@app.route("/modifyAC", methods=["GET", "POST"])
def modifyAC():
    if request.method == "GET":
        return render_template("modifyAC.html")
    else:
        newData = [
            request.form["msn"],
            request.form["type"],
            request.form["regn"],
            request.form["avail"],
            request.form["engine"],
            request.form["engine_hours"],
        ]
        print(newData)
        Aircraft.modifyAircraft(newData, int(request.form["msn"]))
        return render_template("modifyACSuccess.html")


# Flights Management
@app.route("/addFlight", methods=["GET", "POST"])
def addFlight():
    if request.method == "GET":
        return render_template("addFlight.html")
    else:
        flightData = [
            request.form["flight_no"],
            request.form["dep"],
            request.form["arr"],
            [request.form["etd"][0:2], request.form["etd"][2:4]],
            [request.form["eta"][0:2], request.form["eta"][2:4]],
            request.form["actype"],
            [request.form["duration"][0:2], request.form["duration"][2:4]],
        ]
        Flight.addFlight(flightData)
        return render_template("addFlightSuccess.html")


@app.route("/viewFlights", methods=["GET", "POST"])
def viewFlights():
    flts = Flight.viewFlights()
    return render_template("viewFlights.html", flts=flts)


@app.route("/deleteFlight", methods=["GET", "POST"])
def deleteFlight():
    if request.method == "GET":
        return render_template("deleteFlight.html")
    else:
        flt_no = int(request.form["flight_no"])
        Flight.deleteFlight(flt_no)
        return render_template("deleteFlightSuccess.html", flt_no=flt_no)


# MONTHLY ROSTER MANAGEMENT
@app.route("/createRoster", methods=["GET", "POST"])
def createRoster():
    if request.method == "GET":
        return render_template("createRoster.html")
    else:
        month = int(request.form["month"])
        Roster.addRoster(month=month)
        return render_template("createRosterSuccessful.html")


@app.route("/viewRoster", methods=["GET", "POST"])
def viewRoster():
    if request.method == "GET":
        return render_template("rosterSAPInput.html")
    else:
        sap = int(request.form["sap"])
        pairs = Roster.viewYourRoster(sap=sap)
        return render_template("viewRoster.html", pairs=pairs)


# TRAINING MANAGEMENT
@app.route("/addTraining.", methods=["GET", "POST"])
def addTraining():
    if request.method == "GET":
        return render_template("addTraining.html")
    else:
        trgdata = [
            request.form["trgid"],
            request.form["trgname"],
            request.form["trgdesc"],
            request.form["trainerid"],
            request.form["traineeid"],
            request.form["trgdate"],
            request.form["trglocation"],
            [request.form["duration"][0:2], request.form["duration"][2:4]],
        ]
        Training.addTraining(trgdata=trgdata)

        FlightCrew.updateAvail(int(request.form["trainerid"]), False)
        FlightCrew.updateAvail(int(request.form["traineeid"]), False)

        return render_template("addTrainingSuccess.html")


@app.route("/viewTrainings")
def viewTrainings():
    trgdata = Training.viewTrainings()
    return render_template("viewTraining.html", trgdata=trgdata)


@app.route("/deleteTraining", methods=["GET", "POST"])
def deleteTraining():
    if request.method == "GET":
        return render_template("deleteTraining.html")
    else:
        trgid = int(request.form["trgid"])
        Training.deleteTraining(trgid)
        return render_template("deleteTrainingSuccess.html")


# @app.route('/test')
# def test():
#     return render_template('deleteCrew.html')

if __name__ == "__main__":
    app.run(debug=True, port=8000)

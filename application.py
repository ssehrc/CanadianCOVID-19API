from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Case(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prname = db.Column(db.String(80), nullable=False) #province name (removed unique constraint) 
    date = db.Column(db.String(10), nullable=False) #date in YYYY-MM-DD format 
    cases = db.Column(db.Integer, nullable=False) #number of cases
    deaths = db.Column(db.Integer, nullable=False) #number of deaths
    recovered = db.Column(db.Integer, nullable=False) #number of recovered
    weekly_cases = db.Column(db.Integer, nullable=False) #number of weekly cases
    weekly_deaths = db.Column(db.Integer, nullable=False) #number of weekly deaths
    
    def __repr__(self):
        return f"{self.prname} - {self.date} - {self.cases} - {self.deaths} - {self.recovered} - {self.weekly_cases} - {self.weekly_deaths}"
    
@app.route('/')
def index():
    return "COVID-19 Cases in Canada API"

@app.route('/Cases')
def get_cases():
    cases = Case.query.all()
    
    output = []
    for cases in cases:
        case_data = {'prname': cases.prname, 'date': cases.date, 'cases': cases.cases, 'deaths': cases.deaths, 'recovered': cases.recovered, 'weekly_cases': cases.weekly_cases, 'weekly_deaths': cases.weekly_deaths}
        
        output.append(case_data)
    
    return {"cases" : output}

@app.route("/Cases/<id>", methods=['GET'])
def get_case(id):
    print(f"Getting case with ID: {id}") 
    case = Case.query.get_or_404(id)
    return {"prname": case.prname, "date": case.date, "cases": case.cases, "deaths": case.deaths, "recovered": case.recovered, "weekly_cases": case.weekly_cases, "weekly_deaths": case.weekly_deaths}

@app.route('/Cases', methods=['POST'])
def add_case():
    case = Case(
        prname=request.json['prname'], 
        date=request.json['date'], 
        cases=request.json['cases'], 
        deaths=request.json['deaths'], 
        recovered=request.json['recovered'], 
        weekly_cases=request.json['weekly_cases'], 
        weekly_deaths=request.json['weekly_deaths']
    )  
    db.session.add(case)
    db.session.commit()
    return {'id': case.id}
   

@app.route('/Cases/<id>', methods=['DELETE'])
def delete_case(id):
    case = Case.query.get(id)
    if case is None:
        return {"error" : "case not found"}
    db.session.delete(case)
    db.session.commit()
    return {"message" : "case deleted"}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

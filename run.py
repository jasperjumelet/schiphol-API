from api import create_app, db
from api.models import Airlines, Airports, Flights, db
from api.database_init import initialize_data

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {"app", app,
            "db", db}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if len(Airlines.query.all()) == 0 and \
                len(Airports.query.all()) == 0 and \
                len(Flights.query.all()) == 0:
            initialize_data()

    app.run(debug=True, host="0.0.0.0", port=8080)
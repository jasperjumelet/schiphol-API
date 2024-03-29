from api import create_app, db
from api.models import Airlines, Airports, Flights, db
from api.database_init import initialize_data
from flask_apscheduler import APScheduler
from api.database_update import reinitialize_database
app = create_app()

# Scheduler to update database each month
scheduler = APScheduler()

@scheduler.task('interval', id='reinitialize_database', hours=24)
def reinitialize_database_task():
    with app.app_context:
        reinitialize_database()

@app.shell_context_processor
def make_shell_context():
    return {"app": app,
            "db": db}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if len(Airlines.query.all()) == 0 and \
                len(Airports.query.all()) == 0 and \
                len(Flights.query.all()) == 0:
            initialize_data()

    app.run(debug=True, host="0.0.0.0", port=8080)
    scheduler.start()
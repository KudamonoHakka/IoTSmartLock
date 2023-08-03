from flask import Flask, request, render_template
from urllib.parse import unquote
from datetime import datetime

want_lock_change = True # Saves when want to change state
open_state = True # Saves the desired state
current_lock_state = True # Saves the current lock state
gps_location = "38.8951,-77.0364" # GPS location Lat + Long
last_updated = datetime.now()  # Saves when the MSP432 last contacted

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_data():
    global open_state
    global gps_location
    global current_lock_state
    global want_lock_change
    global last_updated

    data = request.args.get('data')
    lock_state = request.args.get('lock_state')
    
    # This GET parameter is set when the user presses a button to set the lock state
    if lock_state:
        # Convert readable text into boolean
        open_state = True if lock_state == 'open' else False

        # Signal that there is change and we want to inform the lock
        want_lock_change = True

    # If there is data then it must be from the MSP432, else a user

    # Format : ?data=Lat+Long lock_state
    if data:
        print(unquote(data))

        # Grab the GPS location from input
        gps_location = unquote(data).split(" ")[0]

        # Grap the current set lock state from input
        current_lock_state = True if unquote(data).split(" ")[1] == 'open' else False

        # Update the last-updated variable
        last_updated = datetime.now()

        # Return data for the MSP432 to know what to chose; if not wanting change allow it to be free
        if want_lock_change:
            # After changing the lock, we don't need to change it further
            want_lock_change = False
            return 'open' if open_state else 'close'
        else:
            return 'free'
    else:
        return open('index.html', 'r').read().replace("[INSERT_GPS]", gps_location).replace("[INSERT_LOCK]", "Open" if current_lock_state else "Closed").replace("[INSERT_DATE]", str(last_updated))
    


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)
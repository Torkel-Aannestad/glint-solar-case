import sys
from flask import Flask, jsonify, request
from flask_cors import CORS
import xarray
import numpy as np


def get_hmax_dataset():
    # Since the case only emphasise on max wave height, I'm extracting the variable hmax from the dataset.
    # This only load the necassery data into memory which is 36MB over 180MB in this case.
    try:
        dataset = xarray.open_dataset("data/waves_2019-01-01.nc", engine="netcdf4")
        return dataset["hmax"]
    except (IOError, OSError) as e:
        print(f"Error opening the file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Return None or raise an error if something fails
    return None


app = Flask(__name__)
CORS(
    app
)  # Allowing all cross site resource sharing. Production I would set content security policy to trusted domains.


# hmax data
hmax_dataset = get_hmax_dataset()
if hmax_dataset is None:
    print("Failed to load the dataset. Exiting...")
    sys.exit(1)


@app.route("/")
def index():
    response_body = {
        "status": "available",
    }
    return jsonify(response_body)


@app.route("/location-data", methods=["Post"])
def location_data():
    try:
        params = request.get_json()

        # Most of the checks for lat lng request body variable could be abstracted in a validation function if several endpoints use it, but for now I leave it here.
        # Check if keys are in the body
        if "lat" not in params or "lng" not in params:
            return jsonify({"error": "missing lat or lng in request body"}), 400

        # Extract lat and lng values
        lat = params.get("lat")
        lng = params.get("lng")

        # Checking for boundaries from dataset
        # latitude   (latitude) float32 1kB 70.0 69.5 69.0 68.5 ... -59.0 -59.5 -60.0
        if not (-60 <= lat <= 70):
            return jsonify({"error": "Latitude value out of range (-60 to 70)"}), 400

        # longitude  (longitude) float32 3kB -180.0 -179.5 -179.0 ... 179.0 179.5
        if not (-180 <= lng <= 179.5):
            return (
                jsonify({"error": "Longitude value out of range (-180 to 179.5)"}),
                400,
            )

        # get location data
        location_data = hmax_dataset.sel(
            longitude=lng,
            latitude=lat,
            method="nearest",
        )
        selected_lat = float(location_data.latitude.values)
        selected_lng = float(location_data.longitude.values)
        max = location_data.max().values

        if np.isnan(location_data.max().values):
            return (
                jsonify({"message": "No data available for the location"}),
                200,
            )

        return (
            jsonify(
                {
                    "nearest_latitude": selected_lat,
                    "nearest_longitude": selected_lng,
                    "max_wave_height": str(max),
                }
            ),
            200,
        )

    except ValueError:
        # Handling ValueError if lat/lot are not convertable to float.
        return (
            jsonify({"error": "expected float values for lat and lng."}),
            400,
        )
    except Exception as e:
        # Returning the error
        # In production this would be handled with an error triage function so that no internal server errors would be sendt to the client.
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=4000, debug=True)

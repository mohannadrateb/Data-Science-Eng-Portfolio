import dagster as dg
import os
import json
from dagster import RunRequest
from ..jobs import adhoc_request_job

@dg.sensor(
        job=adhoc_request_job
)
def adhoc_request_sensor(context: dg.SensorEvaluationContext):
    # the directory the sensor will observe
    PATH_TO_REQUESTS = os.path.join(os.path.dirname(__file__), "../../", "data/requests")
    #to compare the cursor sate, if cursor state is different a run is triggered
    previous_state = json.loads(context.cursor) if context.cursor else {}
    current_state = {}
    #store new requests to run
    runs_to_request = []
    #look at the different files at the the directory for new or modified
    for filename in os.listdir(PATH_TO_REQUESTS):
        file_path = os.path.join(PATH_TO_REQUESTS, filename)
        if filename.endswith(".json") and os.path.isfile(file_path):
            last_modified = os.path.getmtime(file_path)

            current_state[filename] = last_modified

            # if the file is new or has been modified since the last run, add it to the request queue
            if filename not in previous_state or previous_state[filename] != last_modified:
                with open(file_path, "r") as f:
                    request_config = json.load(f)
                    #creates a run request when the file is modified or updated
                    runs_to_request.append(RunRequest(
                        run_key=f"adhoc_request_{filename}_{last_modified}",
                        run_config={
                            "ops": {
                                "adhoc_request": {
                                    "config": {
                                        "filename": filename,
                                        **request_config
                                    }
                                }
                            }
                        }
                    ))
    

    return dg.SensorResult(
        run_requests=runs_to_request,
        cursor=json.dumps(current_state)
    )





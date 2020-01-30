from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)
issues = {
    "new_issues": [],
    "fixed_issues": [],
}


@app.route("/", methods=["GET"])
def get_issue_counts():
    return "INFO: {} new issues, {} fixed issues".format(
        len(issues["new_issues"]), len(issues["fixed_issues"])
    )


@app.route("/get-issue/", methods=["GET"])
def get_one_issue():
    if len(issues["new_issues"]) > 0:
        return str(issues["new_issues"][0])
    else:
        return "INFO: No new_issues found."


@app.route("/", methods=["POST"])
def receive_webhook():
    webhook = request.json

    # There are "new_issues" and "fixed_issues" events in webhooks
    for issue in webhook["issues"]:
        new_issue = Issue(**issue)
        issues[webhook["event"]].append(new_issue)
    return jsonify({"code": "200", "message": "webhook received"})


class Issue:
    """
    New Issues passed in via the webhooks. Intentionally
    flexible due to rapidly changing API
    """

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            print(f"{key}:{val}")
            setattr(self, key, val)

    def __str__(self):
        return json.dumps(vars(self))


# Ports and interfaces are manged in run.py via environment variables
if __name__ == "__main__":
    app.run()

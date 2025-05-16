from flask import Flask, render_template, request, flash, redirect, url_for, send_file
import boto3
import json
import os
from io import BytesIO

app = Flask(__name__)
app.secret_key = "gsom_secret"

REGION = "eu-north-1"
ENDPOINT_NAME = "gsom-cloud-endpoint"
INPUT_BUCKET = "gsom-input-bucket"
OUTPUT_BUCKET = "gsom-output-bucket"

@app.route("/", methods=["GET", "POST"])
def index():
    s3_client = boto3.client("s3", region_name=REGION)

    try:
        buckets = [b["Name"] for b in s3_client.list_buckets()["Buckets"]]
    except Exception as e:
        buckets = []
        flash(f"❌ Error fetching S3 buckets: {str(e)}", "danger")

    try:
        input_keys = [obj["Key"] for obj in s3_client.list_objects_v2(Bucket=INPUT_BUCKET).get("Contents", [])]
    except Exception as e:
        input_keys = []
        flash(f"❌ Error fetching files from {INPUT_BUCKET}: {str(e)}", "danger")

    try:
        output_files = [obj["Key"] for obj in s3_client.list_objects_v2(Bucket=OUTPUT_BUCKET).get("Contents", [])]
    except Exception as e:
        output_files = []
        flash(f"❌ Error fetching output files: {str(e)}", "danger")

    if request.method == "POST":
        input_key = request.form.get("input_key")
        input_bucket = request.form.get("input_bucket")
        output_bucket = request.form.get("output_bucket")

        try:
            gsom_params = {
                "spred_factor": float(request.form.get("spred_factor")),
                "dimensions": int(request.form.get("dimensions")),
                "distance": request.form.get("distance"),
                "initialize": request.form.get("initialize"),
                "learning_rate": float(request.form.get("learning_rate")),
                "smooth_learning_factor": float(request.form.get("smooth_learning_factor")),
                "max_radius": int(request.form.get("max_radius")),
                "FD": float(request.form.get("FD")),
                "r": float(request.form.get("r")),
                "alpha": float(request.form.get("alpha")),
                "initial_node_size": int(request.form.get("initial_node_size"))
            }

            payload = {
                "input_key": input_key,
                "input_bucket": input_bucket,
                "output_bucket": output_bucket,
                "gsom_params": gsom_params
            }

            sm_runtime = boto3.client("sagemaker-runtime", region_name=REGION)
            response = sm_runtime.invoke_endpoint(
                EndpointName=ENDPOINT_NAME,
                Body=json.dumps(payload),
                ContentType="application/json"
            )

            result = json.loads(response["Body"].read().decode("utf-8"))
            flash(f"✅ {result.get('result', 'Execution completed.')}", "success")

        except Exception as e:
            flash(f"❌ Failed: {str(e)}", "danger")

        return redirect(url_for("index"))

    return render_template("index.html", buckets=buckets, input_keys=input_keys, output_files=output_files)

@app.route("/download", methods=["GET"])
def download_file():
    key = request.args.get("output_key")
    if not key:
        return "Missing output_key", 400

    s3 = boto3.client("s3", region_name=REGION)
    try:
        s3_object = s3.get_object(Bucket=OUTPUT_BUCKET, Key=key)
        file_stream = BytesIO(s3_object["Body"].read())
        return send_file(file_stream, as_attachment=True, download_name=os.path.basename(key))
    except Exception as e:
        return f"Download failed: {e}", 500

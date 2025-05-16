from flask import Flask, render_template, request, flash, redirect, url_for
import boto3
import json

app = Flask(__name__)
app.secret_key = "gsom_secret"

REGION = "eu-north-1"
ENDPOINT_NAME = "gsom-cloud-endpoint"

@app.route("/", methods=["GET", "POST"])
def index():
    s3_client = boto3.client("s3", region_name=REGION)

    # Fetch available buckets
    try:
        bucket_list = s3_client.list_buckets()["Buckets"]
        buckets = [b["Name"] for b in bucket_list]
    except Exception as e:
        buckets = []
        flash(f"❌ Error fetching S3 buckets: {str(e)}", "danger")

    if request.method == "POST":
        input_key = request.form.get("input_key")
        input_bucket = request.form.get("input_bucket")
        output_bucket = request.form.get("output_bucket")

        if not input_key or not input_bucket or not output_bucket:
            flash("❌ Please fill in all fields.", "danger")
            return redirect(url_for("index"))

        try:
            sm_runtime = boto3.client("sagemaker-runtime", region_name=REGION)
            payload = {
                "input_key": input_key,
                "input_bucket": input_bucket,
                "output_bucket": output_bucket
            }

            response = sm_runtime.invoke_endpoint(
                EndpointName=ENDPOINT_NAME,
                Body=json.dumps(payload),
                ContentType="application/json"
            )

            result = json.loads(response["Body"].read().decode("utf-8"))
            message = result.get("result", "Execution completed.")
            flash(f"✅ {message}", "success")

        except Exception as e:
            flash(f"❌ Failed: {str(e)}", "danger")

        return redirect(url_for("index"))

    return render_template("index.html", buckets=buckets)

if __name__ == "__main__":
    app.run(debug=True)

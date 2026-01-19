import boto3, json, os, datetime

ddb = boto3.resource("dynamodb")
tracking = ddb.Table("DeploymentTracking")
analytics = ddb.Table("ResumeAnalytics")

commit = os.environ.get("GITHUB_SHA","local")
env = os.environ.get("ENV","beta")

raw = open("analysis.json").read()

# strip markdown if model added it
raw = raw.replace("```json","").replace("```","")

analysis = json.loads(raw)

tracking.put_item(Item={
    "commit_sha": commit,
    "environment": env,
    "status": "SUCCESS",
    "s3_url": os.environ.get("S3_URL",""),
    "model_used": "claude-3-sonnet",
    "timestamp": datetime.datetime.utcnow().isoformat()
})

analytics.put_item(Item={
    "commit_sha": commit,
    **analysis
})

print("DynamoDB write successful")

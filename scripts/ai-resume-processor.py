import boto3, json, os

bedrock = boto3.client("bedrock-runtime")

resume_md = open("Updated_resume.md").read()

HTML_PROMPT = f"""
Convert this markdown resume into a professional ATS-optimized HTML page.
Return ONLY valid HTML.

{resume_md}
"""

ANALYSIS_PROMPT = f"""
Analyze this resume for ATS readiness.
Return STRICT JSON with:
word_count, ats_score, keywords, readability, missing_sections, suggestions.

{resume_md}
"""

def call_bedrock(prompt):
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1500,
        "temperature": 0.2,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=json.dumps(body)
    )

    result = json.loads(response["body"].read())
    return result["content"][0]["text"]

html = call_bedrock(HTML_PROMPT)
analysis = call_bedrock(ANALYSIS_PROMPT)

open("index.html","w").write(html)
open("analysis.json","w").write(analysis)

# Phase 4: AWS

**Prerequisite:** Phase 2 complete (RAG, agents). Phase 3 recommended (Bedrock/Strands overlap).
**Goal:** Production-grade AWS skills for AI systems. Hands-on with boto3 + key services.

---

## Part A: boto3 Foundation

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| client vs resource | "What is the difference between a boto3 client and resource?" | [ ] |
| session management | "How do you manage AWS credentials in Python?" | [ ] |
| error handling | "How do you handle AWS errors in boto3?" | [ ] |
| paginator | "What is a paginator in boto3? When do you need it?" | [ ] |

**Exercise:** Create `src/aws/client.py` with a reusable boto3 session factory:
```python
import boto3
from botocore.exceptions import ClientError

def get_client(service: str, region: str = "eu-west-1"):
    return boto3.client(service, region_name=region)
```

**Resources:** [boto3 docs](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

---

## Part B: S3

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| CRUD operations | "How do you upload and download files from S3 in Python?" | [ ] |
| presigned URLs | "What is a presigned URL? When would you use it?" | [ ] |
| event notifications | "How do S3 event notifications work?" | [ ] |
| storage classes | "What are S3 storage classes? When do you use Glacier?" | [ ] |
| versioning | "What is S3 versioning? Why enable it?" | [ ] |

**Exercise:** Add S3 persistence to PerfumeShop embeddings:
```python
# src/aws/embeddings_store.py
def upload_embeddings(matrix: np.ndarray, bucket: str, key: str):
    s3 = get_client("s3")
    buffer = io.BytesIO()
    np.save(buffer, matrix)
    buffer.seek(0)
    s3.upload_fileobj(buffer, bucket, key)

def download_embeddings(bucket: str, key: str) -> np.ndarray:
    s3 = get_client("s3")
    buffer = io.BytesIO()
    s3.download_fileobj(bucket, key, buffer)
    buffer.seek(0)
    return np.load(buffer)
```

---

## Part C: AWS Lambda [INTERVIEW CRITICAL]

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| packaging dependencies | "How do you package Python dependencies for Lambda?" | [ ] |
| layers | "What are Lambda layers? What goes in them?" | [ ] |
| cold start | "What is a Lambda cold start? How do you reduce it?" | [ ] |
| environment variables | "How do you manage secrets in Lambda?" | [ ] |
| handler signature | "What is the Lambda handler function signature?" | [ ] |
| timeout/memory | "Lambda has a 15-min timeout. How do you handle longer tasks?" | [ ] |

**Exercise:** Create a Lambda handler that wraps the PerfumeShop search endpoint:
```python
# lambda_handler.py
import json
from src.data.loader import DataLoader

loader = None  # initialized outside handler for reuse across warm invocations

def handler(event, context):
    global loader
    if loader is None:
        loader = DataLoader(csv_path="/tmp/perfumes.csv")  # download from S3 on cold start
    
    brand = event.get("queryStringParameters", {}).get("brand")
    results = loader.filter_perfumes({"brand": brand} if brand else {})
    return {
        "statusCode": 200,
        "body": json.dumps(results[:10])
    }
```

**Resources:** [AWS Lambda Python docs](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html)

---

## Part D: Amazon Bedrock [INTERVIEW CRITICAL]

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| Converse API | "What is the Bedrock Converse API?" | [ ] |
| InvokeModel | "How does InvokeModel differ from Converse?" | [ ] |
| Model IDs | "How do you reference models in Bedrock?" | [ ] |
| Knowledge Bases | "What is a Bedrock Knowledge Base?" | [ ] |
| AgentCore | "What is Bedrock AgentCore?" | [ ] |
| Guardrails | "How do you configure guardrails in Bedrock?" | [ ] |

**Exercise:** Create an alternative `ClaudeClient` using Bedrock instead of Anthropic SDK:
```python
import boto3
import json

class BedrockClaudeClient:
    def __init__(self, model_id: str = "anthropic.claude-sonnet-4-6-v1:0"):
        self.client = boto3.client("bedrock-runtime", region_name="us-east-1")
        self.model_id = model_id

    def send_message(self, messages: list, system: str = None, max_tokens: int = 1024):
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": messages,
            **({"system": system} if system else {})
        }
        response = self.client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(body)
        )
        return json.loads(response["body"].read())
```

**Resources:**
- [Bedrock Converse API](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html)
- [AgentCore docs](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)

---

## Part E: DynamoDB

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| partition key + sort key | "What is a partition key? What is a sort key?" | [ ] |
| query vs scan | "What is the difference between query and scan in DynamoDB?" | [ ] |
| GSI | "What is a Global Secondary Index? When do you add one?" | [ ] |
| single table design | "What is single-table design in DynamoDB?" | [ ] |

**Exercise:** Design a DynamoDB table to store PerfumeShop conversation history:
- PK: `userId` (e.g., `user#francisco`)
- SK: `conversationId#timestamp`
- Attributes: `messages` (list), `perfumes_returned` (list), `ttl`

Discuss the design with Claude before implementing.

---

## Part F: Amazon Textract [INTERVIEW CRITICAL]

| Topic | Interview Questions | Status |
|-------|-------------------|--------|
| DetectDocumentText | "What does DetectDocumentText do in Textract?" | [ ] |
| AnalyzeDocument | "When do you use AnalyzeDocument vs DetectDocumentText?" | [ ] |
| quality issues | "How do you handle poor OCR quality from Textract?" | [ ] |
| vs Tesseract | "Textract vs Tesseract — when do you use each?" | [ ] |

**Mental model:** You built OCR with Tesseract in day 11. Textract is the AWS managed equivalent with forms/tables extraction built in.

**Exercise:** Replace `src/ocr/document_processor.py` with a Textract version:
```python
def extract_from_bytes_textract(image_bytes: bytes) -> str:
    textract = get_client("textract")
    response = textract.detect_document_text(
        Document={"Bytes": image_bytes}
    )
    lines = [
        block["Text"]
        for block in response["Blocks"]
        if block["BlockType"] == "LINE"
    ]
    return "\n".join(lines)
```

---

## Part G: Other Services (Conceptual)

| Service | Key Interview Question | Status |
|---------|----------------------|--------|
| SageMaker | "What is SageMaker? How does it differ from Bedrock?" | [ ] |
| Athena | "What is Athena? What's its use case?" | [ ] |
| OpenSearch | "What is OpenSearch? How does its vector search work?" | [ ] |
| EKS | "What is EKS? When do you use it vs Lambda?" | [ ] |
| EC2 | "When would you use EC2 instead of Lambda/EKS?" | [ ] |

**Resources:**
- [AWS Bedrock docs](https://docs.aws.amazon.com/bedrock/)
- [AWS Textract docs](https://docs.aws.amazon.com/textract/)
- [DynamoDB Developer Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/)

---

## Completion Criteria

- [ ] boto3 client factory in `src/aws/client.py`
- [ ] S3 embeddings upload/download working
- [ ] Lambda handler for search endpoint written and explained
- [ ] Bedrock `BedrockClaudeClient` working as drop-in replacement
- [ ] DynamoDB table design for conversation history reviewed by Claude
- [ ] Textract version of document processor working
- [ ] Can explain SageMaker vs Bedrock, Athena, EKS vs Lambda in 1-2 sentences each

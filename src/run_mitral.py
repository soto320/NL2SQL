from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
import torch
import time
import uuid
import os
import re

app = FastAPI()

# 🧠 Configuración del modelo
BASE_MODEL = "mistralai/Mistral-7B-Instruct-v0.1"
LORA_PATH = os.path.join(os.getcwd(), "mistral-lora-out", "checkpoint-21")
HF_TOKEN = os.getenv("HF_TOKEN", None)

device = "cuda" if torch.cuda.is_available() else "cpu"

# 🔧 BitsAndBytes para carga en 4-bit
bnb_config = BitsAndBytesConfig(
    load_in_4bit=False,
    bnb_4bit_compute_dtype=torch.float16,
    #float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

# 🚀 Carga del tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    BASE_MODEL,
    use_auth_token=HF_TOKEN,
    trust_remote_code=False
)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# 🚀 Carga del modelo base cuantizado
base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    quantization_config=bnb_config,
    device_map="auto",
    use_auth_token=HF_TOKEN,
    trust_remote_code=False
)

# 🧠 Aplicar LoRA y descargar pesos fusionados
model = PeftModel.from_pretrained(base_model, LORA_PATH)
#model = model.merge_and_unload()

# ⚡ Optimización para PyTorch 2.0+
if hasattr(torch, "compile"):
    model = torch.compile(model)

model.eval()

# 📦 Esquemas de entrada
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: Optional[float] = 0.0

# 📡 Endpoint principal
@app.post("/v1/chat/completions")
def chat_completion(req: ChatRequest):
    prompt = extract_last_prompt(req.messages)
    full_prompt = f"[INST] {prompt.strip()} [/INST]"
    inputs = tokenizer(full_prompt, return_tensors="pt", padding=True).to(model.device)

    output = model.generate(
        **inputs,
        max_new_tokens=256,
        #temperature=req.temperature or 0.0,
        #top_p=0.9,
        do_sample=False,
        pad_token_id=tokenizer.pad_token_id
    )

    decoded = tokenizer.decode(output[0], skip_special_tokens=True)
    print("⚡ Decodificado:", decoded)

    reply = decoded.replace(full_prompt, "").strip()
    sql_clean = extract_sql_from_response(reply)
    print(f"🧪 SQL extraído: {sql_clean}")

    prompt_tokens = inputs["input_ids"].shape[1]
    completion_tokens = len(tokenizer.encode(reply, add_special_tokens=False))
    total_tokens = prompt_tokens + completion_tokens

    return {
        "id": f"chatcmpl-{uuid.uuid4().hex[:24]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": req.model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": sql_clean,
                    "refusal": None,
                    "annotations": []
                },
                "logprobs": None,
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "prompt_tokens_details": {},
            "completion_tokens_details": {}
        },
        "service_tier": "default",
        "system_fingerprint": f"fp_{uuid.uuid4().hex[:12]}"
    }

# 🔍 Extraer el último mensaje del usuario
def extract_last_prompt(messages: List[Message]) -> str:
    for m in reversed(messages):
        if m.role == "user":
            return m.content
    return messages[-1].content

# 🧼 Extraer SQL desde la respuesta generada
def extract_sql_from_response(response: str) -> str:
    match = re.search(r"(?i)(select\s.+)", response, re.DOTALL)
    if match:
        sql = match.group(1)
        sql = sql.split("\n```")[0]
        return sql.strip()
    return response.strip()

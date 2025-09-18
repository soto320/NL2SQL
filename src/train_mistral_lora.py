import os
import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
    BitsAndBytesConfig
)
from peft import get_peft_model, LoraConfig, TaskType

# Configuración para evitar fragmentación de memoria CUDA
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
os.environ["HF_HOME"] = "/workspace/hf-cache"
os.environ["TRANSFORMERS_CACHE"] = "/workspace/hf-cache"

# Configuración del modelo
model_name = "mistralai/Mistral-7B-Instruct-v0.1"
dataset_path = "/workspace/diagnostico.jsonl"

# Quantización para menor uso de memoria
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.float16
)

# Tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    token=True,  # Reemplazo recomendado para use_auth_token
    trust_remote_code=True
)
tokenizer.pad_token = tokenizer.eos_token

# Modelo base con quantización
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)

# Dataset en formato jsonl estilo OpenAI/chat
dataset = load_dataset("json", data_files={"train": dataset_path})["train"]

# Tokenización del dataset
def tokenize_function(example):
    prompt = ""
    for msg in example["messages"]:
        if msg["role"] == "user":
            prompt += f"[INST] {msg['content'].strip()} [/INST]"
        elif msg["role"] == "assistant":
            prompt += f" {msg['content'].strip()}"
    return tokenizer(prompt, truncation=True, max_length=1024, padding="longest")

tokenized_dataset = dataset.map(tokenize_function, remove_columns=dataset.column_names)

# Configuración de LoRA
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

# Aplicar LoRA
model = get_peft_model(model, lora_config)

# Argumentos de entrenamiento ajustados
training_args = TrainingArguments(
    output_dir="./mistral-lora-out",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,
    num_train_epochs=3,
    learning_rate=2e-4,
    fp16=torch.cuda.is_available(),
    logging_steps=10,
    save_steps=100,
    save_total_limit=2,
    remove_unused_columns=False,
    report_to="none"
)

# Data collator y trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
)

# Iniciar entrenamiento
trainer.train()

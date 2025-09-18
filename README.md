# Implementación de Modelos de Inteligencia Artificial Basados en Tecnologías de Código Abierto para la Traducción Segura de Lenguaje Natural a Consultas Structured Query Language SQL
![Python](https://img.shields.io/badge/Python-3.10-blue)
![License](https://img.shields.io/badge/License-Apache%202.0-green)
![Framework](https://img.shields.io/badge/Framework-FastAPI-red)
![Model](https://img.shields.io/badge/Model-Mistral--7B-orange)


## 📖 Descripción General

Este proyecto implementa un sistema **NL2SQL** (Natural Language to SQL) basado en **modelos de lenguaje abiertos** para traducir preguntas en **español** a consultas SQL válidas.  

El enfoque se centra en tres pilares:

- **Seguridad:** Prevención de inyecciones SQL (*prompt-to-SQL injection*).  
- **Precisión semántica:** Traducción que capture fielmente la intención del usuario.  
- **Reproducibilidad:** Arquitectura abierta y documentación detallada para permitir la replicación en entornos académicos e industriales.  

El trabajo se sustenta en el artículo:  
**“Implementación de Modelos de Inteligencia Artificial Basados en Tecnologías de Código Abierto para la Traducción Segura de Lenguaje Natural a Consultas SQL”** (Saúl, 2025).

---
## ✨ Características

- **Modelo base:** [Mistral-7B-Instruct](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1), ajustado con **LoRA** para español.  
- **API REST** desarrollada con **FastAPI**, estilo OpenAI (`/v1/chat/completions`).  
- **Validación sintáctica:** decodificación restringida (*constrained decoding*).  
- **Validación semántica:** similitud de Jaccard sobre *tokens* SQL.  
- **Seguridad integrada:** ejecución restringida a `SELECT`, listas de denegación (`DROP`, `DELETE`, etc.) y control RBAC.  
- **Interfaz de prueba:** integración con .NET (C#).  

---
## ⚙️ Requisitos del Entorno

### Hardware recomendado
- **Entrenamiento LoRA:** GPU ≥ RTX 3090 (24 GB VRAM).  
- **Inferencia:** GPU ≥ 16 GB VRAM (viable en CPU con menor rendimiento).  

### Software
- **Ubuntu 22.04** + **CUDA 11.8**.  
- **Docker (opcional):** `runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel`.  
- **Python 3.10+** con librerías:
  - `transformers` (v4.30)  
  - `datasets` (v2.12)  
  - `accelerate` (v0.20)  
  - `peft` (v0.4)  
  - `fastapi` (v0.95)  
  - `uvicorn`  

---

## 🚀 Instalación

```bash
# 1) Clonar el repositorio
git clone https://github.com/soto320/NL2SQL.git
cd NL2SQL

# 2) Crear entorno virtual (opcional)
python3 -m venv .venv && source .venv/bin/activate

# 3) Instalar dependencias
pip install -r requirements.txt





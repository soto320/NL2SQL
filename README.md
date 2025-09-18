# Implementación de Modelos de Inteligencia Artificial Basados en Tecnologías de Código Abierto para la Traducción Segura de Lenguaje Natural a Consultas Structured Query Language SQL
![Python](https://img.shields.io/badge/Python-3.10-blue)
![License](https://img.shields.io/badge/License-Apache%202.0-green)
![Framework](https://img.shields.io/badge/Framework-FastAPI-red)
![Model](https://img.shields.io/badge/Model-Mistral--7B-orange)

## 📌 Descripción General

Este proyecto implementa un sistema **NL2SQL (Natural Language to SQL)** seguro y reproducible basado en **modelos de lenguaje abiertos**.  
El objetivo es traducir **preguntas en Lenguaje Natural (LN) en español** a **consultas SQL válidas y seguras**, con:

- Adaptación al idioma español (brecha poco abordada en la literatura).  
- Prevención de ataques **prompt-to-SQL e inyecciones**.  
- Uso de modelos **open-source** con licencia libre (Apache 2.0, MIT, BigCode).  
- Reproducibilidad académica y práctica, documentada paso a paso.  

El proyecto fue desarrollado como parte de la **Maestría en Desarrollo de Software** en la **Universidad Politécnica Salesiana (UPS)**.

---

## 🎯 Objetivos

- **General:** Desarrollar un sistema NL2SQL seguro, reproducible y adaptado al español.  
- **Específicos:**  
  1. Analizar modelos NL2SQL open-source y seleccionar el más adecuado.  
  2. Implementar una **Prueba de Concepto (PoC)** funcional en GPU.  
  3. Afinar el modelo con **LoRA** y dataset propio en español.  
  4. Desarrollar una **API REST con FastAPI** y una interfaz en **.NET**.  
  5. Evaluar exactitud semántica y sintáctica con métricas estándar.  
  6. Integrar validación de seguridad y anonimización conforme a **LOPDP** y **GDPR**.  

---

## 📊 Metodología

Se aplicó un **RUP adaptado con enfoque ágil**【21】, estructurado en 4 fases (ver *Figura 1* del artículo):

1. **Inicio:** Revisión bibliográfica, levantamiento de requisitos y análisis de dominio.  
   - Se evaluaron modelos NL2SQL (Tabla 1 comparativa: LLaMA-3, Mistral, DeepSeek, Yi, StarCoder2).  
   - Se priorizó soporte multilingüe, licencia abierta, rendimiento y hardware requerido.  

2. **Elaboración:** Diseño de la arquitectura y planificación técnica.  
   - Arquitectura en capas (ver *Figura 2*): Interfaz .NET + API FastAPI + PostgreSQL + Módulo de anonimización.  

3. **Construcción:** Implementación del modelo NL2SQL.  
   - Fine-tuning con **LoRA** en dataset propio (50 pares LN→SQL en español, dominio clínico).  
   - Scripts `train_mistral_lora.py` y validación con métricas de similitud (Jaccard).  

4. **Transición:** Validación, pruebas y documentación.  
   - Pruebas unitarias y de seguridad (inyecciones bloqueadas).  
   - Interfaz en .NET probada con consultas clínicas simuladas.  
   - Documentación reproducible en LaTeX/Word.  

Además, se realizaron **entrevistas estructuradas** (1 responsable de TI, 3 investigadores) y **validación con expertos académicos** (n=2) para retroalimentar requisitos y resultados.

---

## 📂 Estructura del Repositorio



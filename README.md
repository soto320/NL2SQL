# Implementación de Modelos de Inteligencia Artificial Basados en Tecnologías de Código Abierto para la Traducción Segura de Lenguaje Natural a Consultas Structured Query Language SQL
![Python](https://img.shields.io/badge/Python-3.10-blue)
![License](https://img.shields.io/badge/License-Apache%202.0-green)
![Framework](https://img.shields.io/badge/Framework-FastAPI-red)
![Model](https://img.shields.io/badge/Model-Mistral--7B-orange)

## Descripción General

NL2SQL es un sistema basado en **modelos de lenguaje abierto** para traducir preguntas expresadas en Lenguaje Natural al español en **consultas SQL válidas y seguras**. El proyecto enfatiza:

- Adaptación al idioma español, una necesidad poco atendida en la literatura actual.  
- Prevención de ataques tipo _prompt-to-SQL_ e inyecciones SQL.  
- Uso de modelos **open-source** con licencias permisivas (Apache 2.0, MIT, BigCode).  
- Reproducibilidad académica y práctica, con pasos claramente documentados.

Fue desarrollado en el marco de la Maestría en Desarrollo de Software de la Universidad Politécnica Salesiana (UPS).

---

## Objetivos

**General**  
Desarrollar un sistema NL2SQL que sea seguro, reproducible y adaptado al español.

**Específicos**

1. Analizar modelos NL2SQL open-source y seleccionar el más adecuado según criterios lingüísticos, de licencia, rendimiento y requerimientos de hardware.  
2. Implementar una prueba de concepto (PoC) operativa en entorno GPU.  
3. Afinar el modelo mediante LoRA usando un dataset propio en español.  
4. Desarrollar una API REST con FastAPI y una interfaz de usuario en .NET.  
5. Evaluar la exactitud semántica y sintáctica con métricas estándar (por ej. Jaccard, BLEU, exact match).  
6. Integrar validaciones de seguridad y anonimización de datos de acuerdo con normativas como LOPDP y GDPR.

---

## Metodología

Se aplicó un **RUP adaptado** con enfoque ágil, estructurado en cuatro fases (ver Figura correspondiente en el artículo):

| Fase     | Actividades principales |
|----------|-------------------------|
| **1. Inicio** | Revisión bibliográfica; levantamiento de requisitos; análisis de dominio; comparación de modelos (LLaMA-3, Mistral, DeepSeek, Yi, StarCoder2) considerando soporte multilingüe, licencia, rendimiento y hardware. |
| **2. Elaboración** | Diseño arquitectónico: capas de interfaz .NET, API con FastAPI, base de datos PostgreSQL, módulo de anonimización. Planificación técnica. |
| **3. Construcción** | Fine-tuning con LoRA del modelo seleccionado usando dataset clínico propio (LN → SQL en español). Implementación de scripts de entrenamiento y validación. Pruebas de seguridad. |
| **4. Transición** | Validación del sistema: pruebas funcionales, pruebas de seguridad (ataques/inyecciones), interfaz de usuario. Documentación reproducible y despliegue. |

Además, se obtuvieron retroalimentaciones de expertos y se realizaron entrevistas estructuradas para validar requisitos y resultados.

---

## Estructura del Repositorio

```text
/
├── data/                    ← Datos y datasets utilizados
├── requirements/            ← Dependencias del proyecto
├── src/                     ← Código fuente
│   ├── train_*.py           ← Scripts de entrenamiento y fine-tuning
│   ├── api/                 ← API REST (FastAPI)
│   ├── ui/                  ← Interfaz .NET
│   ├── security/            ← Módulo de anonimización y validaciones
│   └── utils/               ← Herramientas auxiliares (evaluación, métricas, etc.)
├── LICENSE                  ← Licencia Apache 2.0
└── README.md                ← Este documento



# 🛡️ ART-T v2.5: AI Red Teaming Toolkit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/Next.js-15-black)](https://nextjs.org/)
[![Security: OWASP LLM](https://img.shields.io/badge/Security-OWASP%20LLM%20Top%2010-red)](https://owasp.org/www-project-top-10-list-for-large-language-models/)

## 📖 Overview
The **AI Red Teaming Toolkit (ART-T)** is a comprehensive framework designed to stress-test Large Language Model (LLM) deployments and agentic systems. It provides a sophisticated Command & Control (C2) dashboard for real-time monitoring of adversarial campaigns, policy violations, and data leakage.

## 🚀 Key Features
* **Command & Control Dashboard:** A high-fidelity Next.js interface for real-time telemetry, agent orchestration, and risk posture assessment.
* **Adversarial Prompt Injection:** Automated testing for Indirect and Direct injections.
* **PII Leakage Scanner:** High-fidelity pipeline combining Regex, NER (spaCy), and Semantic reasoning to detect unauthorized data disclosure.
* **Jailbreak Benchmarking:** Implements various "persona adoption" and "base64 encoding" bypass attempts to test model alignment.
* **Vector Guard:** Inspects document embeddings for adversarial signatures, steganography, and low-entropy DoS risks.
* **Excessive Agency Auditor:** LangGraph-based workflow to prevent critical actions without human confirmation (HITL).
* **Automated Eval Reports:** Generates a security posture score (JSON/PDF) based on the [OWASP Top 10 for LLMs](https://owasp.org/www-project-top-10-list-for-large-language-models/).

## 🛠️ Tech Stack
* **Frontend:** Next.js 15, Tailwind CSS, Lucide React (Cyberpunk UI).
* **Core Backend:** Python 3.11+.
* **Orchestration:** LangGraph (multi-step attack state machines).
* **Vector Testing:** Weaviate / Pinecone
* **Evals:** DeepEval / Giskard integrations

## 📥 Getting Started

### 1. Web Dashboard (C2)
```bash
npm install
npm run dev
```

### 2. Core Security Engine
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## 🛠️ Key Features
* **Tri-Stage PII Auditing:** A high-fidelity pipeline combining deterministic Regex, Named Entity Recognition (NER) via spaCy, and Semantic LLM-as-a-Judge reasoning to detect unauthorized data disclosure.

## 🗺️ Roadmap

   - [x] Phase 1: Core CLI and Basic PII Scanner

   - [ ] Phase 2: LangGraph-based Adaptive Attack Engine

   - [ ] Phase 3: RAG Poisoning & Vector DB Stress Testing

   - [ ] Phase 4: Full FastMCP Server integration

# 🛡️ AI Red Teaming Toolkit (ART-T)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Security: OWASP LLM](https://img.shields.io/badge/Security-OWASP%20LLM%20Top%2010-red)](https://owasp.org/www-project-top-10-list-for-large-language-models/)

## 📖 Overview
The **AI Red Teaming Toolkit** is a modular framework designed to stress-test Large Language Model (LLM) deployments against adversarial attacks. As AI moves from chatbots to **agentic systems**, the attack surface has expanded. This toolkit automates the discovery of vulnerabilities such as prompt injection, data leakage, and jailbreaking.

## 🚀 Key Features
* **Adversarial Prompt Injection:** Automated testing for Indirect and Direct injections.
* **PII Leakage Scanner:** Scans RAG (Retrieval-Augmented Generation) outputs for sensitive data (SSNs, API keys, Emails).
* **Jailbreak Benchmarking:** Implements various "persona adoption" and "base64 encoding" bypass attempts to test model alignment.
* **Vector DB Poisoning Simulation:** Tools to test how manipulated context affects RAG accuracy.
* **Automated Eval Reports:** Generates a security posture score (JSON/PDF) based on the [OWASP Top 10 for LLMs](https://owasp.org/www-project-top-10-list-for-large-language-models/).

## 🛠️ Tech Stack
* **Language:** Python 3.11+
* **Orchestration:** LangGraph (for multi-step attack agents)
* **Vector Testing:** Weaviate / Pinecone
* **Evals:** DeepEval / Giskard integrations

## 📥 Installation
```bash
git clone [https://github.com/lucasmulato/AI-Red-Teaming-Toolkit.git](https://github.com/lucasmulato/AI-Red-Teaming-Toolkit.git)
cd AI-Red-Teaming-Toolkit
pip install -r requirements.txt
```

## 🛠️ Key Features
* **Tri-Stage PII Auditing:** A high-fidelity pipeline combining deterministic Regex, Named Entity Recognition (NER) via spaCy, and Semantic LLM-as-a-Judge reasoning to detect unauthorized data disclosure.

## 🗺️ Roadmap

   - [x] Phase 1: Core CLI and Basic PII Scanner

   - [ ] Phase 2: LangGraph-based Adaptive Attack Engine

   - [ ] Phase 3: RAG Poisoning & Vector DB Stress Testing

   - [ ] Phase 4: Full FastMCP Server integration

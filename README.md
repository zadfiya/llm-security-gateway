# LLM Security Gateway
A production-grade security proxy that sanitizes LLM inputs and manages secrets securely
Sanitizes inputs, manages secrets via Azure Key Vault, enforces rate limits, and scans outputs — before anything reaches the model.

---

## Quick Start

## Architecture
See [SYSTEM_DESIGN.md](./SYSTEM_DESIGN.md)

## Chanel Logs
See [Channel_Log.md](./Channel_Log.md)

## Demo
This section demonstrates that the gateway guardrails work correctly across output sanitization, prompt-injection handling, and hard blocking of critical PII.

### 1) Output Sanitization (`output_scan`) - Email Pattern Redaction
User asks for email combinations based on a personal name/domain (for example, "give me combinations of email addresses based on my name").The model may generate email-like strings in response.  
`output_scan` detects those patterns and redacts them before returning to the client.

What this proves:
- Output guardrails run after model generation.
- Sensitive output content is sanitized before API response.
- API still returns useful text while removing protected values.
Reference:
[![Email-Sanitize.jpg](https://i.postimg.cc/mrYcWNg5/Email-Sanitize.jpg)](https://postimg.cc/HJLWQM5w)

### 2) Input Vulnerability - Prompt Injection Handling
User sends a prompt-injection style input (for example, "Ignore previous instructions ..."). Input guardrails detect and sanitize suspicious injection patterns.  
The downstream model response changes accordingly (aligned with safe instructions), and logging captures detections for auditability.

What this proves:
- Injection text is detected and transformed safely.
- Sanitized prompt is what reaches the provider.
- Security logs capture detection type/severity and sanitized flow for traceability.

Reference image: `prompt-Injection.jpg`
[![prompt-Injection.jpg](https://i.postimg.cc/90n0YLLM/prompt-Injection.jpg)](https://postimg.cc/Fk0h9V55)

### 3) Block Sensitive Data (`input_scan`) - Critical PII Block (SIN)
User asks which number is a SIN / sends SIN-like values.  
The request is blocked immediately with `400 Bad Request` and no model call is performed.

What this proves:
- High-risk PII policy is enforced at input stage.
- Blocking is immediate and deterministic.
- Sensitive requests are stopped before they reach the LLM.

Reference image: `Sin-Block.jpg`
[![Sin-Block.jpg](https://i.postimg.cc/wT17jdBG/Sin-Block.jpg)](https://postimg.cc/QHrXfw1Q)

\# Model Record



\## Model identity



\- Full Ollama tag: `llama3.2:3b-instruct-q4\_K\_M`

\- Publisher: Meta

\- Model family: Llama 3.2

\- Architecture: `llama`

\- Model type: Instruction-tuned text model

\- Parameter count: 3.2 billion

\- Quantization: `Q4\_K\_M`

\- Advertised maximum context length: 131,072 tokens

\- Embedding length: 3,072

\- Capabilities: Completion and tools

\- Downloaded artifact size: 2.0 GB

\- Exact download date: 15.09.2026



\## Runtime configuration



Output from `ollama ps`:



```text

NAME                         ID            SIZE    PROCESSOR  CONTEXT

llama3.2:3b-instruct-q4\_K\_M    a80c4f17acd5  2.6 GB  100% GPU   4096

```



\- Model allocation: 100% GPU

\- Active runtime context: 4,096 tokens

\- Reported loaded size: 2.6 GB



The 2.0 GB downloaded artifact size and 2.6 GB loaded size measure

different things. Runtime loading includes additional memory requirements.



The active context is smaller than the model's advertised maximum.

Evaluation reports must record the actual runtime context used.



\## Runtime and hardware



\- Operating system: Windows

\- Ollama version: 0.34.0

\- GPU: NVIDIA GeForce RTX 3070 Laptop GPU

\- GPU memory: 8,192 MiB

\- NVIDIA driver: 616.92



These values describe the environment observed during model setup.



\## Model page and license



\- Model page: https://ollama.com/library/llama3.2

\- Exact model page: https://ollama.com/library/llama3.2:3b-instruct-q4\_K\_M

\- License: Llama 3.2 Community License Agreement

\- Model release date shown in license: September 25, 2024



\## Retrieval and verification commands



```powershell

ollama pull llama3.2:3b-instruct-q4\_K\_M

ollama show llama3.2:3b-instruct-q4\_K\_M

ollama list

ollama --version

```



After loading the model, verify allocation and context:



```powershell

ollama run llama3.2:3b-instruct-q4\_K\_M

ollama ps

```



Record GPU information:



```powershell

nvidia-smi --query-gpu=name,memory.total,driver\_version --format=csv

```



Model tags may change. The recorded model ID identifies the locally

observed artifact and helps detect changes between evaluation runs.



\## Selection rationale



The model was selected for local application evaluation on a laptop

with an NVIDIA RTX 3070 Laptop GPU and 8 GB of GPU memory.



Its quantized 3.2-billion-parameter configuration provides a manageable

memory footprint for repeated Garak requests.



The observed runtime confirms that the model loaded entirely onto the

GPU with a 4,096-token context.



The selection prioritizes practical local inference and resource

headroom rather than maximum model capability.



\## Known limitations



\- The model may hallucinate facts or fabricate completed support actions.

\- Instruction tuning does not guarantee resistance to prompt injection.

\- Quantization can affect output quality compared with higher precision.

\- Small models may struggle with complex instructions.

\- The active 4,096-token context limits the available conversation space.

\- Temperature zero does not guarantee identical results across runtime

&#x20; versions, hardware, and settings.

\- Garak detector signals require investigation and are not automatically

&#x20; confirmed vulnerabilities.

\- Results apply only to the recorded application, system prompt, model,

&#x20; runtime, and evaluation configuration.

\- Model binaries are not included in this repository.


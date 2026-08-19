---


# Universal AI Router Proxy

An OpenAI-compatible API proxy built with **FastAPI** and **Uvicorn**. It serves as a gateway to secure internal keys, map client public keys, enforce specific model targets, and fully support real-time data streaming (Server-Sent Events).

---

## 🚀 Key Features

* **OpenAI-Compatible Endpoints**: Provides standard OpenAI endpoints like `/v1/models` and `/v1/chat/completions`.
* **Credential Isolation**: Uses `PUBLIC_API_KEY` for external client authentication while hiding your confidential `INTERNAL_9ROUTER_KEY`.
* **Model Enforcement**: Automatically overrides or forces incoming requests to use a designated target model (`TARGET_MODEL`).
* **Full Streaming Support**: Seamlessly handles text/event-stream responses as well as standard JSON responses using `httpx.AsyncClient`.

---

## 📦 Prerequisites & Installation

Make sure you have **Python** installed on your system, then install the required dependencies:

```bash
pip install fastapi uvicorn httpx

```

---

## ⚙️ Configuration

The main configuration variables are located at the top of your main script (`main.py`):

| Variable | Description |
| --- | --- |
| `ROUTER_URL` | The upstream target endpoint (e.g., `https://api.b.ai/v1/chat/completions`) |
| `TARGET_MODEL` | The model enforced for all requests (e.g., `bai/deepseek-v4-flash`) |
| `INTERNAL_9ROUTER_KEY` | The secret API key used for upstream authentication |
| `PUBLIC_API_KEY` | The API key distributed to clients or users |

---

## 💻 Running the Application Locally

Run the server using **Uvicorn** (with `--reload` enabled for development convenience):

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

```

The server will be up and running locally at `http://localhost:8000`.

---

## 🌐 Exposing Publicly via Cloudflare Tunnel

To make your local proxy accessible over the public internet with free SSL/TLS protection without port forwarding, you can use **Cloudflare Tunnel (`cloudflared`)**.

### Step 1: Install `cloudflared` (Windows)

Open PowerShell and install Cloudflare Tunnel using winget:

```powershell
winget install Cloudflare.cloudflared

```

Verify the installation:

```powershell
cloudflared --version

```

### Step 2: Authenticate with Cloudflare

Log in with your Cloudflare account (this will open your browser to authorize your domain):

```powershell
cloudflared login

```

### Step 3: Create a Tunnel

Create a new named tunnel (e.g., `my-ai-proxy`):

```powershell
cloudflared tunnel create my-ai-proxy

```

*Note down the generated **Tunnel ID (UUID)** and the path to your credentials JSON file.*

### Step 4: Route your Domain/Subdomain

Connect the tunnel to your preferred subdomain (e.g., `ai.yourdomain.com`):

```powershell
cloudflared tunnel route dns my-ai-proxy ai.yourdomain.com

```

### Step 5: Create a Configuration File (`config.yml`)

Create a `config.yml` file in your project or inside your `.cloudflared` user folder (`C:\Users\YourUser\.cloudflared\config.yml`):

```yaml
tunnel: <YOUR_TUNNEL_UUID>
credentials-file: C:\Users\YourUser\.cloudflared\<YOUR_TUNNEL_UUID>.json

ingress:
  - hostname: ai.yourdomain.com
    service: http://localhost:8000
  - service: http_status:404

```

### Step 6: Run the Tunnel

Start your tunnel:

```powershell
cloudflared tunnel run my-ai-proxy

```

Your local FastAPI proxy is now safely live and accessible worldwide at `https://ai.yourdomain.com`!

---

## 🧪 Usage Examples

You can test your proxy using `curl` by supplying your `PUBLIC_API_KEY` in the `Authorization` header:

### 1. List Models (`GET /v1/models`)

```bash
curl -X GET "[https://ai.yourdomain.com/v1/models](https://ai.yourdomain.com/v1/models)" \
     -H "Authorization: Bearer sk-dhodho-free-23691263gioug9e09812ye018"

```

### 2. Chat Completions (`POST /v1/chat/completions`)

```bash
curl -X POST "[https://ai.yourdomain.com/v1/chat/completions](https://ai.yourdomain.com/v1/chat/completions)" \
     -H "Authorization: Bearer sk-dhodho-free-23691263gioug9e09812ye018" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "gpt-3.5-turbo",
       "messages": [{"role": "user", "content": "Hello, who are you?"}],
       "stream": false
     }'

```

```

```

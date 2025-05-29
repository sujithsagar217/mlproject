# 🐳 Dockerized Flask + MongoDB Application Setup (Windows)

This guide documents the full setup process for containerizing a Flask app with MongoDB using Docker on **Windows** — including installation, troubleshooting, image building, running containers, integrating MongoDB, and verifying data with MongoDB Compass.

---

## 🧰 Prerequisites

* Windows 10 (Build 19044+) or Windows 11
* Admin access to enable features and BIOS settings

---

## 🔧 Step 1: Install Docker Desktop on Windows

1. Download Docker Desktop: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

2. Install it and follow prompts.

3. **Enable WSL2 support**:

   * Run PowerShell as Admin and execute:

     ```powershell
     dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
     dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
     ```
   * Restart your machine.

4. **Enable Virtualization in BIOS**:

   * Restart your PC and press `Esc` or `F10` (for HP).
   * Go to `System Configuration` → `Virtualization Technology` → Enable.
   * Save and exit BIOS.

5. After reboot:

   ```powershell
   wsl --set-default-version 2
   ```

---

## 🐍 Step 2: Build Flask App Docker Image

### 📁 Project Structure

```
mlproject/
│
├— app.py
├— Dockerfile
├— requirements.txt
├— rf_diet_model.pkl
├— rf_exercises_model.pkl
├— label_encoders.pkl
├— templates/
└— static/
```

### 🧱 Dockerfile

```Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_RUN_HOST=0.0.0.0
CMD ["python", "app.py"]
```

### ✏️ Update `app.py` (final line)

```python
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
```

### 🛠 Build Docker Image

```bash
docker build -t flask-ml-app .
```

### ▶️ Run Container

```bash
docker run -d -p 5000:5000 --name flask_container flask-ml-app
```

Access the app at: [http://localhost:5000](http://localhost:5000)

---

## 🧪 Troubleshooting

* ❌ `localhost didn’t send any data`: You forgot to set `host="0.0.0.0"` in `app.run()`.

* ❌ `Container name already in use`: Run:

  ```bash
  docker rm flask_container
  ```

* ❌ `.pkl` not found: Use relative paths in `app.py`:

  ```python
  BASE_DIR = os.path.dirname(os.path.abspath(__file__))
  model = joblib.load(os.path.join(BASE_DIR, 'your_model.pkl'))
  ```

---

## 🍃 Step 3: Add MongoDB via Docker Compose

### 📦 `docker-compose.yml`

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - mongo
    environment:
      - MONGO_URI=mongodb://mongo:27017/
    volumes:
      - .:/app
    restart: always

  mongo:
    image: mongo:6
    container_name: mongodb
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:
```

### 🔧 Update `app.py` MongoDB connection

Replace:

```python
client = MongoClient("mongodb://localhost:27017/")
```

With:

```python
mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)
```

---

## ▶️ Step 4: Run Flask + MongoDB Together

```bash
docker compose up --build
```

To restart containers without rebuilding:

```bash
docker compose up -d
```

To stop containers (without removing):

```bash
docker compose stop
```

To remove containers:

```bash
docker compose down
```

---

## 📃 Step 5: View MongoDB Data in MongoDB Compass

### 🔍 1. Connect to MongoDB from Compass

Use this URI in MongoDB Compass:

```
mongodb://127.0.0.1:27017/
```

If you're using a custom port in Docker Compose (e.g. `27018`):

```
mongodb://127.0.0.1:27018/
```

### 💡 2. Common reasons Compass shows no data:

* MongoDB Compass is connected to your **native Windows MongoDB**, not the Docker one.
* No data has been inserted yet → MongoDB won't show the DB until a collection is created.
* Conflicting MongoDB instances on port 27017.

### 🔎 3. Check data directly in Docker MongoDB

```bash
docker exec -it mongodb mongosh
```

Inside mongosh:

```js
use fitness
db.users.find().pretty()
db.submissions.find().pretty()
```

If data appears here, but not in Compass, you're likely connected to the wrong instance.

### ⛔️ 4. Stop native MongoDB (if needed)

To ensure Compass connects only to Docker MongoDB:

```powershell
net stop MongoDB
```

Then reconnect in Compass.

---

## 🧰 Useful Docker Commands

| Command                            | Description                 |
| ---------------------------------- | --------------------------- |
| `docker ps -a`                     | Show all containers         |
| `docker start <name>`              | Start existing container    |
| `docker stop <name>`               | Stop container              |
| `docker rm <name>`                 | Remove container            |
| `docker images`                    | List images                 |
| `docker rmi <image>`               | Remove image                |
| `docker logs <name>`               | View logs                   |
| `docker exec -it <name> /bin/bash` | Open shell inside container |

---

## ✅ Done!

Your Flask app is now running in Docker with MongoDB connected via Docker Compose.

---

### 🧠 Optional Next Steps

* Add MongoDB GUI like **Mongo Express**
* Deploy to cloud (Render, Railway, Azure)
* Add authentication for MongoDB
* Enable persistent storage for uploads or logs

---

## 🔗 Credits

Built with:

* Flask
* MongoDB
* Docker & Docker Compose
* Joblib + Scikit-learn models

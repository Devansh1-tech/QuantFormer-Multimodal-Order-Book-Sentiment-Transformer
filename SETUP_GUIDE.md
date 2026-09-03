# 🚀 QuantFormer: Setup & Installation Guide

Welcome to the **QuantFormer** project! This guide provides clear, step-by-step instructions on how to download, install dependencies, and run both the frontend and backend servers.

## 1. Download the Project
If you haven't already, clone or download the repository to your local machine:
```bash
git clone https://github.com/yourusername/QuantFormer.git
cd QuantFormer
```
*(If you downloaded a ZIP file, extract it and open your terminal in the extracted `QuantFormer` folder).*

---

## 2. Setup & Run the Backend (Python / FastAPI)
The backend is built with FastAPI, PyTorch, and Hugging Face Transformers.

**Step 2.1: Open a terminal in the root `QuantFormer` directory**

**Step 2.2: Create a Virtual Environment (Optional but Recommended)**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

**Step 2.3: Install Backend Dependencies**
Install all required Python packages from the backend's `requirements.txt`:
```bash
pip install -r backend/requirements.txt
```

**Step 2.4: Start the Backend Server**
Run the FastAPI server using Uvicorn:
```bash
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
- The backend API will be accessible at: `http://127.0.0.1:8000`
- API Documentation (Swagger) is available at: `http://127.0.0.1:8000/docs`

---

## 3. Setup & Run the Frontend (React / Vite)
The frontend is built with React, TypeScript, and Vite. You will need Node.js installed on your system.

**Step 3.1: Open a *new* terminal window/tab and navigate to the frontend directory**
```bash
# Assuming you start from the root 'QuantFormer' folder
cd frontend
```

**Step 3.2: Install Frontend Dependencies**
Install all required Node packages using npm:
```bash
npm install
```

**Step 3.3: Start the Frontend Server**
Run the Vite development server:
```bash
npm run dev
```
- The frontend web application will be accessible at: `http://localhost:5173/`

---

## 🎉 You're All Set!
With both servers running, you can now open your browser and navigate to `http://localhost:5173/` to use the QuantFormer AI Dashboard.

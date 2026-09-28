# Debugging FastAPI Applications

**Doc ID:** `fastapi_debugging_with_vscode_and_pycharm`  
**Category:** `FastAPI`  
**Domain:** `Web APIs & Python Asynchronous Services`  
**Summary:** Configure debuggers in VS Code and PyCharm for breakpoints and step-through debugging.

---

## Debugging Setup
Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "debugpy",
      "request": "launch",
      "module": "uvicorn",
      "args": ["main:app", "--reload", "--port", "8000"],
      "jinja": true
    }
  ]
}
```
Or start directly in code:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
```


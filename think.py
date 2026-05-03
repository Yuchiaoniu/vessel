import os, json, requests

api_key = os.environ["GEMINI_API_KEY"]
event_body = os.environ["EVENT_BODY"]

# 1. 動態鎖定當前最穩定的 Gemini 模型
found_model = None
for v in ["v1beta", "v1"]:
    try:
        resp = requests.get(f"https://generativelanguage.googleapis.com/{v}/models?key={api_key}").json()
        if 'models' in resp:
            for m in resp['models']:
                if 'generateContent' in m.get('supportedGenerationMethods', []):
                    found_model = (v, m['name'])
                    if 'flash' in m['name'].lower(): break
        if found_model: break
    except: continue

if not found_model:
    print("Critical Error: No capable model found.")
    exit(1)

# 2. 構建神諭：要求 AI 以 Bash 形式輸出解決方案
version, model_path = found_model
url = f"https://generativelanguage.googleapis.com/{version}/{model_path}:generateContent?key={api_key}"

# 提供系統上下文：告訴 AI 它現在擁有最高權限與 gh cli 工具
system_context = (
    "你是一個擁有管理員權限的 GitHub Agent。你現在可以使用 'gh variable set' 管理狀態，"
    "可以使用 git 修改任何檔案。請根據主人指令輸出 bash 代碼。"
    "規則：只輸出代碼，不要包含 Markdown 區塊標籤，確保指令可以直接執行。"
)

prompt = f"{system_context}\n\n主人指令：{event_body}"

payload = {"contents": [{"parts": [{"text": prompt}]}]}
response = requests.post(url, json=payload)
data = response.json()

if 'candidates' in data:
    text = data['candidates'][0]['content']['parts'][0]['text']
    # 清理 AI 可能誤加的 markdown 標籤
    clean_code = text.replace('```bash', '').replace('```sh', '').replace('```', '').strip()
    with open("exec.sh", "w") as f:
        f.write(clean_code)
else:
    print(f"Generation Failed: {json.dumps(data)}")

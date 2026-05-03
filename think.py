import os, json, requests, re

api_key = os.environ.get("GEMINI_API_KEY")
event_body = os.environ.get("EVENT_BODY", "")

found_model = None
for v in ["v1beta", "v1"]:
    try:
        resp = requests.get(f"https://generativelanguage.googleapis.com/{v}/models?key={api_key}").json()
        if 'models' in resp:
            for m in resp['models']:
                if 'generateContent' in m.get('supportedGenerationMethods', []):
                    found_model = (v, m['name']); break
        if found_model: break
    except: continue

if not found_model:
    print("Error: No Model Found")
    exit(1)

url = f"https://generativelanguage.googleapis.com/{found_model[0]}/{found_model[1]}:generateContent?key={api_key}"
prompt = f"指令：{event_body}\n規則：你是 Linux 專家。只輸出 Bash 代碼，禁止廢話。必須包含 git add, commit, push 指令來更新 README.md。"

try:
    response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
    data = response.json()
    raw_text = data['candidates'][0]['content']['parts'][0]['text']
    clean_text = re.sub(r'```[a-zA-Z]*', '', raw_text).replace('```', '').strip()
    
    # 這裡採用更寬鬆的保留策略，確保指令不被誤刪
    with open("exec.sh", "w") as f:
        f.write(clean_text)
except Exception as e:
    print(f"Thinking Error: {e}")

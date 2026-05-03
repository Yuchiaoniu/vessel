import os, json, requests, re

api_key = os.environ["GEMINI_API_KEY"]
event_body = os.environ["EVENT_BODY"]

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

if not found_model: exit(1)

url = f"https://generativelanguage.googleapis.com/{found_model[0]}/{found_model[1]}:generateContent?key={api_key}"
prompt = f"指令：{event_body}\n核心規則：你是 Linux 終端機，只能輸出 Bash 代碼。禁止輸出任何自然語言說明。變數同步使用 'gh variable set 變數名 --body 內容'。禁止使用 --repository 參數。"

response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
data = response.json()

if 'candidates' in data:
    raw_text = data['candidates'][0]['content']['parts'][0]['text']
    clean_text = re.sub(r'```[a-zA-Z]*', '', raw_text).replace('```', '').strip()
    # 淨化：移除包含中文字的解釋行，只留下純 Bash 指令
    lines = [line for line in clean_text.split('\n') if not re.search(r'[\u4e00-\u9fa5]', line)]
    
    with open("exec.sh", "w") as f:
        f.write('\n'.join(lines))

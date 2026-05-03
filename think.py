import os
import json
import requests

api_key = os.environ["GEMINI_API_KEY"]
issue_body = os.environ["ISSUE_BODY"]

# 1. 徹底檢查所有版本的所有模型
found_model = None
for v in ["v1beta", "v1"]:
    list_url = f"https://generativelanguage.googleapis.com/{v}/models?key={api_key}"
    resp = requests.get(list_url).json()
    if 'models' in resp:
        for m in resp['models']:
            # 優先找 flash，其次找 pro，只要能生成內容就行
            if 'generateContent' in m.get('supportedGenerationMethods', []):
                found_model = (v, m['name'])
                if 'flash' in m['name'].lower():
                    break
    if found_model: break

if not found_model:
    print("關鍵錯誤：此 API Key 找不到任何支援生成內容的模型。請確認 AI Studio 權限。")
    exit(1)

version, model_path = found_model
print(f"成功鎖定目標：版本={version}, 路徑={model_path}")

# 2. 執行指令生成
url = f"https://generativelanguage.googleapis.com/{version}/{model_path}:generateContent?key={api_key}"
prompt = f"你是一個 GitHub Agent。主人指令：{issue_body}\n請輸出達成目標的 bash 指令（需含 git config/add/commit/push），只輸出代碼，不要解釋。"

payload = {"contents": [{"parts": [{"text": prompt}]}]}
response = requests.post(url, json=payload)
data = response.json()

if 'candidates' in data:
    text = data['candidates'][0]['content']['parts'][0]['text']
    with open("exec.sh", "w") as f:
        f.write(text.replace('```bash', '').replace('```sh', '').replace('```', '').strip())
else:
    print(f"請求失敗：{json.dumps(data, indent=2)}")

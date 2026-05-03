import os, json, requests, re

# 從 GitHub Action 環境變數獲取必要的參數
api_key = os.environ["GEMINI_API_KEY"]
event_body = os.environ["EVENT_BODY"]

# 1. 自動探測可用的 Gemini 模型版本 (v1beta 或 v1)
found_model = None
for v in ["v1beta", "v1"]:
    try:
        resp = requests.get(f"https://generativelanguage.googleapis.com/{v}/models?key={api_key}").json()
        if 'models' in resp:
            for m in resp['models']:
                if 'generateContent' in m.get('supportedGenerationMethods', []):
                    found_model = (v, m['name'])
                    break
        if found_model: break
    except:
        continue

# 若找不到模型則中斷執行
if not found_model:
    print("❌ 無法偵測到可用的 Gemini 模型。")
    exit(1)

# 2. 設定 AI 思考邏輯與 Prompt
url = f"https://generativelanguage.googleapis.com/{found_model[0]}/{found_model[1]}:generateContent?key={api_key}"
prompt = (
    f"指令：{event_body}\n"
    "核心規則：你是 Linux 終端機，只能輸出 Bash 代碼。禁止輸出任何自然語言說明。 "
    "變數同步使用 'gh variable set 變數名 --body 內容'。禁止使用 --repository 參數。"
)

# 3. 發送請求給 Gemini
response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
data = response.json()

if 'candidates' in data:
    raw_text = data['candidates'][0]['content']['parts'][0]['text']
    
    # 清理：移除 Markdown 的代碼塊標籤 (如 ```bash 或 ```)
    clean_text = re.sub(r'```[a-zA-Z]*', '', raw_text).replace('```', '').strip()
    
    # 4. 精準白名單過濾機制 (Kernel v1.3 的核心)
    # 只允許合法的 Bash 指令開頭，這能確保即使 AI 講了廢話（中文或英文解釋），也不會被寫入執行腳本
    bash_whitelist = [
        "git", "gh", "echo", "printf", "cd", "rm", 
        "python", "cat", "mv", "mkdir", "ls", "export"
    ]
    
    lines = []
    for line in clean_text.split('\n'):
        stripped = line.strip()
        # 檢查該行是否以白名單中的指令開頭，或是以路徑符號 (./) 開頭
        if any(stripped.startswith(cmd) for cmd in bash_whitelist) or stripped.startswith("./"):
            lines.append(line)
    
    # 5. 生成最終的執行腳本
    with open("exec.sh", "w") as f:
        # 如果最後沒有內容，則不寫入任何東西，防止錯誤執行
        if lines:
            f.write('\n'.join(lines))
        else:
            print("⚠️ AI 未生成有效的 Bash 指令。")

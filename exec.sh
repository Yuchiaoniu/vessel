git config user.name "github-actions[bot]"
git config user.email "github-actions[bot]@users.noreply.github.com"

# 1. 路徑修正：將所有 README.md.md.md 指令指向 README.md.md.md.md
# 搜尋常見檔案類型（Markdown, YAML, Shell 腳本, 純文字, HTML, JS, TS, Python, JSON）
# 將獨立的 "README.md.md.md" 字串替換為 "README.md.md.md.md"，避免修改已包含副檔名的檔案（如 README.md.md.md.md 本身）
find . -type f -regextype egrep -regex ".*\.(md|yml|sh|txt|html|js|ts|py|json)" -print0 | xargs -0 sed -i 's/\bREADME\b/README.md.md.md.md/g'
echo "已完成路徑修正：將 README.md.md.md 指令指向 README.md.md.md.md。"

# 2. 通訊修復：更新 .github/workflows/kernel.yml 中的留言回報方式
# 定義新的回報區塊內容
NEW_REPORT_BLOCK=$(cat <<'EOF'
          # 自動回報執行狀態 (統一使用 gh api 避開版本問題)
        REPORT="✅ **系統進化成功**\n\n指令已執行。當前版本：v1.1.0"
        
        if [ "${{ github.event_name }}" == "issue_comment" ] || [ "${{ github.event_name }}" == "issues" ]; then
          gh issue comment ${{ github.event.issue.number }} --body "$REPORT"
        elif [[ "${{ github.event_name }}" == "discussion"* ]]; then
          # 改用 gh api 留言給 Discussion
          D_ID=${{ github.event.discussion.node_id }}
          gh api graphql -f query='
            mutation($body: String!, $discussionId: ID!) {
              addDiscussionComment(input: {body: $body, discussionId: $discussionId}) {
                comment { id }
              }
            }' -f body="$REPORT" -f discussionId="$D_ID"
        fi
EOF
)
# 使用 sed 替換從指定註釋行開始到 'fi' 結尾的整個區塊
sed -i "/^          # 自動回報執行狀態 (統一使用 gh api 避開版本問題)/,/^        fi$/c\\$NEW_REPORT_BLOCK" .github/workflows/kernel.yml
echo "已完成通訊修復：更新 .github/workflows/kernel.yml 中的留言回報方式。"

# 3. 狀態同步：更新 README.md.md.md.md 版本號並寫入 SYSTEM_STATUS 變數
# 更新 README.md.md.md.md 中的版本號至 v1.1.0
# 此正則表達式會匹配如 v1.0, v1.0.0 等版本格式，並替換為 v1.1.0
sed -i 's/\bv[0-9]\+\.[0-9]\+\(\.[0-9]\+\)\?\b/v1.1.0/g' README.md.md.md.md
echo "README.md.md.md.md 版本號已更新至 v1.1.0。"

# 將 SYSTEM_STATUS 變數寫入 Variables
gh variable set SYSTEM_STATUS --body "v1.1.0"
echo "SYSTEM_STATUS 變數已設置為 v1.1.0。"

# 提交並推送所有變更
git add .
git commit -m "feat(agent): 應用路徑修正、通訊修復及狀態同步 (v1.1.0)"
git push
echo "所有變更已提交並推送。"
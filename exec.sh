find . -maxdepth 1 -name "README.md*" -exec mv {} README.md \;
cat << 'EOF' > README.md
Vessel Agent v1.2.0
Step 3 & 4: ✅ Implemented
Step 5: ✅ Implemented (Hot-Reload Active)
Step 7: ✅ Implemented (Variables Active)
Step 9: ✅ Implemented (Pages Active)
EOF
git add .
git commit -m "fix: physical cleanup and kernel report refinement"
git push
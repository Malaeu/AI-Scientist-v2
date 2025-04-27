#!/bin/bash

# Цвета
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

BARWIDTH=30
CUR=0

show_progress() {
    local percent="$1"
    local n=$((percent * BARWIDTH / 100))
    local empty=$((BARWIDTH - n))
    printf "\r${CYAN}["
    for ((i = 0; i < n; i++)); do printf "#"; done
    for ((i = 0; i < empty; i++)); do printf "-"; done
    printf "] %s%%" "${percent}"
}

conflicts_resolved=0
total_conflict_files=$(git log --left-right --graph --cherry-pick --oneline HEAD...upstream/main | grep '|' | wc -l)
[[ $total_conflict_files -le 2 ]] && total_conflict_files=10 # fallback estimate в случае пустоты истории

echo -e "${YELLOW}🚀 Запускаю цикл автоматического глотания конфликтов (их версия)${NC}"
while ! git rebase --continue 2>/dev/null; do
    files=$(git diff --name-only --diff-filter=U)
    count_this=$(echo "$files" | wc -w)
    [ $count_this -eq 0 ] && break

    for f in $files; do
        git checkout --theirs "$f"
        git add "$f"
        conflicts_resolved=$((conflicts_resolved + 1))
        prog_now=$((conflicts_resolved * 100 / total_conflict_files))
        show_progress $prog_now
        sleep 0.3 # искусственная задержка ради кайфа визуала!
        
        echo -e "   ${GREEN}✔ Разрулили: $f${NC}"
    done
    
done

echo ""
if git status | grep -q "rebase in progress"; then
   echo -e "${YELLOW}⚡️ Всё равно остались нечаянно сложные конфликты — посмотри их руками!${NC}"
else
   echo -e "${GREEN}🎉 Rebasing endgame: все конфликты разрулены, ветка готова к пушу!${NC}"
fi

# Финальный прикол: вывести статистику числа файлов:
echo -en "${CYAN}\n------------------------\nСтатистика:\n"
echo "- Всего обработано конфликтных файлов: ${conflicts_resolved}" 
echo "- Финальное состояние репозитория:"
git status -sb
echo ------------------------

cat << EOF

🤖 Обработка завершена! Если что-то всё ещё сломалось —
отгадай загадку дня:"Для чего инженеру нужен vim?"
A) Чтобы выйти из nano.
B) Чтобы страдать.
C) Никто не знает.

(Даже если не знаешь ответа — push'ни свои изменения!)
EOF

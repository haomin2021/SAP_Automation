from openpyxl import load_workbook

wb = load_workbook("DataLoader/Polierlinie_4_2025.xlsx")
sheet = wb.active

section_tasks = {}
current_section = None
pending_task = None

for row in sheet.iter_rows(values_only=True):
    # 获取 A列 和 B列的内容（编号和标题/描述）
    first_cell = row[0]  # A列
    second_cell = row[1] if len(row) > 1 else None  # B列

    # 判断标题：A列为空，B列为字符串，且无 ":"（排除 "Intervall:"）
    if first_cell is None and isinstance(second_cell, str) and ":" not in second_cell and len(second_cell.strip()) > 3:
        # 存储上一段未完成任务
        if pending_task and current_section:
            section_tasks[current_section].append(pending_task)
            pending_task = None

        current_section = second_cell.strip()
        section_tasks[current_section] = []
        continue

    # 判断是否是编号开头的新任务（A列为数字）
    if current_section and isinstance(first_cell, (int, float)):
        # 存储上一条未完成的任务
        if pending_task:
            section_tasks[current_section].append(pending_task)

        desc = str(second_cell).strip() if second_cell else ""
        pending_task = f"{int(first_cell)}. {desc}"
        continue

    # 任务补充行：A列为空，B列有内容，拼接描述
    if current_section and pending_task and first_cell is None and second_cell:
        pending_task += " " + str(second_cell).strip()

# 最后一条任务
if pending_task and current_section:
    section_tasks[current_section].append(pending_task)

# 输出结果
for section, tasks in section_tasks.items():
    print(f"\n== {section} ==")
    for task in tasks:
        print(task)

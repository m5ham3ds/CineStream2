with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    lines = f.readlines()

new_lines = []
imports_to_move = []

for line in lines:
    if line.startswith("import ") and "lazy.LazyColumn" in line or "lazy.items" in line or "viewmodel.compose.viewModel" in line:
        imports_to_move.append(line)
    else:
        new_lines.append(line)

final_lines = []
for line in new_lines:
    final_lines.append(line)
    if line.startswith("package com.example.ui.screens.player"):
        for i in imports_to_move:
            final_lines.append(i)

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.writelines(final_lines)

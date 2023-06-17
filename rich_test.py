#!/usr/bin/python3

import time
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn

progress = Progress(TextColumn("[progress.description]{task.description}"), BarColumn(complete_style='green'), TaskProgressColumn())

task1 = progress.add_task("[red]Downloading...", total=1000)

progress_1 = Progress(TextColumn("[progress.description]{task.description}"), BarColumn(complete_style='yellow'), TaskProgressColumn())
task2 = progress.add_task("[green]Processing...", total=1000)
progress_2 = Progress(TextColumn("[progress.description]{task.description}"), BarColumn(complete_style='red'), TaskProgressColumn())
task3 = progress.add_task("[cyan]Cooking...", total=1000)

progress.start()  # Начало отображения прогресса
progress_1.start()
progress_2.start()
while True:
    progress.update(task1, completed=500)
    progress_1.update(task2, advance=0.3)
    progress_2.update(task3, advance=0.9)
    time.sleep(0.02)

progress.stop()  # Остановка отображения прогресса
progress_1.stop()
progress_2.stop()
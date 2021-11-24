import os


file_location = os.path.dirname(os.path.realpath(__file__))

os.chdir(file_location)

exec(open("scrap_match_current.py").read())
exec(open("scrap_stats_current.py").read())
exec(open("current_history_append.py").read())

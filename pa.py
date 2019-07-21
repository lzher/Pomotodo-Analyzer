import datetime
import argparse
import re
from collections import OrderedDict

TIME_ZONE = "+08"
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S" + TIME_ZONE + ":00"

# convert timedelta to string
def timedelta2str(td, show_days=False):
    if show_days:
        return str(td)
    hours, remainder = divmod(td.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return "%d:%02d:%02d" % (hours, minutes, seconds)

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='Pomotodo time entry analyzer.')
    parser.add_argument('-f', '--file', help="Pomotodo time entry file")
    parser.add_argument('-s', '--sort', default="time",
                        choices=["time", "time_asc", "title"],
                        help="Project sort type (default: %(default)s)")
    parser.add_argument('-d', '--days', action="store_true", help="Show days")

    args = parser.parse_args()

    # Read Pomo file
    pomofile = open(args.file, 'r', encoding="utf8")
    lines = pomofile.readlines()
    pomofile.close()

    # Collect entries
    TotalTime = datetime.timedelta()
    Entries = {}
    for line in lines[1:]:
        line = line[:-1]
        sep = line.split(',')
        time_start = datetime.datetime.strptime(sep[1], TIME_FORMAT)
        time_end = datetime.datetime.strptime(sep[2], TIME_FORMAT)
        title = ','.join(sep[3:]).strip()
        time_delta = time_end - time_start
        Entries[title] = Entries.get(title, datetime.timedelta()) + time_delta
        TotalTime += time_delta
    
    # Collect projects
    project_regex = re.compile('#([\S]*)')
    Projects = {}
    for entry in Entries:
        project = project_regex.search(entry).groups()[0].strip() # Get the **first** tag as project
        Projects[project] = Projects.get(project, []) + [entry]
        
    # Calculate project time
    ProjectTime = {}
    for project in Projects:
        ProjectTime[project] = datetime.timedelta()
        for entry in Projects[project]:
            ProjectTime[project] += Entries[entry]
            
    # Sort projects
    if args.sort == "time":
        # Sort by time desc
        SortedProjects = sorted(Projects.items(), key=lambda kv: ProjectTime[kv[0]], reverse=True)
    elif args.sort == "time_asc":
        # Sort by time asc
        SortedProjects = sorted(Projects.items(), key=lambda kv: ProjectTime[kv[0]], reverse=False)
    elif args.sort == "title":
        # Sort by project titles
        SortedProjects = sorted(Projects.items(), key=lambda kv: kv[0], reverse=False)
    Projects = OrderedDict(SortedProjects)
    
    # Print statistical results
    print("")
    print(" Pomotodo Analyzer ".center(48, "+"))
    print("")
    print("TOTAL:", timedelta2str(TotalTime, args.days))
    print("")
    for project in Projects:
        project_title = project + " " + timedelta2str(ProjectTime[project], args.days)
        print("[" + project_title + "]")
        for entry in Projects[project]:
            print("-", entry, timedelta2str(Entries[entry], args.days))
        print("")
    
if __name__ == "__main__":
    main()

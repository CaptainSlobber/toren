import toren
import os
import json

user_dir = os.path.expanduser("~")
proj_dir = os.path.join(os.getcwd(), "schema", "met")
project_file = os.path.join(proj_dir, "project.json")

#p = toren.parser.Parser(proj_dir)
#p.deserializeProject()

mq = toren.Module().initialize("q","q","q")
mr = toren.Module().initialize("r","r","r")

p = toren.Project().initialize("A", "F", "asdf", "1.0.0", [mq,mr])

with open(project_file, "w") as projectfile:
    json.dump(p.to_dict(), projectfile, indent=4)

pjson = ""
with open(project_file, 'r') as projectfile:
    #pjson = json.load(projectfile)
    pjson = projectfile.read()
p2 = toren.Project().from_json(pjson)


p3 = toren.Project()
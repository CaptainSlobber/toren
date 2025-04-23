import toren
import os


user_dir = os.path.expanduser("~")
proj_dir = os.path.join(os.getcwd(), "schema", "met")

#p = toren.parser.Parser(proj_dir)
#p.deserializeProject()

mq = toren.Module().initializeModule("q","q","q")
mr = toren.Module().initializeModule("r","r","r")

modules = [mq,mr]

p = toren.Project().initializeProject("A","F","asdf", modules)

pjson = p.tojson()

p2 = toren.Project().fromjson(pjson)


p3 = toren.Project()
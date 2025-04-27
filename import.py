import toren
import os
import json


user_dir = os.path.expanduser("~")
proj_dir = os.path.join(os.getcwd(), "schema", "met")
project_file = os.path.join(proj_dir, "project.json")


langPython = toren.LanguagePython()

dbSQLite= toren.DatabaseSQLite().initialize(name="sqlite", 
                               description="sqlite", 
                               id="febd77a2-29dc-44ac-8b1b-247ac6b4d45f")
dbPostgreSQL = toren.DatabaseSQLite().initialize(name="postgresql", 
                               description="postgresql", 
                               id="be3f92e2-e2ff-491d-9ca0-eaefb72cc6bf")

cTimeseries = toren.Class().initialize(name="Timeseries", 
                               description="Timeseries", 
                               id="5b6bce9f-669d-46f9-b80d-2b7ec4ecc38c")

mForecast= toren.Module().initialize(name="metforecast", 
                               description="Forecast", 
                               id="6a5494c2-fd2e-4d37-bced-2ee1a981d72a")
mCollect = toren.Module().initialize(name="metcollect", 
                               description="Collect", 
                               id="7b3bb9d0-afc2-48a1-931f-8cf1498c6a4d",
                               classes=[cTimeseries])


pMet = toren.Project().initialize(name="met", 
                               description="Met", 
                               id="250425ed-c32b-4c89-b427-62a2a1d636a5", 
                               version="1.0.0", 
                               modules=[mForecast,mCollect],
                               languages=[langPython],
                               datastores=[dbPostgreSQL,dbSQLite])

with open(project_file, "w") as projectfile:
    json.dump(pMet.to_dict(), projectfile, indent=4)

pjson = ""
with open(project_file, 'r') as projectfile:
    #pjson = json.load(projectfile)
    pjson = projectfile.read()
_pMet = toren.Project().from_json(pjson)

print(_pMet.Name)

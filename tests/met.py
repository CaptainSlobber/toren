import sys 
import os      
main_dir = os.pardir
toren_dir = os.path.join(main_dir, "toren")
output_dir = os.path.join(toren_dir,"schema", "met")
project_file = os.path.join(output_dir, "project.json")
sys.path.append(toren_dir)        
import toren



langPython = toren.LanguagePython()

dbSQLite= toren.DatabaseSQLite().initialize(name="sqlite", 
                               description="sqlite", 
                               id="febd77a2-29dc-44ac-8b1b-247ac6b4d45f")
dbPostgreSQL = toren.DatabasePostgreSQL().initialize(name="postgresql", 
                               description="postgresql", 
                               id="be3f92e2-e2ff-491d-9ca0-eaefb72cc6bf")

cTimeseries = toren.Class().initialize(name="Timeseries", 
                               description="Timeseries", 
                               id="5b6bce9f-669d-46f9-b80d-2b7ec4ecc38c")

cUser_ID = toren.DatatypeUUID().initialize(name="ID", 
                 description = "User.ID", 
                 id = "fd194c8c-63cf-42ce-83bb-952b70fa7bbb",
                 isprimarykey=True)
cUser_Name = toren.DatatypeString().initialize(name="Username",
                                               description="User.Username",
                                               isunique=True,
                                               id="677a796a-9abf-45af-bc62-40095149c4b4")
cUser = toren.Class().initialize(name="User", 
                               description="User", 
                               id="eac67693-f31f-46d9-b2e3-ac618eeae574",
                               properties=[cUser_ID, cUser_Name])
mCore = toren.Module().initialize(name="core", 
                               description="Core", 
                               id="9b6b77c3-5b00-4d5d-94f3-5f04006f2747",
                               classes=[cUser])
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
                               modules=[mCore, mForecast,mCollect],
                               languages=[langPython],
                               datastores=[dbPostgreSQL,dbSQLite])

pMet.Languages.addLanguage(toren.languages.LanguageJava(), pMet)
pMet.Languages.addLanguage(toren.languages.LanguageJavaScript(), pMet)
pMet.Languages.removeLanguage(toren.languages.LanguageJava().ID)

pMet.to_file(project_file)

_pMet = toren.Project().from_file(project_file)

print(_pMet.Name)

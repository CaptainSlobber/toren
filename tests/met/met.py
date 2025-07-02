import sys 
import os      
import pathlib


main_dir = pathlib.Path(os.getcwd()).parent
#main_dir = par_dir.parent
toren_dir = os.path.join(main_dir, "toren")
output_dir = os.path.join(toren_dir,"schema", "met")
project_file = os.path.join(output_dir, "project.json")
sys.path.append(toren_dir)        
import toren

py_dir = str(main_dir)
java_dir = str(os.path.join(main_dir.parent, "java"))
javascript_dir = str(os.path.join(main_dir.parent, "javascript"))
go_dir = str(os.path.join(main_dir.parent, "go"))
csharp_dir = str(os.path.join(main_dir.parent, "dotnet"))

dbSQLite= toren.DatabaseSQLite().initialize(name="sqlite", 
                               description="sqlite", 
                               id="febd77a2-29dc-44ac-8b1b-247ac6b4d45f")
dbPostgreSQL = toren.DatabasePostgreSQL().initialize(name="postgresql", 
                               description="postgresql", 
                               id="be3f92e2-e2ff-491d-9ca0-eaefb72cc6bf")

cTimeseries = toren.Class().initialize(name="Timeseries", 
                               description="Timeseries", 
                               id="5b6bce9f-669d-46f9-b80d-2b7ec4ecc38c")

pBaseObject_ID = toren.DatatypeUUID().initialize(name="ID", 
                 description = "BaseObject.ID", 
                 id = "e2e30d8e-a54c-4222-97c4-e41a7ba51ab3",
                 isprimarykey=True)
cBaseObject = toren.Class().initialize(name="BaseObject", 
                               description="Base Object", 
                               id="617485cc-7640-4167-84a2-5eabf1b63754",
                               properties=[pBaseObject_ID])

# pUser_ID = toren.DatatypeUUID().initialize(name="ID", 
#                  description = "User.ID", 
#                  id = "fd194c8c-63cf-42ce-83bb-952b70fa7bbb",
#                  isprimarykey=True,
#                  inheritsfromid=pBaseObject_ID.ID)
pUser_Name = toren.DatatypeString().initialize(name="Username",
                                               description="User.Username",
                                               isunique=True,
                                               id="677a796a-9abf-45af-bc62-40095149c4b4")

pUser_FavArr = toren.DatatypeString().initialize(name="FavArr", 
                               description="FavArr", 
                               id="a4541b85-69b9-4049-86d4-2cc69c21e2e6",
                               dimensionality=[2, 2, 2])
cUser = toren.Class().initialize(name="User", 
                               description="User", 
                               id="eac67693-f31f-46d9-b2e3-ac618eeae574",
                               properties=[pUser_Name, pUser_FavArr],
                               inheritsfromid=cBaseObject.ID)
mCore = toren.Module().initialize(name="core", 
                               description="Core", 
                               id="9b6b77c3-5b00-4d5d-94f3-5f04006f2747",
                               classes=[cUser, cBaseObject])
mForecast= toren.Module().initialize(name="metforecast", 
                               description="Forecast", 
                               id="6a5494c2-fd2e-4d37-bced-2ee1a981d72a")
mCollect = toren.Module().initialize(name="metcollect", 
                               description="Collect", 
                               id="7b3bb9d0-afc2-48a1-931f-8cf1498c6a4d",
                               classes=[cTimeseries])

langpy = toren.languages.LanguagePython().initialize(py_dir)
langcsharp = toren.languages.LanguageCSharp().initialize(csharp_dir)
langjava = toren.languages.LanguageJava().initialize(java_dir)
pMet = toren.Project().initialize(name="met", 
                               description="Met", 
                               id="250425ed-c32b-4c89-b427-62a2a1d636a5", 
                               version="1.0.0", 
                               modules=[mCore, mForecast,mCollect],
                               languages=[langpy, langjava, langcsharp],
                               datastores=[dbPostgreSQL,dbSQLite])



pMet.to_file(project_file)

_pMet = toren.Project().from_file(project_file)
writer = toren.writer.Writer(_pMet)
writer.write()


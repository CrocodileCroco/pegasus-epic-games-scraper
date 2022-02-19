import epicstore_api
import os
from glob import glob
import json
import urllib.request as urq

api = epicstore_api.EpicGamesStoreAPI()
manifestfiles = glob("C:\ProgramData\Epic\EpicGamesLauncher\Data\Manifests\*.item")

gdatatoprocess = []

for i in manifestfiles:
    ijson = json.loads(open(i, "r").read())
    gamename = ijson["DisplayName"]
    print(gamename)
    installloc = ijson["InstallLocation"] + "\\"
    executablename = ijson["LaunchExecutable"]
    searchgame = api.fetch_store_games(
        product_type='games/edition/base|bundles/games|editors',
        # Default filter in store page.
        count=1,
        sort_by='releaseDate',
        sort_dir='DESC',
        with_price=True,
        keywords=gamename
    )
    firstgameinsr = searchgame["data"]["Catalog"]["searchStore"]["elements"][0]
    gamedesc = firstgameinsr["description"]
    gameimage = ""
    #Get Cover
    for keyimage in firstgameinsr["keyImages"]:
        if keyimage["type"] == "DieselStoreFrontTall":
            gameimage = keyimage["url"]
    try:
        try:
            try:
                os.mkdir("./media")
            except:
                pass
            os.mkdir("./media/" + gamename)
        except:
            pass
        urq.urlretrieve(gameimage, "media/" + gamename + "/cover.jpg")
    except Exception as e:
        print("Game cover not found")
        print(e)
    print(firstgameinsr)
    gdatatoprocess.append({"name":gamename,"installloc":installloc,"executablename":executablename,"cover":"media/" + gamename + "/cover.jpg"})

manifestpega = open("epicgames.pegasus.metadata.txt","w")
manifestpega.write("collection: Epic\n")
#Add each games to the manifest file
for i in gdatatoprocess:
    manifestpega.write("\n\n")
    manifestpega.write("game: " + i["name"] + "\n")
    manifestpega.write("launch: \"" + i["installloc"] + i["executablename"] + "\"\n")
    manifestpega.write("file: \"" + i["installloc"] + i["executablename"] + "\"\n")
    manifestpega.write("assets.boxFront: ./media/" + i["name"] + "/cover.jpg\nassets.steamgrid: ./media/" + i["name"] + "/cover.jpg\nassets.banner: ./media/" + i["name"] + "/cover.jpg\nassets.background: ./media/" + i["name"] + "/cover.jpg\n")

manifestpega.close()

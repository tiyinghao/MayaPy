import requests
import decimal

#this builds our FIPS query and extracts the interesting bits from it
def getFIPS(lat, lon, lev):
    queryString = "http://data.fcc.gov/api/block/find?latitude=" + str(lat)
    queryString += "&longitude=" + str(lon) + "&showall=false&format=json"
    fResponse = requests.get(queryString)
    FIPS = fResponse.json()[lev]['FIPS']
    return FIPS

def getInfo(lat, lon, dataCode):
    
    # first we set our API key. This will expire before too long, but
    # getting another one is easy.
    key = "993fe969db5b1d642b17df8cc66f26ad98f9009e"
    # then we get our FIPS variable to index into our location.
    fps = getFIPS(lat, lon, 'Block') # leave this as block until we figure out why not to.
    stateCode = fps[:2]
    countyCode = fps[2:5]
    tractCode = fps[5:11]
    blockCode = fps[11:]
    queryString  = "http://api.census.gov/data/2013/acs5?get=" + dataCode
    queryString += "&for=tract:" + tractCode + "&in=state: " + stateCode
    queryString += "+county:" + countyCode + "&key=" + key
    req = requests.get(queryString)
    if req.status_code is 200:
        req = req.json()
    else:
        return req.text
    return req


def getCensusData(lat, lon):
    # gender counts for male, female
    dataCode = "B08006_018E,B08006_035E"
    # male drove, carpooled, public, bike, walk (2, 3, 4, 5, 6)
    dataCode += ",B08006_020E,B08006_021E,B08006_025E,B08006_031E,B08006_032E,B08006_034E"
    # female drove, carpooled, public, bike, walk (7,8,9,10,11
    dataCode += ",B08006_037E,B08006_038E,B08006_042E,B08006_048E,B08006_049E,B08006_051E"
    k = getInfo(lat, lon, dataCode)
    k = k[1]
    print(k)
    a = []
    for element in k:
        a.append(float(element))
    totalMale = a[0]
    totalFemale = a[1]
    totG = totalMale + totalFemale
    ret = []
    for mn in range(2,7):
        fi = mn + 6
        tV = 0.0
        if (a[fi] == 0 and a[mn] == 0):
            tV = 0
        else:
            tV = a[fi]*(totalMale/totalFemale)/(a[fi]+a[mn])
            tV = (tV - .5) * 10
            tV = int(round(tV, 0))

        ret.append(tV)
    # ret[mn - 2] = 
    # do things
    
    return (ret[0], ret[1], ret[2], ret[3], ret[4], ret[5])


#didnot:
#"B22008_003E"

#did
#"B22008_002E"

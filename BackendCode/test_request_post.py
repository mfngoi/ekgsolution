import requests
import json


# The API endpoint to communicate with
# url_post = "http://34.217.80.158:5000/ekgclassify"
url_post = "http://localhost:5000/ekgclassify"


# Define header
head = {
    "Content-Type": "application/x-www-form-urlencoded",
}

# Create profile json and convert to string
profile = {"sex":"M","age":23,"height":180.5,"weight":67.8,"ethnicity":"ASIAN"}
profile = json.dumps(profile)

# Define new data to create
new_data = {
    "profile": profile,
    "signals": "2273,2415,2333,2112,2303,2329,2374,2182,2156,1407,2138,2195,2362,2320,1957,1907,2030,1906,1989,1947,2580,1908,1999,2160,2311,2225,1877,2016,1979,1994,2086,1949,3370,1918,1965,2118,2334,2265,1869,2045,2024,1985,2033,2022,2772,1712,1819,2007,2168,2087,1654,1989,2047,2056,2026,2051,2012,2792,1889,1996,2160,2153,1929,1987,2076,2013,2012,1914,2027,2031,4000,1818,1985,2118,2114,1942,1862,1968,1903,1928,1815,1852,1988,1897,3127,1792,1846,1983,2096,2016,1782,1956,1944,1992,1879,2011,1956,1951,1939,3857",
}

# A POST request to tthe API
response = requests.post(url_post, headers=head, data=new_data)

print(response)
# Print the response
print(response.text)

data = json.loads(response.text)
print(f"{data['condition']=}")
print(f"{data['avg_heartbeat']=}")
print(f"{data['pr_interval']=}")
print(f"{data['qt_interval']=}")


# response = json.loads(response)
# print(f"{response=}")

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
profile = {"sex":"M","age":23,"height":180.5,"weight":67.8,"race":"ASIAN"}
profile = json.dumps(profile)

# Define new data to create
new_data = {
    "profile": profile,
    "signals":
        "1665,1687,1679,1728,4009,1608,1783,1940,2256,2089,1524,1494,1635,1671,1651,1670,1738,1806,1817,1796,1843,3753,1721,1839,1985,2307,2353,1724,1650,1721,1782,1776,1794,1858,1861,1912,1922,1975,4012,1705,1850,1970,2244,2245,1812,1809,1863,1962,1965,1996,1994,1943,1980,1932,1878,1407,1847,1954,2088,2392,1916,1733,1740,1763,1796,1781,1838,1807,1876,1941,2034,4008,1823,2043,2245,2545,2396,1906,1943,1976,2013,2068,2086,2075,2099,2068,2114,4011,2016,2181,2375,2703,2323,1897,1959,2002,2027,1954,2019,2025,"
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

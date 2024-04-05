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
    "2116,2252,2162,2306,2369,2410,2564,2518,2555,2592,2538,2629,2506,2224,2152,1960,1855,1750,1630,1717,1644,1628,1694,1571,1679,1666,1623,1705,1610,1731,1725,1712,1672,1553,1678,1661,1669,1684,1631,1753,1676,1634,1717,1627,1728,1652,1656,1753,1732,1942,1901,1893,1949,1773,1885,1748,1735,1940,1828,1968,2446,3801,4003,3864,1588,1916,2041,2097,1990,2139,2137,2149,2294,2127,2216,2216,2220,2472,2402,2548,2641,2636,2790,2668,2661,2621,2453,2527,2303,2267,2177,1974,1894,1878,1774,1885,1798,1768,1787,1671,1776,1771,1700,1779,1623,1733,1712,1682,1745,1672,1751,1754,1645,1696,1620,1713,1653,1596,1712,1608,1728,1637,1606,1734,1673,1822,1816,1800,1847,1752,1862,1783,1759,1875,1587,2175,3411,4004,3993,1506,1825,1899,1858,2049,1924,2148,2092,2057,2211,2101,2255,2241,2262,2448,2366,2497,2525,2463,2611,2494,2512,2503,2343,2379,2183,2123,2127,2020,2168,2129,1994,2125,2032,1952,1929,1792,1874,1807,1768,1845,1747,1776,1731,1697,1801,1761,1889,1868,1800,1828,1719,1807,1736,1748,1794,1715,1811,1744,1689,1759,"
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

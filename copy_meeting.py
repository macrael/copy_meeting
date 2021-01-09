#!/usr/bin/env python3

import http.client

conn = http.client.HTTPSConnection("api.zoom.us")

headers = {
    'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IlVIQTNiYlJxUWV5TFVEVlFXbzZrbFEiLCJleHAiOjE2MTAxODM3OTUsImlhdCI6MTYxMDE3ODM5NX0.whTeyAXvVlXiBMZNNhwP-JY_NeOJnvToDNndFj0gg4k",
    'content-type': "application/json"
    }

conn.request("GET", "/v2/users?status=active&page_size=30&page_number=1", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

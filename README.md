# pysurfline

python client to Surfline API

## [Surfline](https://www.surfline.com/) API v2
)


Requests:

`https://services.surfline.com/kbyg/spots/forecasts/{type}?{params}`


Type|Data
----|----
wave|array of min/max sizes & optimal scores
wind|array of wind directions/speeds & optimal scores
tides|array of types & heights
weather|array of sunrise/set times, array of temperatures/weather conditions

Param|Values|Effect
-----|------|------
spotId|string|Surfline spot id that you want data for. A typical Surfline URL is `https://www.surfline.com/surf-report/venice-breakwater/590927576a2e4300134fbed8` where `590927576a2e4300134fbed8` is the `spotId`
days|integer|Number of forecast days to get (Max 6 w/o access token, Max 17 w/ premium token)
intervalHours|integer|Minimum of 1 (hour)
maxHeights|boolean|`true` seems to remove min & optimal values from the wave data output
sds|boolean|If true, use the new LOTUS forecast engine
accesstoken|string|Auth token to get premium data access (optional)

Anywhere there is an `optimalScore` the value can be interpreted as follows:

Value|Meaning
-----|-------
0|Suboptimal
1|Good
2|Optimal

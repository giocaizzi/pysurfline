# Surfline API

The surfline api is structured as follows:
- `kbyg`/
    - `spots/`
        - `details/` 
        - `forecasts/`
            - `conditions/`
            - `wave`
            - `wind`
            - `tides`
            - `weather`


**Required parameters:**
- `spotId`: the id of the spot you want to get data for

**Optional parameters:**

- `forecasts/`:
    - `days`: the number of days of data you want to get (default: X)
    - `intervalHours`: the interval in hours of the data you want to get (default: X)


## `pysurfline` Objects

Surfline API objects have equivalent python objects.

In order to make the API easier to use, a nested object structure is used to represent the API data and translated into python objects.

### `SpotForecasts`
The main object is `SpotForecasts`.

This object is a fusion of `spots/details `and `spots/forecasts/*` data.

- `spots/details` data is stored as object attributes.
- `spots/forecasts/*` data is stored as lists of objects.

```python
class SpotForecasts:
    spotId: int
    name: str
    waves: List[Wave]
    wind: List[Wind]
    tides: List[Tides]
    weather: List[Weather]
    sunlightTimes: List[SunlightTime]
```


#### `Wave`

```python
class Wave:
    timestamp: Timestamp
    probability: int
    utcOffSet: int
    surf: Surf
    power: float
    swells: List[Swell]
```

##### `Surf`

```python
class Surf:
    min: float
    max: float
    optimalScore: int
    plus: bool
    humanRelation: str
    raw: dict
```

##### `Swell`

```python
class Swell:
    height: float
    period: int
    impact: float
    power: float
    direction: float
    directionMin: float
    optimalScore: float
```

#### `Wind`

```python
class Wind:
    timestamp: Timestamp
    utcOffSet: int
    speed: float
    direction: float
    directionType: str
    gust: float
    optimalScore: int
```

#### `Tides`

```python
class Tides:
    timestamp: Timestamp
    utcOffSet: int
    type    
    height: float
```

#### `Weather`

```python
class Weather:
    midnight: Timestamp,
    midnightUTCOffset: int,
    dawn: Timestamp,
    dawnUTCOffset: int,
    sunrise: Timestamp,
    sunriseUTCOffset: int,
    sunset: Timestamp,
    sunsetUTCOffset: int,
    dusk: Timestamp,
    duskUTCOffset: int,
```

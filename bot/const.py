LOCATION_SEPARATOR = ";"

# Maximum locations allowed in a request
MAX_LOCATIONS_PER_MESSAGE = 10

# Maximum API requests per second (approximately)
# e.g. a rate of 4 means 4 requests/s after exhausting the capacity
# and every 1/4th of a second a token is added
# see https://en.wikipedia.org/wiki/Token_bucket
FETCH_RATE = 4

# Maximum requests made at once (bucket capacity)
FETCH_CAPACITY = 10

# Max attempts to request the weather API
MAX_RETRIES = 5

# Weather API request timeout
REQUEST_TIMEOUT = 10

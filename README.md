# Fatetime

_A funnier datetime._

## Current Functionality

### `fatetime.Datetime`

A class that extends [Python's `datetime` objects](https://docs.python.org/3/library/datetime.html#datetime.datetime) by providing a constructor that accepts one of the following:

* No arguments at all.
  - This will return an object representing the current time in UTC.
* A `datetime` object.
  - Timezone offsets are preserved.
* An [RFC 3339 datetime string](https://www.rfc-editor.org/rfc/rfc3339#section-5.6).
  - Parsable timezone offsets are preserved.
  - A trailing 'z' or 'Z' is treated as the timezone offset +00:00, i.e. UTC or Zulu.

In all cases, the lack of timezone information is treated as the timezone being UTC. In other words, _naive_ datetimes are turned into _aware_, UTC datetimes.

# Foursquare Distance
Calculates distance traveled from Foursquare account, based on airport codes
** Still quite buggy, and highly reliant on valid checkins on departure and arrival **

## Configure
Create `config.ini`, and add the following contents:
```
[auth]
auth_token=XXXX # User's foursquare token here
```

## Install
To setup `virtualenv`
``` bash
virtualenv env
. /env/bin/active
```

## Execute
``` bash
python distance.py
```

# Foursquare Distance
Calculates distance traveled from Foursquare account, based on airport codes
** Still quite buggy, and highly reliant on valid checkins on departure and arrival **

## Install
To setup `virtualenv`
``` bash
virtualenv env
. /env/bin/activate
pip install -r requirements.txt
```

## Configure
Create `config.ini`, and add the following contents:
```
[auth]
auth_token=XXXX # User's foursquare token here
```

## Execute
``` bash
python distance.py
```

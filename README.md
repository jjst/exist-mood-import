# Exist.io mood importer

This script imports mood tracking data from third-party apps into [Exist](https://exist.io/dashboard/).

It supports CSV exports from:
* [Daylio](https://daylio.webflow.io/)
* [iMoodJournal](https://www.imoodjournal.com/)

## Setup

### Install dependencies

The script uses Python 3 and [requests](http://docs.python-requests.org/en/master/). Install dependencies with:

```
pip3 install -r requirements.txt
```

### Export and download data from iMoodJournal/Daylio

Both applications support a way to export all of your data as a CSV file from the app settings. 
You will need a way to export the data out of your phone - easiest is probably to send it to yourself via email.

### Create a new Exist app

You will also need to create a [new app in Exist](https://exist.io/account/apps/edit/). You can use the following values:
* Name: Mood importer
* Redirect URI: http://localhost:9192/
* OAuth2 Client Type: public
* Service category: custom
* Provides: mood-tracking data imported from third-party apps
* Requirements: a CSV export from iMoodJournal or Daylio
* Description: imports mood-tracking data from iMoodJournal/Daylio
* Attributes that client can write: **Custom tracking**, **Mood**, **Daily note**

Once created, copy the value for **YOUR ACCESS TOKEN** in the *DEVELOPER TOKEN* section at the bottom of your app's page.

## Usage

```sh
env ACCESS_TOKEN=<YOUR ACCESS TOKEN> ./import.py <PATH TO YOUR DAYLIO OR IMOODJOURNAL EXPORT.csv>
```

## Caveats

* The imported data will **overwrite existing data** for the corresponding days! 
* iMoodJournal rates moods on a scale from 1-10, but Exists rates from 1-5, so mood levels get scaled down by 2.
* Daylio supports custom mood levels - this is not supported. The script assumes the default mood levels (rad, good, meh, bad, awful) are used.

"""
Extract metadata about public datasets owned and maintained by DTS
and publishes the data in another dataset.
"""
from datetime import datetime, timedelta
import pytz
import logging
import os
import json
import requests

from sodapy import Socrata

import utils

# Socrata creds
SO_WEB = os.getenv("SO_ENDPOINT")
SO_TOKEN = os.getenv("SO_APP_TOKEN")
SO_USER = os.getenv("SO_APP_KEY_ID")
SO_PASS = os.getenv("SO_KEY_SECRET")
RESOURCE_ID = "28ys-ieqv"

# Unique ID for the data publishing account
ATD_USER_ID = "8t3r-wq64"

BASE_URL = "https://data.austintexas.gov/d/"

OUT_FIELDS = [
    "id",
    "name",
    "description",
    "attribution",
    "type",
    "updatedAt",
    "createdAt",
    "metadata_updated_at",
    "data_updated_at",
    "download_count",
    "publication_date",
    "page_views_last_week",
    "page_views_last_month",
    "page_views_total",
]


def extract():
    logger.info("Extracting data")
    res = requests.get(
        f"https://api.us.socrata.com/api/catalog/v1?for_user={ATD_USER_ID}&limit=10000"
    )
    data = json.loads(res.text)
    return data

def convert_tz(date_str):
    # Get UTC timestamp as datetime object
    utc_datetime = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    utc_timezone = pytz.timezone('UTC')
    utc_datetime = utc_timezone.localize(utc_datetime)

    # Convert to central time
    central_timezone = pytz.timezone('US/Central')
    central_datetime = utc_datetime.astimezone(central_timezone)

    # To socrata format
    central_timestamp_string = central_datetime.strftime("%Y-%m-%dT%H:%M:%S")

    return central_timestamp_string


def transform(data):
    logger.info("Transforming data")

    output_data = []
    for row in data["results"]:
        row["resource"]["page_views_last_week"] = row["resource"]["page_views"][
            "page_views_last_week"
        ]
        row["resource"]["page_views_last_month"] = row["resource"]["page_views"][
            "page_views_last_month"
        ]
        row["resource"]["page_views_total"] = row["resource"]["page_views"][
            "page_views_total"
        ]
        filtered_data = {key: row["resource"][key] for key in OUT_FIELDS}
        filtered_data["dataset_url"] = BASE_URL + filtered_data["id"]

        # Convert UTC time to local time
        filtered_data["updatedAt"] = convert_tz(filtered_data["updatedAt"])
        filtered_data["createdAt"] = convert_tz(filtered_data["createdAt"])
        filtered_data["metadata_updated_at"] = convert_tz(filtered_data["metadata_updated_at"])
        filtered_data["data_updated_at"] = convert_tz(filtered_data["data_updated_at"])
        filtered_data["publication_date"] = convert_tz(filtered_data["publication_date"])

        # Getting update freq
        dataset_detailed = requests.get(
            f"https://data.austintexas.gov/api/views/metadata/v1/{filtered_data['id']}"
        )
        dataset_detailed = json.loads(dataset_detailed.text)
        if (
            "customFields" in dataset_detailed
            and "Publishing Information" in dataset_detailed["customFields"]
            and "Update Frequency"
            in dataset_detailed["customFields"]["Publishing Information"]
        ):
            filtered_data["update_frequency"] = dataset_detailed["customFields"][
                "Publishing Information"
            ]["Update Frequency"]
        else:
            filtered_data["update_frequency"] = ""

        # Getting number of rows
        if filtered_data["type"] == "dataset":
            row_count = requests.get(
                f"https://data.austintexas.gov/api/id/{filtered_data['id']}.json?$select=count(*)%20as%20count"
            )
            row_count = json.loads(row_count.text)
            filtered_data["row_count"] = row_count[0]["count"]
        else:
            filtered_data["row_count"] = None

        output_data.append(filtered_data)

    return output_data


def load(soda, data):
    logger.info("Publishing data to Socrata")
    res = soda.replace(RESOURCE_ID, data)
    logger.info(res)


def main():
    client = Socrata(SO_WEB, SO_TOKEN, username=SO_USER, password=SO_PASS, timeout=240)

    data = extract()
    data = transform(data)
    load(client, data)


if __name__ == "__main__":
    logger = utils.get_logger(__file__, level=logging.DEBUG)

    main()

# Copyright 2025 Rahul Samant
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json
import requests

import streamlit as st
import functions_framework

from backend.module.engineer_assignment import OnsiteServiceRequestAssignment


@functions_framework.http
def assign_onsite_service_engineer(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and "customer_id" in request_json:
        customer_id = request_json.get("customer_id")
        request_id = request_json.get("request_id")

        assignment = OnsiteServiceRequestAssignment()
        engineer_id = assignment.assign_available_engineer(
            customer_id,
            request_id,
        )

        if engineer_id:
            return engineer_id
        else:
            return False

    elif request_args and "customer_id" in request_args:
        customer_id = request_args.get("customer_id")
        request_id = request_args.get("request_id")

        assignment = OnsiteServiceRequestAssignment()
        engineer_id = assignment.assign_available_engineer(
            customer_id,
            request_id,
        )

        if engineer_id:
            return engineer_id
        else:
            return False

    else:
        return False


if __name__ == "__main__":
    url = st.secrets["URL_CLOUD_RUN_ONSITE_ENGINEER_ASSIGNMENT_SERVICE"]

    input_customer_id = str(input("Enter customer id: "))
    input_request_id = str(input("Enter request id: "))

    data = {
        "customer_id": input_customer_id,
        "request_id": input_request_id,
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("Response:", response.text)

    else:
        print(
            "Failed to create service request:", 
            response.status_code, 
            response.text,
        )

# Copyright 2020 Google LLC
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

import datetime
import os

from google.cloud import automl_v1beta1 as automl
import pytest

import video_classification_create_dataset


PROJECT_ID = os.environ["AUTOML_PROJECT_ID"]
pytest.DATASET_ID = None


@pytest.fixture(scope="function", autouse=True)
def teardown():
    yield

    # Delete the created dataset
    client = automl.AutoMlClient()
    dataset_full_id = client.dataset_path(
        PROJECT_ID, "us-central1", pytest.DATASET_ID
    )
    response = client.delete_dataset(dataset_full_id)
    response.result()


def test_video_classification_create_dataset(capsys):
    # create dataset
    dataset_name = "test_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    video_classification_create_dataset.create_dataset(
        PROJECT_ID, dataset_name
    )
    out, _ = capsys.readouterr()
    assert "Dataset id: " in out

    # Get the the created dataset id for deletion
    pytest.DATASET_ID = out.splitlines()[1].split()[2]

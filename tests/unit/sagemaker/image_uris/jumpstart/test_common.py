# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
from __future__ import absolute_import

from mock.mock import patch
import pytest

from sagemaker import image_uris
from sagemaker.jumpstart.utils import verify_model_region_and_return_specs

from tests.unit.sagemaker.jumpstart.utils import get_spec_from_base_spec
from sagemaker.jumpstart import constants as sagemaker_constants


@patch("sagemaker.jumpstart.artifacts.image_uris.verify_model_region_and_return_specs")
@patch("sagemaker.jumpstart.accessors.JumpStartModelsAccessor.get_model_specs")
def test_jumpstart_common_image_uri(
    patched_get_model_specs, patched_verify_model_region_and_return_specs
):

    patched_verify_model_region_and_return_specs.side_effect = verify_model_region_and_return_specs
    patched_get_model_specs.side_effect = get_spec_from_base_spec

    image_uris.retrieve(
        framework=None,
        region="us-west-2",
        image_scope="training",
        model_id="pytorch-ic-mobilenet-v2",
        model_version="*",
        instance_type="ml.p2.xlarge",
    )
    patched_get_model_specs.assert_called_once_with(
        region="us-west-2", model_id="pytorch-ic-mobilenet-v2", version="*"
    )
    patched_verify_model_region_and_return_specs.assert_called_once()

    patched_get_model_specs.reset_mock()
    patched_verify_model_region_and_return_specs.reset_mock()

    image_uris.retrieve(
        framework=None,
        region="us-west-2",
        image_scope="inference",
        model_id="pytorch-ic-mobilenet-v2",
        model_version="1.*",
        instance_type="ml.p2.xlarge",
    )
    patched_get_model_specs.assert_called_once_with(
        region="us-west-2", model_id="pytorch-ic-mobilenet-v2", version="1.*"
    )
    patched_verify_model_region_and_return_specs.assert_called_once()

    patched_get_model_specs.reset_mock()
    patched_verify_model_region_and_return_specs.reset_mock()

    image_uris.retrieve(
        framework=None,
        region=None,
        image_scope="training",
        model_id="pytorch-ic-mobilenet-v2",
        model_version="*",
        instance_type="ml.p2.xlarge",
    )
    patched_get_model_specs.assert_called_once_with(
        region=sagemaker_constants.JUMPSTART_DEFAULT_REGION_NAME,
        model_id="pytorch-ic-mobilenet-v2",
        version="*",
    )
    patched_verify_model_region_and_return_specs.assert_called_once()

    patched_get_model_specs.reset_mock()
    patched_verify_model_region_and_return_specs.reset_mock()

    image_uris.retrieve(
        framework=None,
        region=None,
        image_scope="inference",
        model_id="pytorch-ic-mobilenet-v2",
        model_version="1.*",
        instance_type="ml.p2.xlarge",
    )
    patched_get_model_specs.assert_called_once_with(
        region=sagemaker_constants.JUMPSTART_DEFAULT_REGION_NAME,
        model_id="pytorch-ic-mobilenet-v2",
        version="1.*",
    )
    patched_verify_model_region_and_return_specs.assert_called_once()

    with pytest.raises(NotImplementedError):
        image_uris.retrieve(
            framework=None,
            region="us-west-2",
            image_scope="BAD_SCOPE",
            model_id="pytorch-ic-mobilenet-v2",
            model_version="*",
            instance_type="ml.p2.xlarge",
        )

    with pytest.raises(KeyError):
        image_uris.retrieve(
            framework=None,
            region="us-west-2",
            image_scope="training",
            model_id="blah",
            model_version="*",
            instance_type="ml.p2.xlarge",
        )

    with pytest.raises(ValueError):
        image_uris.retrieve(
            framework=None,
            region="mars-south-1",
            image_scope="training",
            model_id="pytorch-ic-mobilenet-v2",
            model_version="*",
            instance_type="ml.p2.xlarge",
        )

    with pytest.raises(ValueError):
        image_uris.retrieve(
            framework=None,
            region="us-west-2",
            model_id="pytorch-ic-mobilenet-v2",
            model_version="*",
            instance_type="ml.p2.xlarge",
        )

    with pytest.raises(ValueError):
        image_uris.retrieve(
            framework=None,
            region="us-west-2",
            image_scope="training",
            model_version="*",
            instance_type="ml.p2.xlarge",
        )

    with pytest.raises(ValueError):
        image_uris.retrieve(
            region="us-west-2",
            framework=None,
            image_scope="training",
            model_id="pytorch-ic-mobilenet-v2",
            instance_type="ml.p2.xlarge",
        )

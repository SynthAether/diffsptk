# ------------------------------------------------------------------------ #
# Copyright 2022 SPTK Working Group                                        #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License");          #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#     http://www.apache.org/licenses/LICENSE-2.0                           #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
# ------------------------------------------------------------------------ #

import pytest

import diffsptk
import tests.utils as U


@pytest.mark.parametrize("device", ["cpu", "cuda"])
def test_compatibility(device, m=19, M=29, alpha=0.1, theta=0.2, B=2):
    freqt2 = diffsptk.SecondOrderAllPassFrequencyTransform(m, M, alpha, theta)
    ifreqt2 = diffsptk.SecondOrderAllPassInverseFrequencyTransform(M, m, alpha, theta)

    U.check_compatibility(
        device,
        [ifreqt2, freqt2],
        [],
        f"nrand -l {B*(m+1)}",
        "cat",
        [],
        dx=m + 1,
        dy=m + 1,
    )

    U.check_differentiable(device, [ifreqt2, freqt2], [B, m + 1])

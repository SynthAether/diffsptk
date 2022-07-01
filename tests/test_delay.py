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
@pytest.mark.parametrize("S", [-2, 0, 2])
@pytest.mark.parametrize("keep_len", [False, True])
def test_compatibility(device, S, keep_len, T=20, B=2):
    delay = diffsptk.Delay(S, keep_len)

    opt = "-k" if keep_len else ""
    U.check_compatibility(
        device,
        delay,
        [],
        f"ramp -l {T}",
        f"delay -s {S} {opt}",
        [],
        opt={"dim": 0},
    )

    U.check_differentiable(device, delay, [B, T])

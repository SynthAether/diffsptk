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
@pytest.mark.parametrize("n_iter", [0, 3])
def test_compatibility(device, n_iter, M=8, L=16, B=2, alpha=0.1):
    spec = diffsptk.Spectrum(L, eps=0)
    mcep = diffsptk.MelCepstralAnalysis(M, L, alpha, n_iter=n_iter)

    U.check_compatibility(
        device,
        [mcep, spec],
        [],
        f"nrand -l {B*L}",
        f"mgcep -g 0 -d 0 -i {n_iter} -l {L} -m {M} -a {alpha}",
        [],
        dx=L,
        dy=M + 1,
    )

    U.check_differentiable(device, [mcep, spec], [B, L])

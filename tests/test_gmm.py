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
@pytest.mark.parametrize("var_type", ["diag", "full"])
@pytest.mark.parametrize("block_size", [None, (2, 2), (3, 1)])
def test_compatibility(device, var_type, block_size, M=3, K=4, B=32, n_iter=50):
    if device == "cuda" and not torch.cuda.is_available():
        return

    gmm = diffsptk.GMM(
        M, K, n_iter=n_iter, var_type=var_type, block_size=block_size
    ).to(device)

    opt = ""
    if var_type == "full":
        opt += "-f "
    if block_size is not None:
        size = " ".join([str(x) for x in block_size])
        opt += f"-B {size}"

    def _gmm(x):
        gmm.warmup(x)
        return gmm(x)[-1]

    tmp1 = "gmm.tmp1"
    tmp2 = "gmm.tmp2"
    tmp3 = "gmm.tmp3"
    tmp4 = "gmm.tmp4"
    tmp5 = "gmm.tmp5"
    U.check_compatibility(
        device,
        _gmm,
        [
            f"nrand -u +2 -l {B*(M+1)} -s 1 > {tmp1}",
            f"nrand -u -2 -l {B*(M+1)} -s 2 > {tmp2}",
            f"nrand -u +4 -l {B*(M+1)} -s 3 > {tmp3}",
            f"nrand -u -4 -l {B*(M+1)} -s 4 > {tmp4}",
        ],
        f"cat {tmp1} {tmp2} {tmp3} {tmp4}",
        (
            f"cat {tmp1} {tmp2} {tmp3} {tmp4} | "
            f"gmm -m {M} -k {K} -i {n_iter} -S {tmp5} {opt} > /dev/null; "
            f"cat {tmp5}"
        ),
        [f"rm {tmp1} {tmp2} {tmp3} {tmp4} {tmp5}"],
        dx=M + 1,
    )

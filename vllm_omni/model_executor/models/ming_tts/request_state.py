# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the vLLM-Omni project

from collections.abc import Mapping
from typing import Any

from .constants import KEY_REQUEST_ID


def request_state_key(info: Mapping[str, Any], internal_request_id: str | None = None) -> str | None:
    """Use the runner's identity for state retired by its finish callback."""
    request_id = internal_request_id
    if request_id is None:
        for key in ("req_id", "request_id", KEY_REQUEST_ID):
            request_id = info.get(key)
            if request_id is not None:
                break
        else:
            request_id = (info.get("kv_metadata") or {}).get(KEY_REQUEST_ID)
    if request_id is not None and (not isinstance(request_id, str) or not request_id):
        raise RuntimeError(f"Ming received invalid request id: {request_id!r}")
    return request_id

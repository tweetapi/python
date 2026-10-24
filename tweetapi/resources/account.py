from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import TweetAPI
    from ..types import AccountUsageResponse


class AccountResource:
    def __init__(self, client: TweetAPI) -> None:
        self._client = client

    def get_usage(self) -> AccountUsageResponse:
        """Get the units left on this API key: the plan allowance, the PAYG balance,
        and the per-minute rate limit. Costs no units; it only counts toward the rate limit.
        """
        return self._client._get("/tw-v2/account/usage")

"""Optional cost-tracking sinks for FinOps visibility.

This module is intentionally fail-open: if telemetry export fails, API requests
still succeed and we log a warning.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Protocol

from ragongcp.config import Settings

logger = logging.getLogger(__name__)


class CostTracker(Protocol):
    def record_query(self, event: dict[str, Any]) -> None:
        """Record a query-level cost/usage event."""


class NoopCostTracker:
    def record_query(self, event: dict[str, Any]) -> None:
        return None


class LoggingCostTracker:
    def record_query(self, event: dict[str, Any]) -> None:
        logger.info("cost_event=%s", event)


class BigQueryCostTracker(LoggingCostTracker):
    def __init__(self, settings: Settings) -> None:
        self.project_id = settings.project_id or None
        self.dataset = settings.cost_tracking_bq_dataset
        self.table = settings.cost_tracking_bq_table
        self._client = None
        self._warned_missing_table = False

    def _get_client(self):
        if self._client is None:
            from google.cloud import bigquery

            self._client = bigquery.Client(project=self.project_id)
        return self._client

    def record_query(self, event: dict[str, Any]) -> None:
        super().record_query(event)

        if not self.dataset or not self.table:
            if not self._warned_missing_table:
                logger.warning(
                    "Cost tracking sink is bigquery but dataset/table is not configured. "
                    "Set RAGONGCP_COST_TRACKING_BQ_DATASET and RAGONGCP_COST_TRACKING_BQ_TABLE."
                )
                self._warned_missing_table = True
            return

        payload = dict(event)
        payload["event_ts"] = datetime.now(timezone.utc).isoformat()
        table_ref = f"{self.dataset}.{self.table}"
        try:
            errors = self._get_client().insert_rows_json(table_ref, [payload])
            if errors:
                logger.warning("Failed to export cost event to BigQuery: %s", errors)
        except Exception as exc:  # pragma: no cover - best effort observability path
            logger.warning("Failed to export cost event to BigQuery: %s", exc)


def build_cost_tracker(settings: Settings) -> CostTracker:
    """Build the configured cost tracker. Disabled by default."""
    if not settings.cost_tracking_enabled:
        return NoopCostTracker()

    if settings.cost_tracking_sink == "bigquery":
        return BigQueryCostTracker(settings)
    return LoggingCostTracker()


"""Tests for auto-pagination helpers."""

import pytest

from tweetapi import paginate, paginate_pages


def make_fetcher(pages):
    """Create a fetcher that returns pre-built pages in sequence."""
    call_count = [0]

    def fetcher(cursor=None):
        idx = call_count[0]
        if idx >= len(pages):
            raise RuntimeError(f"Unexpected call #{idx + 1}")
        call_count[0] += 1
        return pages[idx]

    fetcher.call_count = call_count
    return fetcher


class TestPaginatePages:
    def test_iterates_all_pages(self):
        pages_data = [
            {"data": [{"id": "1"}, {"id": "2"}], "pagination": {"nextCursor": "c2", "prevCursor": None}},
            {"data": [{"id": "3"}], "pagination": {"nextCursor": "c3", "prevCursor": "c2"}},
            {"data": [{"id": "4"}], "pagination": {"nextCursor": None, "prevCursor": "c3"}},
        ]
        fetcher = make_fetcher(pages_data)

        result = list(paginate_pages(fetcher))
        assert len(result) == 3
        assert fetcher.call_count[0] == 3

    def test_respects_max_pages(self):
        pages_data = [
            {"data": [{"id": "1"}], "pagination": {"nextCursor": "c2", "prevCursor": None}},
            {"data": [{"id": "2"}], "pagination": {"nextCursor": "c3", "prevCursor": "c2"}},
            {"data": [{"id": "3"}], "pagination": {"nextCursor": None, "prevCursor": "c3"}},
        ]
        fetcher = make_fetcher(pages_data)

        result = list(paginate_pages(fetcher, max_pages=2))
        assert len(result) == 2
        assert fetcher.call_count[0] == 2

    def test_single_page_no_next_cursor(self):
        pages_data = [
            {"data": [{"id": "1"}], "pagination": {"nextCursor": None, "prevCursor": None}},
        ]
        fetcher = make_fetcher(pages_data)

        result = list(paginate_pages(fetcher))
        assert len(result) == 1

    def test_empty_data(self):
        pages_data = [
            {"data": [], "pagination": {"nextCursor": None, "prevCursor": None}},
        ]
        fetcher = make_fetcher(pages_data)

        result = list(paginate_pages(fetcher))
        assert len(result) == 1
        assert result[0]["data"] == []

    def test_error_propagation(self):
        call_count = [0]

        def fetcher(cursor=None):
            idx = call_count[0]
            call_count[0] += 1
            if idx == 0:
                return {"data": [{"id": "1"}], "pagination": {"nextCursor": "c2", "prevCursor": None}}
            raise RuntimeError("API error")

        with pytest.raises(RuntimeError, match="API error"):
            list(paginate_pages(fetcher))


class TestPaginate:
    def test_yields_individual_items(self):
        pages_data = [
            {"data": [{"id": "1"}, {"id": "2"}], "pagination": {"nextCursor": "c2", "prevCursor": None}},
            {"data": [{"id": "3"}], "pagination": {"nextCursor": None, "prevCursor": "c2"}},
        ]
        fetcher = make_fetcher(pages_data)

        items = list(paginate(fetcher))
        assert items == [{"id": "1"}, {"id": "2"}, {"id": "3"}]

    def test_respects_max_pages(self):
        pages_data = [
            {"data": [{"id": "1"}], "pagination": {"nextCursor": "c2", "prevCursor": None}},
            {"data": [{"id": "2"}], "pagination": {"nextCursor": None, "prevCursor": "c2"}},
        ]
        fetcher = make_fetcher(pages_data)

        items = list(paginate(fetcher, max_pages=1))
        assert items == [{"id": "1"}]
        assert fetcher.call_count[0] == 1

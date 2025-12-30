"""Tests for the MCP JustWatch server using FastMCP."""

import pytest
from unittest.mock import Mock, patch

from mcp_justwatch.server import (
    search_content,
    get_details,
    get_offers_for_countries,
    format_media_entry,
)


class MockMediaEntry:
    """Mock MediaEntry object for testing."""

    def __init__(self, **kwargs):
        self.title = kwargs.get("title", "Test Title")
        self.node_id = kwargs.get("node_id", "tm12345")
        self.entry_type = kwargs.get("entry_type", "MOVIE")
        self.release_year = kwargs.get("release_year", 2020)
        self.release_date = kwargs.get("release_date", None)
        self.runtime_minutes = kwargs.get("runtime_minutes", None)
        self.genres = kwargs.get("genres", [])
        self.imdb_score = kwargs.get("imdb_score", None)
        self.tmdb_score = kwargs.get("tmdb_score", None)
        self.offers = kwargs.get("offers", [])


class MockOffer:
    """Mock Offer object for testing."""

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "Netflix")
        self.monetization_type = kwargs.get("monetization_type", "FLATRATE")
        self.presentation_type = kwargs.get("presentation_type", "HD")
        self.price_string = kwargs.get("price_string", None)
        self.url = kwargs.get("url", "https://example.com")


class TestFormatMediaEntry:
    """Tests for format_media_entry function."""

    def test_format_basic_entry(self):
        """Test formatting a basic media entry."""
        entry = MockMediaEntry(
            title="The Matrix", node_id="tm123", entry_type="MOVIE", release_year=1999
        )

        result = format_media_entry(entry)

        assert "The Matrix" in result
        assert "tm123" in result
        assert "MOVIE" in result
        assert "1999" in result

    def test_format_entry_with_index(self):
        """Test formatting with index number."""
        entry = MockMediaEntry(title="Test Movie")

        result = format_media_entry(entry, index=1)

        assert "1." in result
        assert "Test Movie" in result

    def test_format_entry_with_runtime(self):
        """Test formatting entry with runtime."""
        entry = MockMediaEntry(runtime_minutes=136)

        result = format_media_entry(entry)

        assert "2h 16m" in result

    def test_format_entry_with_runtime_under_hour(self):
        """Test formatting entry with runtime under an hour."""
        entry = MockMediaEntry(runtime_minutes=45)

        result = format_media_entry(entry)

        assert "45m" in result

    def test_format_entry_with_genres(self):
        """Test formatting entry with genres."""
        entry = MockMediaEntry(genres=["Action", "Sci-Fi"])

        result = format_media_entry(entry)

        assert "Action" in result
        assert "Sci-Fi" in result

    def test_format_entry_with_scores(self):
        """Test formatting entry with IMDb and TMDb scores."""
        entry = MockMediaEntry(imdb_score=8.7, tmdb_score=8.5)

        result = format_media_entry(entry)

        assert "8.7" in result
        assert "8.5" in result

    def test_format_entry_with_offers(self):
        """Test formatting entry with streaming offers."""
        offers = [
            MockOffer(name="Netflix", monetization_type="FLATRATE"),
            MockOffer(name="Amazon", monetization_type="RENT", price_string="$3.99"),
        ]
        entry = MockMediaEntry(offers=offers)

        result = format_media_entry(entry)

        assert "Netflix" in result
        assert "Amazon" in result
        assert "FLATRATE" in result
        assert "$3.99" in result

    def test_format_entry_no_offers(self):
        """Test formatting entry with no offers."""
        entry = MockMediaEntry(offers=[])

        result = format_media_entry(entry)

        assert "No streaming offers available" in result


class TestSearchContent:
    """Tests for search_content tool."""

    def test_search_content_success(self):
        """Test successful content search."""
        mock_entry = MockMediaEntry(
            title="The Matrix",
            node_id="tm123",
            entry_type="MOVIE",
            release_year=1999,
            genres=["Action", "Sci-Fi"],
            imdb_score=8.7,
            offers=[MockOffer(name="Netflix")],
        )

        with patch("mcp_justwatch.server.justwatch.search", return_value=[mock_entry]):
            result = search_content.fn(query="The Matrix", country="US")

        assert "The Matrix" in result
        assert "1999" in result
        assert "Netflix" in result

    def test_search_content_no_results(self):
        """Test search with no results."""
        with patch("mcp_justwatch.server.justwatch.search", return_value=[]):
            result = search_content.fn(query="NonexistentMovie12345", country="US")

        assert "No results found" in result

    def test_search_content_with_all_parameters(self):
        """Test search with all optional parameters."""
        mock_entry = MockMediaEntry(title="Test Movie")

        with patch("mcp_justwatch.server.justwatch.search", return_value=[mock_entry]) as mock_search:
            result = search_content.fn(
                query="Test",
                country="GB",
                language="en",
                count=10,
                best_only=False,
            )

        mock_search.assert_called_once_with(
            title="Test", country="GB", language="en", count=10, best_only=False
        )
        assert "Test Movie" in result

    def test_search_normalizes_country_code(self):
        """Test that country codes are normalized to uppercase."""
        mock_entry = MockMediaEntry(title="Test")

        with patch("mcp_justwatch.server.justwatch.search", return_value=[mock_entry]) as mock_search:
            search_content.fn(query="Test", country="us")

        # Check that the country was uppercased
        call_args = mock_search.call_args
        assert call_args.kwargs["country"] == "US"

    def test_search_normalizes_language_code(self):
        """Test that language codes are normalized to lowercase."""
        mock_entry = MockMediaEntry(title="Test")

        with patch("mcp_justwatch.server.justwatch.search", return_value=[mock_entry]) as mock_search:
            search_content.fn(query="Test", language="EN")

        # Check that the language was lowercased
        call_args = mock_search.call_args
        assert call_args.kwargs["language"] == "en"

    def test_search_clamps_count(self):
        """Test that count is clamped to valid range."""
        mock_entry = MockMediaEntry(title="Test")

        with patch("mcp_justwatch.server.justwatch.search", return_value=[mock_entry]) as mock_search:
            # Test upper bound
            search_content.fn(query="Test", count=100)
            assert mock_search.call_args.kwargs["count"] == 20

        with patch("mcp_justwatch.server.justwatch.search", return_value=[mock_entry]) as mock_search:
            # Test lower bound
            search_content.fn(query="Test", count=0)
            assert mock_search.call_args.kwargs["count"] == 1

    def test_search_exception_handling(self):
        """Test exception handling in search."""
        with patch("mcp_justwatch.server.justwatch.search", side_effect=Exception("API Error")):
            result = search_content.fn(query="Test")

        assert "Error" in result
        assert "API Error" in result


class TestGetDetails:
    """Tests for get_details tool."""

    def test_get_details_success(self):
        """Test successful details retrieval."""
        mock_entry = MockMediaEntry(
            title="The Matrix",
            node_id="tm123",
            release_year=1999,
            runtime_minutes=136,
            genres=["Action", "Sci-Fi"],
            imdb_score=8.7,
        )

        with patch("mcp_justwatch.server.justwatch.details", return_value=mock_entry):
            result = get_details.fn(node_id="tm123", country="US")

        assert "The Matrix" in result
        assert "tm123" in result
        assert "8.7" in result

    def test_get_details_not_found(self):
        """Test details retrieval with no results."""
        with patch("mcp_justwatch.server.justwatch.details", return_value=None):
            result = get_details.fn(node_id="tm999", country="US")

        assert "No details found" in result

    def test_get_details_with_all_parameters(self):
        """Test details with all optional parameters."""
        mock_entry = MockMediaEntry(title="Test")

        with patch("mcp_justwatch.server.justwatch.details", return_value=mock_entry) as mock_details:
            result = get_details.fn(
                node_id="tm123", country="FR", language="fr", best_only=False
            )

        mock_details.assert_called_once_with(
            node_id="tm123", country="FR", language="fr", best_only=False
        )
        assert "Test" in result

    def test_get_details_normalizes_codes(self):
        """Test that country and language codes are normalized."""
        mock_entry = MockMediaEntry(title="Test")

        with patch("mcp_justwatch.server.justwatch.details", return_value=mock_entry) as mock_details:
            get_details.fn(node_id="tm123", country="gb", language="EN")

        call_args = mock_details.call_args
        assert call_args.kwargs["country"] == "GB"
        assert call_args.kwargs["language"] == "en"

    def test_get_details_exception_handling(self):
        """Test exception handling in details."""
        with patch("mcp_justwatch.server.justwatch.details", side_effect=Exception("API Error")):
            result = get_details.fn(node_id="tm123")

        assert "Error" in result
        assert "API Error" in result


class TestGetOffersForCountries:
    """Tests for get_offers_for_countries tool."""

    def test_get_offers_success(self):
        """Test successful offers retrieval across countries."""
        mock_offers = {
            "US": [MockOffer(name="Netflix"), MockOffer(name="Hulu")],
            "GB": [MockOffer(name="Netflix")],
        }

        with patch(
            "mcp_justwatch.server.justwatch.offers_for_countries", return_value=mock_offers
        ):
            result = get_offers_for_countries.fn(node_id="tm123", countries=["US", "GB"])

        assert "US:" in result
        assert "GB:" in result
        assert "Netflix" in result
        assert "Hulu" in result

    def test_get_offers_no_results(self):
        """Test offers retrieval with no results."""
        with patch("mcp_justwatch.server.justwatch.offers_for_countries", return_value={}):
            result = get_offers_for_countries.fn(node_id="tm999", countries=["US"])

        assert "No offers found" in result

    def test_get_offers_empty_country(self):
        """Test offers with countries having no offers."""
        mock_offers = {
            "US": [MockOffer(name="Netflix")],
            "XX": [],
        }

        with patch(
            "mcp_justwatch.server.justwatch.offers_for_countries", return_value=mock_offers
        ):
            result = get_offers_for_countries.fn(node_id="tm123", countries=["US", "XX"])

        assert "US:" in result
        assert "XX:" in result
        assert "No offers available" in result

    def test_get_offers_normalizes_country_codes(self):
        """Test that country codes are normalized to uppercase."""
        mock_offers = {"US": [], "GB": []}

        with patch(
            "mcp_justwatch.server.justwatch.offers_for_countries", return_value=mock_offers
        ) as mock_func:
            get_offers_for_countries.fn(node_id="tm123", countries=["us", "gb"])

        # Check that countries were uppercased and converted to set
        call_args = mock_func.call_args
        assert call_args.kwargs["countries"] == {"US", "GB"}

    def test_get_offers_with_all_parameters(self):
        """Test offers with all optional parameters."""
        mock_offers = {"US": []}

        with patch(
            "mcp_justwatch.server.justwatch.offers_for_countries", return_value=mock_offers
        ) as mock_func:
            get_offers_for_countries.fn(
                node_id="tm123",
                countries=["US"],
                language="es",
                best_only=False,
            )

        mock_func.assert_called_once_with(
            node_id="tm123", countries={"US"}, language="es", best_only=False
        )

    def test_get_offers_with_pricing_info(self):
        """Test offers with pricing information."""
        mock_offers = {
            "US": [
                MockOffer(
                    name="Amazon",
                    monetization_type="RENT",
                    presentation_type="4K",
                    price_string="$3.99",
                    url="https://amazon.com/example",
                )
            ]
        }

        with patch(
            "mcp_justwatch.server.justwatch.offers_for_countries", return_value=mock_offers
        ):
            result = get_offers_for_countries.fn(node_id="tm123", countries=["US"])

        assert "Amazon" in result
        assert "RENT" in result
        assert "4K" in result
        assert "$3.99" in result
        assert "https://amazon.com/example" in result

    def test_get_offers_exception_handling(self):
        """Test exception handling in offers."""
        with patch(
            "mcp_justwatch.server.justwatch.offers_for_countries",
            side_effect=Exception("API Error"),
        ):
            result = get_offers_for_countries.fn(node_id="tm123", countries=["US"])

        assert "Error" in result
        assert "API Error" in result

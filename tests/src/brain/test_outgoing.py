"""Tests for Outgoing class."""

from unittest.mock import patch, MagicMock, AsyncMock
import pytest
import httpx
from src.brain._outgoing import Outgoing, Request, Logs, Reports

### OUTGOING ###

@pytest.mark.asyncio
async def test_outgoing_constructor():
    """Test Outgoing constructor."""
    token = "token"
    bike_id = 123
    outgoing = Outgoing(token, bike_id)
    assert outgoing.token == token
    assert outgoing.bike_id == bike_id
    assert outgoing.logs is not None
    assert outgoing.reports is not None
    assert outgoing.request is not None

### REQUEST ###

@pytest.mark.asyncio
async def test_request_zones_success():
    """Test Request.zones() success."""
    req = Request(url="http://randomurl.com", headers={"Authorization": "Bearer"})
    mock_zones_data = {"some": "zones"}
    with patch("httpx.AsyncClient", autospec=True) as mock_client_class:
        mock_client_instance = MagicMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client_instance
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = mock_zones_data
        mock_client_instance.get = AsyncMock(return_value=mock_response)
        result = await req.zones()
        assert result == mock_zones_data
        mock_client_instance.get.assert_awaited_once()
        mock_response.raise_for_status.assert_called_once()

@pytest.mark.asyncio
async def test_request_zones_failure(capfd):
    """Test Request.zones() failure."""
    req = Request(url="http://randomurl.com", headers={})
    with patch("httpx.AsyncClient", autospec=True) as mock_client_class:
        mock_client_instance = MagicMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client_instance
        mock_client_instance.get.side_effect = httpx.RequestError("Connection error")
        result = await req.zones()
        assert result is None
        captured = capfd.readouterr()
        assert "Failed to get zones Connection error" in captured.out

@pytest.mark.asyncio
async def test_request_zone_types_success():
    """Test Request.zone_types() success."""
    req = Request(url="http://randomurl.com", headers={"Authorization": "Bearer"})
    mock_types_data = {"some": "zone_types"}
    with patch("httpx.AsyncClient", autospec=True) as mock_client_class:
        mock_client_instance = MagicMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client_instance
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = mock_types_data
        mock_client_instance.get = AsyncMock(return_value=mock_response)
        result = await req.zone_types()
        assert result == mock_types_data
        mock_client_instance.get.assert_awaited_once()

@pytest.mark.asyncio
async def test_request_zone_types_failure(capfd):
    """Test Request.zone_types() failure."""
    req = Request(url="http://randomurl.com", headers={})
    with patch("httpx.AsyncClient", autospec=True) as mock_client_class:
        mock_client_instance = MagicMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client_instance
        mock_client_instance.get.side_effect = httpx.RequestError("Some error")
        result = await req.zone_types()
        assert result is None
        captured = capfd.readouterr()
        assert "Failed to get zone types. Some error" in captured.out

### LOGS ###

@pytest.mark.asyncio
async def test_logs_send_single():
    """Test sending a single log."""
    logs_obj = Logs(url="http://randomurl.com", headers={})
    single_log = {"a": "log"}
    with patch("httpx.AsyncClient", autospec=True) as mock_client_class:
        mock_client_instance = MagicMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client_instance
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_client_instance.post = AsyncMock(return_value=mock_response)
        await logs_obj.send(single_log)
        mock_client_instance.post.assert_awaited_once_with(
            "http://randomurl.com/v1/trips/",
            headers={},
            data='{"a": "log"}',
            timeout=20.0
        )
        mock_response.raise_for_status.assert_called_once()

@pytest.mark.asyncio
async def test_logs_send_list():
    """Test sending a list of logs."""
    logs_obj = Logs(url="http://randomurl.com", headers={})
    log_list = [{"log": 1}, {"log": 2}]
    with patch("httpx.AsyncClient", autospec=True) as mock_client_class:
        mock_client_instance = MagicMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client_instance
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_client_instance.post = AsyncMock(return_value=mock_response)
        await logs_obj.send(log_list)
        assert mock_client_instance.post.await_count == 2
        mock_response.raise_for_status.assert_called()

@pytest.mark.asyncio
async def test_logs_update_single():
    """Test updating a single log."""
    logs_obj = Logs(url="http://randomurl.com", headers={})
    single_log = {"update": "log"}
    with patch("httpx.AsyncClient", autospec=True) as mock_client_class:
        mock_client_instance = MagicMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client_instance
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_client_instance.patch = AsyncMock(return_value=mock_response)
        await logs_obj.update(single_log)
        mock_client_instance.patch.assert_awaited_once_with(
            "http://randomurl.com/v1/trips/{id}",
            headers={},
            data='{"update": "log"}',
            timeout=20.0
        )
        mock_response.raise_for_status.assert_called_once()

@pytest.mark.asyncio
async def test_logs_update_list():
    """Test updating a list of logs."""
    logs_obj = Logs(url="http://randomurl.com", headers={})
    log_list = [{"update": 1}, {"update": 2}]
    with patch("httpx.AsyncClient", autospec=True) as mock_client_class:
        mock_client_instance = MagicMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client_instance
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_client_instance.patch = AsyncMock(return_value=mock_response)
        await logs_obj.update(log_list)
        assert mock_client_instance.patch.await_count == 2
        mock_response.raise_for_status.assert_called()

@pytest.mark.asyncio
async def test_logs_send_failure(capfd):
    """Test Logs.send() failure."""
    logs_obj = Logs(url="http://randomurl.com", headers={})
    single_log = {"a": "log"}
    with patch("httpx.AsyncClient", autospec=True) as mock_client_class:
        mock_client_instance = MagicMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client_instance
        mock_client_instance.post.side_effect = httpx.RequestError("fail to post")
        await logs_obj.send(single_log)
        captured = capfd.readouterr()
        assert "Failed to send log. fail to post" in captured.out

@pytest.mark.asyncio
async def test_logs_update_failure_print(capfd):
    """Test Logs.update() failure."""
    logs_obj = Logs(url="http://randomurl.com", headers={})
    single_log = {"update": "this"}
    with patch("httpx.AsyncClient", autospec=True) as mock_client_class:
        mock_client_instance = MagicMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client_instance
        mock_client_instance.patch.side_effect = httpx.RequestError("Update error")
        await logs_obj.update(single_log)
        captured = capfd.readouterr()
        assert "Failed to send log. Update error" in captured.out

### REPORTS ###

@pytest.mark.asyncio
async def test_reports_send_single():
    """Test Reports.send() with a single report."""
    reports_obj = Reports(url="http://randomurl.com", headers={}, bike_id=123)
    single_report = {"a": "report"}
    with patch("httpx.AsyncClient", autospec=True) as mock_client_class:
        mock_client_instance = MagicMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client_instance
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_client_instance.patch = AsyncMock(return_value=mock_response)
        await reports_obj.send(single_report)
        expected_url = "http://randomurl.com/v1/bikes/123"
        mock_client_instance.patch.assert_awaited_once_with(
            expected_url,
            headers={},
            data='{"a": "report"}',
            timeout=20.0
        )
        mock_response.raise_for_status.assert_called_once()

@pytest.mark.asyncio
async def test_reports_send_list():
    """Test Reports.send() with a list of reports."""
    reports_obj = Reports(url="http://randomurl.com", headers={}, bike_id=999)
    report_list = [{"report": 1}, {"report": 2}, {"report": 3}]
    with patch("httpx.AsyncClient", autospec=True) as mock_client_class:
        mock_client_instance = MagicMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client_instance
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_client_instance.patch = AsyncMock(return_value=mock_response)
        await reports_obj.send(report_list)
        assert mock_client_instance.patch.await_count == 3
        mock_response.raise_for_status.assert_called()

@pytest.mark.asyncio
async def test_reports_send_failure(capfd):
    """Test Reports.send() failure."""
    reports_obj = Reports(url="http://randomurl.com", headers={}, bike_id=123)
    single_report = {"a": "report"}
    with patch("httpx.AsyncClient", autospec=True) as mock_client_class:
        mock_client_instance = MagicMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client_instance
        mock_client_instance.patch.side_effect = httpx.RequestError("some patch error")
        await reports_obj.send(single_report)
        captured = capfd.readouterr()
        assert "Failed to send report. some patch error" in captured.out

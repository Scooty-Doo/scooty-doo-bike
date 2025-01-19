# pylint: disable=duplicate-code
"""Tests for the Brain class."""

from unittest.mock import patch, MagicMock, AsyncMock
import pytest
import httpx
from src.brain.brain import Brain
from src._utils._clock import Clock
from src._utils._settings import Settings

class TestBrain:
    """Tests for the Brain class."""

    @pytest.mark.asyncio
    async def test_brain_initialize_needs_zones_and_zone_types(self):
        """Test initialize() calls request_zones() and request_zone_types() if they're None."""
        brain = Brain(bike_id=123, longitude=10.0, latitude=20.0, token="token")
        brain.bike.zones = None
        brain.bike.zone_types = None
        mock_zones = {"some": "zones"}
        mock_zone_types = {"some": "zone_types"}
        with patch.object(brain, 'request_zones', return_value=mock_zones) as mock_req_zones, \
            patch.object(
                brain, 'request_zone_types', return_value=mock_zone_types
            ) as mock_req_zone_types:
            await brain.initialize()
            mock_req_zones.assert_awaited_once()
            mock_req_zone_types.assert_awaited_once()
            assert brain.bike.zones == mock_zones
            assert brain.bike.zone_types == mock_zone_types

    @pytest.mark.asyncio
    async def test_brain_initialize_already_has_zones_types(self):
        """
        Test initialize() does not call request_zones() or request_zone_types() 
        if they're already set.
        """
        brain = Brain(123, 10.0, 20.0, "token")
        brain.bike.zones = {"zones": "exist"}
        brain.bike.zone_types = {"zone_types": "exist"}

        with patch.object(brain, 'request_zones') as mock_req_zones, \
            patch.object(brain, 'request_zone_types') as mock_req_zone_types:
            await brain.initialize()
            mock_req_zones.assert_not_awaited()
            mock_req_zone_types.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_brain_send_log(self):
        """Test send_log() calls outgoing.logs.send() with the last log."""
        brain = Brain(1, 1.0, 2.0, 'token')
        mock_log = {"some": "log"}
        brain.bike.logs.last = MagicMock(return_value=mock_log)
        with patch.object(brain.outgoing.logs, 'send', new_callable=AsyncMock) as mock_send:
            await brain.send_log()
            mock_send.assert_awaited_once_with(mock_log)

    @pytest.mark.asyncio
    async def test_brain_update_log_no_arg(self):
        """Test update_log() calls outgoing.logs.update() with the last log."""
        brain = Brain(1, 1.0, 2.0, "token")
        mock_log = {"a": "log"}
        brain.bike.logs.last = MagicMock(return_value=mock_log)
        with patch.object(brain.outgoing.logs, 'update', new_callable=AsyncMock) as mock_update:
            await brain.update_log()
            mock_update.assert_awaited_once_with(mock_log)

    @pytest.mark.asyncio
    async def test_brain_send_logs(self):
        """Test send_logs() calls bike.logs.get() and outgoing.logs.send()."""
        brain = Brain(1, 1.0, 2.0, "token")
        mock_logs = [{"log": 1}, {"log": 2}]
        brain.bike.logs.get = MagicMock(return_value=mock_logs)
        with patch.object(brain.outgoing.logs, 'send', new_callable=AsyncMock) as mock_send:
            await brain.send_logs()
            mock_send.assert_awaited_once_with(mock_logs)

    @pytest.mark.asyncio
    async def test_brain_send_report(self):
        """Test send_report() calls bike.reports.last() and outgoing.reports.send()."""
        brain = Brain(1, 1.0, 2.0, "token")
        mock_report = {"a": "report"}
        brain.bike.reports.last = MagicMock(return_value=mock_report)
        with patch.object(brain.outgoing.reports, 'send', new_callable=AsyncMock) as mock_send:
            await brain.send_report()
            mock_send.assert_awaited_once_with(mock_report)

    @pytest.mark.asyncio
    async def test_brain_send_reports(self):
        """Test send_reports() calls bike.reports.get() and outgoing.reports.send()."""
        brain = Brain(1, 1.0, 2.0, "token")
        mock_reports = [{"report": "1"}, {"report": "2"}]
        brain.bike.reports.get = MagicMock(return_value=mock_reports)
        with patch.object(brain.outgoing.reports, 'send', new_callable=AsyncMock) as mock_send:
            await brain.send_reports()
            mock_send.assert_awaited_once_with(mock_reports)

    @pytest.mark.asyncio
    async def test_brain_request_zones(self):
        """Verify request_zones() delegates to outgoing.request.zones()."""
        brain = Brain(1, 1.0, 2.0, "token")
        mock_zones = {"mock": "zones"}
        with patch.object(
            brain.outgoing.request, 'zones',
            new_callable=AsyncMock, return_value=mock_zones):
            zones = await brain.request_zones()
            assert zones == mock_zones

    @pytest.mark.asyncio
    async def test_brain_request_zone_types(self):
        """Verify request_zone_types() delegates to outgoing.request.zone_types()."""
        brain = Brain(1, 1.0, 2.0, "token")
        mock_zone_types = {"mock": "zone_types"}
        with patch.object(
            brain.outgoing.request, 'zone_types',
            new_callable=AsyncMock, return_value=mock_zone_types):
            zone_types = await brain.request_zone_types()
            assert zone_types == mock_zone_types

    @pytest.mark.asyncio
    async def test_brain_run_once(self):
        """Test running the brain."""
        brain = Brain(1, 1.0, 2.0, "token")
        with patch('random.randint', return_value=0), \
            patch.object(Clock, 'sleep', new_callable=AsyncMock) as mock_sleep, \
            patch.object(brain, 'send_report', new_callable=AsyncMock) as mock_send_report:
            async def _stop_running(*args, **kwargs): # pylint: disable=unused-argument
                brain.running = False
            mock_sleep.side_effect = _stop_running
            await brain.run()
            mock_sleep.assert_awaited_once()
            mock_send_report.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_brain_run_raises_httpstatuserror(self, caplog):
        """Test if run() raises an HTTPStatusError"""
        brain = Brain(1, 1.0, 2.0, "token")
        with patch('random.randint', return_value=0), \
            patch.object(Clock, 'sleep', new_callable=AsyncMock) as mock_sleep, \
            patch.object(brain, 'send_report', new_callable=AsyncMock) as mock_send_report:
            mock_error = httpx.HTTPStatusError("Some HTTP Error", request=None, response=None)
            mock_send_report.side_effect = mock_error
            with pytest.raises(httpx.HTTPStatusError):
                await brain.run()
            assert "HTTPStatusError while sending report" in caplog.text
            mock_sleep.assert_awaited_once()
            mock_send_report.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_brain_run_raises_unexpected_exception(self, caplog):
        """Test if run() raises an unexpected exception."""
        brain = Brain(1, 1.0, 2.0, "token")
        with patch('random.randint', return_value=0), \
            patch.object(Clock, 'sleep', new_callable=AsyncMock) as mock_sleep, \
            patch.object(brain, 'send_report', new_callable=AsyncMock) as mock_send_report:
            mock_send_report.side_effect = ValueError("Unexpected error")
            with pytest.raises(ValueError):
                await brain.run()
            assert "Unexpected error while sending report: Unexpected error" in caplog.text
            mock_sleep.assert_awaited_once()
            mock_send_report.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_brain_terminate(self):
        """Test terminate() sets brain.running=False."""
        brain = Brain(1, 1.0, 2.0, "token")
        assert brain.running is True
        await brain.terminate()
        assert brain.running is False

    def test_brain_is_not_deployed(self):
        """Test _is_not_deployed() returns True if the bike is not deployed."""
        with patch.object(Settings.Position, 'default_longitude', 0.0), \
            patch.object(Settings.Position, 'default_latitude', 0.0):
            brain_matching = Brain(1, 0.0, 0.0, "token")
            assert brain_matching.is_not_deployed() is True
            brain_diff = Brain(2, 10.0, 10.0, "token")
            assert brain_diff.is_not_deployed() is False

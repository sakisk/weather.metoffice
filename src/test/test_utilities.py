from datetime import datetime
from mock import Mock
from xbmctestcase import XBMCTestCase

class TestUtilities(XBMCTestCase):

    def setUp(self):
        super(TestUtilities, self).setUp()
        from metoffice.utils import utilities
        self.utilities = utilities

    def test_strptime(self):
        date = '23:06 Mon 4 Jan 2013'
        fmt = '%H:%M %a %d %b %Y'
        self.assertEqual(datetime.strptime(date, fmt), self.utilities.strptime(date,fmt))
        
    def test_log(self):
        msg = "Log message"
        self.utilities.log(msg)
        self.xbmc.log.assert_called_with('weather.metoffice: {0}'.format(msg), self.xbmc.LOGNOTICE)

    def test_xbmcbusy(self):
        mock_func = Mock()
        mock_func.__name__ = "Percy"
        self.xbmcgui.getCurrentWindowId = Mock(return_value=self.utilities.WINDOW_WEATHER)
        decorated_func = self.utilities.xbmcbusy(mock_func)
        decorated_func(1,2,3)
        self.assertEqual(2, len(self.xbmc.executebuiltin.call_args_list))
        self.assertEqual(self.xbmc.executebuiltin.call_args_list[0], (("ActivateWindow(busydialog)",),))
        self.assertEqual(self.xbmc.executebuiltin.call_args_list[1], (("Dialog.Close(busydialog)",),))
        mock_func.assert_called_with(1,2,3)
    
    def test_panelbusy(self):
        mock_func = Mock()
        mock_func.__name__ = "Percy"
        rightbusy = self.utilities.panelbusy("RightPanel")
        decorated_func = rightbusy(mock_func)
        decorated_func(1,2,3)
        self.xbmcgui.Window.return_value.setProperty.assert_called_once_with('RightPanel.IsBusy', 'true')
        self.xbmcgui.Window.return_value.clearProperty.assert_called_once_with('RightPanel.IsBusy')
        mock_func.assert_called_with(1,2,3)
        
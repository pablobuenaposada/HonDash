from unittest import mock
from unittest.mock import MagicMock

import pytest

from backend.devices.ecu import Ecu
from backend.devices.kpro import constants as kpro_constants
from backend.devices.kpro.kpro import Kpro
from backend.devices.s300 import constants as s300_constants
from backend.devices.s300.s300 import S300


class TestEcu:
    @pytest.mark.parametrize(
        "vendor_id, product_id, result",
        (
            (
                kpro_constants.KPRO23_ID_VENDOR,
                kpro_constants.KPRO23_ID_PRODUCT,
                (Kpro, type(None)),
            ),
            (
                kpro_constants.KPRO4_ID_VENDOR,
                kpro_constants.KPRO4_ID_PRODUCT,
                (Kpro, type(None)),
            ),
            (
                s300_constants.S3003_ID_VENDOR,
                s300_constants.S3003_ID_PRODUCT,
                (Kpro, S300),
            ),
            (
                None,
                None,
                (Kpro, S300),
            ),
        ),
    )
    def test___init__(self, vendor_id, product_id, result):
        def found_device(idVendor, idProduct):
            if idVendor == vendor_id and idProduct == product_id:
                return MagicMock()
            else:
                return None

        with mock.patch("usb.core.find") as m_find, mock.patch(
            "threading.Thread.start"
        ):
            m_find.side_effect = found_device
            ecu = Ecu()

        assert isinstance(ecu.kpro, result[0])
        assert isinstance(ecu.s300, result[1])

    @pytest.mark.parametrize(
        "vendor_id, product_id, value, result",
        (
            (kpro_constants.KPRO4_ID_VENDOR, kpro_constants.KPRO4_ID_PRODUCT, "tps", 0),
            (
                kpro_constants.KPRO4_ID_VENDOR,
                kpro_constants.KPRO4_ID_PRODUCT,
                "foo",
                666,
            ),
            (s300_constants.S3003_ID_VENDOR, s300_constants.S3003_ID_PRODUCT, "tps", 0),
            (None, None, "tps", 666),
        ),
    )
    def test__get_value_from_ecu(self, vendor_id, product_id, value, result):
        def found_device(idVendor, idProduct):
            if idVendor == vendor_id and idProduct == product_id:
                return MagicMock()
            else:
                return None

        with mock.patch("usb.core.find") as m_find, mock.patch(
            "threading.Thread.start"
        ):
            m_find.side_effect = found_device
            ecu = Ecu()
            assert ecu._get_value_from_ecu(value, fallback=666) == result

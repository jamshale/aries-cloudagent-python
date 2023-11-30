from unittest import IsolatedAsyncioTestCase
from aries_cloudagent.tests import mock

from .....admin.request_context import AdminRequestContext
from .....connections.models.conn_record import ConnRecord
from .....core.in_memory import InMemoryProfile

from ....didcomm_prefix import DIDCommPrefix
from ....didexchange.v1_0.message_types import ARIES_PROTOCOL as DIDX_PROTO

from ..models.invitation import InvitationRecord, InvitationMessage

from .. import routes as test_module


class TestOutOfBandRoutes(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.profile = InMemoryProfile.test_profile()
        self.context = AdminRequestContext.test_context(profile=self.profile)
        self.request_dict = {
            "context": self.context,
            "outbound_message_router": mock.CoroutineMock(),
        }
        self.request = mock.MagicMock(
            app={},
            match_info={},
            query={},
            __getitem__=lambda _, k: self.request_dict[k],
        )

    async def test_invitation_create(self):
        self.request.query = {
            "multi_use": "true",
            "auto_accept": "true",
        }
        body = {
            "attachments": mock.MagicMock(),
            "handshake_protocols": [test_module.HSProto.RFC23.name],
            "use_public_did": True,
            "metadata": {"hello": "world"},
        }
        self.request.json = mock.CoroutineMock(return_value=body)

        with mock.patch.object(
            test_module, "OutOfBandManager", autospec=True
        ) as mock_oob_mgr, mock.patch.object(
            test_module.web, "json_response", mock.Mock()
        ) as mock_json_response:
            mock_oob_mgr.return_value.create_invitation = mock.CoroutineMock(
                return_value=mock.MagicMock(
                    serialize=mock.MagicMock(return_value={"abc": "123"})
                )
            )

            result = await test_module.invitation_create(self.request)
            mock_oob_mgr.return_value.create_invitation.assert_called_once_with(
                my_label=None,
                auto_accept=True,
                public=True,
                multi_use=True,
                hs_protos=[test_module.HSProto.RFC23],
                attachments=body["attachments"],
                metadata=body["metadata"],
                alias=None,
                mediation_id=None,
                service_accept=None,
                protocol_version=None,
                goal_code=None,
                goal=None,
            )
            mock_json_response.assert_called_once_with({"abc": "123"})

    async def test_ret_invitations_single_item(self):
        invi = InvitationMessage(
            comment="Hello",
            label="A label",
            handshake_protocols=[DIDCommPrefix.qualify_current(DIDX_PROTO)],
            services=["did:sov:55GkHamhTU1ZbTbV2ab9DE"],
        )
        invi_rec_1 = InvitationRecord(
            state=InvitationRecord.STATE_AWAIT_RESPONSE,
            invitation=invi.serialize(),
        )
        await invi_rec_1.save(await self.profile.session())
        invi_rec_2 = InvitationRecord(
            state=InvitationRecord.STATE_AWAIT_RESPONSE,
            invitation=invi.serialize(),
        )
        await invi_rec_2.save(await self.profile.session())
        self.request.query = {
            "invitation_id": invi_rec_1.invitation_id,
        }
        with mock.patch.object(
            test_module.web, "json_response", mock.Mock()
        ) as mock_json_response:
            result = await test_module.ret_invitation_list(self.request)
            mock_json_response.assert_called_once()

    async def test_ret_invitations_list(self):
        invi = InvitationMessage(
            comment="Hello",
            label="A label",
            handshake_protocols=[DIDCommPrefix.qualify_current(DIDX_PROTO)],
            services=["did:sov:55GkHamhTU1ZbTbV2ab9DE"],
        )
        invi_rec_1 = InvitationRecord(
            state=InvitationRecord.STATE_AWAIT_RESPONSE,
            invitation=invi.serialize(),
        )
        await invi_rec_1.save(await self.profile.session())
        invi_rec_2 = InvitationRecord(
            state=InvitationRecord.STATE_AWAIT_RESPONSE,
            invitation=invi.serialize(),
        )
        await invi_rec_2.save(await self.profile.session())
        self.request.query = {}
        with mock.patch.object(
            test_module.web, "json_response", mock.Mock()
        ) as mock_json_response:
            result = await test_module.ret_invitation_list(self.request)
            mock_json_response.assert_called_once()

    async def test_invitation_create_with_accept(self):
        self.request.query = {
            "multi_use": "true",
            "auto_accept": "true",
        }
        body = {
            "attachments": mock.MagicMock(),
            "handshake_protocols": [test_module.HSProto.RFC23.name],
            "accept": ["didcomm/aip1", "didcomm/aip2;env=rfc19"],
            "use_public_did": True,
            "metadata": {"hello": "world"},
        }
        self.request.json = mock.CoroutineMock(return_value=body)

        with mock.patch.object(
            test_module, "OutOfBandManager", autospec=True
        ) as mock_oob_mgr, mock.patch.object(
            test_module.web, "json_response", mock.Mock()
        ) as mock_json_response:
            mock_oob_mgr.return_value.create_invitation = mock.CoroutineMock(
                return_value=mock.MagicMock(
                    serialize=mock.MagicMock(return_value={"abc": "123"})
                )
            )

            await test_module.invitation_create(self.request)
            mock_oob_mgr.return_value.create_invitation.assert_called_once_with(
                my_label=None,
                auto_accept=True,
                public=True,
                multi_use=True,
                hs_protos=[test_module.HSProto.RFC23],
                attachments=body["attachments"],
                metadata=body["metadata"],
                alias=None,
                mediation_id=None,
                service_accept=["didcomm/aip1", "didcomm/aip2;env=rfc19"],
                protocol_version=None,
                goal_code=None,
                goal=None,
            )
            mock_json_response.assert_called_once_with({"abc": "123"})

    async def test_invitation_create_x(self):
        self.request.query = {"multi_use": "true"}
        self.request.json = mock.CoroutineMock(
            return_value={
                "attachments": mock.MagicMock(),
                "handshake_protocols": [23],
                "use_public_did": True,
            }
        )

        with mock.patch.object(
            test_module, "OutOfBandManager", autospec=True
        ) as mock_oob_mgr, mock.patch.object(
            test_module.web, "json_response", mock.Mock()
        ) as mock_json_response:
            mock_oob_mgr.return_value.create_invitation = mock.CoroutineMock(
                side_effect=test_module.OutOfBandManagerError()
            )

            with self.assertRaises(test_module.web.HTTPBadRequest):
                await test_module.invitation_create(self.request)
            mock_json_response.assert_not_called()

    async def test_invitation_receive(self):
        self.request.json = mock.CoroutineMock()
        expected_connection_record = ConnRecord(connection_id="some-id")

        with mock.patch.object(
            test_module, "OutOfBandManager", autospec=True
        ) as mock_oob_mgr, mock.patch.object(
            test_module.InvitationMessage, "deserialize", mock.Mock()
        ), mock.patch.object(
            test_module.web, "json_response", mock.Mock()
        ) as mock_json_response:
            mock_oob_mgr.return_value.receive_invitation = mock.CoroutineMock(
                return_value=expected_connection_record
            )

            await test_module.invitation_receive(self.request)
            mock_json_response.assert_called_once_with(
                expected_connection_record.serialize()
            )

    async def test_invitation_receive_forbidden_x(self):
        self.context.update_settings({"admin.no_receive_invites": True})
        with self.assertRaises(test_module.web.HTTPForbidden):
            await test_module.invitation_receive(self.request)

    async def test_invitation_receive_x(self):
        self.request.json = mock.CoroutineMock()

        with mock.patch.object(
            test_module, "OutOfBandManager", autospec=True
        ) as mock_oob_mgr, mock.patch.object(
            test_module.InvitationMessage, "deserialize", mock.Mock()
        ) as mock_invi_deser, mock.patch.object(
            test_module.web, "json_response", mock.Mock()
        ) as mock_json_response:
            mock_oob_mgr.return_value.receive_invitation = mock.CoroutineMock(
                side_effect=test_module.StorageError("cannot write")
            )

            with self.assertRaises(test_module.web.HTTPBadRequest):
                await test_module.invitation_receive(self.request)

    async def test_register(self):
        mock_app = mock.MagicMock()
        mock_app.add_routes = mock.MagicMock()

        await test_module.register(mock_app)
        mock_app.add_routes.assert_called_once()

    async def test_post_process_routes(self):
        mock_app = mock.MagicMock(_state={"swagger_dict": {}})
        test_module.post_process_routes(mock_app)
        assert "tags" in mock_app._state["swagger_dict"]

from models import RoleType
from test.base import TestAPIBase, generate_token
from test.factories import (
    CustomerFactory,
)


class TestAuthorizationAndPermissionRequirements(TestAPIBase):
    def test_auth_requirements(self):
        methods = {
            "GET": self.client.get,
            "POST": self.client.post,
            "PUT": self.client.put,
            "DELETE": self.client.delete,
        }
        all_urls = [
            ("POST", "/insurence/vehicle"),
            ("POST", "/insurence/estate"),
            ("GET", "/insurence/vehicle/1/accept"),
            ("GET", "/insurence/vehicle/1/cancel"),
            # ("DELETE", "/insurence/vehicle/<int:pk>"),
            # ("POST", "/insurence/payments/card"),
            # ("GET", "/insurence/search"),
            # ("GET", "/insurence/stats"),
        ]
        for method, url in all_urls:
            result = methods[method](url)
            assert result.status_code == 401
            assert result.json == {"message": "Invalid or missing token"}

        # Testing create vehicle permission customer

    def test_permission__required_create_insurence_vehicle_requires_customer(self):
        # Testing employee role
        customer = CustomerFactory(role=RoleType.employee)
        token = generate_token(customer)
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.post("/insurence/vehicle", headers=headers)
        assert response.status_code == 403
        assert response.json == {"message": "You not have permission to access this"}

        # Testing admin role too
        customer = CustomerFactory(role=RoleType.admin)
        token = generate_token(customer)
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.post("/insurence/vehicle", headers=headers)
        assert response.status_code == 403
        assert response.json == {"message": "You not have permission to access this"}

        # Testing customer role too
        customer = CustomerFactory(role=RoleType.customer)
        token = generate_token(customer)
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.post("/insurence/vehicle", headers=headers)
        assert response.status_code == 400

        # Testing create estate permission customer

    def test_permission__required_create_estate_vehicle_requires_customer(self):
        # Testing employee role
        customer = CustomerFactory(role=RoleType.employee)
        token = generate_token(customer)
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.post("/insurence/estate", headers=headers)
        assert response.status_code == 403
        assert response.json == {"message": "You not have permission to access this"}

        # Testing admin role too
        customer = CustomerFactory(role=RoleType.admin)
        token = generate_token(customer)
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.post("/insurence/estate", headers=headers)
        assert response.status_code == 403
        assert response.json == {"message": "You not have permission to access this"}

        # Testing customer role too
        customer = CustomerFactory(role=RoleType.customer)
        token = generate_token(customer)
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.post("/insurence/estate", headers=headers)
        assert response.status_code == 400

    def test_permission_required_accept_insurence(self):
        # Testing admin user
        customer = CustomerFactory(role=RoleType.admin)
        token = generate_token(customer)
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.get("/insurence/vehicle/1/accept", headers=headers)
        assert response.status_code == 403
        assert response.json == {"message": "You not have permission to access this"}

        # Testing customer user
        customer = CustomerFactory(role=RoleType.customer)
        token = generate_token(customer)
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.get("/insurence/vehicle/1/accept", headers=headers)
        assert response.status_code == 403
        assert response.json == {"message": "You not have permission to access this"}

        # Testing employee user
        customer = CustomerFactory(role=RoleType.employee)
        token = generate_token(customer)
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.get("/insurence/vehicle/1/accept", headers=headers)
        assert response.status_code == 400

    def test_permission_required_cancel_insurence(self):
        # Testing admin user
        customer = CustomerFactory(role=RoleType.admin)
        token = generate_token(customer)
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.get("/insurence/vehicle/1/cancel", headers=headers)
        assert response.status_code == 403
        assert response.json == {"message": "You not have permission to access this"}

        # Testing customer user
        customer = CustomerFactory(role=RoleType.customer)
        token = generate_token(customer)
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.get("/insurence/vehicle/1/cancel", headers=headers)
        assert response.status_code == 403
        assert response.json == {"message": "You not have permission to access this"}

        # Testing employee user
        customer = CustomerFactory(role=RoleType.employee)
        token = generate_token(customer)
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.get("/insurence/vehicle/1/cancel", headers=headers)
        assert response.status_code == 400


# # Testing create complaint about
# class TestInsurence(TestAPIBase):
#     @patch("uuid.uuid4", mock_uuid)
#     @patch.object(ComplaintManager, "issue_transaction", return_value=None)
#     @patch.object(S3Service, "upload_file", return_value="test_url.bg")
#     def test_create_complaint(self, mocked_s3_url, mocked_transaction):
#         complaints = Complaint.query.all()
#         assert len(complaints) == 0
#         user = UserFactory(role=RoleType.complainer)
#         token = generate_token(user)
#         headers = {
#             "Authorization": f"Bearer {token}",
#             "Content-Type": "application/json",
#         }
#         data = {
#             "title": "Test title",
#             "description": "Test description",
#             "extension": "jpeg",
#             "photo": encoded_photo,
#             "amount": 100,
#         }
#         response = self.client.post("/complaints", headers=headers, json=data)
#         complaints = Complaint.query.all()
#         assert len(complaints) == 1
#         assert response.status_code == 201
#         assert response.json["photo_url"] == "test_url.bg"
#         assert response.json["status"] == State.pending.value
#         expected_photo_name = f"{mock_uuid()}.{data['extension']}"
#         expected_path_file = os.path.join(TEMP_FILE_FOLDER, expected_photo_name)
#         mocked_s3_url.assert_called_once_with(expected_path_file, expected_photo_name)
#         full_name = f"{user.first_name} {user.last_name}"
#         mocked_transaction.assert_called_once_with(
#             data["amount"], full_name, user.iban, complaints[0].id
#         )
#
#     @patch.object(WiseService, "fund_transfer", return_value=None)
#     def test_approve_complaint(self, mocked_transaction):
#         approver = UserFactory(role=RoleType.approver)
#         complainer = UserFactory()
#         token = generate_token(approver)
#         headers = {
#             "Authorization": f"Bearer {token}",
#             "Content-Type": "application/json",
#         }
#         complaint = ComplaintFactory(user_id=complainer.id)
#         transaction = TransactionFactory(complaint_id=complaint.id)
#         complaints = Complaint.query.all()
#         assert len(complaints) == 1
#         assert complaints[0].status == State.pending
#
#         url = f"complaints/{complaint.id}/approve"
#         response = self.client.get(url, headers=headers)
#         # TODO Refactor code to return 201
#         assert response.status_code == 200
#         complaints = Complaint.query.all()
#         assert len(complaints) == 1
#         assert complaints[0].status == State.approved
#         mocked_transaction.assert_called_with(transaction.transfer_id)
#
#     @patch.object(WiseService, "cancel_transfers", return_value=None)
#     def test_reject_complaint(self, mocked_transaction):
#         approver = UserFactory(role=RoleType.approver)
#         complainer = UserFactory()
#         token = generate_token(approver)
#         headers = {
#             "Authorization": f"Bearer {token}",
#             "Content-Type": "application/json",
#         }
#         complaint = ComplaintFactory(user_id=complainer.id)
#         transaction = TransactionFactory(complaint_id=complaint.id)
#         complaints = Complaint.query.all()
#         assert len(complaints) == 1
#         assert complaints[0].status == State.pending
#
#         url = f"complaints/{complaint.id}/reject"
#         response = self.client.get(url, headers=headers)
#         # TODO Refactor code to return 201
#         assert response.status_code == 200
#         complaints = Complaint.query.all()
#         assert len(complaints) == 1
#         assert complaints[0].status == State.rejected
#         mocked_transaction.assert_called_with(transaction.transfer_id)

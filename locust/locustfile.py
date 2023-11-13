from locust import HttpUser, task

import logging
from urllib.parse import urlparse, parse_qs
from uuid import uuid4


class OAuthClientRegistration(HttpUser):

    @task
    def register_client(self):
        r = self.client.post("https://localhost:6884/oauth2/client", data=
        {
            "clientType": "public",  # TODO implement different types for different auth flows
            "clientProfile": "mobile",  # TODO put different if important?
            "clientName": str(uuid4())[:32],
            "clientDesc": str(uuid4()),
            "scope": "read write",  # TODO implement different scopes
            "redirectUri": "http://localhost:8000/authorization",
            "ownerId": "admin",  # TODO implement different users
            "host": "lightapi.net"
        }, verify=False, allow_redirects=False)

        r = r.json()
        logging.info(f"Registered client: clientName = {r['clientName']}, clientId = {r['clientId']},\
        clientSecret = {r['clientSecret']}")


class OAuthUser(HttpUser):
    @task
    def get_access_code(self):
        r = self.client.get(
            "/oauth2/code?response_type=code&client_id=f7d42348-c647-4efb-a52d-4c5787421e72&redirect_uri=http://localhost:8080/authorization",
            auth=('admin', '123456'),
            verify=False,
            allow_redirects=False)
        if r.status_code == 302:
            parsed_redirect = urlparse(r.headers['Location'])
            redirect_params = parse_qs(parsed_redirect.query)
            auth_code = redirect_params.get('code')[0]
            logging.info(f"Authorization_code: {auth_code}")
        else:
            logging.info("Auth_code endpoint did not redirect")

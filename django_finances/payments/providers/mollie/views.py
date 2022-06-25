from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from django_finances.settings import Settings

from .provider import ProviderMollie


class MollieWebhookView(APIView):

    def get_provider(self, request, *args, **kwargs):
        provider = Settings.get_payment_provider(ProviderMollie)
        if provider:
            return provider
        raise APIException('Mollie provider could not be found.')

    def post(self, request, *args, **kwargs):
        data = request.data

        mollie_id = data.get('id')
        if not mollie_id:
            raise ValidationError('Missing Mollie ID.')

        provider = self.get_provider(request, *args, **kwargs)
        provider.webhook(mollie_id)

        return Response(status=204)

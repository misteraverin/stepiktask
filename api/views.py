from django.views.generic import View
from django.http import JsonResponse
from django.core.cache import cache
from .forms import StepsForm
from .stepik import StepikAPI
from requests.exceptions import RequestException
from dateutil.parser import parse


class StepsView(View):
    """View for getting lesson steps of specific type"""

    supported_step_types = ['text']
    stepik_api = StepikAPI()

    @staticmethod
    def response(status, message, ids=None):
        """
        Generates JSON response
        :param status: Status of response
        :param message: Message describing status
        :param ids: Ids of filtered steps
        :return: Response in JsonResponse format
        """
        if ids is None:
            ids = []

        return JsonResponse({
            'status': status,
            'message': message,
            'ids': ids
        })

    @staticmethod
    def error(message, ids=None):
        """
        Proxy for error responses
        :param message: Error description
        :param ids: Ids of filtered steps
        :return: Response in JsonResponse format
        """
        return StepsView.response('error', message, ids)

    @staticmethod
    def success(message, ids=None):
        """
        Proxy for success responses
        :param message: Result description
        :param ids: Ids of filtered steps
        :return: Response in JsonResponse format
        """
        return StepsView.response('success', message, ids)

    @staticmethod
    def get(request, step_type):
        """
        GET requests dispatcher
        :param request: HttpRequest object
        :param step_type: Type of step to filter
        :return: Response in JsonResponse format
        """
        # filter step type
        if step_type not in StepsView.supported_step_types:
            return StepsView.error('Unsupported step type')

        # validate request parameters
        form = StepsForm(request.GET)
        if not form.is_valid():
            return StepsView.error('Invalid parameters')

        # try to get lesson description
        lesson_id = form.cleaned_data['lesson']
        try:
            result = StepsView.stepik_api.get('lessons', ids=lesson_id)
        except RequestException:
            return StepsView.error('API is unavailable')

        # validate id of the lesson
        if len(result['lessons']) == 0:
            return StepsView.error('Lesson not found')

        lesson = result['lessons'][0]
        update_date = parse(lesson['update_date'])

        # try to find fresh cached version of response
        cached = cache.get(lesson_id, None)
        if cached is not None and cached['update_date'] >= update_date:
            return StepsView.success('Restored from cache', cached['ids'])

        step_ids = lesson['steps']

        # request ids by small portions to make valid (short enough) GET requests
        filtered_ids = []
        offset = 0
        delta = 10
        while offset < len(step_ids):
            # iterate by pages if needed as Stepik's API docs
            # say that we should not rely on fixed page size
            page = 1
            while True:
                # try to get steps description
                try:
                    result = StepsView.stepik_api.get('steps',
                                                      step_ids[offset:offset+delta],
                                                      page=page)
                except RequestException:
                    return StepsView.error('API is unavailable')

                # filter steps of specified type
                for step in result['steps']:
                    if step['block']['name'] == step_type:
                        filtered_ids.append(step['id'])

                page += 1
                # stop if next page does not exist
                if not result['meta']['has_next']:
                    break
            # move offset to the next ids portion
            offset += delta

        # store result in cache
        cache.set(lesson_id, {
            'update_date': update_date,
            'ids': filtered_ids
        })
        return StepsView.success('Requested from API', filtered_ids)

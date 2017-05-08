from django.test import TestCase


class StepsTest(TestCase):
    """Tests for API requests to /api/steps/<step_type>"""

    def test_filtering(self):
        """Tests filtering steps of specified type"""
        ids = [45138, 45117, 45359]
        answers = [[182960], [], []]

        for id, answer in zip(ids, answers):
            response = self.client.get('/api/steps/text/?lesson={}'.format(id))
            report = response.json()

            self.assertEqual(report['status'], 'success')
            self.assertEqual(report['ids'], answer)

    def test_parameters_check(self):
        """Tests checking parameters for validity"""
        types = ['text', 'video', 'werfrsv']
        ids = ['sfsd', -100]

        for step_type in types:
            for id in ids:
                path = '/api/steps/{0}/?lesson={1}'.format(step_type, id)
                response = self.client.get(path)
                report = response.json()

                self.assertEqual(report['status'], 'error')
                self.assertEqual(report['ids'], [])

    def test_caching(self):
        """Test caching feature"""
        self.client.get('/api/steps/text/?lesson=45138')
        response = self.client.get('/api/steps/text/?lesson=45138')
        report = response.json()

        self.assertEqual(report['status'], 'success')
        self.assertEqual(report['ids'], [182960])
        self.assertIn('cache', report['message'])

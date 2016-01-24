import six.moves.urllib as urllib


class JasmineUrlBuilder(object):

    def __init__(self, jasmine_config):
        self.jasmine_config = jasmine_config

    def build_url(self, port, seed=None):
        netloc = "localhost:{0}".format(port)
        query_string = self._build_query_params(seed=seed)
        jasmine_url = urllib.parse.urlunparse(('http', netloc, "", "", query_string, ""))
        return jasmine_url

    def _build_query_params(self, seed):
        query_params = {
            "throwFailures": self.jasmine_config.stop_spec_on_expectation_failure(),
            "random": self.jasmine_config.random(),
            "seed": seed
        }
        query_params = self._remove_empty_params(query_params)
        return urllib.parse.urlencode(query_params)

    def _remove_empty_params(self, query_params):
        return dict(((k, v) for k, v in query_params.items() if v))

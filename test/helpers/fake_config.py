class FakeConfig(object):
    def __init__(
            self,
            src_dir=None,
            spec_dir=None,
            stylesheet_urls=None,
            script_urls=None,
            stop_spec_on_expectation_failure=False,
            random=False
    ):
        self._src_dir = src_dir
        self._spec_dir = spec_dir
        self._stylesheet_urls = stylesheet_urls
        self._script_urls = script_urls
        self._stop_spec_on_expectation_failure = stop_spec_on_expectation_failure
        self._random = random

        self.reload_call_count = 0

    def src_dir(self):
        return self._src_dir

    def spec_dir(self):
        return self._spec_dir

    def stylesheet_urls(self):
        return self._stylesheet_urls

    def script_urls(self):
        return self._script_urls

    def stop_spec_on_expectation_failure(self):
        return self._stop_spec_on_expectation_failure

    def random(self):
        return self._random

    def reload(self):
        self.reload_call_count += 1

class BlackList:
    def __init__(self, config_file: str):
        self.blacklist = self._read_blocked_urls(config_file)

    @staticmethod
    def _read_blocked_urls(config_file: str) -> list[str]:
        with open(config_file, 'r', encoding='utf-8') as fin:
            return [row.strip() for row in fin.readlines()]

    def __contains__(self, url: str) -> bool:
        return any(
            blocked_url in url
            for blocked_url in self.blacklist
        )

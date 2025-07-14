from dataclasses import dataclass, field


def parse_comment(comment: str) -> str:
    if comment is None:
        return ''
    return comment.strip().replace('\\n', '\n')


@dataclass
class Symbol:
    name: str
    type: str
    comment: str = field(default="")
    _comment: str = field(init=False, repr=False)

    def __post_init__(self):
        self._comment = parse_comment(self.comment)

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    def comment(self, value: str):
        self._comment = parse_comment(value)

class CommandResponse:
    need_to_interrupt: bool = True
    last_response: dict = None

    def __init__(
        self,
        need_to_interrupt: bool = True,
        last_response: dict = None,
    ) -> None:
        self.need_to_interrupt = need_to_interrupt
        self.last_response = last_response


class CommandProcessorResponse:
    need_to_interrupt: bool = True
    last_response: dict = None
    responses: list[dict] = None

    def __init__(
        self,
        need_to_interrupt: bool = True,
        last_response: dict = None,
        responses: list[dict] = None,
    ) -> None:
        self.need_to_interrupt = need_to_interrupt
        self.last_response = last_response
        if last_response:
            if responses:
                self.responses = responses + [last_response]
            else:
                self.responses = [last_response]

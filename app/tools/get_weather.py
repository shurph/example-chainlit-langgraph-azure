from typing import Literal

from langchain_core.tools import tool


@tool
def get_weather(city: Literal["nyc", "sf", "berezino", "paris", "lodz", "moscow"]):
    """Use this to get weather information."""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    elif city == "berezino":
        return "It's always sunny in berezino, but a bit cloudy"
    elif city == "lodz":
        return "It's always rainy in lodz"
    elif city == "paris":
        return "It's always rainy in paris"
    else:  # for "moscow" case: I'm unable to fetch the weather for Moscow due to a technical issue.
        raise AssertionError("Unknown city")

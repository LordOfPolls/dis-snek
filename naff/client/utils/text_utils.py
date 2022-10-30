import re
import naff.client.const as const
import naff.models as models

__all__ = ("mentions",)


def mentions(text: str, query: "str | re.Pattern[str] | models.BaseUser | models.BaseChannel | models.Role") -> bool:
    """Checks whether a query is present in a text.

    Args:
        text: The text to search in
        query: The query to search for

    Returns:
        Whether the query could be found in the text
    """
    # don't use match/case witch type(query) since subclasses aren't checked
    if isinstance(query, str):
        return query in text
    elif isinstance(query, re.Pattern):
        return query.match(text) is not None
    elif isinstance(query, models.BaseUser):
        # mentions with <@!ID> aren't detected without the replacement
        return (query.mention in text.replace("@!", "@")) or (query.tag in text if const.tag_as_mention else False)
    elif isinstance(query, (models.BaseChannel, models.Role)):
        return (query.mention in text) or (query.name in text)
    else:
        return False

import string
from typing import Dict, List, Union


def get_extractive_summary_spans(full_text: str, summary_text: str) -> List[Dict[str, Union[int, str]]]:
    """
    Function which marks the extracted elements from the summary in the original text.
    :param full_text: string contains text from which the summary was taken.
    :param summary_text: string contains extractive summary from full_text document.
    :return: returns list of dictionaries with spans text and indexes.
    """

    # add the dummy char to the end of the summary text, because without it,
    # it won't trigger the condition that adds span to the dictionary list
    dummie_char = "^"
    summary_text += dummie_char

    search_start_index = 0
    summary_spans = []
    span = ""
    previous_span = None
    is_punc = False
    for i, char in enumerate(summary_text):
        # initial span with one char
        if not span:
            span = char
        # add char to the span and save in memory previous one
        else:
            previous_span = span
            span += char
        # find span in the text if it is in the text, it means that span can be further developed
        try:
            full_text.index(span)
            # if span is only punctuation take whole span with space and further clear span, don't assign present char
            if span.strip() in string.punctuation and i != len(summary_text) - 2:
                previous_span = span
                is_punc = True
                raise ValueError
        # if span is not present in the text, it means that the previous span is the longest matching string in the text
        except ValueError:

            if not previous_span:
                previous_span = span

            if previous_span.strip() in string.punctuation or previous_span.strip().isspace():
                try:
                    span_start = full_text.index(previous_span, search_start_index)
                except ValueError:
                    pass
            else:
                try:
                    span_start = full_text.index(previous_span)
                except ValueError:
                    pass

            span_end = span_start + len(previous_span)
            search_start_index = span_end
            summary_spans.append({"span_start": span_start, "span_end": span_end, "span_text": previous_span})

            if not is_punc:
                span = char
            else:
                span = ""
                is_punc = False

    script_summary = "".join([obj["span_text"] for obj in summary_spans])
    assert script_summary == summary_text[:-1]

    return summary_spans

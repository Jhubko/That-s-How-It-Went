import re


def parse_lrc(lrc_text):

    lines = []


    for line in lrc_text.splitlines():

        match = re.match(
            r"\[(\d+):(\d+\.\d+)\](.*)",
            line
        )


        if match:

            minutes = int(
                match.group(1)
            )

            seconds = float(
                match.group(2)
            )


            time_ms = int(
                (minutes * 60 + seconds) * 1000
            )


            text = match.group(3).strip()



            if text:

                lines.append({

                    "time": time_ms,

                    "text": text

                })


    return lines
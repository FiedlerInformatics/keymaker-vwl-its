import re

wholeString = "This is a [test] string with (some) brackets."

cleanedString = re.sub(r"[\(\[].*?[\)\]]", "", wholeString)

print(cleanedString)
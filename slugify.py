import re
from unidecode import unidecode

def slugify(title):
    # Convert accented characters to ASCII characters
    title = unidecode(title)

    # Convert the title to lowercase and replace spaces with hyphens
    slug = title.lower().replace(" ", "-")

    # Remove any characters that are not alphanumeric or hyphens
    slug = re.sub(r"[^a-z0-9-]", "", slug)

    return slug

print(slugify("Fürdőszoba felújítás panel lakásban?"))
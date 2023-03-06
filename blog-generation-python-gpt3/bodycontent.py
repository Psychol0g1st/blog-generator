import re

html_string = "<body><h1>Heading</h1><p>Paragraph1</p></body><html><head><title>Page Title</title></head><body><h1>Heading</h1><p>Paragraph2</p></body></html><body><h1>Heading</h1><p>Paragraph3</p></body>"

# Define a regular expression to match the body tag and its contents
body_pattern = re.compile(r'<body>(.*?)</body>', re.DOTALL)

# Extract the content of the body tag
html_string = html_string.replace("h1>", "h2>")
body_content = re.findall(body_pattern, html_string)


print(body_content)
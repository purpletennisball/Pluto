import json, os

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)

themeCSS = f"""/* -- {config["name"]} {config["version"]} -- */
/* © {config["author"]} {config["year"]} */

"""
    
def appendFile(snippetName):
	global themeCSS
	with open(snippetName, 'r', encoding='utf-8') as file:
		themeCSS = themeCSS + f"/* {snippetName} */\n"
		themeCSS = themeCSS + f"{file.read()}\n\n"

folderContents = os.listdir(".")
snippets = []
dist = False

for content in folderContents:
	if content.endswith(".css"):
		snippets.append(content)
	if content == "dist":
		dist = True
        
if not dist:
	os.mkdir("dist")

for prioritySnippet in config["order"]:
	prioritySnippetName = f"{prioritySnippet}.css"
	if prioritySnippetName in snippets:
		appendFile(prioritySnippetName)
		snippets.pop(snippets.index(prioritySnippetName))

for snippet in snippets:
	appendFile(snippet)

with open(f'dist/theme.css', 'w', encoding='utf-8') as file:
    file.write(themeCSS)
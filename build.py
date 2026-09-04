import json, os, sys

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)

manifest = {
	"name": config["name"],
	"version": config["version"],
	"author": config["author"],
	"authorUrl": config["authorUrl"],
	"minAppVersion": config["minAppVersion"]
}

try:
	duplicateThemeDestination = sys.argv[1]
except IndexError:
	duplicateThemeDestination = None

basePath = "dist"

themeCSS = f"""/* -- {config["name"]} {config["version"]} -- */
/* © {config["author"]} {config["year"]} */

"""
    
def appendFile(snippetName):
	global themeCSS
	with open(snippetName, 'r', encoding='utf-8') as file:
		themeCSS = themeCSS + f"/* {snippetName} */\n"
		themeCSS = themeCSS + f"{file.read()}\n\n"

def writeBuildContents(basePath: str):
	global themeCSS
	global manifest
	themeLocation = os.path.join(basePath, "theme.css")
	manifestLocation = os.path.join(basePath, "manifest.json")
	with open(themeLocation, 'w', encoding='utf-8') as file:
			file.write(themeCSS)
	with open(manifestLocation, 'w', encoding='utf-8') as file:
		json.dump(manifest, file)

folderContents = os.listdir(".")
snippets = []

for content in folderContents:
	if content.endswith(".css"):
		snippets.append(content)

os.makedirs(basePath, exist_ok=True)

for prioritySnippet in config["order"]:
	prioritySnippetName = f"{prioritySnippet}.css"
	if prioritySnippetName in snippets:
		appendFile(prioritySnippetName)
		snippets.pop(snippets.index(prioritySnippetName))

for snippet in snippets:
	appendFile(snippet)

writeBuildContents(basePath)

print("Theme built successfully")

if duplicateThemeDestination:
	print(f"Duplicating theme to {duplicateThemeDestination}")
	writeBuildContents(duplicateThemeDestination)
	print("Theme duplicated successfully")
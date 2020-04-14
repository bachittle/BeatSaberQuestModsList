### add.py: adds items quickly and efficiently to the markdown table
### run it in console using python version 3

import json

print("--------------------------------------------------------")
print("  ____             _      _____       _               ")
print(" |  _ \           | |    / ____|     | |              ")
print(" | |_) | ___  __ _| |_  | (___   __ _| |__   ___ _ __ ")
print(" |  _ < / _ \/ _\` | __|  \___ \ / _\` | '_ \ / _ \ '__|")
print(" | |_) |  __/ (_| | |_   ____) | (_| | |_) |  __/ |   ")
print(" |____/ \___|\__,_|\__| |_____/ \__,_|_.__/ \___|_|   ")
print("                                                      ")
print("                                                      ")
print("--------------------------------------------------------")

LATEST_VERSION = "v1.9.0"
JSON_FILENAME = "table.json"
MD_FILENAME = "README.md"
fp = open(JSON_FILENAME, "r")
table_json = json.loads(fp.read())
fp.close()

#print(table_json)

print("""
if you edited the json instead of using this scanning input, 
just type n to not add any new items and the program will write your json to markdown
""")

def boolean_input(str):
   return True if input(str + " (y/n): ")[0].lower() == "y" else False 

def save_file():
    print("saving json file...")
    fd = open(JSON_FILENAME, "w")
    json.dump(table_json, fd, indent=4)

    print("converting json to md format...")
    table_md = """
Compatible | Mod Name | Author(s) and Github Link | Downloads
-----------|----------|---------|--------
"""
    for mod_name in table_json.keys():
        item = table_json[mod_name]
        table_md += ":heavy_check_mark:" if item["version"] == LATEST_VERSION else ":x:"
        table_md += "| " + mod_name + " | <ul>"
        for author in item["authors"]:
            contributions = author["contributions"]
            if contributions:
                contributions = " (" + contributions + ")"
            name = author["name"] + contributions
            github = author["github"]
            if github:
                name = "[" + name + "](" + github + ")" 
            table_md += "<li>" + name + "</li>"
        table_md += "</ul> | "
        for download in item["downloads"]:
            text = download["text"]
            if text == "LATEST":
                text = "**Latest ("+item['version']+")**"
            table_md += "<li>[" + text + "](" + download["link"] + ")</li>"
        table_md += "</ul>\n"

    # print(table_md)

    print("saving to md file...")

    table_str = open(MD_FILENAME, "r").read()
    key = "<!--add more items with add.py-->"
    index1 = table_str.find(key)
    index2 = table_str.rfind(key)

    fp = open("GEN.md", "w")
    fp.write(table_str[:index1 + len(key)] + table_md + table_str[index2:])
    fp.close()

# scanning input
while boolean_input("add a new item to the table?"):
    try:
        item = {}
        item['version'] = LATEST_VERSION
        mod_name = input("mod name: ")
        compatible = boolean_input("is it compatible wiht latest version "+LATEST_VERSION+"?")
        if not compatible:
            item['version'] = input("enter the version this mod is compatible with: ")
        authors = []
        while boolean_input("add a new author?"):
            authors.append({
                'name': input("author name (mandatory): "),
                'contributions': input("author's contributions (optional): "),
                'github': input("author's github link (optional): ")
            })
            print(authors)
            if not authors[-1]['name']: 
                print("invalid author! must have a name")
                authors.pop()
        item['authors'] = authors
        downloads = []
        downloads.append({
            "text": "LATEST",
            "link": input("Enter the download link (.zip) for the version "+item['version']+": ")
        })
        while boolean_input("add another download link?"):
            downloads.append({
                "text": input("Enter the text for the download link (ex: version #): "),
                "link": input("Enter the download link (.zip/download site): ")
            })
            print(downloads)
            if not downloads[-1]['text'] or not downloads[-1]['link']: 
                print("invalid download! must have text and link")
                downloads.pop()
        item['downloads'] = downloads
        table_json[mod_name] = item
        #print(table_json)
        save_file()
    except Exception as e:
        print(e)
        continue

save_file()